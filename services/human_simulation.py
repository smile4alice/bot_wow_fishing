from random import randint, uniform, choice, random
from time import sleep

import pyautogui


def smoothly_move(end_x, end_y, start_x=None, start_y=None):
    if not start_x or not start_y:
        start_x, start_y = pyautogui.position()

    step_x = abs(start_x - end_x)
    step_y = abs(end_y - start_y)

    x_reversed = start_x > end_x
    y_reversed = start_y > end_y

    x_indicator = True
    y_indicator = True

    while x_indicator or y_indicator:
        pyautogui.PAUSE = uniform(0.002, 0.015)

        x_indicator = end_x != start_x
        y_indicator = end_y != start_y

        if x_reversed:
            if x_indicator:
                step = randint(int(step_x * 0.005), int(step_x * 0.03)) or 1
                start_x -= step if start_x - step > end_x else 1
        else:
            if x_indicator:
                step = randint(int(step_x * 0.005), int(step_x * 0.03)) or 1
                start_x += step if end_x > start_x + step else 1

        if y_reversed:
            if y_indicator:
                step = randint(int(step_y * 0.005), int(step_y * 0.03)) or 1
                start_y -= step if start_y - step > end_y else 1
        else:
            if y_indicator:
                step = randint(int(step_y * 0.005), int(step_y * 0.03)) or 1
                start_y += step if end_y > start_y + step else 1

        pyautogui.moveTo(start_x, start_y)


def jump_and_see_bag():
    bag_bind="b"
    jump_bind="space"
    smoothly_move(randint(200, 720), randint(50, 720))
    pyautogui.press(bag_bind)
    sleep(uniform(1, 7))
    for _ in range(randint(1, 5)):
        pyautogui.press(jump_bind)
        sleep(uniform(1, 7))
    pyautogui.press(bag_bind)


def jump_and_worldmap():
    worldmap_bind="m", 
    jump_bind="space"
    pyautogui.press(worldmap_bind)
    sleep(uniform(1, 7))
    for _ in range(randint(1, 5)):
        pyautogui.press(jump_bind)
        sleep(uniform(1, 7))
    pyautogui.press(worldmap_bind)


def trinket_and_turn():
    trinket_bind=["alt", "q"]
    jump_bind="space"
    pyautogui.hotkey(trinket_bind)
    smoothly_move(randint(200, 720), randint(50, 720))
    pyautogui.mouseDown(button="right")

    return_sector = list()

    distance = randint(200, 600)
    while distance > 0:
        end_x = randint(1, 6)
        end_y = randint(-1 if end_x % 2 else 0, 1 if end_x % 3 else 0)
        distance -= end_x
        pyautogui.PAUSE = uniform(0.002, 0.015)
        pyautogui.move(end_x, end_y)
        return_sector.append({"end_x": end_x, "end_y": end_y})
        if random() < 0.03:
            pyautogui.press(jump_bind)

    distance = randint(-600, -200)
    while distance < 0:
        end_x = randint(-6, -1)
        end_y = randint(-1 if end_x % 2 else 0, 1 if end_x % 3 else 0)
        distance -= end_x
        pyautogui.PAUSE = uniform(0.002, 0.015)
        pyautogui.move(end_x, end_y)
        return_sector.append({"end_x": end_x, "end_y": end_y})
        if random() < 0.03:
            pyautogui.press(jump_bind)

    for coord in return_sector:
        end_x = coord["end_x"] * -1
        end_y = coord["end_y"] * -1
        pyautogui.PAUSE = uniform(0.002, 0.015)
        pyautogui.move(end_x, end_y)
        if random() < 0.01:
            pyautogui.press(jump_bind)
    else:
        pyautogui.PAUSE = uniform(0.002, 0.015)
        pyautogui.move(randint(-3, 3), randint(-3, 3))
        pyautogui.PAUSE = uniform(0.002, 0.015)
        pyautogui.move(randint(-3, 3), randint(-3, 3))

    pyautogui.mouseUp(button="right")


def go_side():
    sides: list = ["a", "d"]
    duration = uniform(0.1, 0.5)
    smoothly_move(randint(200, 720), randint(50, 720))
    while sides:
        key = choice(sides)
        sides.remove(key)
        pyautogui.mouseDown(button="right")
        pyautogui.keyDown(key)
        sleep(uniform(duration - 0.05, duration + 0.05))
        pyautogui.keyUp(key)
        pyautogui.mouseUp(button="right")
        sleep(uniform(1, 5))

def jump_and_stay():
    jump_bind="space"
    duration = uniform(10, 20)
    pyautogui.press(jump_bind)
    for _ in range(randint(1, 3)):
        pyautogui.press(jump_bind)
        sleep(uniform(1, 3))
    sleep(duration)

def cast_ability():
    ability_hotkeys = [
        ["ctrl", "r"],
        ["alt", "e"],
        ["shift", "3"],
        ["shift", "5"],
        ["shift", "6"],
        ["f"],
    ]
    smoothly_move(randint(200, 720), randint(50, 720))
    sleep(uniform(1, 5))
    pyautogui.hotkey(choice(ability_hotkeys))


human_simulatons: list[dict] = [
    trinket_and_turn,
    jump_and_worldmap,
    go_side,
    jump_and_see_bag,
    cast_ability,
]
