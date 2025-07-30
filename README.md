# 🤖 AI Fitness Coach
**By ElectrobladeCoder**  
An intelligent real-time fitness assistant using OpenCV, MediaPipe, and pose estimation to track, count, and evaluate your form for workouts like squats, push-ups, shoulder presses, and boxing.

> 🧠 Built in Python  
> 🏋️ Real-time feedback, calorie estimation, fatigue detection, and stick figure overlay  
> 🔊 Voice feedback included  

---

## 🧩 Features

- ✅ **Multi-Exercise Support** – Squats, Push-Ups, Shoulder Presses, and Boxing
- 🧠 **Form Detection** – Joint-angle calculations with MediaPipe
- 🔁 **Rep & Set Counting** – Automatically tracks workout progress
- 📉 **Fatigue Detection** – Detects performance drop via rep speed
- 🔥 **Calorie Estimation** – Based on MET and body weight
- 🗣️ **Voice Feedback** – Speaks rep counts and set completion
- 🕴️ **Stick Figure Overlay** – Skeleton visual with sweat animations on fatigue
- ⚙️ **Real-Time Controls** – Sliders to adjust detection thresholds
- 💪 **Boxing Mode** – Punch speed estimation and efficiency detection
- 🌐 *(Optional)* HTML version (lightweight, less powerful)

---

## 📸   How It Works

1. Launches webcam and tracks user using **MediaPipe Pose**.
2. Calculates joint angles between keypoints.
3. Detects motion phase (e.g., squat "down" vs. "up").
4. Automatically logs reps and time per rep.
5. Provides **on-screen and spoken** feedback.
6. Displays stats, fatigue warnings, and visual overlays.

---

## 🖥️ Requirements

Install Python dependencies using the Command Line Interface of your operating system. (Terminal for MacOS, Command Prompt for Windows, and Termial/Terminator for Linux) :

<pre lang="markdown"> pip install opencv-python mediapipe numpy pyttsx3 flask </pre>


