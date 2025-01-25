from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import transformers

CHROME_DRIVER_PATH = "/Users/aarnavkapoor/Downloads/chromedriver-mac-arm64/chromedriver"
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)

whitehouse = ["https://www.whitehouse.gov/briefings-statements/","https://www.whitehouse.gov/fact-sheets/"]
frontPageLinks = []
try:
    for wh in whitehouse: 
        driver.get(wh)

        time.sleep(3)

        links = driver.find_elements(By.CSS_SELECTOR, "h2.wp-block-post-title a")
    
        for link in links:
            l = link.get_attribute("href") 
            if l:
                frontPageLinks.append(l)

        allText = []
    
        for link in frontPageLinks:
            try:
                driver.get(link)  # Replace with your target URL
                time.sleep(2)
                
                page_text = driver.find_element(By.TAG_NAME, "body").text
                allText.append(page_text)
            except Exception as e:
                print(f"Error visiting link {link}: {e}")
                    
finally:
    # Close the WebDriver
    driver.quit()

titles = []
dates =  []
texts = []
for p in allText:
    c = p.split("\n")
    datePointer = 8
    while not "January" in c[datePointer]:
        datePointer += 1
    titles.append(" ".join(c[7:datePointer]))
    dates.append(c[datePointer])
    texts.append(" ".join(c[9:-12]))

data = zip(frontPageLinks, titles, dates, texts)
df = pd.DataFrame(data, columns=["link", "title", "date", "text"])


def summarize_text(text):
    summary = summarizer(
            text,
            max_length=150,
            min_length=30,
            do_sample=False
        )
    return summary[0]['summary_text']

summarizer = transformers.pipeline("summarization", model="facebook/bart-large-cnn")
df["summary"] = df["text"].apply(summarize_text)
df["summary"].to_csv('test.txt', index=False)
