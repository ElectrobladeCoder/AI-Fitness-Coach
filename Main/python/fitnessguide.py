import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import time
from collections import deque
import flask as fl


user_weight_kg = float(input("Enter your weight (kg): "))
target_reps_per_set = int(input("Enter desired reps per set: "))
current_exercise = "squat"  # Default mode


MET_VALUES = {"squat": 5.0, "pushup": 7.0, "shoulder": 4.5, "boxing": 8.0}


def estimate_calories(ex, weight, dur):
    met = MET_VALUES.get(ex, 4.0)
    return (met * weight * dur) / 3600

def speak(text):
    engine.say(text)
    engine.runAndWait()

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    diff = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    ang = abs(diff * 180.0/np.pi)
    return ang if ang <= 180 else 360 - ang


def calculate_speed(point1, point2, dt):
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    return np.sqrt(dx**2 + dy**2) / dt if dt > 0 else 0


message_queue = deque()
def queue_message(text, duration=3.0):
    expiry = time.time() + duration
    message_queue.append((text, expiry))


class ExerciseTracker:
    def __init__(self, name, min_ang, max_ang):
        self.name = name
        self.min_ang = min_ang
        self.max_ang = max_ang
        self.stage = None
        self.reps = 0
        self.sets = 0
        self.rep_times = deque(maxlen=10)
        self.last_transition = time.time()

    def detect_rep(self, ang):
        # Down: ang < min_ang
        if ang < self.min_ang and self.stage != 'down':
            self.stage = 'down'
            queue_message(f"{self.name} down phase detected")
        # Up: ang > max_ang after down
        if ang > self.max_ang and self.stage == 'down':
            now = time.time()
            dur = now - self.last_transition
            self.last_transition = now
            self.reps += 1
            self.rep_times.append(dur)
            self.stage = 'up'
            queue_message(f"{self.name} Rep {self.reps}")
            speak(f"{self.name} rep {self.reps}")
            # set completion
            if self.reps % target_reps_per_set == 0:
                self.sets += 1
                queue_message(f"Set {self.sets} complete!")
                speak(f"Set {self.sets} complete, good job!")
            return dur
        return None

    def detect_fatigue(self):
        if len(self.rep_times) < 5: return False
        avg = sum(list(self.rep_times)[:-1])/(len(self.rep_times)-1)
        return self.rep_times[-1] > avg*1.3
    
#Stick figures testing... prob not gonna work, but let us pray :D

def draw_stick_figure(canvas, landmarks, scale=0.5, offset=(400, 100), color=(255,255,255)):
    keypoints = {
        'left_shoulder': 11, 'right_shoulder': 12,
        'left_elbow': 13, 'right_elbow': 14,
        'left_wrist': 15, 'right_wrist': 16,
        'left_hip': 23, 'right_hip': 24,
        'left_knee': 25, 'right_knee': 26,
        'left_ankle': 27, 'right_ankle': 28
    }

    def get_point(name):
        lm = landmarks[keypoints[name]]
        return (int(offset[0] + lm.x * scale * w), int(offset[1] + lm.y * scale * h))

    limbs = [
        ('left_shoulder', 'right_shoulder'),
        ('left_shoulder', 'left_elbow'),
        ('left_elbow', 'left_wrist'),
        ('right_shoulder', 'right_elbow'),
        ('right_elbow', 'right_wrist'),
        ('left_shoulder', 'left_hip'),
        ('right_shoulder', 'right_hip'),
        ('left_hip', 'right_hip'),
        ('left_hip', 'left_knee'),
        ('left_knee', 'left_ankle'),
        ('right_hip', 'right_knee'),
        ('right_knee', 'right_ankle'),
    ]

    for a, b in limbs:
        pt1 = get_point(a)
        pt2 = get_point(b)
        cv2.line(canvas, pt1, pt2, color, 2)

    head_center = ((get_point('left_shoulder')[0] + get_point('right_shoulder')[0]) // 2,
                   get_point('left_shoulder')[1] - 30)
    cv2.circle(canvas, head_center, 15, color, 2)

    if fatigue:
        np.random.seed(0)  # Keep sweat positions consistent per frame
        for i in range(3):
            dx = np.random.randint(-10, 10)
            dy = np.random.randint(10, 20)
            drop_center = (head_center[0] + dx, head_center[1] + dy)
            cv2.ellipse(canvas, drop_center, (3, 6), 0, 0, 360, (255, 100, 100), -1)

