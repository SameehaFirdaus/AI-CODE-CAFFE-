import streamlit as st
import cv2
import numpy as np
import tempfile
import time
import speech_recognition as sr
import pandas as pd
import random
from textblob import TextBlob
from deepface import DeepFace

# Initialize session states
if "order_queue" not in st.session_state:
    st.session_state.order_queue = []
if "daily_report" not in st.session_state:
    st.session_state.daily_report = []

# Mood to coffee mapping
mood_to_coffee = {
    "happy": "Cappuccino ☕",
    "sad": "Hot Chocolate 🍫",
    "angry": "Black Coffee ☕",
    "surprise": "Mocha ☕",
    "fear": "Latte ☕",
    "neutral": "Espresso ☕",
}

# Health tips & motivational quotes
health_tips = [
    "Drink water with coffee to stay hydrated.",
    "Too much caffeine can affect sleep.",
    "Try decaf in the evening for better rest.",
]
motivational_quotes = [
    "Your energy is fueled by determination and caffeine!",
    "Success is brewing! Keep going!",
    "Every day is a fresh start. Enjoy your coffee!",
]

# Function to detect mood from image
def detect_mood(img_path):
    try:
        analysis = DeepFace.analyze(img_path, actions=["emotion"], enforce_detection=False)
        detected_emotion = analysis[0]["dominant_emotion"]
        return detected_emotion.capitalize(), mood_to_coffee.get(detected_emotion, "Espresso ☕")
    except Exception as e:
        return "Neutral", "Espresso ☕"

# Function to get voice command
def get_voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now!")
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            return command
        except:
            return "Could not understand voice."

# Function to add order to queue
def add_order(name, coffee_type, size, sugar, milk):
    order = {
        "Name": name,
        "Coffee": coffee_type,
        "Size": size,
        "Sugar": sugar,
        "Milk": milk,
        "Time": time.strftime("%H:%M:%S"),
    }
    st.session_state.order_queue.append(order)
    st.session_state.daily_report.append(order)

# Streamlit UI
st.title("☕ Code Caffe - AI-Powered Coffee Vending Machine")

# Face-Based Mood Detection
st.subheader("🎥 Detect Mood & Get Coffee Suggestion")
cam = cv2.VideoCapture(0)

if st.button("Capture Mood"):
    ret, frame = cam.read()
    if ret:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as img_file:
            img_path = img_file.name
            cv2.imwrite(img_path, frame)
        
        st.image(img_path, caption="Captured Image", use_column_width=True)
        mood, coffee_suggestion = detect_mood(img_path)
        st.success(f"Detected Mood: {mood}")
        st.info(f"Suggested Coffee: {coffee_suggestion}")
        st.session_state["last_suggested_coffee"] = coffee_suggestion

cam.release()

# Voice Command Ordering
st.subheader("🎙️ Order via Voice")
if st.button("Speak"):
    voice_text = get_voice_command()
    st.write("You said:", voice_text)
    if voice_text != "Could not understand voice.":
        analysis = TextBlob(voice_text)
        polarity = analysis.sentiment.polarity
        mood = "Happy" if polarity > 0.3 else "Sad" if polarity < -0.3 else "Neutral"
        coffee_suggestion = mood_to_coffee.get(mood.lower(), "Espresso ☕")
        st.success(f"Detected Mood from Voice: {mood}")
        st.info(f"Suggested Coffee: {coffee_suggestion}")

# Coffee Customization
st.subheader("☕ Customize Your Coffee")
name = st.text_input("Enter Your Name", "Guest")
coffee_type = st.selectbox("Select Coffee Type", ["Cappuccino", "Espresso", "Latte", "Mocha", "Hot Chocolate"])
size = st.radio("Select Size", ["Small", "Medium", "Large"])
sugar = st.slider("Sugar Level", 0, 5, 2)
milk = st.slider("Milk Quantity", 0, 5, 3)

if st.button("Place Order"):
    add_order(name, coffee_type, size, sugar, milk)
    st.success(f"Order placed: {coffee_type} for {name} ☕")

# AI Queue Management
st.subheader("📋 Order Queue")
if len(st.session_state.order_queue) > 0:
    for idx, order in enumerate(st.session_state.order_queue):
        st.write(f"{idx+1}. {order['Name']} - {order['Coffee']} ({order['Size']})")
else:
    st.write("No pending orders.")

# Personalized Greeting
st.subheader("👋 Personalized Greeting")
if len(st.session_state.order_queue) > 0:
    current_order = st.session_state.order_queue[0]
    st.success(f"Good day, {current_order['Name']}! Your {current_order['Coffee']} is being prepared.")

# Daily Consumption Report
st.subheader("📊 Daily Consumption Report")
if len(st.session_state.daily_report) > 0:
    df = pd.DataFrame(st.session_state.daily_report)
    st.dataframe(df)
else:
    st.write("No orders placed today.")

# Health Tips & Motivational Quotes
st.subheader("💡 Tip / Quote of the Day")
st.info(random.choice(health_tips + motivational_quotes))
