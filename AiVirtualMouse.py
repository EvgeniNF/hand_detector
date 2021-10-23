import cv2
import HandsTracking as h_trc
import autopy
import time


def main():
    capture = cv2.VideoCapture(0)
    tracking = h_trc.HandsTracking(max_num_hands=1)
    w_scr, h_scr = autopy.screen.size()
    flag_click = False
    status_moving = 0
    frame = 50
    exit_cu = 0
    start_time_exit = None
    flag_exit = False
    prev_x, prev_y = 0, 0
    step = 3

    while True:
        success, img = capture.read()
        w_cam, h_cam = img.shape[:2]
        hand_points = tracking.find_hands(img)
        cv2.rectangle(img, (frame, frame), (h_cam - frame, w_cam - frame), (255, 0, 255), 2)

        if hand_points != {}:
            fingers_status = tracking.finger_up()

            if fingers_status[0] == 1 and fingers_status[1] == 1:
                if status_moving == 0:
                    status_moving = 1
                    prev_x, prev_y = hand_points["hand_1"][9]
                elif status_moving == 1:
                    x, y = hand_points["hand_1"][9]
                    x = prev_x - x
                    y = prev_y - y

                    num_step_x = int(x / step)
                    num_step_y = int(y / step)

                    if num_step_y != 0 or num_step_x != 0:
                        prev_x, prev_y = hand_points["hand_1"][9]
                        mouse_x, mouse_y = autopy.mouse.location()
                        mouse_x += num_step_x * 4
                        mouse_y -= num_step_y * 4
                        print(num_step_x, num_step_y)
                        if mouse_x > w_scr:
                            mouse_x = w_scr - 1
                        elif mouse_x < 0:
                            mouse_x = 1.
                        if mouse_y > h_scr:
                            mouse_y = h_scr - 1
                        elif mouse_y < 0:
                            mouse_y = 1.
                        autopy.mouse.move(mouse_x, mouse_y)
            else:
                status_moving = 0
            if fingers_status[0] == 0 and flag_click is False:
                flag_click = True
                autopy.mouse.click()
            elif fingers_status[0] == 1 and flag_click is True:
                flag_click = False

            if fingers_status[0] and \
                    fingers_status[1] and \
                    fingers_status[2] and \
                    fingers_status[3] and \
                    exit_cu == 0:
                start_time_exit = time.time()
                exit_cu = 1
                print(1)

            if fingers_status[0] == 0 and \
                    fingers_status[1] == 0 and \
                    fingers_status[2] == 0 and \
                    fingers_status[3] == 0 and \
                    exit_cu == 1:
                exit_cu = 2
                print(2)

            if fingers_status[0] and \
                    fingers_status[1] and \
                    fingers_status[2] and \
                    fingers_status[3] and \
                    exit_cu == 2:
                exit_cu = 3
                print(3)

            if fingers_status[0] == 0 and \
                    fingers_status[1] == 0 and \
                    fingers_status[2] == 0 and \
                    fingers_status[3] == 0 and \
                    exit_cu == 3:
                print(4)
                flag_exit = True
        else:
            status_moving = 0

        if flag_exit:
            break

        if exit_cu != 0 and time.time() - start_time_exit > 2:
            exit_cu = 0

        cv2.imshow("out", img)
        key = cv2.waitKey(1)
        if key == 27:
            break


if __name__ == "__main__":
    main()