engine = pyttsx3.init()
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
trackers = {
    'squat':    ExerciseTracker('Squat',    min_ang=70, max_ang=160),
    'pushup':   ExerciseTracker('Push-up',  min_ang=65, max_ang=160),
    'shoulder': ExerciseTracker('Shoulder', min_ang=45, max_ang=160),
    'boxing':   ExerciseTracker('Boxing',   min_ang=30, max_ang=150)
}

total_calories = 0.0
angle_hist = deque(maxlen=5)
duration_buffer = deque(maxlen=100)
motion_buffer = deque(maxlen=2)
squat_depth_y = None
session_start = time.time()


cv2.namedWindow('AI Fitness Coach')
def set_mode_trackbars(mode):
    cv2.setTrackbarPos('MinAngle','AI Fitness Coach',trackers[mode].min_ang)
    cv2.setTrackbarPos('MaxAngle','AI Fitness Coach',trackers[mode].max_ang)

def on_trackbar(val):
    pass

cv2.createTrackbar('MinAngle','AI Fitness Coach',0,180,on_trackbar)
cv2.createTrackbar('MaxAngle','AI Fitness Coach',0,180,on_trackbar)
set_mode_trackbars(current_exercise)

print("=== AI Fitness Coach ===")
speak("Press 1 squat, 2 pushup, 3 shoulder, 4 boxing. C to calibrate squat bottom. Adjust sliders for thresholds.")


