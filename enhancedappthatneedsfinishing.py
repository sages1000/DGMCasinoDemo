import streamlit as st
import pandas as pd
from MysticSimulator import MysticWagerCasino
from models.enums import LoyaltyTier
import time
import random

# Page config with enhanced styling
st.set_page_config(
    page_title="🎰 Mystic Wager Casino",
    page_icon="🎰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with the casino theme
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    /* Global Styling */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a0f2e 25%, #2d1b4e 50%, #1a0f2e 75%, #0a0a0a 100%);
        color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.9) 0%, rgba(45, 27, 78, 0.9) 100%);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 2px solid rgba(255, 215, 0, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .casino-title {
        font-family: 'Orbitron', monospace;
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(45deg, #ffd700, #ffed4e, #ffd700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
        margin-bottom: 0.5rem;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 20px rgba(255, 215, 0, 0.5)); }
        to { filter: drop-shadow(0 0 30px rgba(255, 215, 0, 0.8)); }
    }
    
    .casino-subtitle {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.8);
        margin-bottom: 1rem;
    }
    
    /* Stat cards */
    .stat-row {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-top: 1rem;
        flex-wrap: wrap;
    }
    
    .stat-card {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 15px;
        padding: 1rem 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        min-width: 120px;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(255, 215, 0, 0.2);
        border-color: rgba(255, 215, 0, 0.6);
    }
    
    .stat-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #ffd700;
        display: block;
        font-family: 'Orbitron', monospace;
    }
    
    .stat-label {
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.7);
        margin-top: 0.25rem;
    }
    
    /* Game cards */
    .game-card {
        background: linear-gradient(145deg, rgba(0, 0, 0, 0.8), rgba(45, 27, 78, 0.6));
        backdrop-filter: blur(15px);
        border: 2px solid rgba(255, 215, 0, 0.2);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .game-card:hover {
        transform: translateY(-10px);
        border-color: rgba(255, 215, 0, 0.6);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3), 0 0 60px rgba(255, 215, 0, 0.2);
    }
    
    .game-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #ffd700;
        margin-bottom: 1rem;
        font-family: 'Orbitron', monospace;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .game-icon {
        font-size: 2rem;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    /* Slot machine styling */
    .slot-machine {
        background: linear-gradient(145deg, #1a1a2e, #16213e);
        border: 3px solid #ffd700;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .slot-reels {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin: 1rem 0;
    }
    
    .reel {
        width: 80px;
        height: 80px;
        background: linear-gradient(145deg, #000, #333);
        border: 2px solid #ffd700;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        color: #ffd700;
        position: relative;
        overflow: hidden;
        font-family: 'Orbitron', monospace;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(145deg, #ffd700, #ffed4e) !important;
        color: #000 !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 25px !important;
        font-size: 1rem !important;
        font-weight: bold !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        font-family: 'Orbitron', monospace !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 25px rgba(255, 215, 0, 0.4) !important;
    }
    
    /* Metric styling */
    .metric-container {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: linear-gradient(145deg, rgba(0, 0, 0, 0.8), rgba(45, 27, 78, 0.6));
        border-radius: 15px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 10px;
        color: #ffd700;
        font-weight: bold;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(145deg, #ffd700, #ffed4e);
        color: #000;
    }
    
    /* Sidebar styling */
    .stSidebar {
        background: linear-gradient(180deg, rgba(0, 0, 0, 0.9) 0%, rgba(45, 27, 78, 0.9) 100%);
    }
    
    .stSidebar .stMarkdown {
        color: #ffd700;
    }
    
    /* Input styling */
    .stNumberInput > div > div > input {
        background: rgba(0, 0, 0, 0.5) !important;
        border: 2px solid rgba(255, 215, 0, 0.3) !important;
        border-radius: 10px !important;
        color: #fff !important;
    }
    
    .stSelectbox > div > div > div {
        background: rgba(0, 0, 0, 0.5) !important;
        border: 2px solid rgba(255, 215, 0, 0.3) !important;
        border-radius: 10px !important;
        color: #fff !important;
    }
    
    /* Progress bar styling */
    .stProgress .st-bo {
        background: linear-gradient(90deg, #ffd700, #ffed4e) !important;
    }
    
    /* Success/error styling */
    .stSuccess {
        background: linear-gradient(145deg, rgba(76, 175, 80, 0.2), rgba(76, 175, 80, 0.1)) !important;
        border: 2px solid #4CAF50 !important;
        border-radius: 15px !important;
        color: #4CAF50 !important;
    }
    
    .stError {
        background: linear-gradient(145deg, rgba(244, 67, 54, 0.2), rgba(244, 67, 54, 0.1)) !important;
        border: 2px solid #f44336 !important;
        border-radius: 15px !important;
        color: #f44336 !important;
    }
    
    /* DataFrame styling */
    .stDataFrame {
        background: linear-gradient(145deg, rgba(0, 0, 0, 0.8), rgba(45, 27, 78, 0.6)) !important;
        border-radius: 15px !important;
        border: 2px solid rgba(255, 215, 0, 0.3) !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05)) !important;
        border: 1px solid rgba(255, 215, 0, 0.3) !important;
        border-radius: 10px !important;
        color: #ffd700 !important;
    }
    
    /* Tournament card styling */
    .tournament-card {
        background: linear-gradient(145deg, rgba(139, 69, 19, 0.3), rgba(160, 82, 45, 0.2));
        border: 2px solid rgba(255, 215, 0, 0.4);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .tournament-card:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 30px rgba(255, 215, 0, 0.3);
    }
    
    .tournament-prize {
        font-size: 1.8rem;
        font-weight: bold;
        color: #ffd700;
        text-align: center;
        margin-bottom: 0.5rem;
        font-family: 'Orbitron', monospace;
    }
    
    /* Leaderboard styling */
    .leaderboard-item {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .leaderboard-item:hover {
        background: rgba(255, 215, 0, 0.1);
        transform: translateX(5px);
    }
    
    /* Animation classes */
    .fade-in {
        animation: fadeIn 0.6s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .slide-in-right {
        animation: slideInRight 0.6s ease-out;
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Tier progress styling */
    .tier-progress-container {
        background: rgba(0, 0, 0, 0.5);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 2px solid rgba(255, 215, 0, 0.3);
    }
    
    /* Result display styling */
    .result-display {
        background: linear-gradient(145deg, rgba(0, 0, 0, 0.8), rgba(45, 27, 78, 0.6));
        border: 2px solid rgba(255, 215, 0, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .result-win {
        border-color: #4CAF50 !important;
        background: linear-gradient(145deg, rgba(76, 175, 80, 0.2), rgba(76, 175, 80, 0.1)) !important;
        animation: winGlow 1s ease-in-out;
    }
    
    .result-lose {
        border-color: #f44336 !important;
        background: linear-gradient(145deg, rgba(244, 67, 54, 0.2), rgba(244, 67, 54, 0.1)) !important;
    }
    
    @keyframes winGlow {
        0%, 100% { box-shadow: 0 0 20px rgba(76, 175, 80, 0.5); }
        50% { box-shadow: 0 0 40px rgba(76, 175, 80, 0.8); }
    }
</style>
""", unsafe_allow_html=True)

# Initialize casino in session state
if 'casino' not in st.session_state:
    st.session_state.casino = MysticWagerCasino()

casino = st.session_state.casino

# Register or load player
player_id = "DGMCasinoPlayer"
email = "john@example.com"
if player_id not in casino.players:
    player = casino.register_player(player_id, "John", email)
else:
    player = casino.players[player_id]

# Enhanced Header with animated title
st.markdown("""
<div class="main-header fade-in">
    <h1 class="casino-title">🎰 MYSTIC WAGER CASINO</h1>
    <p class="casino-subtitle">Where Fortune Favors the Bold</p>
    <div class="stat-row">
        <div class="stat-card">
            <span class="stat-value">€{:.2f}</span>
            <span class="stat-label">💰 Balance</span>
        </div>
        <div class="stat-card">
            <span class="stat-value">€{:.2f}</span>
            <span class="stat-label">🎁 Bonus</span>
        </div>
        <div class="stat-card">
            <span class="stat-value">{}</span>
            <span class="stat-label">🏆 Tier</span>
        </div>
        <div class="stat-card">
            <span class="stat-value">{:,}</span>
            <span class="stat-label">💎 Points</span>
        </div>
    </div>
</div>
""".format(
    casino.players[player_id].balance,
    casino.players[player_id].bonus_balance,
    casino.players[player_id].tier.value,
    casino.players[player_id].loyalty_points
), unsafe_allow_html=True)

# Enhanced Sidebar
with st.sidebar:
    st.markdown("## 🎛️ Casino Controls")
    
    # Current balance display
    current_balance = casino.players[player_id].balance
    bonus_balance = casino.players[player_id].bonus_balance
    total_balance = current_balance + bonus_balance
    
    st.markdown(f"""
    <div class="metric-container">
        <div style="text-align: center;">
            <div class="stat-value">€{current_balance:.2f}</div>
            <div class="stat-label">💰 Main Balance</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="metric-container">
        <div style="text-align: center;">
            <div class="stat-value">€{bonus_balance:.2f}</div>
            <div class="stat-label">🎁 Bonus Balance</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="metric-container">
        <div style="text-align: center;">
            <div class="stat-value">€{total_balance:.2f}</div>
            <div class="stat-label">💎 Total Balance</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tier Management Section
    st.markdown("### 🏆 Tier Management")
    
    # Display current player tier and points
    current_tier = casino.players[player_id].tier
    current_points = casino.players[player_id].loyalty_points
    st.write(f"**Current Tier:** {current_tier.value}")
    st.write(f"**Current Points:** {current_points:,}")
    
    # Tier point adjustment controls
    with st.expander("⚙️ Adjust Tier Requirements", expanded=False):
        st.write("Modify points required for each tier:")
        
        # Store original values if not already stored
        if 'original_tier_config' not in st.session_state:
            st.session_state.original_tier_config = {
                tier: config.points_required 
                for tier, config in casino.loyalty_config.items()
            }
        
        # Create sliders for each tier (except BEGINNER which is always 0)
        new_tier_points = {}
        new_tier_points[LoyaltyTier.BEGINNER] = 0  # Always 0
        
        for tier in [LoyaltyTier.ENTHUSIAST, LoyaltyTier.STRATEGIST, LoyaltyTier.PROFESSIONAL, LoyaltyTier.ELITE]:
            current_requirement = casino.loyalty_config[tier].points_required
            original_requirement = st.session_state.original_tier_config[tier]
            
            new_points = st.slider(
                f"{tier.value}",
                min_value=0,
                max_value=50000,
                value=current_requirement,
                step=100,
                key=f"tier_{tier.value}",
                help=f"Original: {original_requirement:,} points"
            )
            new_tier_points[tier] = new_points
        
        # Apply changes button
        if st.button("🔄 Apply Tier Changes"):
            for tier, new_points in new_tier_points.items():
                casino.loyalty_config[tier].points_required = new_points
            
            # Update player tier based on new requirements
            casino._update_player_tier(casino.players[player_id])
            st.success("Tier requirements updated!")
            st.rerun()
        
        # Reset to original button
        if st.button("↩️ Reset to Original"):
            for tier, original_points in st.session_state.original_tier_config.items():
                casino.loyalty_config[tier].points_required = original_points
            
            # Update player tier based on reset requirements
            casino._update_player_tier(casino.players[player_id])
            st.success("Tier requirements reset to original values!")
            st.rerun()
    
    # Quick loyalty points adjustment
    st.markdown("### ⚡ Quick Point Adjustment")
    point_adjustment = st.selectbox(
        "Adjust Player Points:",
        [0, 100, 500, 1000, 2500, 5000, 10000, -100, -500, -1000],
        format_func=lambda x: f"{'Add' if x >= 0 else 'Remove'} {abs(x):,} points" if x != 0 else "No change"
    )
    
    if st.button("🎯 Apply Point Adjustment") and point_adjustment != 0:
        old_points = casino.players[player_id].loyalty_points
        old_tier = casino.players[player_id].tier
        
        # Apply adjustment (ensure points don't go below 0)
        casino.players[player_id].loyalty_points = max(0, old_points + point_adjustment)
        
        # Update tier
        casino._update_player_tier(casino.players[player_id])
        
        new_points = casino.players[player_id].loyalty_points
        new_tier = casino.players[player_id].tier
        
        if new_tier != old_tier:
            st.success(f"Points: {old_points:,} → {new_points:,}\nTier: {old_tier.value} → {new_tier.value}")
        else:
            st.success(f"Points adjusted: {old_points:,} → {new_points:,}")
        st.rerun()
    
    # Deposit section
    st.markdown("### 💵 Make Deposit")
    deposit_amount = st.slider("Amount (€)", 10, 10000, 500)
    if st.button("💵 Deposit"):
        success = casino.deposit(player_id, deposit_amount, email)
        if success:
            st.success(f"Deposited €{deposit_amount}")
            st.rerun()
    
    # Session simulation
    st.markdown("### 🎮 Session Settings")
    session_minutes = st.slider("⏱️ Duration (min)", 10, 300, 60)
    average_bet = st.slider("🎲 Avg Bet (€)", 1.0, 50.0, 10.0)
    rtp = st.slider("📈 RTP (%)", 80, 99, 95)
    
    casino.set_rtp(rtp / 100)
    
    if st.button("▶️ Simulate Session"):
        if total_balance <= 0:
            st.error("Please make a deposit first!")
        else:
            with st.spinner("Simulating session..."):
                session = casino.simulate_player_session(player_id, session_minutes, average_bet)
                st.session_state.last_session = session
            st.success("Session completed!")
            st.rerun()
    
    # Bonus section
    st.markdown("### 🎁 Quick Bonuses")
    if st.button("🔄 Weekly Reload (25%)"):
        success = casino.apply_weekly_reload_bonus(player_id, 100.0, "RELOAD25")
        if success:
            st.success("Weekly reload applied!")
            st.rerun()
        else:
            st.error("Already used this week")
    
    if st.button("🎃 Special Event Bonus"):
        success = casino.apply_special_event_bonus(player_id, "Halloween Special", "free_spins")
        if success:
            st.success("Event bonus applied!")
            st.rerun()
    
    if st.button("📅 Process Monthly Rewards"):
        casino.process_monthly_rewards(player_id)
        st.success("Monthly rewards processed!")
        st.rerun()

# Main content area with enhanced tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🎰 Casino Floor", 
    "📊 Session Results", 
    "👤 Player Stats", 
    "🎁 Bonuses", 
    "🏆 Tournaments", 
    "📈 Analytics",
    "🎮 Quick Play"
])

with tab1:
    st.markdown("## 🎰 Welcome to the Casino Floor")
    
    # Casino floor with enhanced game cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="game-card fade-in">
            <h2 class="game-title">
                <span class="game-icon">🎰</span>
                Mystic Slots
            </h2>
            <div class="slot-machine">
        """, unsafe_allow_html=True)
        
        # Slot machine reels
        if 'slot_symbols' not in st.session_state:
            st.session_state.slot_symbols = ['🍒', '🍋', '🔔']
        
        reel_col1, reel_col2, reel_col3 = st.columns(3)
        with reel_col1:
            st.markdown(f'<div class="reel">{st.session_state.slot_symbols[0]}</div>', unsafe_allow_html=True)
        with reel_col2:
            st.markdown(f'<div class="reel">{st.session_state.slot_symbols[1]}</div>', unsafe_allow_html=True)
        with reel_col3:
            st.markdown(f'<div class="reel">{st.session_state.slot_symbols[2]}</div>', unsafe_allow_html=True)
        
        # Bet amount input
        bet_amount = st.number_input("Bet Amount (€)", min_value=1.0, max_value=100.0, value=10.0, step=1.0, key="slot_bet")
        
        # Spin button
        if st.button("🎰 SPIN TO WIN", key="spin_slots"):
            if total_balance >= bet_amount:
                # Animate reels
                symbols = ['🍒', '🍋', '🔔', '💎', '⭐', '🍇', '🎰']
                
                # Show spinning animation (simulate)
                with st.spinner("Spinning reels..."):
                    time.sleep(1)
                    new_symbols = [random.choice(symbols) for _ in range(3)]
                    st.session_state.slot_symbols = new_symbols
                
                # Place bet and get result
                result = casino.place_bet(player_id, bet_amount)
                if result["success"]:
                    st.session_state.slot_result = result
                    st.rerun()
                else:
                    st.error(result["message"])
            else:
                st.error("Insufficient balance!")
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Display slot result
        if 'slot_result' in st.session_state:
            result = st.session_state.slot_result
            result_class = "result-win" if result["won"] else "result-lose"
            status = "🎉 YOU WON!" if result["won"] else "😔 Try again!"
            
            st.markdown(f"""
            <div class="result-display {result_class}">
                <h3>{status}</h3>
                <p>Bet: €{result['bet_amount']:.2f} | Payout: €{result.get('payout', 0):.2f} | Net: €{result['net_result']:.2f}</p>
                <p>Points Earned: {result.get('points_earned', 0)}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="game-card slide-in-right">
            <h2 class="game-title">
                <span class="game-icon">🎯</span>
                Multi-Bet Challenge
            </h2>
        """, unsafe_allow_html=True)
        
        multi_bet_amount = st.number_input("Bet Amount (€)", min_value=1.0, max_value=50.0, value=5.0, step=1.0, key="multi_bet")
        num_bets = st.number_input("Number of Bets", min_value=1, max_value=20, value=5, step=1)
        
        if st.button("🎯 START CHALLENGE", key="multi_challenge"):
            if total_balance >= (multi_bet_amount * num_bets):
                multi_results = []
                total_wagered = 0
                total_won = 0
                total_points = 0
                
                with st.spinner(f"Placing {num_bets} bets..."):
                    for i in range(num_bets):
                        result = casino.place_bet(player_id, multi_bet_amount)
                        if result["success"]:
                            multi_results.append({
                                "Bet #": i + 1,
                                "Bet Amount": f"€{result['bet_amount']:.2f}",
                                "Won": "✅" if result["won"] else "❌",
                                "Payout": f"€{result.get('payout', 0):.2f}",
                                "Net": f"€{result['net_result']:.2f}"
                            })
                            total_wagered += result['bet_amount']
                            total_won += result.get('payout', 0)
                            total_points += result.get('points_earned', 0)
                        else:
                            st.error(f"Bet {i+1} failed: {result['message']}")
                            break
                
                st.session_state.multi_bet_results = {
                    "results": multi_results,
                    "total_wagered": total_wagered,
                    "total_won": total_won,
                    "net_result": total_won - total_wagered,
                    "total_points": total_points,
                    "win_rate": len([r for r in multi_results if "✅" in r["Won"]]) / len(multi_results) * 100 if multi_results else 0
                }
                st.rerun()
            else:
                st.error("Insufficient balance for all bets!")
        
        # Display multi-bet results
        if 'multi_bet_results' in st.session_state:
            results_data = st.session_state.multi_bet_results
            
            st.markdown(f"""
            <div class="result-display">
                <h3>Challenge Results</h3>
                <div class="stat-row">
                    <div class="stat-card">
                        <span class="stat-value">{len(results_data['results'])}</span>
                        <span class="stat-label">Bets Placed</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-value">€{results_data['total_wagered']:.2f}</span>
                        <span class="stat-label">Total Wagered</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-value">€{results_data['total_won']:.2f}</span>
                        <span class="stat-label">Total Won</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-value">{results_data['total_points']}</span>
                        <span class="stat-label">Points Earned</span>
                    </div>
                </div>
                <p style="text-align: center; margin-top: 1rem;">
                    <strong>Win Rate:</strong> {results_data['win_rate']:.1f}% | 
                    <strong>Net Result:</strong> €{results_data['net_result']:.2f}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Individual results table
            st.markdown("### 📋 Individual Bet Results")
            results_df = pd.DataFrame(results_data['results'])
            st.dataframe(results_df, use_container_width=True, hide_index=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    # Continue with other tabs
    with tab2:
        st.markdown("## 📊 Latest Session Results")
        
        if 'last_session' in st.session_state and st.session_state.last_session:
            session = st.session_state.last_session
            
            if 'error' not in session:
                # Session metrics
                st.markdown("""
                <div class="stat-row">
                    <div class="stat-card">
                        <span class="stat-value">{session["bets_placed"]}</span>
                        <span class="stat-label">Bets Placed</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-value">{session["points_earned"]}</span>
                        <span class="stat-label">Points Earned</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-value">{session["session_duration"]} min</span>
                        <span class="stat-label">Duration</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-value">€{session["ending_balance"]:.2f}</span>
                        <span class="stat-label">Ending Balance</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Financial summary
                st.markdown("""
                <div class="stat-row">
                    <div class="stat-card">
                        <span class="stat-value">€{session["total_wagered"]:.2f}</span>
                        <span class="stat-label">Total Wagered</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-value">€{session["total_won"]:.2f}</span>
                        <span class="stat-label">Total Won</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-value">€{session["net_result"]:.2f}</span>
                        <span class="stat-label">Net Result</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Tournament points earned
                if session.get("tournament_points_earned"):
                    st.markdown("### 🏆 Tournament Points Earned")
                    for tournament_id, points in session["tournament_points_earned"].items():
                        if points > 0:
                            tournament_name = casino.tournaments[tournament_id].name
                            st.markdown(f"""
                            <div class="leaderboard-item">
                                <span>{tournament_name}</span>
                                <span class="stat-value">{points:.2f}</span>
                            </div>
                            """, unsafe_allow_html=True)
                
                # Individual bets table
                if session["individual_bets"]:
                    st.markdown("### 📄 Individual Bets")
                    bet_df = pd.DataFrame(session["individual_bets"])
                    bet_df.index = range(1, len(bet_df) + 1)
                    st.dataframe(bet_df, use_container_width=True)
                    
                    # Session summary stats
                    st.markdown("### 📈 Session Summary")
                    win_rate = (bet_df['won'].sum() / len(bet_df)) * 100
                    biggest_win = bet_df['payout'].max()
                    avg_bet = bet_df['bet'].mean()
                    
                    st.markdown(f"""
                    <div class="stat-row">
                        <div class="stat-card">
                            <span class="stat-value">{win_rate:.1f}%</span>
                            <span class="stat-label">Win Rate</span>
                        </div>
                        <div class="stat-card">
                            <span class="stat-value">€{biggest_win:.2f}</span>
                            <span class="stat-label">Biggest Win</span>
                        </div>
                        <div class="stat-card">
                            <span class="stat-value">€{avg_bet:.2f}</span>
                            <span class="stat-label">Average Bet</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Charts
                    st.markdown("### 📊 Performance Charts")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### Bet Results Distribution")
                        st.bar_chart(bet_df['net'])
                    
                    with col2:
                        st.markdown("#### Cumulative Results")
                        bet_df['cumulative'] = bet_df['net'].cumsum()
                        st.line_chart(bet_df['cumulative'])
            else:
                st.error(f"Session error: {session['error']}")
        else:
            st.info("No session data available. Run a simulation to see results!")

    # Continue with other tabs (tab3 through tab7) following the same pattern
    # For brevity, I'll show one more tab example

    with tab3:
        st.markdown("## 👤 Player Statistics")
        
        stats = casino.get_player_stats(player_id)
        if 'error' not in stats:
            # Player info
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="game-card">
                    <h3>📊 Basic Info</h3>
                    <p><strong>Player ID:</strong> {player_id}</p>
                    <p><strong>Name:</strong> {stats['name']}</p>
                    <p><strong>Tier:</strong> {stats['tier']}</p>
                    <p><strong>Main Balance:</strong> €{stats['balance']:.2f}</p>
                    <p><strong>Bonus Balance:</strong> €{casino.players[player_id].bonus_balance:.2f}</p>
                    <p><strong>Loyalty Points:</strong> {stats['loyalty_points']:,}</p>
                </div>
                """.format(player_id=player_id, **stats), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="game-card">
                    <h3>💰 Financial Summary</h3>
                    <p><strong>Total Deposited:</strong> €{stats['total_deposited']:.2f}</p>
                    <p><strong>Total Wagered:</strong> €{stats['total_wagered']:.2f}</p>
                    <p><strong>Monthly Wagered:</strong> €{stats['monthly_wagered']:.2f}</p>
                    <p><strong>Monthly Losses:</strong> €{stats['monthly_losses']:.2f}</p>
                    <p><strong>Monthly Deposits:</strong> €{casino.players[player_id].monthly_deposits:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Tier benefits
            st.markdown("### 💎 Current Tier Benefits")
            benefits_df = pd.DataFrame([
                {"Benefit": "Monthly Free Spins", "Value": str(stats['tier_benefits']['free_spins_monthly'])},
                {"Benefit": "Loyalty Store Discount", "Value": f"{stats['tier_benefits']['loyalty_store_discount']}%"},
                {"Benefit": "Cashback Percentage", "Value": f"{stats['tier_benefits']['cashback_percentage']}%"},
                {"Benefit": "Deposit Bonus", "Value": f"{stats['tier_benefits']['deposit_bonus_percentage']}%"},
                {"Benefit": "Cashback Cap", "Value": f"€{stats['tier_benefits']['cashback_cap']}"},
                {"Benefit": "Points Multiplier", "Value": str(stats['tier_benefits']['euros_per_point'])}
            ])
            st.dataframe(benefits_df, use_container_width=True, hide_index=True)
            
            # Activity summary
            st.markdown("### ⚡ Activity Summary")
            st.markdown("""
            <div class="stat-row">
                <div class="stat-card">
                    <span class="stat-value">{stats['active_bonuses']}</span>
                    <span class="stat-label">Active Bonuses</span>
                </div>
                <div class="stat-card">
                    <span class="stat-value">{stats['bonus_history']}</span>
                    <span class="stat-label">Bonus History</span>
                </div>
                <div class="stat-card">
                    <span class="stat-value">{stats['tournaments_entered']}</span>
                    <span class="stat-label">Tournaments Entered</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"Error: {stats['error']}")

    # ... (previous imports and setup code remains the same until tab4)

    with tab4:
        st.markdown("## 🎁 Bonus Management")
        
        # Get detailed bonus information
        bonus_info = casino.get_bonus_withdrawal_info(player_id)
        if 'error' not in bonus_info:
            # Bonus summary
            st.markdown("### 📊 Bonus Summary")
            summary = bonus_info['summary']
            
            st.markdown("""
            <div class="stat-row">
                <div class="stat-card">
                    <span class="stat-value">€{:.2f}</span>
                    <span class="stat-label">Total Bonus</span>
                </div>
                <div class="stat-card">
                    <span class="stat-value">€{:.2f}</span>
                    <span class="stat-label">Locked</span>
                </div>
                <div class="stat-card">
                    <span class="stat-value">€{:.2f}</span>
                    <span class="stat-label">Withdrawable</span>
                </div>
                <div class="stat-card">
                    <span class="stat-value">{}</span>
                    <span class="stat-label">Active</span>
                </div>
            </div>
            """.format(
                summary['total_bonus_balance'],
                summary['total_locked_amount'],
                summary['total_withdrawable_amount'],
                summary['active_bonuses_count']
            ), unsafe_allow_html=True)
            
            # Active bonuses with detailed info
            st.markdown("### 🔥 Active Bonuses")
            if bonus_info['bonuses']:
                for bonus in bonus_info['bonuses']:
                    with st.expander(f"{bonus['type']} - €{bonus['amount']:.2f} ({bonus['status']})", expanded=False):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Description:** {bonus['description']}")
                            st.markdown(f"**Amount:** €{bonus['amount']:.2f}")
                            st.markdown(f"**Status:** {bonus['status']}")
                            st.markdown(f"**Expires:** {bonus['expiry_date']}")
                        
                        with col2:
                            st.markdown(f"**Required Wagering:** €{bonus['required_wagering']:.2f}")
                            st.markdown(f"**Wagered Amount:** €{bonus['wagered_amount']:.2f}")
                            st.markdown(f"**Remaining:** €{bonus['remaining_wagering']:.2f}")
                            st.markdown(f"**Progress:** {bonus['progress_percentage']:.1f}%")
                            
                            # Progress bar
                            st.progress(bonus['progress_percentage'] / 100)
                            
                            if bonus['estimated_completion']:
                                st.markdown(f"**Est. Completion:** {bonus['estimated_completion']}")
            else:
                st.info("No active bonuses")
        
        # Available bonuses
        bonuses = casino.get_all_bonuses(player_id)
        if 'error' not in bonuses:
            st.markdown("### ✨ Available Bonuses")
            if bonuses['available_bonuses']:
                for bonus in bonuses['available_bonuses']:
                    with st.expander(f"{bonus['type']}", expanded=False):
                        st.markdown(f"**Description:** {bonus['description']}")
                        st.markdown(f"**Requirements:** {bonus['requirements']}")
            else:
                st.info("No bonuses available to claim")
            
            # Bonus application section
            st.markdown("### 🎯 Apply Bonuses")
            bonus_col1, bonus_col2 = st.columns(2)
            
            with bonus_col1:
                if st.button("🔄 Apply Weekly Reload", key="tab_reload"):
                    success = casino.apply_weekly_reload_bonus(player_id, 100.0)
                    if success:
                        st.success("Weekly reload bonus applied!")
                        st.rerun()
                    else:
                        st.error("Weekly reload not available")
            
            with bonus_col2:
                event_options = ["Halloween Special", "Christmas Bonus", "New Year Celebration"]
                selected_event = st.selectbox("Select Event", event_options)
                if st.button("🎃 Apply Event Bonus", key="tab_event"):
                    success = casino.apply_special_event_bonus(player_id, selected_event, "deposit")
                    if success:
                        st.success(f"{selected_event} bonus applied!")
                        st.rerun()
        else:
            st.error(f"Error: {bonuses['error']}")

    with tab5:
        st.markdown("## 🏆 Tournament Center")
        
        tournaments = casino.get_all_tournaments()
        
        # Tournament entry section
        st.markdown("### 🎯 Enter Tournaments")
        tournament_options = {t['name']: t_id for t_id, t in tournaments.items() 
                            if t['status'] == 'Active'}
        
        if tournament_options:
            selected_tournament = st.selectbox("Select Tournament", list(tournament_options.keys()))
            tournament_id = tournament_options[selected_tournament]
            tournament_info = tournaments[tournament_id]
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Entry Fee:** €{tournament_info['entry_requirements']['entry_fee']}")
                st.markdown(f"**Minimum Tier:** {tournament_info['entry_requirements']['min_tier']}")
                st.markdown(f"**Prize Pool:** €{tournament_info['prize_pool']:,.2f}")
                st.markdown(f"**Description:** {tournament_info['description']}")
            
            with col2:
                st.markdown(f"**Participants:** {tournament_info['participants']}")
                st.markdown(f"**Starts:** {tournament_info['start_date']}")
                st.markdown(f"**Ends:** {tournament_info['end_date']}")
                
                if st.button("🏆 Enter Tournament"):
                    success = casino.enter_tournament(player_id, tournament_id)
                    if success:
                        st.success(f"Entered {selected_tournament}!")
                        st.rerun()
                    else:
                        st.error("Cannot enter tournament (insufficient tier/balance or already entered)")
        else:
            st.info("No active tournaments available for entry")
        
        # Tournament overview
        st.markdown("### 🎮 All Tournaments")
        
        tournament_data = []
        for t_id, tournament in tournaments.items():
            tournament_data.append({
                "Name": tournament['name'],
                "Type": tournament['type'],
                "Status": tournament['status'],
                "Prize Pool": f"€{tournament['prize_pool']:,.2f}",
                "Participants": tournament['participants'],
                "Entry Fee": f"€{tournament['entry_requirements']['entry_fee']}",
                "Min Tier": tournament['entry_requirements']['min_tier'],
                "End Date": tournament['end_date']
            })
        
        tournament_df = pd.DataFrame(tournament_data)
        st.dataframe(tournament_df, use_container_width=True, hide_index=True)
        
        # Leaderboards
        st.markdown("### 🏅 Leaderboards")
        active_tournaments = {t_id: t for t_id, t in tournaments.items() if t['status'] == 'Active'}
        
        if active_tournaments:
            selected_leaderboard = st.selectbox("Select Tournament Leaderboard", 
                                            [t['name'] for t in active_tournaments.values()])
            
            # Find tournament ID
            leaderboard_tournament_id = None
            for t_id, t in active_tournaments.items():
                if t['name'] == selected_leaderboard:
                    leaderboard_tournament_id = t_id
                    break
            
            if leaderboard_tournament_id:
                leaderboard = tournaments[leaderboard_tournament_id]['leaderboard']
                if leaderboard:
                    leaderboard_df = pd.DataFrame(leaderboard)
                    leaderboard_df.index = range(1, len(leaderboard_df) + 1)
                    leaderboard_df.columns = ['Player ID', 'Name', 'Points', 'Tier']
                    st.dataframe(leaderboard_df, use_container_width=True)
                else:
                    st.info("No participants yet in this tournament")
        else:
            st.info("No active tournaments for leaderboards")

    with tab6:
        st.markdown("## 📊 Analytics Dashboard")
        
        # RTP and Game Settings
        st.markdown("### ⚙️ Game Configuration")
        st.markdown("""
        <div class="stat-row">
            <div class="stat-card">
                <span class="stat-value">{:.1f}%</span>
                <span class="stat-label">Current RTP</span>
            </div>
            <div class="stat-card">
                <span class="stat-value">{:.1f}%</span>
                <span class="stat-label">House Edge</span>
            </div>
            <div class="stat-card">
                <span class="stat-value">{:.1f}%</span>
                <span class="stat-label">Win Probability</span>
            </div>
        </div>
        """.format(
            casino.rtp*100,
            casino.house_edge*100,
            casino.rtp/2*100
        ), unsafe_allow_html=True)
        
        # Player progression
        st.markdown("### 📈 Player Progression")
        current_tier = player.tier
        current_points = player.loyalty_points
        
        # Show progression to next tier
        tier_progression = []
        for tier, config in casino.loyalty_config.items():
            tier_progression.append({
                "Tier": tier.value,
                "Points Required": config.points_required,
                "Status": "✅ Achieved" if current_points >= config.points_required else 
                        "🎯 Current" if tier == current_tier else "⏳ Locked"
            })
        
        progression_df = pd.DataFrame(tier_progression)
        st.dataframe(progression_df, use_container_width=True, hide_index=True)
        
        # Session statistics
        if 'last_session' in st.session_state and st.session_state.last_session:
            session = st.session_state.last_session
            st.markdown("### 📊 Last Session Analytics")
            
            if session.get("individual_bets"):
                bets_df = pd.DataFrame(session["individual_bets"])
                
                col1, col2 = st.columns(2)
                with col1:
                    win_rate = (bets_df['won'].sum() / len(bets_df)) * 100
                    st.markdown("""
                    <div class="stat-card">
                        <span class="stat-value">{:.1f}%</span>
                        <span class="stat-label">Win Rate</span>
                    </div>
                    """.format(win_rate), unsafe_allow_html=True)
                    
                    st.markdown("""
                    <div class="stat-card">
                        <span class="stat-value">€{:.2f}</span>
                        <span class="stat-label">Average Bet</span>
                    </div>
                    """.format(bets_df['bet'].mean()), unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div class="stat-card">
                        <span class="stat-value">€{:.2f}</span>
                        <span class="stat-label">Largest Win</span>
                    </div>
                    """.format(bets_df['payout'].max()), unsafe_allow_html=True)
                    
                    st.markdown("""
                    <div class="stat-card">
                        <span class="stat-value">{}</span>
                        <span class="stat-label">Total Bets</span>
                    </div>
                    """.format(len(bets_df)), unsafe_allow_html=True)
                
                # Win/Loss chart
                st.markdown("### 📈 Bet Results Chart")
                st.bar_chart(bets_df.set_index(bets_df.index)['net'])
                
                # Cumulative results
                bets_df['cumulative'] = bets_df['net'].cumsum()
                st.markdown("### 📊 Cumulative Results")
                st.line_chart(bets_df.set_index(bets_df.index)['cumulative'])

    with tab7:
        st.markdown("## 🎮 Quick Play")
        
        st.markdown("### 🎲 Individual Bet Simulator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            quick_bet_amount = st.number_input("Bet Amount (€)", min_value=1.0, max_value=100.0, value=10.0, step=1.0, key="quick_bet")
            
            if st.button("🎰 Place Bet", key="quick_bet"):
                if total_balance >= quick_bet_amount:
                    result = casino.place_bet(player_id, quick_bet_amount)
                    if result["success"]:
                        st.session_state.quick_bet_result = result
                        st.rerun()
                    else:
                        st.error(result["message"])
                else:
                    st.error("Insufficient balance!")
        
        with col2:
            if 'quick_bet_result' in st.session_state:
                result = st.session_state.quick_bet_result
                result_class = "result-win" if result["won"] else "result-lose"
                status = "🎉 YOU WON!" if result["won"] else "😔 You lost"
                
                st.markdown(f"""
                <div class="result-display {result_class}">
                    <h3>{status}</h3>
                    <p>Bet: €{result['bet_amount']:.2f}</p>
                    <p>Payout: €{result.get('payout', 0):.2f}</p>
                    <p>Net Result: €{result['net_result']:.2f}</p>
                    <p>New Balance: €{result['new_balance']:.2f}</p>
                    <p>Points Earned: {result.get('points_earned', 0)}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Multi-bet simulator
        st.markdown("### 🎯 Multi-Bet Simulator")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            multi_bet_amount = st.number_input("Bet Amount (€)", min_value=1.0, max_value=50.0, value=5.0, step=1.0, key="multi_bet")
        
        with col2:
            num_bets = st.number_input("Number of Bets", min_value=1, max_value=20, value=5, step=1)
        
        with col3:
            if st.button("🎰 Place Multiple Bets", key="multi_bet_button"):
                if total_balance >= (multi_bet_amount * num_bets):
                    multi_results = []
                    total_wagered = 0
                    total_won = 0
                    total_points = 0
                    
                    with st.spinner(f"Placing {num_bets} bets..."):
                        for i in range(num_bets):
                            result = casino.place_bet(player_id, multi_bet_amount)
                            if result["success"]:
                                multi_results.append({
                                    "Bet #": i + 1,
                                    "Bet Amount": f"€{result['bet_amount']:.2f}",
                                    "Won": "✅" if result["won"] else "❌",
                                    "Payout": f"€{result.get('payout', 0):.2f}",
                                    "Net": f"€{result['net_result']:.2f}"
                                })
                                total_wagered += result['bet_amount']
                                total_won += result.get('payout', 0)
                                total_points += result.get('points_earned', 0)
                            else:
                                st.error(f"Bet {i+1} failed: {result['message']}")
                                break
                    
                    st.session_state.multi_bet_results = {
                        "results": multi_results,
                        "total_wagered": total_wagered,
                        "total_won": total_won,
                        "net_result": total_won - total_wagered,
                        "total_points": total_points,
                        "win_rate": len([r for r in multi_results if "✅" in r["Won"]]) / len(multi_results) * 100 if multi_results else 0
                    }
                    st.rerun()
                else:
                    st.error("Insufficient balance for all bets!")
        
        # Display multi-bet results
        if 'multi_bet_results' in st.session_state:
            st.markdown("### 📊 Multi-Bet Results")
            
            results_data = st.session_state.multi_bet_results
            
            # Summary metrics
            st.markdown("""
            <div class="stat-row">
                <div class="stat-card">
                    <span class="stat-value">{}</span>
                    <span class="stat-label">Bets Placed</span>
                </div>
                <div class="stat-card">
                    <span class="stat-value">€{:.2f}</span>
                    <span class="stat-label">Total Wagered</span>
                </div>
                <div class="stat-card">
                    <span class="stat-value">€{:.2f}</span>
                    <span class="stat-label">Total Won</span>
                </div>
                <div class="stat-card">
                    <span class="stat-value">{}</span>
                    <span class="stat-label">Points Earned</span>
                </div>
            </div>
            """.format(
                len(results_data['results']),
                results_data['total_wagered'],
                results_data['total_won'],
                results_data['total_points']
            ), unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-container">
                <div style="text-align: center;">
                    <div class="stat-value">{results_data['win_rate']:.1f}%</div>
                    <div class="stat-label">Win Rate</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Individual results table
            if results_data['results']:
                st.markdown("### 📋 Individual Bet Results")
                results_df = pd.DataFrame(results_data['results'])
                st.dataframe(results_df, use_container_width=True, hide_index=True)
        
        # Quick stats section
        st.markdown("### ⚡ Quick Stats")
        
        current_player = casino.players[player_id]
        
        st.markdown("""
        <div class="stat-row">
            <div class="stat-card">
                <span class="stat-value">{}</span>
                <span class="stat-label">Current Tier</span>
            </div>
            <div class="stat-card">
                <span class="stat-value">€{:.2f}</span>
                <span class="stat-label">Today's Wagering</span>
            </div>
            <div class="stat-card">
                <span class="stat-value">{}</span>
                <span class="stat-label">Active Bonuses</span>
            </div>
        </div>
        """.format(
            current_player.tier.value,
            current_player.daily_wagering,
            len(current_player.active_bonuses)
        ), unsafe_allow_html=True)
        
        # Balance management
        st.markdown("### 💰 Balance Management")
        
        balance_col1, balance_col2 = st.columns(2)
        
        with balance_col1:
            st.markdown("""
            <div class="game-card">
                <h3>Current Balances</h3>
                <p>• Main Balance: €{:.2f}</p>
                <p>• Bonus Balance: €{:.2f}</p>
                <p>• <strong>Total Available: €{:.2f}</strong></p>
            </div>
            """.format(
                current_player.balance,
                current_player.bonus_balance,
                total_balance
            ), unsafe_allow_html=True)
        
        with balance_col2:
            st.markdown("""
            <div class="game-card">
                <h3>Quick Actions</h3>
            """, unsafe_allow_html=True)
            
            if st.button("🔄 Refresh Balance", key="refresh_balance"):
                st.rerun()
            
            if st.button("💸 Simulate Loss (€10)", key="simulate_loss"):
                if current_player.balance >= 10:
                    current_player.balance -= 10
                    current_player.monthly_losses += 10
                    st.success("Simulated €10 loss")
                    st.rerun()
                else:
                    st.error("Insufficient balance")
            
            if st.button("💰 Quick Deposit (€100)", key="quick_deposit"):
                casino.deposit(player_id, 100.0, current_player.email)
                st.success("Deposited €100")
                st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Game settings for quick play
        st.markdown("### ⚙️ Quick Play Settings")
        
        settings_col1, settings_col2 = st.columns(2)
        
        with settings_col1:
            st.markdown(f"**Current RTP:** {casino.rtp*100:.1f}%")
            st.markdown(f"**House Edge:** {casino.house_edge*100:.1f}%")
            
            # Quick RTP adjustment
            quick_rtp = st.selectbox(
                "Quick RTP Setting:",
                [85, 90, 92, 95, 96, 97, 98],
                index=3,  # Default to 95%
                format_func=lambda x: f"{x}% RTP"
            )
            
            if st.button("🔧 Apply RTP", key="apply_quick_rtp"):
                casino.set_rtp(quick_rtp / 100)
                st.success(f"RTP set to {quick_rtp}%")
                st.rerun()
        
        with settings_col2:
            st.markdown("**Tier Progress:**")
            
            # Show progress to next tier
            next_tier = None
            for tier, config in casino.loyalty_config.items():
                if config.points_required > current_player.loyalty_points:
                    next_tier = tier
                    break
            
            if next_tier:
                next_tier_points = casino.loyalty_config[next_tier].points_required
                progress = (current_player.loyalty_points / next_tier_points) * 100
                points_needed = next_tier_points - current_player.loyalty_points
                
                st.markdown(f"**Next Tier:** {next_tier.value}")
                st.markdown(f"**Points Needed:** {points_needed:,}")
                st.progress(min(progress / 100, 1.0))
            else:
                st.success("🏆 Max Tier Achieved!")