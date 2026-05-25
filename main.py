import requests
import os
from bs4 import BeautifulSoup

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

KEYWORDS = [
    "Assistant Psychologist",
    "Trainee Psychological Wellbeing Practitioner",
    "Research Assistant",
    "Occupational Therapy Assistant",
    "Trainee Children's Wellbeing Practitioner",
    "Educational Mental Health Practitioner",
    "Mental Health Wellbeing Practitioner"
]

LOCATIONS = [
    "London",
    "Greater London",
    "Exeter",
    "Oxford",
    "Cambridge",
    "Leeds",
    "York",
    "Manchester",
    "Nottingham"
]

EXCLUDE_TERMS = [
    "qualified pwp only",
    "nurse only"
]

all_jobs = []

for keyword in KEYWORDS:

    url = f"https://www.jobs.nhs.uk/api/search?keyword={keyword.replace(' ', '+')}&format=rss"

    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=30
        )

        soup = BeautifulSoup(response.content, "xml")

        items = soup.find_all("item")

        for item in items:

            try:
                title = item.title.text.strip()
            except:
                title = ""

            try:
                link = item.link.text.strip()
            except:
                link = ""

            try:
                description = item.description.text.strip()
            except:
                description = ""

            full_text = f"{title} {description}".lower()

            # location filter
            if not any(
                location.lower() in full_text
                for location in LOCATIONS
            ):
                continue

            # exclude filter
            if any(
                excluded in full_text
                for excluded in EXCLUDE_TERMS
            ):
                continue

            all_jobs.append({
                "title": title,
                "description": description[:300],
                "link": link
            })

    except Exception as e:
        print(f"ERROR: {e}")

# remove duplicates
unique_jobs = []
seen_links = set()

for job in all_jobs:
    if job["link"] not in seen_links:
        unique_jobs.append(job)
        seen_links.add(job["link"])

job_html = ""

for job in unique_jobs[:20]:

    job_html += f"""
    <div style="margin-bottom:25px;">
        <h3>{job['title']}</h3>
        <p>{job['description']}</p>
        <a href="{job['link']}">View Job</a>
    </div>
    <hr>
    """

if not job_html:
    job_html = "<p>No matching jobs found.</p>"

# SEND EMAIL

url = "https://api.resend.com/emails"

headers = {
    "Authorization": f"Bearer {RESEND_API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "from": "onboarding@resend.dev",
    "to": "margaretchai071@gmail.com",
    "subject": "🧠 New NHS Mental Health Jobs",
    "html": f"""
    <h1>New NHS Mental Health Jobs</h1>
    {job_html}
    """
}

response = requests.post(
    url,
    headers=headers,
    json=data
)

print(response.status_code)
print(response.text)
