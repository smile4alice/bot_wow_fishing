import cv2
import pyautogui
import numpy as np

from services.logger import logger


def create_screenshot(mode: str | None = None, bbox=tuple[int] | None) -> np.ndarray:
    base_screen = np.array(pyautogui.screenshot())
    if bbox:
        base_screen = base_screen[bbox[1] : bbox[3], bbox[0] : bbox[2]]
    if mode == "bgr":
        return cv2.cvtColor(base_screen, cv2.COLOR_RGB2BGR)
    else:
        return cv2.cvtColor(base_screen, cv2.COLOR_RGB2GRAY)


def search_floater(img_gray):
    results = list()
    templates = [
        "templates/floater1.png",
        "templates/floater2.png",
        "templates/floater1_plaguelands.png",
        "templates/floater2_plaguelands.png",
    ]
    for template_path in templates:
        template = cv2.imread(template_path)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        loc = np.where(res >= 0.68)
        results.append({"template": template, "max_val": max_val, "loc": loc, "res": res, 'template_path' : template_path})

    result = max(results, key=lambda x: x["max_val"])
    logger.warning('+ ' + result['template_path'].split('/')[-1])
    logger.warning('? ' + str(round(result["max_val"], 3)) + ' > 0.67')

    return result


if __name__ == "__main__":
    bgr = create_screenshot()
