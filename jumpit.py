import requests
from bs4 import BeautifulSoup
import csv


base_url = "https://www.jumpit.co.kr"
user_agent = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
keywords = ["데이터 엔지니어", "데이터 엔지니어링", "데이터 분석가", "데이터 분석", "데이터 사이언티스트", "데이터 사이언스"]
selected_jobs = {}

for keyword in keywords:
    res = requests.get(f"{base_url}/search?sort=relation&keyword={keyword}", user_agent)
    soup = BeautifulSoup(res.text, "html.parser")
    jobs = soup.find_all("div", class_="sc-c8169e0e-0")

    for job in jobs:
        company_info = job.find("div", class_="sc-635ec9d6-0")

        # 회사명, 직무, 상세 링크, 기술 스택
        company = company_info.find("div").get_text(strip=True)
        position = job.find("h2", class_="position_card_info_title").get_text(strip=True)
        job_url = job.find("a")["href"]
        link = f"{base_url}{job_url}"
        skills = company_info.find("ul").get_text(strip=True)

        items = company_info.find_all("ul")[-1]
        location = items.find_all("li")[0].get_text(strip=True)
        career = items.find_all("li")[1].get_text(strip=True)

        # 마감일
        res = requests.get(link, user_agent)
        soup = BeautifulSoup(res.text, "html.parser")
        descriptions = soup.find_all("dl", class_="sc-2da322c6-1")
        due_date = descriptions[2].find("dd").get_text()

        # 중복 항목 확인
        job_id = link  # 채용 공고의 URL을 고유 식별자로 사용
        if job_id not in selected_jobs:
            result = {
                "company": company,
                "position": position,
                "link": link,
                "skills": skills,
                "location": location,
                "career": career,
                "due_date": due_date
            }

            # 공백 제거 후 출력
            result = {key: value.strip() if isinstance(value, str) else value for key, value in result.items()}
            selected_jobs[job_id] = result


data = [job.values() for job in selected_jobs.values()]
with open('jumpit.csv', mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    
    # 헤더 작성
    writer.writerow(selected_jobs[list(selected_jobs.keys())[0]].keys())
    
    # 데이터 작성
    writer.writerows(data)
