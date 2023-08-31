import threading
from time import sleep
from random import uniform, randint, random, choice
import os

import numpy as np
import pyautogui
import keyboard

from services.logger import logger
from services.vision_helpers import create_screenshot, search_floater
from services.human_simulation import smoothly_move, human_simulatons

workspace_bbox = (0, 0, 1484, 843)


def exit_on_esc():
    while True:
        sleep(1)
        if keyboard.is_pressed("esc"):
            current_pid = os.getpid()
            logger.critical(f"pressed the [ESC] and killed the pid: {current_pid}")
            os.kill(current_pid, 15)  # 15 - control kill /  9 force kill


def main():
    global workspace_bbox

    exit_thread = threading.Thread(target=exit_on_esc)
    exit_thread.daemon = True
    exit_thread.start()

    average = [0]
    interruption_indicator = False
    break_counter = 0

    for i in range(1, 501):
        logger.info(f"#{i}")
        sleep(uniform(2, 7))
        if random() <= 0.05:
            func = choice(human_simulatons)
            logger.warning(func.__name__)
            func()

        if break_counter > 2:
            logger.warning("OVER")
            pyautogui.press("space")
            sleep(uniform(1, 10))
            pyautogui.press("space")
            break

        pyautogui.press("1")
        sleep(uniform(1.8,2.2))

        img_gray = create_screenshot("bgr", bbox=workspace_bbox)

        res = search_floater(img_gray)
        loc = res["loc"]
        template_width, template_heigth, _ = res["template"].shape
        sleep(1)
        for _ in range(100):
            sleep(0.23)
            try:
                clean_screen = create_screenshot(bbox=(x, y, x + template_width, y + template_heigth))
                mean = np.mean(clean_screen)
                diff = average[-1] - mean
                logger.info("? " + f"{diff.round(2)}".rjust(6) + " > +-3")
                break_counter = 0

                if (diff >= 3 or diff <= -3) and len(average) > 1:
                    logger.warning(f"submit {x+10, y+10}")
                    sleep(uniform(0.1, 0.3))
                    smoothly_move(x + 10, y + 10)
                    sleep(uniform(0.2, 0.5))
                    pyautogui.mouseDown(button="right")
                    sleep(uniform(0.1, 0.3))
                    pyautogui.mouseUp(button="right")
                    sleep(uniform(0.2, 0.6))
                    break

                average.append(mean)

            except Exception as exc:
                if not interruption_indicator:
                    for pt in zip(*loc[::-1]):
                        x = int(pt[0])
                        y = int(pt[1])
                    interruption_indicator = True
                    break_counter += 1
                else:
                    logger.error('bad matching')
                    break

        smoothly_move(randint(40, 325), randint(40, 720))

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
