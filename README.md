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

## 📸 How It Works

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

## 🚀 How to run?

If using Python, simply download the file of your choice from the 'Main' folder, or the following direct links:
[Python File](Main/python/fitnessguide.py)
[HTML File](Main/html/fitnessguide.html)
and navigate to the file directory on your computer. After that, it is as simple as typing:

<pre lang="markdown">python3 fitnessguide.py</pre>

When the OpenCV window opens, you can use the key-binds as follows:

| Key | Action                  |
| --- | ----------------------- |
| `1` | Switch to Squat Mode    |
| `2` | Switch to Push-Up Mode  |
| `3` | Switch to Shoulder Mode |
| `4` | Switch to Boxing Mode   |
| `C` | Calibrate squat depth   |
| `Q` | Quit the application    |

---

# ⭐ Key Features

## 🧮 Calorie Estimation

## 🧑‍🎨 Stick Figure Visualisation

## 🥊 Boxing Mode (NEW ADDITION!!)

# Language Support

Currently, the app only supports two programming languages:

## 🌐 HTML and 🐍 Python

While Python is the more powerful version, it requires a bit more setup. The HTML version is designed to be lightweight and easy to download and use immediately, without requiring further setup. (Sorry to the Apple device users out there, but you may encounter some issues using the program on Safari. Any other browser should work well.)

# 🧠 Future Plans

[o] Real-time XP & level-up system
[o] Flask backend API for mobile logging
[o] Voice command control
[o] Export workout history to CSV or Google Sheets
[o] Machine learning-based form rating system

---

# 🔐 Privacy

Your webcam feed is never recorded or uploaded. All processing is done locally on your machine.

---

# Credits

Created by [ElectrobladeCoder](https://github.com/ElectrobladeCoder)
[MediaPipe Pose by Google](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker)
[OpenCV](https://opencv.org/) for image handling
[pyttsx3](https://pypi.org/project/pyttsx3/) for voice synthesis
