from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from .enums import LoyaltyTier, BonusType, TournamentType, TournamentStatus, BonusStatus

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
    wagered_amount: float = 0.0  # Track how much has been wagered
    created_date: datetime = field(default_factory=datetime.now)
    
    @property
    def required_wagering(self) -> float:
        """Calculate total wagering required"""
        return self.amount * self.wagering_requirement
    
    @property
    def remaining_wagering(self) -> float:
        """Calculate remaining wagering requirement"""
        return max(0, self.required_wagering - self.wagered_amount)
    
    @property
    def wagering_progress(self) -> float:
        """Calculate wagering progress as percentage"""
        if self.required_wagering == 0:
            return 100.0
        return min(100.0, (self.wagered_amount / self.required_wagering) * 100)
    
    @property
    def status(self) -> BonusStatus:
        """Get bonus status"""
        if datetime.now() > self.expiry_date:
            return BonusStatus.EXPIRED
        elif self.wagering_progress >= 100.0:
            return BonusStatus.COMPLETED
        elif self.used:
            return BonusStatus.LOCKED
        else:
            return BonusStatus.ACTIVE
    
    @property
    def withdrawable_amount(self) -> float:
        """Calculate how much can be withdrawn"""
        if self.status == BonusStatus.COMPLETED:
            return self.amount
        return 0.0
    
    @property
    def estimated_completion_time(self) -> Optional[datetime]:
        """Estimate when wagering will be completed based on recent activity"""
        if self.status == BonusStatus.COMPLETED:
            return datetime.now()
        
        if self.wagered_amount <= 0:
            return None
        
        # Estimate based on current wagering rate
        days_since_creation = max(1, (datetime.now() - self.created_date).days)
        daily_wagering_rate = self.wagered_amount / days_since_creation
        
        if daily_wagering_rate <= 0:
            return None
        
        days_remaining = self.remaining_wagering / daily_wagering_rate
        return datetime.now() + timedelta(days=days_remaining)

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
    bonus_balance: float = 0.0  # Separate bonus balance
    loyalty_points: int = 0
    tier: LoyaltyTier = LoyaltyTier.BEGINNER
    total_deposited: float = 0.0
    total_wagered: float = 0.0
    total_withdrawn: float = 0.0
    monthly_losses: float = 0.0
    monthly_deposits: float = 0.0
    monthly_wagered: float = 0.0
    daily_wagering: float = 0.0  # Track daily wagering for bonus completion estimates
    active_bonuses: List[Bonus] = field(default_factory=list)
    bonus_history: List[Bonus] = field(default_factory=list)
    tournament_entries: List[TournamentEntry] = field(default_factory=list)
    last_monthly_reset: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    welcome_bonus_used: bool = False
    monthly_enthusiast_bonus_used: bool = False
    weekly_reload_used: bool = False
    last_weekly_reload: Optional[datetime] = None