import cv2
import mediapipe as mp


class HandTracker:

    def __init__(self):

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7
        )

        self.mpDraw = mp.solutions.drawing_utils

        self.tipIds = [4, 8, 12, 16, 20]

    def find_hands(self, img):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = self.hands.process(imgRGB)

        landmarks = []

        if results.multi_hand_landmarks:

            for handLms in results.multi_hand_landmarks:

                for id, lm in enumerate(handLms.landmark):

                    h, w, c = img.shape

                    cx, cy = int(lm.x * w), int(lm.y * h)

                    landmarks.append((id, cx, cy))

                self.mpDraw.draw_landmarks(
                    img,
                    handLms,
                    self.mpHands.HAND_CONNECTIONS
                )

        return img, landmarks

    # ---------- finger detection ----------

    def fingers_up(self, landmarks):

        fingers = []

        if len(landmarks) == 0:
            return fingers

        # thumb

        if landmarks[self.tipIds[0]][1] > landmarks[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # other 4 fingers

        for i in range(1, 5):

            if landmarks[self.tipIds[i]][2] < landmarks[self.tipIds[i] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def find_distance(self, p1, p2, landmarks):

        if len(landmarks) == 0:
            return 0

        x1, y1 = landmarks[p1][1], landmarks[p1][2]
        x2, y2 = landmarks[p2][1], landmarks[p2][2]

        dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

        return dist