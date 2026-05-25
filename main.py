import requests
import os

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")

SEARCH_TERMS = [
    "Assistant Psychologist NHS Band 3",
    "Assistant Psychologist NHS Band 4",
    "Trainee Psychological Wellbeing Practitioner NHS",
    "Research Assistant Mental Health NHS",
    "Occupational Therapy Assistant NHS",
    "Educational Mental Health Practitioner NHS",
    "Mental Health Wellbeing Practitioner NHS"
]

LOCATIONS = [
    "London",
    "Oxford",
    "Cambridge",
    "Manchester",
    "Leeds",
    "York",
    "Nottingham",
    "Exeter"
]

EXCLUDE = [
    "qualified PWP only",
    "nurse only"
]

all_jobs = []

for term in SEARCH_TERMS:

    params = {
        "engine": "google_jobs",
        "q": term,
        "api_key": SERPAPI_KEY
    }

    response = requests.get(
        "https://serpapi.com/search",
        params=params
    )

    data = response.json()

    jobs = data.get("jobs_results", [])

    for job in jobs:

        title = job.get("title", "")
        company = job.get("company_name", "")
        location = job.get("location", "")
        description = job.get("description", "")
        link = job.get("related_links", [{}])[0].get("link", "")

        full_text = f"{title} {description} {location}".lower()

        # location filter
        if not any(loc.lower() in full_text for loc in LOCATIONS):
            continue

        # exclude filter
        if any(ex.lower() in full_text for ex in EXCLUDE):
            continue

        all_jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "description": description[:250],
            "link": link
        })

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
        <p><strong>{job['company']}</strong></p>
        <p><strong>{job['location']}</strong></p>
        <p>{job['description']}</p>
        <a href="{job['link']}">View Job</a>
    </div>
    <hr>
    """

if not html_jobs:
    html_jobs = "<h2>No matching jobs found.</h2>"

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
    "https://api.resend.com/emails",
    headers=headers,
    json=data
)

print(response.status_code)
print(response.text)
