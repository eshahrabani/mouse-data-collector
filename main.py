import time
from pymouse import PyMouse
import pyautogui


mouse = PyMouse()

def capture():
    with open('mouse_movement.txt', 'w') as file:
        last_x = last_y = 0
        current_time = time.time()

        while True:
            x, y = pyautogui.position()
            if x != last_x or y != last_y:
                # Calculate time delta in seconds
                time_delta = (time.time() - current_time)
                line = [str(time_delta), str(x), str(y)]
                line = ' '.join(line)

                file.write(line)
                file.write('\n')

                last_x = x
                last_y = y
                current_time = time.time()

def replay(filePath):
    with open(filePath, 'r') as file:
        for line in list(file):
            fields = line.split(' ')

            delta = float(fields[0])

            x = int(fields[1])
            y = int(fields[2])

            time.sleep(delta)
            mouse.move(x, y)

#replay('mouse_movement.txt')
capture()
