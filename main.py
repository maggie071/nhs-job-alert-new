import requests
from bs4 import BeautifulSoup
import os

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

URL = "https://www.jobs.nhs.uk/candidate/search/results?keyword=assistant+psychologist"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)

print(response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

print(soup.prettify()[:5000])

jobs_html = ""

cards = soup.find_all("a")

for card in cards:

    text = card.get_text(" ", strip=True)

    lower = text.lower()

    keywords = [
        "assistant psychologist",
        "trainee psychological wellbeing practitioner",
        "research assistant",
        "occupational therapy assistant",
        "educational mental health practitioner",
        "children wellbeing practitioner",
        "mental health wellbeing practitioner"
    ]

    locations = [
        "london",
        "greater london",
        "oxford",
        "cambridge",
        "manchester",
        "leeds",
        "york",
        "nottingham",
        "exeter"
    ]

    if any(k in lower for k in keywords):

        if any(loc in lower for loc in locations):

            if "nurse" in lower:
                continue

            link = card.get("href")

            if link and not link.startswith("http"):
                link = "https://www.jobs.nhs.uk" + link

            jobs_html += f"""
            <p>
            <b>{text}</b><br>
            <a href="{link}">View Job</a>
            </p>
            <hr>
            """

if jobs_html == "":
    jobs_html = "<h2>Still no jobs found.</h2>"

email_data = {
    "from": "onboarding@resend.dev",
    "to": "margaretchai071@gmail.com",
    "subject": "🧠 New NHS Mental Health Jobs",
    "html": jobs_html
}

requests.post(
    "https://api.resend.com/emails",
    headers={
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    },
    json=email_data
)

print("EMAIL SENT")
