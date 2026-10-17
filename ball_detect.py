
import cv2
import numpy as np

# Camera setup
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Could not open webcam")

# Tennis ball HSV range (yellow-green)
lower = np.array([20, 40, 40])
upper = np.array([85, 255, 255])

kernel = np.ones((5, 5), np.uint8)

# Tracking settings
smooth_center = None
smooth_radius = None
alpha = 0.75

MIN_AREA = 300
MIN_CIRCULARITY = 0.55

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 1. Preprocess
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # 2. Color segmentation
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.morphologyEx(
        mask, cv2.MORPH_OPEN, kernel
    )
    mask = cv2.morphologyEx(
        mask, cv2.MORPH_CLOSE, kernel
    )

    # 3. Find candidate contours
    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    candidates = []

    for contour in contours:
        area = cv2.contourArea(contour)

        if area < MIN_AREA:
            continue

        perimeter = cv2.arcLength(contour, True)

        if perimeter == 0:
            continue

        circularity = (
            4 * np.pi * area / (perimeter ** 2)
        )

        if circularity < MIN_CIRCULARITY:
            continue

        (x, y), radius = cv2.minEnclosingCircle(
            contour
        )

        if radius < 10:
            continue

        candidates.append(
            (area, x, y, radius, circularity, contour)
        )

    # 4. Select the largest valid candidate
    if candidates:
        area, x, y, radius, circularity, contour = max(
            candidates, key=lambda item: item[0]
        )

        # 5. Smooth position and radius
        if smooth_center is None:
            smooth_center = (x, y)
            smooth_radius = radius
        else:
            old_x, old_y = smooth_center

            smooth_center = (
                alpha * x + (1 - alpha) * old_x,
                alpha * y + (1 - alpha) * old_y
            )

            smooth_radius = (
                alpha * radius
                + (1 - alpha) * smooth_radius
            )

        sx, sy = map(int, smooth_center)
        sr = int(smooth_radius)
        
        # Draw the actual detected contour in yellow
        cv2.drawContours(frame, [contour], -1, (0, 255, 255), 2)
        
        # 6. Draw tracking overlay
        cv2.circle(
            frame, (sx, sy), sr,
            (0, 255, 0), 2
        )

        cv2.circle(
            frame, (sx, sy), 4,
            (0, 0, 255), -1
        )

        cv2.putText(
            frame,
            f"Ball ({sx}, {sy}) C:{circularity:.2f}",
            (max(0, sx - 80), max(20, sy - sr - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (255, 255, 255), 2
        )

    else:
        # No ball detected: reset smoothing
        smooth_center = None
        smooth_radius = None

    # 7. Display
    cv2.imshow("Ball Detector", frame)
    cv2.imshow("HSV Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
