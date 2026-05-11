import streamlit as st
import cv2
import numpy as np
import time
import random
import os
from gtts import gTTS
from pygame import mixer
import json

USER_FILE = "users.json"
st.markdown("""
<style>
.center-card {
    background: #111111;
    padding: 25px;
    border-radius: 20px;
    border: 2px solid #93C572;
    width: 350px;
    margin: auto;
    margin-top: 8%;
    box-shadow: 0px 0px 20px rgba(182,255,108,0.2);
}
</style>
""", unsafe_allow_html=True)
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}
def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)
        
# ---------------- LOGIN SYSTEM STATE ----------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

if "users" not in st.session_state:
    st.session_state.users = load_users()
    
if "current_user" not in st.session_state:
    st.session_state.current_user = None
    
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# --- 🎨 THEME CONFIGURATION ---
st.set_page_config(page_title="A-FIT | AI Gym Trainer", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #000000; color: #FFFFFF; }

section[data-testid="stSidebar"] {
    background-color: #0A0A0A !important;
    border-right: 2px solid #93C572 !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #B6FF6C !important;
    font-weight: 800 !important;
    text-shadow: 0px 0px 12px rgba(182, 255, 108, 0.5);
    letter-spacing: 1px;
}

p, label, span {
    color: #FFFFFF !important;
}

input, textarea {
    color: #000000 !important;
    background-color: #FFFFFF !important;
    font-weight: bold;
}

div[data-testid="stNumberInput"] input {
    color: #000000 !important;
    background-color: #FFFFFF !important;
}

[data-testid="stChatInputContainer"] {
    background-color: #1A1A1A !important;
    border: 1px solid #93C572 !important;
}

div.stButton > button {
    background: linear-gradient(135deg, #B6FF6C, #93C572) !important;
    color: #000000 !important;
    border-radius: 25px;
    font-weight: bold;
    border: none;
    transition: all 0.3s ease;
    box-shadow: 0px 0px 15px rgba(182, 255, 108, 0.6);
    height: 3em;
}

div.stButton > button:hover {
    transform: scale(1.05);
    background: linear-gradient(135deg, #C8FF8C, #A8E063) !important;
    box-shadow: 0px 0px 25px rgba(182, 255, 108, 1);
    color: #000000 !important;
}

div.stButton > button:active {
    transform: scale(0.96);
    box-shadow: 0px 0px 10px rgba(182, 255, 108, 0.8);
}

div.stButton > button p {
    color: #000000 !important;
}

[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
}

[data-testid="stMetricLabel"] {
    color: #C8FF8C !important;
    font-weight: bold !important;
    text-shadow: 0px 0px 8px rgba(182, 255, 108, 0.7);
    font-size: 18px !important;
}
[data-testid="stChatMessage"] {
    background-color: #111111 !important;
    color: white !important;
    border-radius: 10px;
    padding: 10px;
}
.main .block-container {
    background-color: #000000 !important;
    padding-top: 1rem;
}

[data-testid="stAppViewContainer"] {
    background-color: #000000 !important;
}

[data-testid="stHeader"] {
    background-color: #000000 !important;
}

section.main {
    background-color: #000000 !important;
}
/* --- FORCE CHATBOT DARK --- */
div[data-testid="stChatMessage"] {
    background-color: #111111 !important;
    border: 2px solid #93C572 !important;
    border-radius: 15px !important;
    padding: 12px !important;
    margin-bottom: 10px !important;
}

div[data-testid="stChatMessageContent"] {
    background-color: #111111 !important;
    color: white !important;
}

div[data-testid="stChatMessageContent"] p {
    color: white !important;
}

[data-testid="stChatInputContainer"] {
    background-color: #111111 !important;
    border: 2px solid #93C572 !important;
    border-radius: 15px !important;
}
/* --- REMOVE WHITE BOTTOM AREA --- */
html, body, [class*="css"] {
    background-color: #000000 !important;
}

.main {
    background-color: #000000 !important;
}

.block-container {
    background-color: #000000 !important;
    padding-bottom: 3rem !important;
}

footer {
    background-color: #000000 !important;
}

header {
    background-color: #000000 !important;
}
/* --- FULL BLACK APP --- */
.stApp {
    background-color: #000000 !important;
}

[data-testid="stAppViewContainer"] {
    background-color: #000000 !important;
}

[data-testid="stBottomBlockContainer"] {
    background-color: #000000 !important;
}

[data-testid="stFooter"] {
    background-color: #000000 !important;
}

footer {
    visibility: hidden;
}
/* --- AI CHATBOT STYLE --- */
[data-testid="stChatMessage"] {
    background: linear-gradient(145deg, #111111, #1A1A1A) !important;
    border: 1px solid #B6FF6C !important;
    border-radius: 18px !important;
    padding: 14px !important;
    margin-bottom: 12px !important;
    box-shadow: 0px 0px 12px rgba(182, 255, 108, 0.25);
}

[data-testid="stChatMessageContent"] {
    color: white !important;
    font-size: 16px !important;
    font-weight: 500 !important;
}

/* --- USER MESSAGE --- */
[data-testid="stChatMessage"]:has(.stChatMessageContent) {
    animation: fadeIn 0.3s ease-in-out;
}

/* --- CHAT INPUT --- */
[data-testid="stChatInputContainer"] {
    background: #111111 !important;
    border: 2px solid #B6FF6C !important;
    border-radius: 20px !important;
    box-shadow: 0px 0px 15px rgba(182, 255, 108, 0.35);
}

/* --- CHAT TITLE --- */
.chat-title {
    color: #B6FF6C;
    font-size: 24px;
    font-weight: bold;
    text-shadow: 0px 0px 10px rgba(182,255,108,0.7);
}

/* --- ANIMATION --- */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(8px);
    }
    to {
        opacity: 1;
        transform: translateY(0px);
    }
}
</style>
""", unsafe_allow_html=True)

def login():

    st.markdown("## 🏋️ A-FIT LOGIN")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        email = st.text_input("📧 Email")
        password = st.text_input("🔐 Password", type="password")

        # LOGIN BUTTON
        if st.button("LOGIN", key="login_btn"):

            # Get user from saved users
            user = st.session_state.users.get(email)

            # Check credentials
            if user and user["password"] == password:
                st.session_state.logged_in = True
                st.session_state.current_user = user
                st.session_state.page = "home"

                # Admin Check
                if email == "admin@afit.com":
                    st.session_state.is_admin = True
                else:
                    st.session_state.is_admin = False

                st.rerun()

            else:
                st.error("Invalid credentials ❌")

        st.markdown("---")

        # CREATE ACCOUNT BUTTON
        if st.button("Create Account", key="create_account_btn"):
            st.session_state.page = "register"
            st.rerun()
            
def register():

    st.markdown("## 📝 CREATE ACCOUNT")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        name = st.text_input("👤 Full Name")
        mobile = st.text_input("📱 Mobile Number")
        email = st.text_input("📧 Email")
        password = st.text_input("🔐 Password", type="password")
        confirm = st.text_input("🔁 Confirm Password", type="password")

        if st.button("REGISTER", key="register_btn"):

            if not name or not mobile or not email:
                st.error("Please fill all fields ❌")

            elif password != confirm:
                st.error("Passwords do not match ❌")

            elif email in st.session_state.users:
                st.error("User already exists ❌")

            else:
                st.session_state.users[email] = {
                    "name": name,
                    "mobile": mobile,
                    "password": password
                }
                save_users(st.session_state.users)

                st.success("Account created successfully ✅")
                st.session_state.page = "login"
                st.rerun()

        st.markdown("---")

        if st.button("Back to Login", key="back_to_login_btn"):
            st.session_state.page = "login"
            st.rerun()
        # ---------------- PAGE ROUTING ----------------
if st.session_state.page == "login":
    login()
    st.stop()

elif st.session_state.page == "register":
    register()
    st.stop()
elif st.session_state.page != "home":
    st.session_state.page = "login"
    login()
    st.stop()
    if not st.session_state.logged_in:
        st.warning("🔒 Please login to access AI Gym Trainer")
    st.stop()
    
# --- MEDIAPIPE ---
import mediapipe as mp
from mediapipe.python.solutions import pose as mp_pose
from mediapipe.python.solutions import drawing_utils as mp_drawing

# --- VOICE ENGINE ---
from gtts import gTTS
from pygame import mixer
import os
import time

mixer.init()

def speak(text):
    try:

        tts = gTTS(text=text, lang='en')

        filename = "voice.mp3"

        tts.save(filename)

        mixer.music.load(filename)
        mixer.music.play()

        while mixer.music.get_busy():
            time.sleep(0.1)

        mixer.music.unload()

        os.remove(filename)

    except Exception as e:
        print(e)
# --- SESSION STATE ---
if 'counter' not in st.session_state:
    st.session_state.counter = 0

if 'workout_idx' not in st.session_state:
    st.session_state.workout_idx = 0

if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

if 'stage' not in st.session_state:
    st.session_state.stage = "DOWN"

if 'camera_on' not in st.session_state:
    st.session_state.camera_on = False

if 'exercise_start' not in st.session_state:
    st.session_state.exercise_start = time.time()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "workout_complete" not in st.session_state:
    st.session_state.workout_complete = False

if "last_count_time" not in st.session_state:
    st.session_state.last_count_time = 0

if "exercise_name" not in st.session_state:
    st.session_state.exercise_name = ""

# --- MOTIVATION ---
MOTIVATION_LINES = [
    "Great job! Keep pushing.",
    "You are doing amazing.",
    "Consistency builds strength.",
    "Keep going, you are stronger than yesterday.",
    "Excellent form. Stay focused.",
    "Push harder. You can do it."
]

# --- WORKOUT DATABASE ---
WORKOUT_DATABASE = [
    {"name": "Bicep Curls", "target": 10, "time": 300, "met": 3.0},
    {"name": "Squats", "target": 12, "time": 300, "met": 5.0},
    {"name": "Jumping Jacks", "target": 15, "time": 300, "met": 4.0}
]

# --- SIDEBAR ---
with st.sidebar:

    user = st.session_state.get("current_user", {})

    user_name = user.get("name", "User")
    user_mobile = user.get("mobile", "")

    st.markdown(f"""
    <div style="
        background:#111;
        padding:10px;
        border-radius:10px;
        border:1px solid #93C572;
        text-align:left;
        font-size:14px;
        color:#B6FF6C;
        margin-bottom:10px;">
        👤 {user_name}<br>
        📱 {user_mobile}
    </div>
    """, unsafe_allow_html=True)
if st.sidebar.button("🔓 Logout"):
    st.session_state.logged_in = False
    st.session_state.page = "login"
    st.rerun()
    # 👑 ADMIN PANEL
if st.session_state.get("is_admin", False):
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 👑 Admin Panel")

    total_users = len(st.session_state.users)
    st.sidebar.success(f"👥 Registered Users: {total_users}")

    if st.sidebar.checkbox("Show User Emails"):
        for email in st.session_state.users.keys():
            st.sidebar.write(f"📧 {email}")
with st.sidebar:

    st.markdown("## 🧑 User Profile")

age = st.number_input("Age", 10, 100, 22, key="age_id_unique")
height = st.number_input("Height (cm)", 100, 250, 170, key="height_id_unique")
weight = st.number_input("Weight (kg)", 30, 200, 65, key="weight_id_unique")

st.markdown("---")

st.markdown("## 🥗 Diet Preference")

diet_pref = st.radio(
        "Choose your diet type:",
        ["🥦Veg", "🍗Non-Veg", "🍱Both"]
    )

    st.markdown("---")

    st.markdown("## 🎯 Goal")

    goal = st.radio(
        "Select Goal",
        ["Weight Loss", "Muscle Gain"]
    )

    st.markdown("---")

    st.markdown("## 📊 Results")

    if st.button("🔥 Check Calories Burnt"):

        if st.session_state.workout_complete:

            duration_hr = (
                time.time() - st.session_state.start_time
            ) / 3600

            avg_met = sum(
                w['met'] for w in WORKOUT_DATABASE
            ) / len(WORKOUT_DATABASE)

            calories = avg_met * weight * duration_hr

            st.success(f"🔥 Calories Burnt: {calories:.2f} kcal")

        else:
            st.warning("Complete workout to unlock calories!")

    if st.button("Reset Workout"):

        st.session_state.counter = 0
        st.session_state.workout_idx = 0
        st.session_state.start_time = time.time()
        st.session_state.stage = "DOWN"
        st.session_state.camera_on = False
        st.session_state.exercise_start = time.time()
        st.session_state.messages = []
        st.session_state.workout_complete = False
        st.session_state.exercise_name = ""

        st.rerun()

# --- MAIN ---
if not st.session_state.logged_in:
    if st.session_state.page == "register":
        register()
    else:
        login()
    st.stop()
st.title("🏋️ A-FIT")

if st.session_state.workout_idx >= len(WORKOUT_DATABASE):
    st.session_state.workout_idx = len(WORKOUT_DATABASE) - 1

current = WORKOUT_DATABASE[st.session_state.workout_idx]

# --- EXERCISE CHANGE ---
if st.session_state.exercise_name != current["name"]:

    st.session_state.exercise_name = current["name"]
    st.session_state.counter = 0
    st.session_state.stage = "DOWN"
    st.session_state.last_count_time = 0
    st.session_state.exercise_start = time.time()

elapsed = time.time() - st.session_state.exercise_start
remaining = int(current["time"] - elapsed)

c1, c2, c3, c4 = st.columns(4)

exercise_box = c1.empty()
reps_box = c2.empty()
time_box = c3.empty()
goal_box = c4.empty()

exercise_box.metric("Exercise", st.session_state.exercise_name)

reps_box.metric(
    "Reps",
    f"{st.session_state.counter}/{current['target']}"
)

time_box.metric("Time Left", f"{remaining}s")

goal_box.metric("Goal", goal)

col1, col2 = st.columns(2)

# --- LEFT SIDE ---
with col1:

    st.subheader("Status")

    status_placeholder = st.empty()

    status_placeholder.success(
        f"Stage: {st.session_state.stage}"
    )

    st.markdown('<p class="chat-title">🤖 A-FIT AI Coach</p>', unsafe_allow_html=True)

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Ask me for diet..."):

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    if "diet" in prompt.lower():

        # --- WEIGHT LOSS ---
        if goal == "Weight Loss":

            if diet_pref == "🥦Veg":
                response = "🥦 Veg weight loss diet: Oats, dal, paneer, salads and fruits."
                speak(response)

            elif diet_pref == "🍗Non-Veg":
                response = "🍗 Non veg weight loss diet: Boiled eggs, grilled chicken and vegetables."
                speak(response)

            else:
                response = "🍱 Balanced weight loss diet: Eggs, fruits, vegetables, rice and protein foods."
                speak(response)
        # --- MUSCLE GAIN ---
        else:

            if diet_pref == "🥦Veg":
                response = "🥦 Veg muscle gain diet: Paneer, milk, bananas and dry fruits."
                speak(response)

            elif diet_pref == "🍗Non-Veg":
                response = "🍗 Non veg muscle gain diet: Chicken, eggs, fish and protein rich foods."
                speak(response)

            else:
                response = "🍱 Balanced muscle gain diet: Protein foods, eggs, paneer, chicken and healthy carbs."
                speak(response)

    else:

        response = random.choice(MOTIVATION_LINES)

        speak(response)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
# --- CAMERA ---
with col2:

    frame_placeholder = st.empty()

    colA, colB = st.columns(2)

    if colA.button("Start Camera"):
        st.session_state.camera_on = True

    if colB.button("Stop Camera"):
        st.session_state.camera_on = False

    if st.session_state.camera_on:

        cap = cv2.VideoCapture(0)

        pose = mp_pose.Pose(model_complexity=0)

        while st.session_state.camera_on:

            ret, frame = cap.read()

            if not ret:
                break

            frame = cv2.flip(frame, 1)

            frame = cv2.resize(frame, (480, 360))

            image_rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            results = pose.process(image_rgb)

            if results.pose_landmarks:

                lm = results.pose_landmarks.landmark

                # --- SQUATS ---
                if current["name"] == "Squats":

                    hip = [lm[23].x, lm[23].y]
                    knee = [lm[25].x, lm[25].y]
                    ankle = [lm[27].x, lm[27].y]

                    angle = np.abs(
                        np.arctan2(
                            ankle[1]-knee[1],
                            ankle[0]-knee[0]
                        ) -
                        np.arctan2(
                            hip[1]-knee[1],
                            hip[0]-knee[0]
                        )
                    ) * 180 / np.pi

                    if angle > 160:
                        st.session_state.stage = "STAND"

                    elif angle < 90:

                        if st.session_state.stage == "STAND":

                            if (
                                time.time() -
                                st.session_state.last_count_time
                            ) > 0.8:

                                st.session_state.counter += 1

                                speak("Good squat")

                                st.session_state.last_count_time = time.time()

                                if st.session_state.counter % 3 == 0:
                                    speak(random.choice(MOTIVATION_LINES))

                            st.session_state.stage = "SIT"

                # --- OTHER EXERCISES ---
                else:

                    shoulder = [lm[11].x, lm[11].y]
                    elbow = [lm[13].x, lm[13].y]
                    wrist = [lm[15].x, lm[15].y]

                    angle = np.abs(
                        np.arctan2(
                            wrist[1]-elbow[1],
                            wrist[0]-elbow[0]
                        ) -
                        np.arctan2(
                            shoulder[1]-elbow[1],
                            shoulder[0]-elbow[0]
                        )
                    ) * 180 / np.pi

                    if angle > 150:
                        st.session_state.stage = "DOWN"

                    elif angle < 50:

                        if st.session_state.stage == "DOWN":

                            if (
                                time.time() -
                                st.session_state.last_count_time
                            ) > 0.8:

                                st.session_state.counter += 1

                                speak("Perfect rep")

                                st.session_state.last_count_time = time.time()

                                if st.session_state.counter % 3 == 0:
                                    speak(random.choice(MOTIVATION_LINES))

                            st.session_state.stage = "UP"

                # --- STATUS UPDATE ---
                status_placeholder.success(
                    f"Stage: {st.session_state.stage}"
                )

                # --- DRAW LANDMARKS ---
                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS
                )

            # --- SHOW CAMERA ---
            frame_placeholder.image(frame, channels="BGR")

            # --- LIVE UPDATE ---
            exercise_box.metric(
                "Exercise",
                current["name"]
            )

            reps_box.metric(
                "Reps",
                f"{st.session_state.counter}/{current['target']}"
            )

            time_box.metric(
                "Time Left",
                f"{int(current['time'] - (time.time() - st.session_state.exercise_start))}s"
            )

            # --- AUTO SWITCH ---
            if (
                remaining <= 0 or
                st.session_state.counter >= current["target"]
            ):

                st.session_state.workout_idx += 1

                st.session_state.counter = 0

                st.session_state.stage = "DOWN"

                st.session_state.exercise_start = time.time()

                if st.session_state.workout_idx >= len(WORKOUT_DATABASE):

                    st.session_state.camera_on = False

                    st.session_state.workout_complete = True

                    speak("Workout completed successfully")

                    break

                current = WORKOUT_DATABASE[
                    st.session_state.workout_idx
                ]

                st.session_state.exercise_name = current["name"]

                continue

            time.sleep(0.05)

        cap.release()

# --- COMPLETE ---
if st.session_state.workout_complete:

    st.balloons()

    st.markdown("""
    <div style="
        background-color:#93C572;
        padding:20px;
        border-radius:15px;
        text-align:center;
        color:black;
        font-size:20px;
        font-weight:bold;">
        🎉 Your Exercise is Completed for Today!
    </div>
    """, unsafe_allow_html=True)
