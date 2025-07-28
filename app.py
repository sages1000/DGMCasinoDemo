import streamlit as st
import pandas as pd
from MysticSimulator import MysticWagerCasino, LoyaltyTier

# Page config
st.set_page_config(
    page_title="🎰 Mystic Wager Casino",
    page_icon="🎰",
    layout="wide"
)

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

# Main title
st.title("🎰 Mystic Wager Casino - Complete Experience")

# Sidebar for controls
st.sidebar.title("🎛️ Casino Controls")

# Current balance display
current_balance = casino.players[player_id].balance
st.sidebar.metric("💰 Current Balance", f"€{current_balance:.2f}")

# Tier Management Section
st.sidebar.subheader("🏆 Tier Point Management")

# Display current player tier and points
current_tier = casino.players[player_id].tier
current_points = casino.players[player_id].loyalty_points
st.sidebar.write(f"**Current Tier:** {current_tier.value}")
st.sidebar.write(f"**Current Points:** {current_points:,}")

# Tier point adjustment controls
with st.sidebar.expander("⚙️ Adjust Tier Requirements", expanded=False):
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
st.sidebar.subheader("⚡ Quick Point Adjustment")
point_adjustment = st.sidebar.selectbox(
    "Adjust Player Points:",
    [0, 100, 500, 1000, 2500, 5000, 10000, -100, -500, -1000],
    format_func=lambda x: f"{'Add' if x >= 0 else 'Remove'} {abs(x):,} points" if x != 0 else "No change"
)

if st.sidebar.button("🎯 Apply Point Adjustment") and point_adjustment != 0:
    old_points = casino.players[player_id].loyalty_points
    old_tier = casino.players[player_id].tier
    
    # Apply adjustment (ensure points don't go below 0)
    casino.players[player_id].loyalty_points = max(0, old_points + point_adjustment)
    
    # Update tier
    casino._update_player_tier(casino.players[player_id])
    
    new_points = casino.players[player_id].loyalty_points
    new_tier = casino.players[player_id].tier
    
    if new_tier != old_tier:
        st.sidebar.success(f"Points: {old_points:,} → {new_points:,}\nTier: {old_tier.value} → {new_tier.value}")
    else:
        st.sidebar.success(f"Points adjusted: {old_points:,} → {new_points:,}")
    st.rerun()

# Deposit section
st.sidebar.subheader("💵 Make Deposit")
deposit_amount = st.sidebar.slider("Amount (€)", 10, 10000, 500)
if st.sidebar.button("💵 Deposit"):
    success = casino.deposit(player_id, deposit_amount, email)
    if success:
        st.sidebar.success(f"Deposited €{deposit_amount}")
        st.rerun()

# Session simulation
st.sidebar.subheader("🎮 Session Settings")
session_minutes = st.sidebar.slider("⏱️ Duration (min)", 10, 300, 60)
average_bet = st.sidebar.slider("🎲 Avg Bet (€)", 1.0, 50.0, 10.0)
rtp = st.sidebar.slider("📈 RTP (%)", 80, 99, 95)

casino.set_rtp(rtp / 100)

if st.sidebar.button("▶️ Simulate Session"):
    if current_balance <= 0:
        st.sidebar.error("Please make a deposit first!")
    else:
        session = casino.simulate_player_session(player_id, session_minutes, average_bet)
        st.session_state.last_session = session

# Bonus section
st.sidebar.subheader("🎁 Quick Bonuses")
if st.sidebar.button("🔄 Weekly Reload (25%)"):
    success = casino.apply_weekly_reload_bonus(player_id, 100.0, "RELOAD25")
    if success:
        st.sidebar.success("Weekly reload applied!")
        st.rerun()
    else:
        st.sidebar.error("Already used this week")

if st.sidebar.button("🎃 Special Event Bonus"):
    success = casino.apply_special_event_bonus(player_id, "Halloween Special", "free_spins")
    if success:
        st.sidebar.success("Event bonus applied!")
        st.rerun()

if st.sidebar.button("📅 Process Monthly Rewards"):
    casino.process_monthly_rewards(player_id)
    st.sidebar.success("Monthly rewards processed!")
    st.rerun()

# Main content area with tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🎰 Session Results", "👤 Player Stats", "🎁 Bonuses", "🏆 Tournaments", "📊 Analytics", "🏆 Tier System"])

with tab1:
    st.header("🎰 Latest Session Results")
    
    if 'last_session' in st.session_state and st.session_state.last_session:
        session = st.session_state.last_session
        
        if 'error' not in session:
            # Session metrics
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Bets Placed", session["bets_placed"])
            col2.metric("Points Earned", session["points_earned"])
            col3.metric("Duration", f"{session['session_duration']} min")
            col4.metric("Ending Balance", f"€{session['ending_balance']:.2f}")
            
            col5, col6, col7 = st.columns(3)
            col5.metric("Total Wagered", f"€{session['total_wagered']:.2f}")
            col6.metric("Total Won", f"€{session['total_won']:.2f}")
            col7.metric("Net Result", f"€{session['net_result']:.2f}", 
                       delta=f"€{session['net_result']:.2f}")
            
            # Tournament points earned
            if session.get("tournament_points_earned"):
                st.subheader("🏆 Tournament Points Earned")
                for tournament_id, points in session["tournament_points_earned"].items():
                    tournament_name = casino.tournaments[tournament_id].name
                    st.write(f"**{tournament_name}:** {points:.2f} points")
            
            # Individual bets table
            if session["individual_bets"]:
                st.subheader("📄 Individual Bets")
                bet_df = pd.DataFrame(session["individual_bets"])
                bet_df.index = range(1, len(bet_df) + 1)
                st.dataframe(bet_df, use_container_width=True)
        else:
            st.error(f"Session error: {session['error']}")
    else:
        st.info("No session data available. Run a simulation to see results!")

