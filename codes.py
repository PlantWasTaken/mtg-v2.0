import time as t
import pyautogui
import asyncio

async def redeem_code(lock):
    f = open('codes.txt').readlines()
    f = [i.split() for i in f]
    await asyncio.sleep(4)
    for i in range(len(f)):
        #ctrl + a
        pyautogui.keyDown('ctrl')
        pyautogui.press('a') 
        pyautogui.keyUp('ctrl')
    
        pyautogui.write(str(f[i])[2:-2])
        pyautogui.press('enter') 
