import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime

URL = "https://tyomarkkinatori.fi/henkiloasiakkaat/avoimet-tyopaikat?pa=MAX_1_DAY&r=06"

# Hakusäännöt syrjiviin ehtoihin
tests = {
    "ika": r"\b(\d{2}\s?vuotia|alle\s?\d{2}|yli\s?\d{2})\b",
    "sukupuoli": r"\b(mies|nainen|naishakija|mieshakija)\b",
    "kansalaisuus": r"\b(suomen kansalainen|vain suomalainen)\b",
    "aidinkieli": r"\b(äidinkielenä suomi|natiivi suomi)\b",
    "arkaluonteinen": r"\b(kuva\s?vaaditaan|kuva mukaan|siviilisääty|syntymäaika)\b",
    "rikosrekisteri": r"\b(rikosrekisteri|rikosrekisteriote|luottotiedot)\b",
    "terveys": r"\b(terveydentila|hyväkuntoinen|ei sairauksia)\b"
}

def fetch_jobs():
    html = requests.get(URL).text
    soup = BeautifulSoup(html, "html.parser")

    # Etsi työpaikkailmoitusten linkit
    links = soup.select("a[href*='/avoimet-tyopaikat/']")
    results = []

    for a in links:
        link = "https://tyomarkkinatori.fi" + a.get("href")
        content = requests.get(link).text.lower()

        job_errors = []

        for name, pattern in tests.items():
            if re.search(pattern, content, re.IGNORECASE):
                job_errors.append(name)

        results.append({
            "url": link,
            "errors": job_errors
        })

    return results

def main():
    jobs = fetch_jobs()

    report = {
        "timestamp": datetime.now().isoformat(),
        "count": len(jobs),
        "jobs": jobs
    }

    with open("latest_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()
  
