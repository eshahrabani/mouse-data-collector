import pyautogui
import time

def capture():
    with open('mouse_movement.txt', 'w') as file:
        last_x = last_y = 0
        current_time = time.time()

        while True:
            x, y = pyautogui.position()
            if x != last_x or y != last_y:
                # Calculate time delta in milliseconds.
                time_delta = (time.time() - current_time) * 1000
                line = [str(time_delta), str(x), str(y)]
                line = ' '.join(line)

                file.write(line)
                file.write('\n')

                last_x = x
                last_y = y
                current_time = time.time()

def replay(filePath):
    with open(filePath, 'r') as file:
        prev_time = 0
        for line in list(file):
            fields = line.split(' ')

            current_time = float(fields[0])

            if prev_time == 0:
                move_duration = 0
            else:
                move_duration = float(current_time) - prev_time

            x = int(fields[1])
            y = int(fields[2])

            pyautogui.moveTo(x, y, move_duration)

            prev_time = current_time

#replay('mouse_movement.txt')
capture()
