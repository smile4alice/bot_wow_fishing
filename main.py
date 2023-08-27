import threading
from time import sleep
from random import uniform, randint
import os

import numpy as np
from PIL import ImageGrab
import cv2
import pyautogui
import keyboard

from services.logger import logger


def create_screenshot(mode: str | None = None) -> np.ndarray:
    base_screen = np.array(ImageGrab.grab(bbox=(0, 0, 1484, 843)))
    if mode == "bgr":
        return cv2.cvtColor(base_screen, cv2.COLOR_RGB2BGR)
    else:
        # cv2.imshow("s", cv2.cvtColor(base_screen, cv2.COLOR_RGB2GRAY))
        # cv2.waitKey(0)
        return cv2.cvtColor(base_screen, cv2.COLOR_RGB2GRAY)


def exit_on_esc():
    while True:
        sleep(1)
        if keyboard.is_pressed("esc"):
            current_pid = os.getpid()
            logger.critical(f"pressed the [ESC] and killed the pid: {current_pid}")
            os.kill(current_pid, 15)  # 15 - control kill /  9 force kill


def main():
    exit_thread = threading.Thread(target=exit_on_esc)
    exit_thread.daemon = True
    exit_thread.start()

    average = [
        0,
    ]
    interruption_indicator = False
    break_counter = 0

    template = cv2.imread("templates/template.png", 0)
    w, h = template.shape

    for i in range(1000):
        logger.info(f'iteration #{i}')
        sleep(uniform(1, 7))

        if break_counter > 5:
            logger.warning("OVER")
            pyautogui.press("space")
            sleep(uniform(1, 10))
            pyautogui.press("space")
            break

        pyautogui.press("1")
        sleep(2)

        img_gray = create_screenshot()
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

        # TODO test
        test_match = cv2.minMaxLoc(res)
        logger.warning(test_match[1])

        loc = np.where(res >= 0.68)

        for _ in range(100):
            sleep(0.25)
            try:
                clean_screen = ImageGrab.grab(bbox=(x, y, x + w, y + h))
                mean = np.mean(clean_screen)
                diff = average[-1] - mean
                logger.info(diff.round(3))
                break_counter = 0
                if diff > 5:
                    sleep(uniform(0.3, 1))
                    pyautogui.moveTo(x + 20, y + 20)
                    logger.warning(f"submit {x+20, y+20}")
                    pyautogui.mouseDown()
                    sleep(uniform(0.2, 0.5))
                    pyautogui.mouseUp()
                    break
                average.append(mean)
            except:
                if not interruption_indicator:
                    logger.warning("skip and continue")
                    for pt in zip(*loc[::-1]):
                        x = int(pt[0])
                        y = int(pt[1])
                    interruption_indicator = True
                    break_counter += 1
                else:
                    break
        pyautogui.moveTo(randint(50, 150), randint(50, 150))

        # reload variables
        try:
            del x
            del y
        except:
            pass
        average = [
            0,
        ]
        interruption_indicator = False


if __name__ == "__main__":
    main()
