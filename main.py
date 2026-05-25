import requests
import os
from bs4 import BeautifulSoup

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

SEARCH_TERMS = [
    "assistant psychologist",
    "trainee psychological wellbeing practitioner",
    "research assistant",
    "occupational therapy assistant",
    "educational mental health practitioner",
    "mental health wellbeing practitioner",
    "trainee children's wellbeing practitioner"
]

LOCATIONS = [
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

EXCLUDE = [
    "qualified pwp only",
    "nurse only"
]

all_jobs = []

headers = {
    "User-Agent": "Mozilla/5.0"
}

for term in SEARCH_TERMS:

    url = f"https://www.jobs.nhs.uk/candidate/search/results?keyword={term.replace(' ', '+')}"

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        soup = BeautifulSoup(response.text, "html.parser")

        cards = soup.find_all("li", class_="search-result")

        for card in cards:

            text = card.get_text(" ", strip=True).lower()

            # location filter
            if not any(location in text for location in LOCATIONS):
                continue

            # exclude filter
            if any(word in text for word in EXCLUDE):
                continue

            # band filter
            if "band 3" not in text and "band 4" not in text:
                continue

            title_tag = card.find("h2")

            if not title_tag:
                continue

            title = title_tag.get_text(strip=True)

            link_tag = title_tag.find("a")

            if link_tag:
                link = "https://www.jobs.nhs.uk" + link_tag["href"]
            else:
                link = ""

            summary = text[:300]

            all_jobs.append({
                "title": title,
                "link": link,
                "summary": summary
            })

    except Exception as e:
        print(e)

# remove duplicates
unique_jobs = []
seen = set()

for job in all_jobs:
    if job["link"] not in seen:
        unique_jobs.append(job)
        seen.add(job["link"])

html_jobs = ""

for job in unique_jobs[:20]:

    html_jobs += f"""
    <div style="margin-bottom:25px;">
        <h3>{job['title']}</h3>
        <p>{job['summary']}</p>
        <a href="{job['link']}">View Job</a>
    </div>
    <hr>
    """

if not html_jobs:
    html_jobs = "<h2>No matching jobs found.</h2>"

# SEND EMAIL

url = "https://api.resend.com/emails"

headers = {
    "Authorization": f"Bearer {RESEND_API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "from": "onboarding@resend.dev",
    "to": "margaretchai071@gmail.com",
    "subject": "🧠 NHS Mental Health Jobs Alert",
    "html": f"""
    <h1>New NHS Mental Health Jobs</h1>
    {html_jobs}
    """
}

response = requests.post(
    url,
    headers=headers,
    json=data
)

print(response.status_code)
print(response.text)
