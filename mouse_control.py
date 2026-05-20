import pyautogui

screen_w, screen_h = pyautogui.size()

def move_mouse(x, y, cam_w, cam_h):

    x = cam_w - x

    screen_x = int(x * screen_w / cam_w)
    screen_y = int(y * screen_h / cam_h)

    pyautogui.moveTo(screen_x, screen_y)


def click():

    pyautogui.click()


def drag():

    pyautogui.mouseDown()


def release():

    pyautogui.mouseUp()


def scroll_up():

    pyautogui.scroll(50)


def scroll_down():

    pyautogui.scroll(-50)