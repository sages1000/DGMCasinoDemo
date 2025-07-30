from typing import Dict, List
from datetime import datetime, timedelta
from models.enums import TournamentType, TournamentStatus, LoyaltyTier
from models.dataclasses import Tournament, TournamentEntry, Player

class TournamentManager:
    def __init__(self):
        self.tournaments: Dict[str, Tournament] = {}
        self._setup_tournaments()
    
    def _setup_tournaments(self):
        """Initialize all tournament types"""
        now = datetime.now()
        
        # Theme of the Month (Monthly)
        self.tournaments["theme_monthly"] = Tournament(
            tournament_id="theme_monthly",
            tournament_type=TournamentType.THEME_OF_MONTH,
            name="November Adventure Quest",
            description="Each month brings a fresh adventure! Compete in our monthly themed tournaments and collect points on selected games.",
            start_date=now.replace(day=1),
            end_date=now.replace(day=30),
            status=TournamentStatus.ACTIVE,
            prize_pool=5000.0,
            entry_requirements={"min_tier": LoyaltyTier.BEGINNER, "entry_fee": 0}
        )
        
        # Weekly Blitz Showdown
        self.tournaments["weekly_blitz"] = Tournament(
            tournament_id="weekly_blitz",
            tournament_type=TournamentType.WEEKLY_BLITZ,
            name="Weekly Blitz Showdown",
            description="Every week, jump into the action and earn rewards! Join the Weekly Blitz and rack up points through consistent play.",
            start_date=now - timedelta(days=now.weekday()),
            end_date=now - timedelta(days=now.weekday()) + timedelta(days=6),
            status=TournamentStatus.ACTIVE,
            prize_pool=1500.0,
            entry_requirements={"min_tier": LoyaltyTier.BEGINNER, "entry_fee": 0}
        )
        
        # Weekend Flash - Cash Grab
        weekend_start = now - timedelta(days=(now.weekday() - 4) % 7)  # Last Friday
        self.tournaments["weekend_flash"] = Tournament(
            tournament_id="weekend_flash",
            tournament_type=TournamentType.WEEKEND_FLASH,
            name="Weekend Flash - Cash Grab",
            description="Ready for a fast-paced weekend? Play your favorite games Friday through Sunday for instant cash prizes!",
            start_date=weekend_start,
            end_date=weekend_start + timedelta(days=2),
            status=TournamentStatus.ACTIVE if now.weekday() >= 4 else TournamentStatus.UPCOMING,
            prize_pool=2000.0,
            entry_requirements={"min_tier": LoyaltyTier.BEGINNER, "entry_fee": 0}
        )
        
        # Game Master Challenge (Bi-weekly)
        self.tournaments["game_master"] = Tournament(
            tournament_id="game_master",
            tournament_type=TournamentType.GAME_MASTER,
            name="Game Master Challenge - Slots Edition",
            description="Love a specific game or provider? Showcase your skills and win prizes on featured games!",
            start_date=now,
            end_date=now + timedelta(days=14),
            status=TournamentStatus.ACTIVE,
            prize_pool=3000.0,
            entry_requirements={"min_tier": LoyaltyTier.BEGINNER, "entry_fee": 0}
        )
        
        # Progressive Jackpot Challenge (Strategist+)
        self.tournaments["progressive_jackpot"] = Tournament(
            tournament_id="progressive_jackpot",
            tournament_type=TournamentType.PROGRESSIVE_JACKPOT,
            name="Mystic Progressive Jackpot Challenge",
            description="Dive into the Progressive Jackpot Challenge, exclusive for Strategist level and above!",
            start_date=now,
            end_date=now + timedelta(days=30),
            status=TournamentStatus.ACTIVE,
            prize_pool=10000.0,
            entry_requirements={"min_tier": LoyaltyTier.STRATEGIST, "entry_fee": 50}
        )
        
        # Elite High Roller's Club (Professional+)
        self.tournaments["high_roller"] = Tournament(
            tournament_id="high_roller",
            tournament_type=TournamentType.HIGH_ROLLER,
            name="Elite High Roller's Club",
            description="For those who play big! Reserved for Professional and Elite players with top-tier prizes.",
            start_date=now,
            end_date=now + timedelta(days=7),
            status=TournamentStatus.ACTIVE,
            prize_pool=25000.0,
            entry_requirements={"min_tier": LoyaltyTier.PROFESSIONAL, "entry_fee": 100}
        )
        
        # The Grand Slam (Bi-annual)
        self.tournaments["grand_slam"] = Tournament(
            tournament_id="grand_slam",
            tournament_type=TournamentType.GRAND_SLAM,
            name="The Grand Slam Championship",
            description="Twice a year, we go big! The ultimate tournament with the largest rewards and fiercest competition.",
            start_date=now + timedelta(days=30),
            end_date=now + timedelta(days=37),
            status=TournamentStatus.UPCOMING,
            prize_pool=100000.0,
            entry_requirements={"min_tier": LoyaltyTier.STRATEGIST, "entry_fee": 200}
        )
    
    def enter_tournament(self, player: Player, tournament_id: str) -> bool:
        """Enter a player into a tournament"""
        if tournament_id not in self.tournaments:
            return False
        
        tournament = self.tournaments[tournament_id]
        
        # Check eligibility
        min_tier = tournament.entry_requirements.get("min_tier", LoyaltyTier.BEGINNER)
        entry_fee = tournament.entry_requirements.get("entry_fee", 0)
        
        # Check tier requirement
        tier_values = {tier: i for i, tier in enumerate(LoyaltyTier)}
        if tier_values[player.tier] < tier_values[min_tier]:
            return False
        
        if player.balance < entry_fee:
            return False
        
        # Check if already entered
        for entry in player.tournament_entries:
            if entry.tournament_id == tournament_id:
                return False
        
        # Deduct entry fee
        if entry_fee > 0:
            player.balance -= entry_fee
        
        # Create tournament entry
        entry = TournamentEntry(
            tournament_id=tournament_id,
            player_id=player.player_id
        )
        
        player.tournament_entries.append(entry)
        tournament.participants += 1
        
        return True
    
    def update_tournament_points(self, player: Player, tournament_id: str, points: float):
        """Update tournament points for a player"""
        for entry in player.tournament_entries:
            if entry.tournament_id == tournament_id:
                entry.points += points
                break
    
    def update_all_tournament_points(self, player: Player, bet_amount: float):
        """Update points for all active tournaments the player is in"""
        for tournament_id, tournament in self.tournaments.items():
            if tournament.status == TournamentStatus.ACTIVE:
                # Tournament points = bet amount (simple scoring)
                self.update_tournament_points(player, tournament_id, bet_amount)
    
    def get_tournament_leaderboard(self, tournament_id: str, players_dict: Dict[str, Player]) -> List[Dict]:
        """Get tournament leaderboard"""
        if tournament_id not in self.tournaments:
            return []
        
        leaderboard = []
        for player_id, player in players_dict.items():
            for entry in player.tournament_entries:
                if entry.tournament_id == tournament_id:
                    leaderboard.append({
                        "player_id": player_id,
                        "name": player.name,
                        "points": entry.points,
                        "tier": player.tier.value
                    })
        
        return sorted(leaderboard, key=lambda x: x["points"], reverse=True)
    
    def get_all_tournaments(self, players_dict: Dict[str, Player]) -> Dict:
        """Get all tournament information"""
        return {
            tournament_id: {
                "name": tournament.name,
                "type": tournament.tournament_type.value,
                "description": tournament.description,
                "start_date": tournament.start_date.strftime("%Y-%m-%d"),
                "end_date": tournament.end_date.strftime("%Y-%m-%d"),
                "status": tournament.status.value,
                "prize_pool": tournament.prize_pool,
                "participants": tournament.participants,
                "entry_requirements": {
                    "min_tier": tournament.entry_requirements["min_tier"].value,
                    "entry_fee": tournament.entry_requirements["entry_fee"]
                },
                "leaderboard": self.get_tournament_leaderboard(tournament_id, players_dict)[:10]  # Top 10
            }
            for tournament_id, tournament in self.tournaments.items()
        }