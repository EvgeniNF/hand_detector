import cv2
import mediapipe as mp

"""
Hand detection
"""


class HandsTracking:
    """
    This class find hands
    on picture
    """

    def __init__(self,
                 static_image_mode=False,
                 max_num_hands=2,
                 model_complexity=1,
                 min_detection_confidence=0.3,
                 min_tracking_confidence=0.3):
        """

        :param static_image_mode:
        :param max_num_hands:
        :param model_complexity:
        :param min_detection_confidence:
        :param min_tracking_confidence:
        """
        self.hand_points = {}
        self.hands = mp.solutions.hands.Hands(static_image_mode,
                                              max_num_hands,
                                              model_complexity,
                                              min_detection_confidence,
                                              min_tracking_confidence)

    def find_hands(self,
                   img,
                   drawing=True):
        """

        :param img:
        :param drawing:
        :return:
        """
        results = self.hands.process(img)
        h, w, c = img.shape
        hands = dict()
        if results.multi_hand_landmarks:
            cu_h = 0
            for handLms in results.multi_hand_landmarks:
                cu_h += 1
                hand_name = "hand_" + str(cu_h)
                if drawing is True:
                    mp.solutions.drawing_utils.draw_landmarks(img,
                                                              handLms,
                                                              mp.solutions.hands.HAND_CONNECTIONS)
                mark_hands = list()
                for index, lm in enumerate(handLms.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    mark_hands.append([cx, cy])
                hands[hand_name] = mark_hands
        self.hand_points = hands
        return hands

    def finger_up(self):
        """
        This method returned tuple with state fingers
        :return:
        """
        zero_point = self.hand_points["hand_1"][0]
        state_fingers = []
        for i in range(5, 20, 4):
            point_1 = self.hand_points["hand_1"][i]
            point_2 = self.hand_points["hand_1"][i + 1]
            point_3 = self.hand_points["hand_1"][i + 2]
            point_4 = self.hand_points["hand_1"][i + 3]
            z_1 = (((point_1[0] - zero_point[0]) ** 2) +
                   ((point_1[1] - zero_point[1]) ** 2)) ** (1 / 2)
            z_2 = (((point_2[0] - zero_point[0]) ** 2) +
                   ((point_2[1] - zero_point[1]) ** 2)) ** (1 / 2)
            z_3 = (((point_3[0] - zero_point[0]) ** 2) +
                   ((point_3[1] - zero_point[1]) ** 2)) ** (1 / 2)
            z_4 = (((point_4[0] - zero_point[0]) ** 2) +
                   ((point_4[1] - zero_point[1]) ** 2)) ** (1 / 2)
            if z_1 < z_2 < z_3 < z_4:
                state_fingers.append(1)
            else:
                state_fingers.append(0)
        return state_fingers


def main():
    """
    Main function
    :return: None
    """
    capture = cv2.VideoCapture(0)
    tracking = HandsTracking(max_num_hands=1)

    while True:
        success, img = capture.read()
        tracking.find_hands(img)
        cv2.imshow("out", img)
        key = cv2.waitKey(1)
        if key == 27:
            break


if __name__ == '__main__':
    main()
