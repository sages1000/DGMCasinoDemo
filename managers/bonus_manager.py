from typing import List, Dict, Optional
from datetime import datetime, timedelta
from models.enums import BonusType, BonusStatus, LoyaltyTier
from models.dataclasses import Player, Bonus

class BonusManager:
    def __init__(self, loyalty_config):
        self.loyalty_config = loyalty_config
    
    def apply_welcome_bonus(self, player: Player, deposit_amount: float):
        """Apply welcome bonus: 100% match up to $500 + 50 free spins"""
        if player.welcome_bonus_used:
            return False
        
        bonus_amount = min(deposit_amount, 500.0)
        player.bonus_balance += bonus_amount
        
        welcome_bonus = Bonus(
            bonus_type=BonusType.WELCOME,
            amount=bonus_amount,
            wagering_requirement=30,
            expiry_date=datetime.now() + timedelta(days=30),
            description=f"Welcome bonus: €{bonus_amount} + 50 free spins"
        )
        
        # Add free spins bonus
        free_spins_bonus = Bonus(
            bonus_type=BonusType.FREE_SPINS,
            amount=50,
            wagering_requirement=20,
            expiry_date=datetime.now() + timedelta(days=30),
            description="Welcome bonus: 50 free spins"
        )
        
        player.active_bonuses.extend([welcome_bonus, free_spins_bonus])
        player.welcome_bonus_used = True
        return True
    
    def check_deposit_bonus(self, player: Player, deposit_amount: float):
        """Check and apply tier-based deposit bonuses"""
        if player.tier == LoyaltyTier.ENTHUSIAST and not player.monthly_enthusiast_bonus_used:
            # 10% bonus up to $200 monthly
            bonus_amount = min(deposit_amount * 0.10, 200.0)
            if bonus_amount > 0:
                player.bonus_balance += bonus_amount
                bonus = Bonus(
                    bonus_type=BonusType.DEPOSIT,
                    amount=bonus_amount,
                    wagering_requirement=25,
                    expiry_date=datetime.now() + timedelta(days=30),
                    description=f"Enthusiast deposit bonus: €{bonus_amount}"
                )
                player.active_bonuses.append(bonus)
                player.monthly_enthusiast_bonus_used = True
    
    def apply_weekly_reload_bonus(self, player: Player, deposit_amount: float, promo_code: str = None) -> bool:
        """Apply weekly reload bonus: 25% up to $100"""
        # Check if already used this week
        if (player.last_weekly_reload and 
            datetime.now() - player.last_weekly_reload < timedelta(days=7)):
            return False
        
        bonus_amount = min(deposit_amount * 0.25, 100.0)
        player.bonus_balance += bonus_amount
        
        bonus = Bonus(
            bonus_type=BonusType.WEEKLY_RELOAD,
            amount=bonus_amount,
            wagering_requirement=20,
            expiry_date=datetime.now() + timedelta(days=7),
            description=f"Weekly reload bonus: €{bonus_amount}",
            promo_code=promo_code
        )
        
        player.active_bonuses.append(bonus)
        player.last_weekly_reload = datetime.now()
        return True
    
    def apply_special_event_bonus(self, player: Player, event_name: str, bonus_type: str = "deposit") -> bool:
        """Apply special event bonuses"""
        if bonus_type == "deposit":
            # 50% deposit match up to $200
            bonus_amount = min(player.monthly_deposits * 0.50, 200.0)
            player.bonus_balance += bonus_amount
            description = f"{event_name} Event: €{bonus_amount} bonus"
        else:  # free_spins
            bonus_amount = 100  # 100 free spins
            description = f"{event_name} Event: {bonus_amount} free spins"
        
        bonus = Bonus(
            bonus_type=BonusType.SPECIAL_EVENT,
            amount=bonus_amount,
            wagering_requirement=20,
            expiry_date=datetime.now() + timedelta(days=7),
            description=description
        )
        
        player.active_bonuses.append(bonus)
        return True
    
    def update_bonus_wagering(self, player: Player, wager_amount: float):
        """Update wagering progress for all active bonuses"""
        for bonus in player.active_bonuses:
            if bonus.status == BonusStatus.ACTIVE:
                bonus.wagered_amount += wager_amount
                
                # If wagering completed, move bonus amount to main balance
                if bonus.wagering_progress >= 100.0:
                    player.balance += bonus.amount
                    player.bonus_balance = max(0, player.bonus_balance - bonus.amount)
                    
                    # Move to history
                    player.bonus_history.append(bonus)
        
        # Remove completed/expired bonuses from active list
        player.active_bonuses = [
            bonus for bonus in player.active_bonuses 
            if bonus.status in [BonusStatus.ACTIVE, BonusStatus.LOCKED]
        ]
    
    def get_bonus_withdrawal_info(self, player: Player) -> Dict:
        """Get detailed bonus withdrawal information"""
        bonus_info = []
        total_locked = 0
        total_withdrawable = 0
        
        for bonus in player.active_bonuses:
            info = {
                "type": bonus.bonus_type.value,
                "amount": bonus.amount,
                "status": bonus.status.value,
                "required_wagering": bonus.required_wagering,
                "wagered_amount": bonus.wagered_amount,
                "remaining_wagering": bonus.remaining_wagering,
                "progress_percentage": bonus.wagering_progress,
                "withdrawable_amount": bonus.withdrawable_amount,
                "expiry_date": bonus.expiry_date.strftime("%Y-%m-%d %H:%M"),
                "description": bonus.description,
                "estimated_completion": None
            }
            
            if bonus.estimated_completion_time:
                info["estimated_completion"] = bonus.estimated_completion_time.strftime("%Y-%m-%d %H:%M")
            
            if bonus.status == BonusStatus.ACTIVE:
                total_locked += bonus.amount
            elif bonus.status == BonusStatus.COMPLETED:
                total_withdrawable += bonus.withdrawable_amount
            
            bonus_info.append(info)
        
        return {
            "bonuses": bonus_info,
            "summary": {
                "total_bonus_balance": player.bonus_balance,
                "total_locked_amount": total_locked,
                "total_withdrawable_amount": total_withdrawable,
                "active_bonuses_count": len([b for b in player.active_bonuses if b.status == BonusStatus.ACTIVE]),
                "completed_bonuses_count": len([b for b in player.active_bonuses if b.status == BonusStatus.COMPLETED])
            }
        }
    
    def get_all_bonuses(self, player: Player) -> Dict:
        """Get all bonus information for a player"""
        return {
            "active_bonuses": [
                {
                    "type": bonus.bonus_type.value,
                    "amount": bonus.amount,
                    "wagering_requirement": bonus.wagering_requirement,
                    "expiry_date": bonus.expiry_date.strftime("%Y-%m-%d"),
                    "description": bonus.description,
                    "used": bonus.used
                }
                for bonus in player.active_bonuses
            ],
            "available_bonuses": self._get_available_bonuses(player)
        }
    
    def _get_available_bonuses(self, player: Player) -> List[Dict]:
        """Get list of bonuses available to claim"""
        available = []
        
        # Weekly reload (if not used this week)
        if not player.last_weekly_reload or datetime.now() - player.last_weekly_reload >= timedelta(days=7):
            available.append({
                "type": "Weekly Reload",
                "description": "25% bonus on deposits up to €100",
                "requirements": "Available once per week"
            })
        
        # Monthly bonuses (check if month has reset)
        if datetime.now().month != player.last_monthly_reset.month:
            config = self.loyalty_config[player.tier]
            if config.cashback_percentage > 0:
                available.append({
                    "type": "Monthly Cashback",
                    "description": f"{config.cashback_percentage}% cashback up to €{config.cashback_cap}",
                    "requirements": "Automatic at month end"
                })
        
        return available