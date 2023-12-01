#meowkingkitten314@gmail.com 
#DELETE m.eowkingkitten314@gmail.com account
#wiz pass: CoolCat123
#mammaogpappa
#881804771981-5phsg8mqt1g7jk8lja2gcprhedcuu3ui.apps.googleusercontent.com
import asyncio
async def get_verification_link(lock):
    print("read mail")
    import email, imaplib
    import re

    username= "meowkingkitten314@gmail.com "
    password = 'pass'

    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(username, password) #log into googuru

    status, messages = imap.select("INBOX") #access inbox

    tmp, messages = imap.search(None, 'ALL') #search all mails
    message_ids = messages[0].split()

    last_mail = message_ids[-1] #last mail.
    print(last_mail)
    while True: #check for new mail
        status, messages = imap.select("INBOX") #access inbox

        tmp, messages = imap.search(None, 'ALL') #search all mails
        message_ids = messages[0].split()

        current_latest_mail = message_ids[-1] #last mail.

        #check for new mail
        if(last_mail == current_latest_mail): #no new mail
            await asyncio.sleep(5) #check for new mail every 5 seconds
        else:
            break
    
    #print(message_ids) how many mails

    tmp, data = imap.fetch(current_latest_mail, '(RFC822)') #-1 get last mail

    msg = email.message_from_bytes(data[0][1])

    verification_mail = str(msg.get_payload()[1])

    verification_mail = str(verification_mail[84:]) #filter out non html text

    # Define a regular expression pattern to extract the link
    link_pattern = re.compile(r'https://myaccounts\.wizards\.com/verify\?verification=[^"\']+', re.IGNORECASE)

    # Find matches in the HTML string
    matches = str(link_pattern.findall(verification_mail))[2:] #extracting the link + extra fluff

    verification_link = str(matches.split()[0]) #removing fluff

    cleaned_link = re.sub(r'\\n', '', verification_link)

    parts = cleaned_link.split('=')  # Split the string at each '=' character
    cleaned_link = parts[0] + '=' + ''.join(parts[1:])
    cleaned_link = cleaned_link.replace("=3D", "=", 1)

    imap.logout()
    return cleaned_link

#asyncio.run(get_verification_link(None))
