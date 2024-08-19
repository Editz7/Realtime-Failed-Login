import subprocess
import requests
import time

GOTIFY_URL = "##GOTIFY_URL##"
GOTIFY_TOKEN = "##GOTIFY_TOKEN"

last_failed_login = None

def check_failed_logins():
    """
    Checks for the most recent failed login attempt and sends a notification if it's new.
    """
    global last_failed_login

    try:
        result = subprocess.run(['lastb', '-1'], capture_output=True, text=True)
        failed_login = result.stdout.strip()

        if failed_login and failed_login != last_failed_login:
            send_gotify_notification(failed_login)
            last_failed_login = failed_login

    except Exception as e:
        print(f"Error checking failed logins: {e}")

def send_gotify_notification(failed_login):
    """
    Sends a Gotify notification with the details of the new failed login attempt.
    """
    data = {
        "title": "New Failed Login Attempt Detected",
        "message": failed_login,
    }
    headers = {
        "X-Gotify-Key": GOTIFY_TOKEN
    }

    try:
        response = requests.post(f"{GOTIFY_URL}/message", json=data, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"Error sending Gotify notification: {e}")

if __name__ == "__main__":
    while True:
        check_failed_logins()
        time.sleep(60)