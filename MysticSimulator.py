import random
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import json

class LoyaltyTier(Enum):
    BEGINNER = "Beginner"
    ENTHUSIAST = "Enthusiast"
    STRATEGIST = "Strategist"
    PROFESSIONAL = "Professional"
    ELITE = "Elite"

class BonusType(Enum):
    WELCOME = "Welcome"
    DEPOSIT = "Deposit"
    CASHBACK = "Cashback"
    FREE_SPINS = "Free Spins"
    WEEKLY_RELOAD = "Weekly Reload"
    SPECIAL_EVENT = "Special Event"
    MONTHLY_LOYALTY = "Monthly Loyalty"

class TournamentType(Enum):
    THEME_OF_MONTH = "Theme of the Month"
    WEEKLY_BLITZ = "Weekly Blitz Showdown"
    WEEKEND_FLASH = "Weekend Flash - Cash Grab"
    GAME_MASTER = "Game Master Challenge"
    PROGRESSIVE_JACKPOT = "Mystic Progressive Jackpot Challenge"
    HIGH_ROLLER = "Elite High Roller's Club"
    GRAND_SLAM = "The Grand Slam"

class TournamentStatus(Enum):
    UPCOMING = "Upcoming"
    ACTIVE = "Active"
    COMPLETED = "Completed"

@dataclass
class LoyaltyTierConfig:
    tier: LoyaltyTier
    points_required: int
    free_spins_monthly: int
    loyalty_store_discount: float
    cashback_percentage: float
    deposit_bonus_percentage: float
    cashback_cap: float
    euros_per_point: float

@dataclass
class Bonus:
    bonus_type: BonusType
    amount: float
    wagering_requirement: int
    expiry_date: datetime
    used: bool = False
    description: str = ""
    promo_code: Optional[str] = None

@dataclass
class Tournament:
    tournament_id: str
    tournament_type: TournamentType
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    status: TournamentStatus
    prize_pool: float
    entry_requirements: Dict
    leaderboard: List[Dict] = field(default_factory=list)
    participants: int = 0

@dataclass
class TournamentEntry:
    tournament_id: str
    player_id: str
    points: float = 0.0
    position: int = 0
    entry_date: datetime = field(default_factory=datetime.now)

@dataclass
class Player:
    player_id: str
    name: str
    email: str
    registration_date: datetime
    balance: float = 0.0
    loyalty_points: int = 0
    tier: LoyaltyTier = LoyaltyTier.BEGINNER
    total_deposited: float = 0.0
    total_wagered: float = 0.0
    total_withdrawn: float = 0.0
    monthly_losses: float = 0.0
    monthly_deposits: float = 0.0
    monthly_wagered: float = 0.0
    active_bonuses: List[Bonus] = field(default_factory=list)
    bonus_history: List[Bonus] = field(default_factory=list)
    tournament_entries: List[TournamentEntry] = field(default_factory=list)
    last_monthly_reset: datetime = field(default_factory=datetime.now)
    welcome_bonus_used: bool = False
    monthly_enthusiast_bonus_used: bool = False
    weekly_reload_used: bool = False
    last_weekly_reload: Optional[datetime] = None

