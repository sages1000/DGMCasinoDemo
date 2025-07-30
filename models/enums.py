from enum import Enum

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

class BonusStatus(Enum):
    ACTIVE = "Active"
    COMPLETED = "Completed"
    EXPIRED = "Expired"
    LOCKED = "Locked"