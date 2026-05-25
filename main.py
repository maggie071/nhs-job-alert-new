import requests
import os

print("STARTING...")

api_key = os.getenv("RESEND_API_KEY")

print("API KEY FOUND:", bool(api_key))

response = requests.post(
    "https://api.resend.com/emails",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json={
        "from": "onboarding@resend.dev",
        "to": "margaretchai071@gmail.com",
        "subject": "NHS JOB TEST",
        "html": "<h1>EMAIL WORKS</h1>"
    }
)

print(response.status_code)
print(response.text)
