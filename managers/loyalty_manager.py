from typing import Dict
from models.enums import LoyaltyTier, BonusType
from models.dataclasses import LoyaltyTierConfig, Player, Bonus
from datetime import datetime, timedelta

class LoyaltyManager:
    def __init__(self):
        self.loyalty_config = self._setup_loyalty_tiers()
    
    def _setup_loyalty_tiers(self) -> Dict[LoyaltyTier, LoyaltyTierConfig]:
        return {
            LoyaltyTier.BEGINNER: LoyaltyTierConfig(
                tier=LoyaltyTier.BEGINNER,
                points_required=0,
                free_spins_monthly=5,
                loyalty_store_discount=0.0,
                cashback_percentage=0.0,
                deposit_bonus_percentage=0.0,
                cashback_cap=0.0,
                euros_per_point=1.0
            ),
            LoyaltyTier.ENTHUSIAST: LoyaltyTierConfig(
                tier=LoyaltyTier.ENTHUSIAST,
                points_required=500,
                free_spins_monthly=10,
                loyalty_store_discount=0.0,
                cashback_percentage=0.0,
                deposit_bonus_percentage=10.0,
                cashback_cap=0.0,
                euros_per_point=1.2
            ),
            LoyaltyTier.STRATEGIST: LoyaltyTierConfig(
                tier=LoyaltyTier.STRATEGIST,
                points_required=1500,
                free_spins_monthly=20,
                loyalty_store_discount=10.0,
                cashback_percentage=3.0,
                deposit_bonus_percentage=15.0,
                cashback_cap=50.0,
                euros_per_point=1.5
            ),
            LoyaltyTier.PROFESSIONAL: LoyaltyTierConfig(
                tier=LoyaltyTier.PROFESSIONAL,
                points_required=5000,
                free_spins_monthly=30,
                loyalty_store_discount=15.0,
                cashback_percentage=5.0,
                deposit_bonus_percentage=20.0,
                cashback_cap=100.0,
                euros_per_point=1.8
            ),
            LoyaltyTier.ELITE: LoyaltyTierConfig(
                tier=LoyaltyTier.ELITE,
                points_required=15000,
                free_spins_monthly=50,
                loyalty_store_discount=20.0,
                cashback_percentage=7.0,
                deposit_bonus_percentage=25.0,
                cashback_cap=200.0,
                euros_per_point=2.0
            )
        }
    
    def update_player_tier(self, player: Player):
        """Update player's loyalty tier based on points"""
        for tier, config in reversed(list(self.loyalty_config.items())):
            if player.loyalty_points >= config.points_required:
                player.tier = tier
                break
    
    def award_loyalty_points(self, player: Player, bet_amount: float) -> int:
        """Award loyalty points based on bet amount and tier multiplier"""
        config = self.loyalty_config[player.tier]
        points_earned = int(bet_amount * config.euros_per_point)
        player.loyalty_points += points_earned
        return points_earned
    
    def process_monthly_rewards(self, player: Player):
        """Process all monthly rewards (cashback, free spins, loyalty boost)"""
        config = self.loyalty_config[player.tier]
        
        # Apply cashback based on tier
        if config.cashback_percentage > 0 and player.monthly_losses > 0:
            cashback_amount = min(
                player.monthly_losses * (config.cashback_percentage / 100),
                config.cashback_cap
            )
            if cashback_amount > 0:
                player.balance += cashback_amount  # Cashback goes to main balance
                bonus = Bonus(
                    bonus_type=BonusType.CASHBACK,
                    amount=cashback_amount,
                    wagering_requirement=1,
                    expiry_date=datetime.now() + timedelta(days=30),
                    description=f"Monthly cashback ({config.cashback_percentage}%): €{cashback_amount}"
                )
                player.active_bonuses.append(bonus)
        
        # Award monthly free spins
        free_spins = config.free_spins_monthly
        if free_spins > 0:
            bonus = Bonus(
                bonus_type=BonusType.FREE_SPINS,
                amount=free_spins,
                wagering_requirement=20,
                expiry_date=datetime.now() + timedelta(days=30),
                description=f"Monthly free spins: {free_spins} spins"
            )
            player.active_bonuses.append(bonus)
        
        # Monthly loyalty boost (if wagered >= $1000)
        if player.monthly_wagered >= 1000:
            loyalty_boost = min(player.monthly_deposits * 0.20, 150.0)
            if loyalty_boost > 0:
                player.bonus_balance += loyalty_boost
                bonus = Bonus(
                    bonus_type=BonusType.MONTHLY_LOYALTY,
                    amount=loyalty_boost,
                    wagering_requirement=25,
                    expiry_date=datetime.now() + timedelta(days=30),
                    description=f"Monthly loyalty boost: €{loyalty_boost}"
                )
                player.active_bonuses.append(bonus)
        
        # Reset monthly counters
        player.monthly_losses = 0.0
        player.monthly_deposits = 0.0
        player.monthly_wagered = 0.0
        player.monthly_enthusiast_bonus_used = False
        player.last_monthly_reset = datetime.now()
    
    def get_tier_benefits(self, tier: LoyaltyTier) -> Dict:
        """Get benefits for a specific tier"""
        config = self.loyalty_config[tier]
        return {
            "free_spins_monthly": config.free_spins_monthly,
            "loyalty_store_discount": config.loyalty_store_discount,
            "cashback_percentage": config.cashback_percentage,
            "deposit_bonus_percentage": config.deposit_bonus_percentage,
            "cashback_cap": config.cashback_cap,
            "euros_per_point": config.euros_per_point
        }