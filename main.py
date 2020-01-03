import time
import pyautogui

def capture(duration):
    start_time = time.time()

    with open('mouse_movement.txt', 'w') as file:
        last_x = last_y = 0
        current_time = time.time()

        count = 0
        while time.time() - start_time < duration:
            x, y = pyautogui.position()
            if x != last_x or y != last_y:
                # Calculate time delta in milliseconds
                time_delta = (time.time() - current_time) * 1000
                line = [str(time_delta), str(x), str(y)]
                line = ' '.join(line)

                file.write(line)
                file.write('\n')

                last_x = x
                last_y = y
                current_time = time.time()

                count = count + 1

def replay(file_path):
    with open(file_path, 'r') as file:
        for line in list(file):
            if 'move' in line:
                fields = line.split(' ')
                x = fields[1]
                y = fields[2]

                pyautogui.moveTo(x, y)
            elif 'wait' in line:
                fields = line.split(' ')
                delta_s = float(fields[1]) / 1000

                time.sleep(delta_s)
            elif 'end' in line:
                # REMOVE ME: sleep 5 seconds to indicate end of path
                time.sleep(5)

# create encoding.txt
def encode_paths(mouse_movement_file_path):
    out_lines = []

    with open(mouse_movement_file_path, 'r') as file:
        line_num = 1

        for line in file:
            fields = line.split(' ')

            delta = float(fields[0])
            x = int(fields[1])
            y = int(fields[2])

            # if delta > 50 ms, the break was long enough before this point, so we start a new path
            if delta > 50 or line_num == 1:
                # end the last path
                # don't output a wait command here
                if line_num > 1:
                    out_lines.append('end\n')

                # begin a new path
                out_lines.append('begin\n')
                out_lines.append('move {x} {y}\n'.format(x=x, y=y))
            else:
                out_lines.append('wait {delta}\n'.format(delta=delta))
                out_lines.append('move {x} {y}\n'.format(x=x, y=y))

            line_num = line_num + 1

    formatted_lines = []
    index = 0
    for line in out_lines:
        if 'begin' in line:
            next_line = out_lines[index + 1]
            next_fields = next_line.split(' ')
            x1 = next_fields[1]
            y1 = next_fields[2].replace('\n', '')

            # find [x, y] end point
            x2 = 0
            y2 = 0
            for offset in range(1, len(out_lines) - index):
                future_line = out_lines[index + offset]
                if 'end' in future_line:
                    prev_fields = out_lines[index + offset - 1].split(' ')
                    x2 = prev_fields[1]
                    y2 = prev_fields[2].replace('\n', '')
                    break

            line = 'begin {x1} {y1} {x2} {y2}\n'.format(x1=x1, y1=y1, x2=x2, y2=y2)

        formatted_lines.append(line)


        index += 1
    with open('encoding.txt', 'w') as file:
        file.writelines(formatted_lines)



#replay('mouse_movement.txt')
capture(10)
encode_paths('mouse_movement.txt')

