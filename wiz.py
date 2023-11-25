import pyautogui
import time as t

import json
import psutil
import random

from salted import get_bin_salt
from wizreq import open_register_site

#ORDER
#open website, tab 3 times
#make account
def create_account(usn):
    process_id = open_register_site(url='https://myaccounts.wizards.com/register')    

    def gen_pass():
        ps = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        ps = [i for i in ps]
        random.shuffle(ps)
        return "".join(ps[0:10])

    t.sleep(3)

    with open("accountdatabase.json", "r") as read_file:
        data = json.load(read_file)

    seed = data['salt_seed'] #salt seed
    data['salt_seed'] = int(data['salt_seed'])+1

    with open("accountdatabase.json", "w") as write_file:
        json.dump(data, write_file, indent=4)


    mail = 'meowkingkitten314'

    mail2 = 'gmail.com'

    passw = 'CoolCat123'
    passw = gen_pass()

    #usn = 'Cool cat'
    usn = usn

    mail_salt = get_bin_salt(seed=seed, mail=mail)

    mail_salt='me.owkingkitten314'
    print(mail_salt)

    t.sleep(0.7)    
    pyautogui.press('tab') 
    t.sleep(0.3)
    pyautogui.press('tab') 
    t.sleep(0.3)
    pyautogui.press('tab') 

    pyautogui.write("plant")
    pyautogui.press('tab') 
    pyautogui.write("egg")
    pyautogui.press('tab') 
    for i in range(13):
        pyautogui.write("n")
    pyautogui.press('tab') 
    for i in range(2):
        pyautogui.write("j")
    pyautogui.press('tab') 
    pyautogui.write("2")
    pyautogui.press('tab') 
    pyautogui.write("1")
    for i in range(2):
        pyautogui.press('tab') 
        pyautogui.write(mail_salt)
        pyautogui.hotkey('altright','2')

        pyautogui.write(mail2)

    pyautogui.press('tab') 
    pyautogui.write(usn)
    for i in range(2):
        pyautogui.press('tab') 
        pyautogui.write(passw)

    for i in range(6):
        pyautogui.press('tab') 

    pyautogui.press('enter') 

    t.sleep(2) #terminate browser
    print(process_id)
    process = psutil.Process(process_id)
    process.terminate()
    #account has been created.
    #awaiting email confirmation

    from reademail import get_verification_link #get link, open link, redeem codes.
    t.sleep(20) #wait for email to come through

    verification_link = get_verification_link()
    print(verification_link)

    process_id = open_register_site(url=verification_link)  #activate account

    t.sleep(5)

    #account login and code redemption
    for i in range(3):
        pyautogui.press('tab') 

    pyautogui.write(mail_salt) #username
    pyautogui.hotkey('altright','2')
    pyautogui.write(mail2)

    pyautogui.press('tab') #password

    pyautogui.write(passw)

    for i in range(2):
        pyautogui.press('tab') 

    #3V5l6PhNUK m.e.owkingkitten314
    pyautogui.press('enter')    #login
    t.sleep(2)

    for i in range(2):
        pyautogui.press('tab') 

    #run code redemption
    from codes import redeem_code

    redeem_code() #code redeems
    process = psutil.Process(process_id)
    process.terminate()
    #terminate process.

    return [f'{mail_salt}@{mail2}', passw, usn]

#exit()
#f = open('accounts.txt', 'a')
#
#print(f'MTG AREMA {usn}')
#print(f'Mail: {mail_salt}@{mail2}')
#print(f'Password: {passw}')
#
#f.write(f'MTG AREMA {usn}: Wildcards: \n')
#f.write(f'Mail: {mail_salt}@{mail2}\n')
#f.write(f'Password: {passw}\n\n')
#
#f.close()