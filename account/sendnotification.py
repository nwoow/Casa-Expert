import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("firebasekey.json")
firebase_admin.initialize_app(cred)
from firebase_admin import messaging

from decouple import config

import requests
import json

# def send_push_notification(expo_push_token,title,message):
#     url = "https://exp.host/--/api/v2/push/send"
    
#     headers = {
#         'Accept': 'application/json',
#         'Accept-Encoding': 'gzip, deflate',
#         'Content-Type': 'application/json'
#     }
    
#     payload = {
#         'to': expo_push_token,
#         'sound': 'default',
#         'title': title,
#         'body': message,
#         'data': {'extraData': 'Some extra data'}
#     }
    
#     response = requests.post(url, headers=headers, data=json.dumps(payload))
    
#     if response.status_code == 200:
#         print("Notification sent successfully!")
#     else:
#         print("Failed to send notification.")
#         print(response.text)


def send_push_notification(push_token,title,message_body):
    try:
        message = messaging.Message(
            notification=messaging.Notification(title=title, body=message_body),
            token=push_token,
        )
        response = messaging.send(message)
        print('Successfully sent message:', response)
    except Exception as e:
        print(e)
