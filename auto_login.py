import requests
import time
from datetime import datetime
import os


NEW_CONN = "NEW_CONN"
ALREADY_CONN = "ALREADY_CONN"
INVALID_CREDS = "INVALID_CREDS"
RETRYING = "RETRYING"


GOT_CREDS = False
CRED_FILE = "cred_file.txt"
CREDS = [-1, -1]
LAST_STATUS = "GETTING STARTED"
# datetime object containing current date and time


# dd/mm/YY H:M:S


def is_connected(data):
    data = data.lower()
    return "redirecting" not in str(data)


def get_creds():
    if CREDS[0] == -1:
        if GOT_CREDS:
            try:
                file = open("./" + CRED_FILE, "r")
                data = file.read().split("}")
                file.close()
                return data[0], data[1]
            except:
                return -1, -1
        else:
            return CREDS[0], CREDS[1]
    else:
        return -1, -1


def set_creds():
    global GOT_CREDS
    if CRED_FILE in os.listdir("."):
        GOT_CREDS = True
    else:
        print("Credential file is absent, we will now ask for your credentials")
        GOT_CREDS = False


def get_status(data):
    """

    :param data:
    :return: new_connection, already_connected, invalid_credentials

    1. NEW_CONN
    2. ALREADY_CONN
    3. INVALID_CREDS
    """

    data = data.lower()

    if "redirecting" in data:
        return NEW_CONN
    elif "invalid credentials" in data:
        return INVALID_CREDS
    else:
        return ALREADY_CONN


print("Starting Lan Auto Login System (LALSy)")
while True:
    set_creds()
    if GOT_CREDS:

        if CREDS[0] == -1:

            CREDS[0], CREDS[1] = get_creds()

        if CREDS[0] != -1:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

            api_url = "http://172.16.1.3:8002/index.php"
            data = {
                "zone": "lan",
                "rediurl": "https://mnit.ac.in",
                "auth_user": CREDS[0],
                "auth_pass": CREDS[1],
                "accept": "LOGIN"
            }

            try:
                response = requests.post(url=api_url, data=data)

                response_status = get_status(str(response.content))

                if LAST_STATUS != response_status or LAST_STATUS == "GETTING STARTED":
                    if response_status == NEW_CONN:
                        print("New connection made at", dt_string)
                        pass
                    elif response_status == INVALID_CREDS:
                        print("The credentials you had given were wrong, please provide details again", dt_string)
                        os.remove(CRED_FILE)
                        CREDS[0] = -1
                        CREDS[1] = -1
                        pass
                    elif response_status == ALREADY_CONN:
                        print("Connection exists at", dt_string)
                    else:
                        print("response status", response_status)
                        pass

                LAST_STATUS = response_status

            except:
                print("Could not connect, retrying")
                LAST_STATUS = RETRYING
        else:
            print("Could not find Credentials")
            if CRED_FILE in os.listdir():
                CREDS[0] = -1
                CREDS[1] = -1
                os.remove(CRED_FILE)
    else:
        print("We have to take the username and password once")
        username = input("Username: ")
        password = input("Password: ")
        file = open(CRED_FILE, "w")
        file.write(username + "}" + password)
        print("write complete")
        CREDS[0] = username
        CREDS[1] = password
        file.close()
        LAST_STATUS = INVALID_CREDS

    time.sleep(1)

    """
    1. taking in username and password
    2. verifying username and password
    3. 
    
    """