# The whole main loop... pls dont mess with this unless you know what you're doing
print("[+] Welcome to your personal AI Fitness Coach! From ElectrobladeCoder on GitHub.")
cap = cv2.VideoCapture(0)
with mp_pose.Pose(min_detection_confidence=0.4, min_tracking_confidence=0.4) as pose:
    while True:
        ret, frame = cap.read()
        if not ret: break
        h, w = frame.shape[:2]
        key = cv2.waitKey(10) & 0xFF
        if key == ord('q'): break
        elif key == ord('1'):
            current_exercise = 'squat'; queue_message('Mode: Squat'); set_mode_trackbars(current_exercise)
        elif key == ord('2'):
            current_exercise = 'pushup'; queue_message('Mode: Push-up'); set_mode_trackbars(current_exercise)
        elif key == ord('3'):
            current_exercise = 'shoulder'; queue_message('Mode: Shoulder'); set_mode_trackbars(current_exercise)
        elif key == ord('4'):
            current_exercise = 'boxing'; queue_message('Mode: Boxing'); set_mode_trackbars(current_exercise)
        elif key == ord('c') and current_exercise=='squat':
            squat_depth_y = None; queue_message('Calibrate bottom: press C at squat bottom')
        elif key == ord('c') and squat_depth_y is None and 'coords' in locals():
            squat_depth_y = coords['hip'][1]; queue_message('Squat depth set')

        # update thresholds from sliders
        trackers[current_exercise].min_ang = cv2.getTrackbarPos('MinAngle','AI Fitness Coach')
        trackers[current_exercise].max_ang = cv2.getTrackbarPos('MaxAngle','AI Fitness Coach')

        # pose detection
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img.flags.writeable = False
        results = pose.process(img)
        img.flags.writeable = True
        image = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        feedback = ''
        try:
            lm = results.pose_landmarks.landmark
            coords = {n:(int(lm[i].x*w), int(lm[i].y*h)) for n,i in
                [('shoulder',11),('elbow',13),('wrist',15),('hip',23),('knee',25),('ankle',27)]}
            tracker = trackers[current_exercise]

            # angle calc per exercise
            if current_exercise=='squat':
                ang = calculate_angle(coords['hip'],coords['knee'],coords['ankle'])
            elif current_exercise=='pushup':
                ang = calculate_angle(coords['shoulder'],coords['elbow'],coords['wrist'])
            else:
                ang = calculate_angle(coords['elbow'],coords['shoulder'],coords['hip'])
            angle_hist.append(ang)
            smooth_ang = sum(angle_hist)/len(angle_hist)

            # rep detection
            dur = tracker.detect_rep(smooth_ang)
            if dur:
                total_calories += estimate_calories(current_exercise, user_weight_kg, dur)
                duration_buffer.append(int(dur*100))
            if tracker.detect_fatigue(): feedback = 'Fatigue: rest 30s'

            # guidance per phase
            if current_exercise=='squat':
                torso = calculate_angle(coords['shoulder'],coords['hip'],coords['knee'])
                if tracker.stage=='down':
                    if smooth_ang > tracker.min_ang:
                        feedback = 'Go lower: aim for parallel or below.'
                    elif torso < 155:
                        feedback = 'Keep chest up: maintain neutral spine.'
                elif tracker.stage=='up':
                    if smooth_ang < tracker.max_ang:
                        feedback = 'Stand fully: extend hips and knees.'
                if squat_depth_y:
                    color=(0,255,0) if coords['hip'][1]>=squat_depth_y else (0,0,255)
                    cv2.line(image,(0,squat_depth_y),(w,squat_depth_y),color,2)
            elif current_exercise=='pushup':
                back = calculate_angle(coords['shoulder'],coords['hip'],coords['ankle'])
                if tracker.stage=='down':
                    if smooth_ang > tracker.min_ang:
                        feedback = 'Lower more: chest toward floor.'
                    elif back < 165:
                        feedback = 'Keep body straight: avoid sag.'
                elif tracker.stage=='up':
                    if smooth_ang < tracker.max_ang:
                        feedback = 'Press up: full arm extension.'
            
            if current_exercise == 'boxing':
                wrist = coords['wrist']
                now = time.time()
                motion_buffer.append((wrist, now))

                if len(motion_buffer) == 2:
                    (p1, t1), (p2, t2) = motion_buffer
                    punch_speed = calculate_speed(p1, p2, t2 - t1)
                    punch_eff = "High" if punch_speed > 1200 else "Moderate" if punch_speed > 800 else "Low"
                    cv2.putText(image, f"Punch Speed: {int(punch_speed)} px/s", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 150, 0), 2)
                    cv2.putText(image, f"Efficiency: {punch_eff}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 200), 2)

                    if punch_eff == "Low":
                        feedback = "Punch faster! Explosive power matters."
                    elif punch_eff == "High":
                        feedback = "Great punch! Keep up the speed."
            else:
                if tracker.stage=='down' and smooth_ang > tracker.min_ang:
                    feedback = 'Lower until elbows ~90°.'
                elif tracker.stage=='up' and smooth_ang < tracker.max_ang:
                    feedback = 'Press fully overhead.'
            if results.pose_landmarks:
                fatigue = tracker.detect_fatigue()
                draw_stick_figure(image, results.pose_landmarks.landmark)
            # draw core stats
            cv2.putText(image, f"Mode: {current_exercise.title()}", (10,30), cv2.FONT_HERSHEY_SIMPLEX,0.8,(200,200,0),2)
            cv2.putText(image, f"Sets: {tracker.sets}  Reps: {tracker.reps}", (10,60), cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
            cv2.putText(image, f"Cals: {total_calories:.2f} kcal", (10,90), cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)

            # display feedback and messages
            if feedback:
                cv2.putText(image, feedback, (10,140), cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,0,255),2)
            now=time.time()
            while message_queue and message_queue[0][1]<now:
                message_queue.popleft()
            for i,(msg,_) in enumerate(message_queue):
                cv2.putText(image,msg,(10,180+30*i),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,255),2)
  
        except Exception as e:
            print("Error:",e)

        mp_drawing.draw_landmarks(image,results.pose_landmarks,mp_pose.POSE_CONNECTIONS)
        cv2.imshow('AI Fitness Coach',image)

cap.release()
cv2.destroyAllWindows()

