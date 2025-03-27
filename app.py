import streamlit as st
import speech_recognition as sr
from textblob import TextBlob
import pandas as pd
import random
import datetime

# Initialize global variables
orders = []
rewards = 0
inventory = {'milk': 10, 'sugar': 10, 'coffee': 10}

# Coffee types based on mood
coffee_suggestions = {
    'happy': 'Cappuccino',
    'sad': 'Hot Chocolate',
    'tired': 'Espresso',
    'neutral': 'Latte',
    'excited': 'Mocha',
    'stressed': 'Americano',
    'relaxed': 'Flat White',
    'bored': 'Cold Brew',
    'adventurous': 'Affogato'
}

# Function to detect mood and suggest coffee
def detect_mood(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return coffee_suggestions['happy']
    elif analysis.sentiment.polarity < 0:
        return coffee_suggestions['sad']
    elif "tired" in text.lower():
        return coffee_suggestions['tired']
    elif "excited" in text.lower():
        return coffee_suggestions['excited']
    elif "stressed" in text.lower():
        return coffee_suggestions['stressed']
    elif "relaxed" in text.lower():
        return coffee_suggestions['relaxed']
    elif "bored" in text.lower():
        return coffee_suggestions['bored']
    elif "adventurous" in text.lower():
        return coffee_suggestions['adventurous']
    else:
        return coffee_suggestions['neutral']

# Function to convert speech to text
def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening for your order...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language='en-IN')  # Change language code as needed
            st.success("You said: " + text)
            return text
        except sr.UnknownValueError:
            st.error("Could not understand audio")
            return ""
        except sr.RequestError as e:
            st.error(f"Could not request results; {e}")
            return ""

# Function to process order
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

# Function to simulate payment
def simulate_payment():
    st.success("Payment successful! Thank you for your order.")

# Main application
def main():
    st.title("Code Caffe - Smart Coffee Vending Machine")

    # Voice Ordering
    if st.button("Order via Voice"):
        order_input = speech_to_text()
        if order_input:
            mood = detect_mood(order_input)
            process_order(mood)

    # WhatsApp Ordering Simulation
    order_input = st.text_input("Order via WhatsApp:")
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

    # Touchless Payment Option
    if st.button("Confirm Order and Pay"):
        simulate_payment()

if __name__ == "__
    main()