with tab2:
    st.header("👤 Player Statistics")
    
    stats = casino.get_player_stats(player_id)
    if 'error' not in stats:
        # Player info
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📊 Basic Info")
            st.write(f"**Player ID:** {stats['player_id']}")
            st.write(f"**Name:** {stats['name']}")
            st.write(f"**Tier:** {stats['tier']}")
            st.write(f"**Balance:** €{stats['balance']:.2f}")
            st.write(f"**Loyalty Points:** {stats['loyalty_points']:,}")
        
        with col2:
            st.subheader("💰 Financial Summary")
            st.write(f"**Total Deposited:** €{stats['total_deposited']:.2f}")
            st.write(f"**Total Wagered:** €{stats['total_wagered']:.2f}")
            st.write(f"**Monthly Wagered:** €{stats['monthly_wagered']:.2f}")
            st.write(f"**Monthly Losses:** €{stats['monthly_losses']:.2f}")
        
        # Tier benefits
        st.subheader("💎 Current Tier Benefits")
        benefits_df = pd.DataFrame([
            {"Benefit": "Monthly Free Spins", "Value": str(stats['tier_benefits']['free_spins_monthly'])},
            {"Benefit": "Loyalty Store Discount", "Value": f"{stats['tier_benefits']['loyalty_store_discount']}%"},
            {"Benefit": "Cashback Percentage", "Value": f"{stats['tier_benefits']['cashback_percentage']}%"},
            {"Benefit": "Deposit Bonus", "Value": f"{stats['tier_benefits']['deposit_bonus_percentage']}%"},
            {"Benefit": "Cashback Cap", "Value": f"€{stats['tier_benefits']['cashback_cap']}"},
            {"Benefit": "Euros per Point", "Value": str(stats['tier_benefits']['euros_per_point'])}
        ])
        st.dataframe(benefits_df, use_container_width=True, hide_index=True)
        
        # Activity summary
        col3, col4, col5 = st.columns(3)
        col3.metric("Active Bonuses", stats['active_bonuses'])
        col4.metric("Bonus History", stats['bonus_history'])
        col5.metric("Tournaments Entered", stats['tournaments_entered'])
    else:
        st.error(f"Error: {stats['error']}")

with tab3:
    st.header("🎁 Bonus Management")
    
    bonuses = casino.get_all_bonuses(player_id)
    if 'error' not in bonuses:
        # Active bonuses
        st.subheader("🔥 Active Bonuses")
        if bonuses['active_bonuses']:
            for i, bonus in enumerate(bonuses['active_bonuses']):
                with st.expander(f"{bonus['type']} - €{bonus['amount']:.2f}"):
                    st.write(f"**Description:** {bonus['description']}")
                    st.write(f"**Wagering Requirement:** {bonus['wagering_requirement']}x")
                    st.write(f"**Expires:** {bonus['expiry_date']}")
                    st.write(f"**Status:** {'Used' if bonus['used'] else 'Available'}")
        else:
            st.info("No active bonuses")
        
        # Available bonuses
        st.subheader("✨ Available Bonuses")
        if bonuses['available_bonuses']:
            for bonus in bonuses['available_bonuses']:
                with st.expander(f"{bonus['type']}"):
                    st.write(f"**Description:** {bonus['description']}")
                    st.write(f"**Requirements:** {bonus['requirements']}")
        else:
            st.info("No bonuses available to claim")
        
        # Bonus application section
        st.subheader("🎯 Apply Bonuses")
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

with tab4:
    st.header("🏆 Tournament Center")
    
    tournaments = casino.get_all_tournaments()
    
    # Tournament entry section
    st.subheader("🎯 Enter Tournaments")
    tournament_options = {t['name']: t_id for t_id, t in tournaments.items() 
                         if t['status'] == 'Active'}
    
    if tournament_options:
        selected_tournament = st.selectbox("Select Tournament", list(tournament_options.keys()))
        tournament_id = tournament_options[selected_tournament]
        tournament_info = tournaments[tournament_id]
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Entry Fee:** €{tournament_info['entry_requirements']['entry_fee']}")
            st.write(f"**Minimum Tier:** {tournament_info['entry_requirements']['min_tier']}")
            st.write(f"**Prize Pool:** €{tournament_info['prize_pool']:,.2f}")
        
        with col2:
            st.write(f"**Participants:** {tournament_info['participants']}")
            st.write(f"**Ends:** {tournament_info['end_date']}")
            
            if st.button("🏆 Enter Tournament"):
                success = casino.enter_tournament(player_id, tournament_id)
                if success:
                    st.success(f"Entered {selected_tournament}!")
                    st.rerun()
                else:
                    st.error("Cannot enter tournament (insufficient tier/balance or already entered)")
    
    # Tournament overview
    st.subheader("🎮 All Tournaments")
    
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
    st.subheader("🏅 Leaderboards")
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

