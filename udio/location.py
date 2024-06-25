import pyautogui

try:
    while True:
        x, y = pyautogui.position()
        positionStr = 'Coordenadas del mouse: X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
except KeyboardInterrupt:
    print('\n')