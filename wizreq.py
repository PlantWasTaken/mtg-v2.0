import requests as r
import subprocess
import asyncio
import psutil

async def open_register_site(url, lock):
    print("open reg site")
    url = url
    pid = await open_url_in_incognito(url, lock)
    return pid

async def open_url_in_incognito(url, lock):
    print("open incog")
    # Specify the path to your Chrome executable
    chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'  # Change this to your Chrome executable path

    # Use subprocess to run the command
    process = subprocess.Popen([chrome_path, '--incognito', url])
    
    process_id = process.pid
    return process_id

    #print("Opened at ID: " + str(process_id))

    
#print(open_register_site(url='https://myaccounts.wizards.com/login'))

#open_register_site()
#request = r.get(url)
#print(request.text)

#https:\u002F\u002Flogin.microsoftonline.com\u002Fconsumers\u002Foauth2\u002Fv2.0\u002Fauthorize
