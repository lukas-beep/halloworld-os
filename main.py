import os
from platform import version
import time
import shutil
import sys
from utils.utils import logo
from console import Console
import requests
from colorama import Fore

from rich.panel import Panel
from rich import print

user_menu = """
Choose one opition for {0}:

[1] log-in
[2] change username/password
[3] delete
"""

version_ = "v0.4.0-beta"

def clear():
    os.system("cls")
    print(Panel(logo))

def check_version():
    response = requests.get("https://api.github.com/repos/lukas-beep/halloworld-os/releases/latest")
    version_latest = response.json()["name"]
    if version_latest != version_:
        sys.exit(Fore.RED + "Please update the program from github" +Fore.BLUE+ f"\tlatest version is {version_latest} you are using {version_}" +Fore.CYAN+"\thttps://github.com/lukas-beep/halloworld-os/releases/latest"+ Fore.RESET)
        
    
def presetup():
    check_version()
    path = os.getcwd()
    if not os.path.exists(os.path.join(path, "os")):
        os.mkdir(os.path.join(path, "os"))
        
    path = os.path.join(path, "os")
    in_main_dir = os.listdir(path)
    if in_main_dir == []:
        user = None
    else:
        user = in_main_dir
    return user, path


def create_user(path):
    username = input("Type here your username to be displayed: ")
    password = input("Type here your password: ")
    os.mkdir(os.path.join(path, username))
    with open(os.path.join(path, username, "login_info.txt"), "w") as f:
        f.writelines(username + "\n" + password)
    print("user was setup sucessfuly now the program shut down")
    time.sleep(1.20)
    sys.exit()


def select_user(users):
    clear()
    print("select user: ")
    users.append("Create a new user")
    for i, user in enumerate(users):
        print(f"[{i}] {user}")
    print("")
    while True:
        usr_id = int(input("[?] "))
        if usr_id + 1 <= len(users) and usr_id + 1 >= 0:
            break
        else:
            print("Check again something was wrong")

    return users[usr_id]


def change_password(path, username):
    clear()
    username_new = input("Type here your new username to be displayed (empty for current): ")
    password_new = input("Type here your new password: ")
    
    if username_new == "":
        username_new = username
    
    with open(os.path.join(path, "login_info.txt"), "w") as f:
        f.writelines(username_new + "\n" + password_new)
    print("user was setup sucessfuly now the program shut down")
    time.sleep(1.20)
    sys.exit()


def main():
    clear()
    users, path = presetup()

    if users == None:
        create_user(path)
    else:
        user = select_user(users)
        if user == "Create a new user":
            create_user(path)
        usr_path = os.path.join(path, user)
        with open(os.path.join(usr_path, "login_info.txt"), "r") as f:
            lines = f.readlines()
            password = lines[1]
        clear()
        print(user_menu.format(user))
        while True:
            opition = int(input("[?] "))
            if opition <= 3 and opition >= 0:
                break
            else:
                print("Check again something went wrong")
        if opition == 1:
            password_ = input("Type your password: ")
            if password == password_:
                clear()
                console = Console(usr_path, user)
                console.command_input()
        elif opition == 2:
            password_ = input("Type your password: ")
            if password == password_:
                change_password(usr_path, user)
        elif opition == 3:
            delete = input(f"Do you really want to delete {user} user Y/N ").lower()
            if delete == "y":
                password_ = input("Type your password: ")
                if password == password_:
                    shutil.rmtree(usr_path)


if __name__ == "__main__":
    main()

# TODO implement rich console
# TODO forgot password-- databases
# TODO create instaler/updater