class MysticWagerCasino:
    def __init__(self):
        self.players: Dict[str, Player] = {}
        self.tournaments: Dict[str, Tournament] = {}
        self.loyalty_config = self._setup_loyalty_tiers()
        self.house_edge = 0.04  # 4% house edge (96% RTP)
        self.rtp = 0.96  # 96% Return to Player
        self._setup_tournaments()
        
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
        
        # Check for welcome bonus
        if not player.welcome_bonus_used:
            self._apply_welcome_bonus(player, amount)
        
        # Check for tier-based deposit bonus
        self._check_deposit_bonus(player, amount)
        
        return True
    
    def _apply_welcome_bonus(self, player: Player, deposit_amount: float):
        """Apply welcome bonus: 100% match up to $500 + 50 free spins"""
        bonus_amount = min(deposit_amount, 500.0)
        player.balance += bonus_amount
        
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
    
    def _check_deposit_bonus(self, player: Player, deposit_amount: float):
        """Check and apply tier-based deposit bonuses"""
        if player.tier == LoyaltyTier.ENTHUSIAST and not player.monthly_enthusiast_bonus_used:
            # 10% bonus up to $200 monthly
            bonus_amount = min(deposit_amount * 0.10, 200.0)
            if bonus_amount > 0:
                player.balance += bonus_amount
                bonus = Bonus(
                    bonus_type=BonusType.DEPOSIT,
                    amount=bonus_amount,
                    wagering_requirement=25,
                    expiry_date=datetime.now() + timedelta(days=30),
                    description=f"Enthusiast deposit bonus: €{bonus_amount}"
                )
                player.active_bonuses.append(bonus)
                player.monthly_enthusiast_bonus_used = True
    
    def apply_weekly_reload_bonus(self, player_id: str, deposit_amount: float, promo_code: str = None) -> bool:
        """Apply weekly reload bonus: 25% up to $100"""
        if player_id not in self.players:
            return False
        
        player = self.players[player_id]
        
        # Check if already used this week
        if (player.last_weekly_reload and 
            datetime.now() - player.last_weekly_reload < timedelta(days=7)):
            return False
        
        bonus_amount = min(deposit_amount * 0.25, 100.0)
        player.balance += bonus_amount
        
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
    
    def apply_special_event_bonus(self, player_id: str, event_name: str, bonus_type: str = "deposit") -> bool:
        """Apply special event bonuses"""
        if player_id not in self.players:
            return False
        
        player = self.players[player_id]
        
        if bonus_type == "deposit":
            # 50% deposit match up to $200
            bonus_amount = min(player.monthly_deposits * 0.50, 200.0)
            player.balance += bonus_amount
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
    
    def process_monthly_rewards(self, player_id: str):
        """Process all monthly rewards (cashback, free spins, loyalty boost)"""
        if player_id not in self.players:
            return
        
        player = self.players[player_id]
        config = self.loyalty_config[player.tier]
        
        # Apply cashback based on tier
        if config.cashback_percentage > 0 and player.monthly_losses > 0:
            cashback_amount = min(
                player.monthly_losses * (config.cashback_percentage / 100),
                config.cashback_cap
            )
            if cashback_amount > 0:
                player.balance += cashback_amount
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
                player.balance += loyalty_boost
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
    
    def enter_tournament(self, player_id: str, tournament_id: str) -> bool:
        """Enter a player into a tournament"""
        if player_id not in self.players or tournament_id not in self.tournaments:
            return False
        
        player = self.players[player_id]
        tournament = self.tournaments[tournament_id]
        
        # Check eligibility
        min_tier = tournament.entry_requirements.get("min_tier", LoyaltyTier.BEGINNER)
        entry_fee = tournament.entry_requirements.get("entry_fee", 0)
        
        if player.tier.value < min_tier.value:
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
            player_id=player_id
        )
        
        player.tournament_entries.append(entry)
        tournament.participants += 1
        
        return True
    
    def update_tournament_points(self, player_id: str, tournament_id: str, points: float):
        """Update tournament points for a player"""
        if player_id not in self.players:
            return
        
        player = self.players[player_id]
        for entry in player.tournament_entries:
            if entry.tournament_id == tournament_id:
                entry.points += points
                break
    
    def get_tournament_leaderboard(self, tournament_id: str) -> List[Dict]:
        """Get tournament leaderboard"""
        if tournament_id not in self.tournaments:
            return []
        
        leaderboard = []
        for player_id, player in self.players.items():
            for entry in player.tournament_entries:
                if entry.tournament_id == tournament_id:
                    leaderboard.append({
                        "player_id": player_id,
                        "name": player.name,
                        "points": entry.points,
                        "tier": player.tier.value
                    })
        
        return sorted(leaderboard, key=lambda x: x["points"], reverse=True)
    
    def place_bet(self, player_id: str, bet_amount: float) -> Dict:
        """Simulate placing a bet and update tournament points"""
        if player_id not in self.players:
            return {"success": False, "message": "Player not found"}
        
        player = self.players[player_id]
        
        if player.balance < bet_amount:
            return {"success": False, "message": "Insufficient balance"}
        
        # Deduct bet from balance
        player.balance -= bet_amount
        player.total_wagered += bet_amount
        player.monthly_wagered += bet_amount
        
        # Award loyalty points
        config = self.loyalty_config[player.tier]
        points_earned = int(bet_amount * config.euros_per_point)
        player.loyalty_points += points_earned
        
        # Update tier
        self._update_player_tier(player)
        
        # Simulate game outcome
        win_probability = self.rtp / 2
        won = random.random() < win_probability
        
        result = {
            "success": True,
            "bet_amount": bet_amount,
            "won": won,
            "points_earned": points_earned,
            "new_tier": player.tier.value
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
        
        # Update tournament points for active tournaments
        self._update_all_tournament_points(player_id, bet_amount)
        
        result["new_balance"] = player.balance
        return result
    
    def _update_all_tournament_points(self, player_id: str, bet_amount: float):
        """Update points for all active tournaments the player is in"""
        for tournament_id, tournament in self.tournaments.items():
            if tournament.status == TournamentStatus.ACTIVE:
                # Tournament points = bet amount (simple scoring)
                self.update_tournament_points(player_id, tournament_id, bet_amount)
    
    def _update_player_tier(self, player: Player):
        """Update player's loyalty tier based on points"""
        for tier, config in reversed(list(self.loyalty_config.items())):
            if player.loyalty_points >= config.points_required:
                player.tier = tier
                break
    
    def set_rtp(self, rtp_percentage: float):
        """Set the RTP (Return to Player) percentage"""
        if not 0.80 <= rtp_percentage <= 0.99:
            raise ValueError("RTP must be between 80% and 99%")
        
        self.rtp = rtp_percentage
        self.house_edge = 1.0 - rtp_percentage
    
    def get_player_stats(self, player_id: str) -> Dict:
        """Get comprehensive player statistics"""
        if player_id not in self.players:
            return {"error": "Player not found"}
            
        player = self.players[player_id]
        config = self.loyalty_config[player.tier]
        
        return {
            "player_id": player.player_id,
            "name": player.name,
            "tier": player.tier.value,
            "balance": player.balance,
            "loyalty_points": player.loyalty_points,
            "total_deposited": player.total_deposited,
            "total_wagered": player.total_wagered,
            "total_withdrawn": player.total_withdrawn,
            "monthly_losses": player.monthly_losses,
            "monthly_deposits": player.monthly_deposits,
            "monthly_wagered": player.monthly_wagered,
            "tier_benefits": {
                "free_spins_monthly": config.free_spins_monthly,
                "loyalty_store_discount": config.loyalty_store_discount,
                "cashback_percentage": config.cashback_percentage,
                "deposit_bonus_percentage": config.deposit_bonus_percentage,
                "cashback_cap": config.cashback_cap,
                "euros_per_point": config.euros_per_point
            },
            "active_bonuses": len(player.active_bonuses),
            "bonus_history": len(player.bonus_history),
            "tournaments_entered": len(player.tournament_entries)
        }
    
    def get_all_bonuses(self, player_id: str) -> Dict:
        """Get all bonus information for a player"""
        if player_id not in self.players:
            return {"error": "Player not found"}
        
        player = self.players[player_id]
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
            "available_bonuses": self._get_available_bonuses(player_id)
        }
    
    def _get_available_bonuses(self, player_id: str) -> List[Dict]:
        """Get list of bonuses available to claim"""
        player = self.players[player_id]
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
    
    def get_all_tournaments(self) -> Dict:
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
                "leaderboard": self.get_tournament_leaderboard(tournament_id)[:10]  # Top 10
            }
            for tournament_id, tournament in self.tournaments.items()
        }
    
    def simulate_player_session(self, player_id: str, session_duration_minutes: int = 60, 
                               avg_bet_amount: float = 10.0) -> Dict:
        """Simulate a complete player session with tournament participation"""
        if player_id not in self.players:
            return {"error": "Player not found"}
        
        player = self.players[player_id]
        
        session_results = {
            "player_id": player_id,
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
            
            bet_result = self.place_bet(player_id, bet_amount)
            
            if bet_result["success"]:
                session_results["bets_placed"] += 1
                session_results["total_wagered"] += bet_amount
                session_results["total_won"] += bet_result.get("payout", 0)
                session_results["net_result"] += bet_result["net_result"]
                session_results["points_earned"] += bet_result["points_earned"]
                session_results["individual_bets"].append({
                    "bet": round(bet_amount, 2),
                    "won": bet_result["won"],
                    "payout": round(bet_result.get("payout", 0), 2),
                    "net": round(bet_result["net_result"], 2)
                })
            else:
                break  # Stop if insufficient balance
        
        # Calculate tournament points earned during session
        for tournament_id in self.tournaments.keys():
            if self.tournaments[tournament_id].status == TournamentStatus.ACTIVE:
                session_results["tournament_points_earned"][tournament_id] = session_results["total_wagered"]
        
        session_results["ending_balance"] = player.balance
        return session_results

# Example usage and testing
if __name__ == "__main__":
    # Create casino instance
    casino = MysticWagerCasino()
    
    # Register a player
    player = casino.register_player("player001", "John Doe", "john@example.com")
    print(f"Registered player: {player.name}")
    
    # Make initial deposit (triggers welcome bonus)
    casino.deposit("player001", 500.0, "john@example.com")
    print(f"After deposit: Balance = €{player.balance} (includes welcome bonus)")
    
    # Enter some tournaments
    casino.enter_tournament("player001", "theme_monthly")
    casino.enter_tournament("player001", "weekly_blitz")
    print("Entered tournaments")
    
    # Apply weekly reload bonus
    casino.apply_weekly_reload_bonus("player001", 100.0, "RELOAD25")
    print(f"After reload bonus: Balance = €{player.balance}")
    
    # Simulate a session
    session = casino.simulate_player_session("player001", session_duration_minutes=120, avg_bet_amount=15.0)
    print(f"\nSession Results:")
    print(f"Bets placed: {session['bets_placed']}")
    print(f"Total wagered: €{session['total_wagered']:.2f}")
    print(f"Net result: €{session['net_result']:.2f}")
    print(f"Points earned: {session['points_earned']}")
    print(f"Tournament points: {session['tournament_points_earned']}")
    
    # Check player stats
    stats = casino.get_player_stats("player001")
    print(f"\nPlayer Stats:")
    print(f"Tier: {stats['tier']}")
    print(f"Balance: €{stats['balance']:.2f}")
    print(f"Loyalty Points: {stats['loyalty_points']}")
    print(f"Tournaments Entered: {stats['tournaments_entered']}")
    
    # Check bonuses
    bonuses = casino.get_all_bonuses("player001")
    print(f"\nActive Bonuses: {len(bonuses['active_bonuses'])}")
    for bonus in bonuses['active_bonuses']:
        print(f"- {bonus['description']}")
    
    # Check tournaments
    tournaments = casino.get_all_tournaments()
    print(f"\nActive Tournaments:")
    for t_id, tournament in tournaments.items():
        if tournament['status'] == 'Active':
            print(f"- {tournament['name']}: {tournament['participants']} participants")
    
    # Process monthly rewards
    casino.process_monthly_rewards("player001")
    print(f"After monthly rewards: Balance = €{casino.players['player001'].balance:.2f}")
    
    # Apply special event bonus
    casino.apply_special_event_bonus("player001", "Halloween Special", "free_spins")
    print("Applied Halloween special event bonus")
    
    print(f"\nFinal balance: €{casino.players['player001'].balance:.2f}")
    print(f"Total active bonuses: {len(casino.players['player001'].active_bonuses)}")