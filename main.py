import requests
import os

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

KEYWORDS = [
    "Assistant Psychologist",
    "Trainee Psychological Wellbeing Practitioner",
    "Research Assistant",
    "Occupational Therapy Assistant",
    "Educational Mental Health Practitioner",
    "Mental Health Wellbeing Practitioner",
    "Trainee Children's Wellbeing Practitioner"
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

for keyword in KEYWORDS:

    url = f"https://www.jobs.nhs.uk/api/job/search?keyword={keyword.replace(' ', '%20')}"

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        jobs = response.json().get("jobs", [])

        for job in jobs:

            title = job.get("jobTitle", "")
            description = job.get("jobDescription", "")
            location = job.get("locationName", "")
            band = job.get("payScheme", "")
            link = "https://www.jobs.nhs.uk/candidate/jobadvert/" + str(job.get("id", ""))

            full_text = f"{title} {description} {location}".lower()

            # location filter
            if not any(loc in full_text for loc in LOCATIONS):
                continue

            # exclude filter
            if any(ex in full_text for ex in EXCLUDE):
                continue

            # band filter
            if "band 3" not in full_text and "band 4" not in full_text:
                continue

            all_jobs.append({
                "title": title,
                "location": location,
                "summary": description[:250],
                "link": link
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
        <p><strong>Location:</strong> {job['location']}</p>
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
