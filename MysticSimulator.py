from datetime import datetime
from typing import Dict, List
from models.enums import LoyaltyTier, TournamentStatus
from models.dataclasses import Player
from managers.loyalty_manager import LoyaltyManager
from managers.bonus_manager import BonusManager
from managers.tournament_manager import TournamentManager
from managers.game_engine import GameEngine

class MysticWagerCasino:
    def __init__(self):
        self.players: Dict[str, Player] = {}
        self.loyalty_manager = LoyaltyManager()
        self.bonus_manager = BonusManager(self.loyalty_manager.loyalty_config)
        self.tournament_manager = TournamentManager()
        self.game_engine = GameEngine()
        
        # Expose loyalty config for backward compatibility
        self.loyalty_config = self.loyalty_manager.loyalty_config
        self.tournaments = self.tournament_manager.tournaments
    
    @property
    def house_edge(self):
        return self.game_engine.house_edge
    
    @property
    def rtp(self):
        return self.game_engine.rtp
    
    def set_rtp(self, rtp_percentage: float):
        """Set the RTP (Return to Player) percentage"""
        self.game_engine.set_rtp(rtp_percentage)
    
    def register_player(self, player_id: str, name: str, email: str) -> Player:
        """Register a new player"""
        if player_id in self.players:
            raise ValueError(f"Player {player_id} already exists")
        
        player = Player(
            player_id=player_id,
            name=name,
            email=email,
            registration_date=datetime.now()
        )
        self.players[player_id] = player
        return player
    
    def deposit(self, player_id: str, amount: float, email: str) -> bool:
        """Process a deposit for a player"""
        if player_id not in self.players:
            self.register_player(player_id, name=player_id, email=email)
        
        player = self.players[player_id]
        player.balance += amount
        player.total_deposited += amount
        player.monthly_deposits += amount
        player.last_activity = datetime.now()
        
        # Check for welcome bonus
        if not player.welcome_bonus_used:
            self.bonus_manager.apply_welcome_bonus(player, amount)
        
        # Check for tier-based deposit bonus
        self.bonus_manager.check_deposit_bonus(player, amount)
        
        return True
    
    def apply_weekly_reload_bonus(self, player_id: str, deposit_amount: float, promo_code: str = None) -> bool:
        """Apply weekly reload bonus: 25% up to $100"""
        if player_id not in self.players:
            return False
        
        player = self.players[player_id]
        return self.bonus_manager.apply_weekly_reload_bonus(player, deposit_amount, promo_code)
    
    def apply_special_event_bonus(self, player_id: str, event_name: str, bonus_type: str = "deposit") -> bool:
        """Apply special event bonuses"""
        if player_id not in self.players:
            return False
        
        player = self.players[player_id]
        return self.bonus_manager.apply_special_event_bonus(player, event_name, bonus_type)
    
    def process_monthly_rewards(self, player_id: str):
        """Process all monthly rewards (cashback, free spins, loyalty boost)"""
        if player_id not in self.players:
            return
        
        player = self.players[player_id]
        self.loyalty_manager.process_monthly_rewards(player)
    
    def enter_tournament(self, player_id: str, tournament_id: str) -> bool:
        """Enter a player into a tournament"""
        if player_id not in self.players:
            return False
        
        player = self.players[player_id]
        return self.tournament_manager.enter_tournament(player, tournament_id)
    
    def place_bet(self, player_id: str, bet_amount: float) -> Dict:
        """Simulate placing a bet and update tournament points"""
        if player_id not in self.players:
            return {"success": False, "message": "Player not found"}
        
        player = self.players[player_id]
        
        # Place the bet
        result = self.game_engine.place_bet(player, bet_amount)
        
        if result["success"]:
            # Update bonus wagering requirements
            self.bonus_manager.update_bonus_wagering(player, bet_amount)
            
            # Award loyalty points
            points_earned = self.loyalty_manager.award_loyalty_points(player, bet_amount)
            result["points_earned"] = points_earned
            
            # Update tier
            self.loyalty_manager.update_player_tier(player)
            result["new_tier"] = player.tier.value
            
            # Update tournament points for active tournaments
            self.tournament_manager.update_all_tournament_points(player, bet_amount)
        
        return result
    
    def _update_player_tier(self, player: Player):
        """Update player's loyalty tier based on points (backward compatibility)"""
        self.loyalty_manager.update_player_tier(player)
    
    def simulate_player_session(self, player_id: str, session_duration_minutes: int = 60, 
                               avg_bet_amount: float = 10.0) -> Dict:
        """Simulate a complete player session with tournament participation"""
        if player_id not in self.players:
            return {"error": "Player not found"}
        
        player = self.players[player_id]
        
        # Define callbacks for the game engine
        def award_points_callback(player_obj, bet_amt):
            return self.loyalty_manager.award_loyalty_points(player_obj, bet_amt)
        
        def update_tournaments_callback(player_obj, bet_amt):
            self.tournament_manager.update_all_tournament_points(player_obj, bet_amt)
            # Update bonus wagering
            self.bonus_manager.update_bonus_wagering(player_obj, bet_amt)
            # Update tier
            self.loyalty_manager.update_player_tier(player_obj)
        
        session = self.game_engine.simulate_player_session(
            player, session_duration_minutes, avg_bet_amount,
            award_points_callback, update_tournaments_callback
        )
        
        # Calculate tournament points earned during session
        for tournament_id in self.tournaments.keys():
            if self.tournaments[tournament_id].status == TournamentStatus.ACTIVE:
                session["tournament_points_earned"][tournament_id] = session["total_wagered"]
        
        return session
    
    def get_bonus_withdrawal_info(self, player_id: str) -> Dict:
        """Get detailed bonus withdrawal information"""
        if player_id not in self.players:
            return {"error": "Player not found"}
        
        player = self.players[player_id]
        return self.bonus_manager.get_bonus_withdrawal_info(player)
    
    def get_player_stats(self, player_id: str) -> Dict:
        """Get comprehensive player statistics"""
        if player_id not in self.players:
            return {"error": "Player not found"}
            
        player = self.players[player_id]
        tier_benefits = self.loyalty_manager.get_tier_benefits(player.tier)
        
        return {
            "player_id": player.player_id,
            "name": player.name,
            "tier": player.tier.value,
            "balance": player.balance,
            "bonus_balance": player.bonus_balance,  # Add this line
            "loyalty_points": player.loyalty_points,
            "total_deposited": player.total_deposited,
            "total_wagered": player.total_wagered,
            "total_withdrawn": player.total_withdrawn,
            "monthly_losses": player.monthly_losses,
            "monthly_deposits": player.monthly_deposits,
            "monthly_wagered": player.monthly_wagered,
            "tier_benefits": tier_benefits,
            "active_bonuses": len(player.active_bonuses),
            "bonus_history": len(player.bonus_history),
            "tournaments_entered": len(player.tournament_entries)
        }
    
    def get_all_bonuses(self, player_id: str) -> Dict:
        """Get all bonus information for a player"""
        if player_id not in self.players:
            return {"error": "Player not found"}
        
        player = self.players[player_id]
        return self.bonus_manager.get_all_bonuses(player)
    
    def get_all_tournaments(self) -> Dict:
        """Get all tournament information"""
        return self.tournament_manager.get_all_tournaments(self.players)