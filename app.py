import streamlit as st
from textblob import TextBlob
import pandas as pd
import random

# Initialize global variables
orders = []
rewards = 0
inventory = {'milk': 10, 'sugar': 10, 'coffee': 10}

# Coffee types based on mood
coffee_suggestions = {
    'happy': 'Cappuccino',
    'sad': 'Hot Chocolate',
    'tired': 'Espresso',
    'neutral': 'Latte'
}

# Function to detect mood and suggest coffee
def detect_mood(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return coffee_suggestions['happy']
    elif analysis.sentiment.polarity < 0:
        return coffee_suggestions['sad']
    else:
        return coffee_suggestions['neutral']

# Function to simulate order processing
def process_order(order):
    global rewards
    orders.append(order)
    rewards += 1  # Increment rewards for each order
    st.success(f"Order placed: {order}")
    st.balloons()  # Show balloons for a fun effect

# Function to display daily consumption report
def display_report():
    if orders:
        df = pd.DataFrame(orders, columns=["Order"])
        st.write("Daily Coffee Orders:")
        st.dataframe(df)
        st.bar_chart(df['Order'].value_counts())

# Function to check inventory
def check_inventory():
    for item, amount in inventory.items():
        if amount < 3:
            st.warning(f"Low on {item}. Please refill!")

# Main application
def main():
    st.title("Code Caffe - Smart Coffee Vending Machine")

    # WhatsApp/Telegram Ordering
    order_input = st.text_input("Order via WhatsApp/Telegram:")
    if st.button("Place Order"):
        if order_input:
            mood = detect_mood(order_input)
            process_order(mood)

    # Coffee Customization Options
    st.sidebar.header("Coffee Customization")
    coffee_type = st.sidebar.selectbox("Select Coffee Type", list(coffee_suggestions.values()))
    sugar_level = st.sidebar.slider("Sugar Level", 0, 5, 2)
    milk_quantity = st.sidebar.slider("Milk Quantity", 0, 5, 2)
    coffee_strength = st.sidebar.slider("Coffee Strength", 1, 5, 3)
    size = st.sidebar.selectbox("Size", ["Small", "Medium", "Large"])
    
    if st.sidebar.button("Save Favorite Customization"):
        st.success("Favorite customization saved!")

    # Eco-Friendly Mode
    eco_friendly = st.sidebar.checkbox("Use Reusable Cup")
    if eco_friendly:
        global rewards
        rewards += 1  # Increment rewards for using a reusable cup
        st.success("Thank you for using a reusable cup! Rewards increased.")

    # AI Queue Management System
    st.sidebar.header("Order Queue")
    st.sidebar.write("Current Orders:")
    for idx, order in enumerate(orders):
        st.sidebar.write(f"{idx + 1}. {order}")

    # Personalized Greeting
    if orders:
        st.success("Good Morning, enjoy your coffee!")

    # Daily Consumption Report
    display_report()

    # Health Tip / Motivational Quote
    health_tips = [
        "Stay hydrated!",
        "Take short breaks while working.",
        "Remember to stretch!",
        "A positive mindset brings positive things."
    ]
    st.write(random.choice(health_tips))

    # Refill Reminder (Simulated)
    check_inventory()

if __name__ == "__main__":
    main()
