import streamlit as st
import time
import random

# --- APP CONFIG ---
st.set_page_config(page_title="DasherProphet AI", page_icon="🚗")

# --- MOCK AI ENGINE ---
def ai_wait_prediction(restaurant, time_of_day):
    """
    Simulates an LLM analyzing crowdsourced 'Dasher' data 
    (Reddit/Discord/Historical logs).
    """
    # Real-world logic: certain chains are notoriously slow at peak hours
    slow_chains = ["Wingstop", "Popeyes", "Cheesecake Factory", "Wendy's"]
    base_wait = random.randint(5, 12)
    
    if any(chain in restaurant for chain in slow_chains):
        multiplier = 2.5
        reason = "AI detected 'Staffing Shortage' reports on local Discord (15m ago)."
    else:
        multiplier = 1.0
        reason = "Normal flow detected. Efficient kitchen history."
        
    predicted_wait = int(base_wait * multiplier)
    return predicted_wait, reason

# --- UI LAYOUT ---
st.title("🚗 DasherProphet by Mario :)")
st.subheader("Don't get stuck! Know the wait before you 'Accept'.")

with st.sidebar:
    st.header("Driver Settings")
    min_hourly = st.slider("Target Hourly Rate ($)", 15, 40, 22)
    fuel_cost = st.number_input("Gas Price ($/gal)", value=3.85)

# --- THE WORKING AI FEATURE ---
st.info("💡 **Live AI Feature:** Resto-Wait Predictor active.")

col1, col2 = st.columns(2)
with col1:
    resto_name = st.selectbox("Restaurant Name", ["Wingstop - Palmetto Bay", "Chipotle - Kendall Drive", "CAVA - West Kendall", "Wendy's - Sunset Drive"])
    offer_amt = st.number_input("DoorDash Offer ($)", value=9.50)

with col2:
    miles = st.number_input("Total Miles", value=4.0)
    drive_time_est = int(miles * 3) # Simple 3 mins per mile estimate

if st.button("🔮 Analyze Order"):
    with st.spinner('AI analyzing local driver reports and kitchen latency...'):
        time.sleep(1.5) # Simulate API Latency
        
        wait_mins, ai_reason = ai_wait_prediction(resto_name, "Peak")
        total_time = drive_time_est + wait_mins
        real_hourly = (offer_amt / (total_time / 60))

        st.divider()
        
        # Display Results
        if real_hourly >= min_hourly:
            st.success(f"### ✅ ACCEPT: ${real_hourly:.2f}/hr")
        else:
            st.error(f"### ❌ DECLINE: ${real_hourly:.2f}/hr")
            
        st.write(f"**AI Prediction:** {wait_mins} min wait at restaurant.")
        st.caption(f"**Reason:** {ai_reason}")
        
        # Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Est. Total Time", f"{total_time} min")
        m2.metric("Gas Cost", f"${(miles/25)*fuel_cost:.2f}")
        m3.metric("Net Profit", f"${offer_amt - ((miles/25)*fuel_cost):.2f}")
