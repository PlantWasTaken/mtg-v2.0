import time as t
import pyautogui

def redeem_code():
    f = open('codes.txt').readlines()
    f = [i.split() for i in f]
    t.sleep(4)
    for i in range(len(f)):
        #ctrl + a
        pyautogui.keyDown('ctrl')
        pyautogui.press('a') 
        pyautogui.keyUp('ctrl')
    
        pyautogui.write(str(f[i])[2:-2])
        pyautogui.press('enter') 
