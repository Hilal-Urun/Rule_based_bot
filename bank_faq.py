import requests
from bs4 import BeautifulSoup

urls = ["https://www.ziraatbank.com.tr/en/faq/digital-banking/mobile-banking",
        "https://www.ziraatbank.com.tr/en/faq/digital-banking/internet-banking",
        "https://www.ziraatbank.com.tr/en/faq/digital-banking/atm",
        "https://www.ziraatbank.com.tr/en/faq/digital-banking/money-order-to-mobile",
        "https://www.ziraatbank.com.tr/en/faq/digital-banking/otp"]


def return_faq():
    q_a = []
    for url in urls:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        elements = soup.find(id="accWrap")
        content = elements.find_all("div", class_="acc-box")
        for c in content:
            question = c.find("h2")
            answer = c.find("div", class_="acc-content")
            q_a.append(question.text)
            q_a.append(answer.text)
    return q_a

