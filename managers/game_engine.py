import random
from typing import Dict
from datetime import datetime
from models.dataclasses import Player

class GameEngine:
    def __init__(self):
        self.house_edge = 0.04  # 4% house edge (96% RTP)
        self.rtp = 0.96  # 96% Return to Player
    
    def set_rtp(self, rtp_percentage: float):
        """Set the RTP (Return to Player) percentage"""
        if not 0.80 <= rtp_percentage <= 0.99:
            raise ValueError("RTP must be between 80% and 99%")
        
        self.rtp = rtp_percentage
        self.house_edge = 1.0 - rtp_percentage
    
    def place_bet(self, player: Player, bet_amount: float) -> Dict:
        """Simulate placing a bet"""
        total_balance = player.balance + player.bonus_balance
        
        if total_balance < bet_amount:
            return {"success": False, "message": "Insufficient balance"}
        
        # Deduct bet from balance (prefer bonus balance first)
        if player.bonus_balance >= bet_amount:
            player.bonus_balance -= bet_amount
        else:
            remaining = bet_amount - player.bonus_balance
            player.bonus_balance = 0
            player.balance -= remaining
        
        # Update player stats
        player.total_wagered += bet_amount
        player.monthly_wagered += bet_amount
        player.daily_wagering += bet_amount
        player.last_activity = datetime.now()
        
        # Simulate game outcome
        win_probability = self.rtp / 2
        won = random.random() < win_probability
        
        result = {
            "success": True,
            "bet_amount": bet_amount,
            "won": won
        }
        
        if won:
            payout = bet_amount * 2
            player.balance += payout
            result["payout"] = payout
            result["net_result"] = payout - bet_amount
        else:
            player.monthly_losses += bet_amount
            result["payout"] = 0
            result["net_result"] = -bet_amount
        
        result["new_balance"] = player.balance
        result["bonus_balance"] = player.bonus_balance
        return result
    
    def simulate_player_session(self, player: Player, session_duration_minutes: int = 60, 
                               avg_bet_amount: float = 10.0, 
                               award_points_callback=None,
                               update_tournaments_callback=None) -> Dict:
        """Simulate a complete player session"""
        session_results = {
            "player_id": player.player_id,
            "session_duration": session_duration_minutes,
            "bets_placed": 0,
            "total_wagered": 0.0,
            "total_won": 0.0,
            "net_result": 0.0,
            "points_earned": 0,
            "starting_balance": player.balance,
            "ending_balance": 0.0,
            "individual_bets": [],
            "tournament_points_earned": {}
        }
        
        # Estimate number of bets
        num_bets = max(1, session_duration_minutes // 2)
        
        for i in range(num_bets):
            bet_amount = max(1.0, avg_bet_amount * random.uniform(0.5, 1.5))
            
            bet_result = self.place_bet(player, bet_amount)
            
            if bet_result["success"]:
                session_results["bets_placed"] += 1
                session_results["total_wagered"] += bet_amount
                session_results["total_won"] += bet_result.get("payout", 0)
                session_results["net_result"] += bet_result["net_result"]
                
                # Award loyalty points if callback provided
                if award_points_callback:
                    points = award_points_callback(player, bet_amount)
                    session_results["points_earned"] += points
                
                # Update tournaments if callback provided
                if update_tournaments_callback:
                    update_tournaments_callback(player, bet_amount)
                
                session_results["individual_bets"].append({
                    "bet": round(bet_amount, 2),
                    "won": bet_result["won"],
                    "payout": round(bet_result.get("payout", 0), 2),
                    "net": round(bet_result["net_result"], 2)
                })
            else:
                break  # Stop if insufficient balance
        
        session_results["ending_balance"] = player.balance
        return session_results