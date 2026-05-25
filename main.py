import requests
from bs4 import BeautifulSoup
import os

# RSS feed
RSS_URL = "https://findajob.dwp.gov.uk/rss?keywords=psychology"

# 获取 RSS 内容
response = requests.get(
    RSS_URL,
    headers={
        "User-Agent": "Mozilla/5.0"
    },
    timeout=120
)

# 解析 XML
soup = BeautifulSoup(response.content, "xml")

items = soup.find_all("item")

# HTML 邮件内容
html_content = """
<h1>🧠 New Assistant Psychologist Jobs</h1>
"""

# 如果没有岗位
if len(items) == 0:
    html_content += "<p>No jobs found.</p>"

# 最多显示 10 个岗位
for item in items[:10]:

    title = item.title.text if item.title else "No title"
    link = item.link.text if item.link else "#"

    html_content += f"""
    <div style="margin-bottom:20px;">
        <h3>{title}</h3>
        <a href="{link}">View Job</a>
    </div>
    """

# Resend API
RESEND_API_KEY = os.getenv("RESEND_API_KEY")

headers = {
    "Authorization": f"Bearer {RESEND_API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "from": "onboarding@resend.dev",
    "to": os.getenv("TO_EMAIL"),
    "subject": "🧠 New Assistant Psychologist Jobs",
    "html": html_content
}

# 发送邮件
res = requests.post(
    "https://api.resend.com/emails",
    headers=headers,
    json=data
)

print(res.status_code)
print(res.text)