with tab5:
    st.header("📊 Analytics Dashboard")
    
    # RTP and Game Settings
    st.subheader("⚙️ Game Configuration")
    col1, col2, col3 = st.columns(3)
    col1.metric("Current RTP", f"{casino.rtp*100:.1f}%")
    col2.metric("House Edge", f"{casino.house_edge*100:.1f}%")
    col3.metric("Win Probability", f"{casino.rtp/2*100:.1f}%")
    
    # Player progression
    st.subheader("📈 Player Progression")
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
        st.subheader("📊 Last Session Analytics")
        
        if session.get("individual_bets"):
            bets_df = pd.DataFrame(session["individual_bets"])
            
            col1, col2 = st.columns(2)
            with col1:
                win_rate = (bets_df['won'].sum() / len(bets_df)) * 100
                st.metric("Win Rate", f"{win_rate:.1f}%")
                st.metric("Average Bet", f"€{bets_df['bet'].mean():.2f}")
            
            with col2:
                st.metric("Largest Win", f"€{bets_df['payout'].max():.2f}")
                st.metric("Total Bets", len(bets_df))
            
            # Win/Loss chart
            st.bar_chart(bets_df.set_index(bets_df.index)['net'])

with tab6:
    st.header("🏆 Tier System Overview")
    
    # Current tier configuration
    st.subheader("🎯 Current Tier Requirements")
    
    tier_config_data = []
    for tier, config in casino.loyalty_config.items():
        # Check if player would qualify for this tier
        player_qualifies = current_points >= config.points_required
        status = "✅ Achieved" if player_qualifies else "⏳ Locked"
        if tier == current_tier:
            status = "🎯 Current Tier"
        
        tier_config_data.append({
            "Tier": tier.value,
            "Points Required": f"{config.points_required:,}",
            "Monthly Free Spins": config.free_spins_monthly,
            "Cashback %": f"{config.cashback_percentage}%",
            "Deposit Bonus %": f"{config.deposit_bonus_percentage}%",
            "Cashback Cap": f"€{config.cashback_cap}",
            "Points Multiplier": f"{config.euros_per_point}x",
            "Status": status
        })
    
    tier_df = pd.DataFrame(tier_config_data)
    st.dataframe(tier_df, use_container_width=True, hide_index=True)
    
    # Tier progression visualization
    st.subheader("📈 Your Progression")
    
    # Calculate progress to next tier
    next_tier = None
    for tier, config in casino.loyalty_config.items():
        if config.points_required > current_points:
            next_tier = tier
            break
    
    if next_tier:
        next_tier_points = casino.loyalty_config[next_tier].points_required
        progress_percentage = (current_points / next_tier_points) * 100
        points_needed = next_tier_points - current_points
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Points", f"{current_points:,}")
        col2.metric("Next Tier", next_tier.value)
        col3.metric("Points Needed", f"{points_needed:,}")
        
        # Progress bar
        st.progress(min(progress_percentage / 100, 1.0))
        st.write(f"Progress to {next_tier.value}: {progress_percentage:.1f}%")
    else:
        st.success("🎉 Congratulations! You've reached the highest tier (Elite)!")
    
    # Tier benefits comparison
    st.subheader("💎 Tier Benefits Comparison")
    
    current_config = casino.loyalty_config[current_tier]
    
    if next_tier:
        next_config = casino.loyalty_config[next_tier]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Current Tier: {current_tier.value}**")
            st.write(f"• Monthly Free Spins: {current_config.free_spins_monthly}")
            st.write(f"• Cashback: {current_config.cashback_percentage}%")
            st.write(f"• Deposit Bonus: {current_config.deposit_bonus_percentage}%")
            st.write(f"• Points Multiplier: {current_config.euros_per_point}x")
        
        with col2:
            st.write(f"**Next Tier: {next_tier.value}**")
            st.write(f"• Monthly Free Spins: {next_config.free_spins_monthly} (+{next_config.free_spins_monthly - current_config.free_spins_monthly})")
            st.write(f"• Cashback: {next_config.cashback_percentage}% (+{next_config.cashback_percentage - current_config.cashback_percentage}%)")
            st.write(f"• Deposit Bonus: {next_config.deposit_bonus_percentage}% (+{next_config.deposit_bonus_percentage - current_config.deposit_bonus_percentage}%)")
            st.write(f"• Points Multiplier: {next_config.euros_per_point}x (+{next_config.euros_per_point - current_config.euros_per_point}x)")

# Footer
st.markdown("---")
st.markdown("🎰 **Mystic Wager Casino** - Complete Casino Experience Simulator")
st.markdown("*Featuring loyalty tiers, tournaments, comprehensive bonuses, and real-time analytics*")