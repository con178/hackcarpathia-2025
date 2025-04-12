from datetime import datetime
import cv2
import numpy as np
import time
import logs

# Configuration
LOG_INTERVAL = 5  # Log people count every 5 seconds
CAMERA_NAME = 'Przychodnia kwiatuszek'
camera_latitude = 50.031200
camera_longitude = 22.018000

# Load MobileNet SSD model
net = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'mobilenet_iter_73000.caffemodel')

# Class labels for the MobileNet SSD model
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
           "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]


# Main function
def main():
    # Open camera stream
    cap = cv2.VideoCapture(0)  # Change to 0 if you want to use camera
    # cap = cv2.VideoCapture('rtsp://admin:Catmedia1!@10.0.0.101/')

    if not cap.isOpened():
        logs.log_message("Cannot open camera or video file")
        return

    # Initialize timers and counters
    last_log_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        current_time = time.time()

        # Count people in current frame
        people_count = 0

        # Process entire frame for object detection
        blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()

        height, width = frame.shape[:2]

        # Detect people in the frame
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.4:  # Only consider confident detections
                idx = int(detections[0, 0, i, 1])
                label = CLASSES[idx]

                # Only detect people
                if label == "person":
                    people_count += 1
                    box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
                    (vx, vy, vw, vh) = box.astype("int")
                    cv2.rectangle(frame, (vx, vy), (vx + vw, vy + vh), (0, 255, 0), 2)
                    cv2.putText(frame, "Person", (vx, vy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display people count on frame
        cv2.putText(frame, f"People Count: {people_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Log the number of people every minute
        if current_time - last_log_time >= LOG_INTERVAL:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logs.log_message(f"{camera_latitude},{camera_longitude},{CAMERA_NAME}, {people_count}, {timestamp}")
            last_log_time = current_time

        # Display video with labeled people
        cv2.imshow('People Detection', frame)

        # Exit loop by pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release camera and close windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()