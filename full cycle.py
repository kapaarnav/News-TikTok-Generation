from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import transformers
from moviepy import VideoFileClip, TextClip, CompositeVideoClip
import google.generativeai as genai

CHROME_DRIVER_PATH = "/Users/aarnavkapoor/Downloads/chromedriver-mac-arm64/chromedriver"
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)

# array that holds relavant links
whitehouse = ["https://www.whitehouse.gov/briefings-statements/","https://www.whitehouse.gov/fact-sheets/"]
frontPageLinks = [] # storage for all the sublinks we will get

# standard try for selenium driver
try:
    # for each link that we scrape
    for wh in whitehouse: 
        driver.get(wh) # open the site

        time.sleep(3) # wait for it to load

        # get all js objects that are this css selector, found by inspecting
        links = driver.find_elements(By.CSS_SELECTOR, "h2.wp-block-post-title a")
    
        # each link has a href for the site we actually want
        for link in links:
            l = link.get_attribute("href") 
            if l:
                frontPageLinks.append(l) # store it

        allText = [] # storage for the text on each site

        # navigate each sublink and extract text
        for link in frontPageLinks:
            try:
                driver.get(link)  # launch site

                time.sleep(2) # wait for site to load
                
                # get all the text
                page_text = driver.find_element(By.TAG_NAME, "body").text

                # store it
                allText.append(page_text)
            except Exception as e:
                print(f"Error visiting link {link}: {e}")
                    
finally:
    # Close the WebDriver
    driver.quit()

titles = [] # store all titles
dates =  [] # date etc
texts = []
for p in allText:
    c = p.split("\n") # split the text into lines
    datePointer = 8 # based on formatting of the site, 
    # 8 is usually the index of where the date is but we scoot it forward until we find it
    # january because we are in january, can be futureproofed by using a hashmap and time modele
    while not "January" in c[datePointer]:
        datePointer += 1
    
    #everything before the date is the title
    titles.append(" ".join(c[7:datePointer]))
    #add the date ptointer
    dates.append(c[datePointer])
    # everything after is the article body
    texts.append(" ".join(c[9:-12]))

# make the dataframe from those columns and keep the original link for citations
data = zip(frontPageLinks, titles, dates, texts)
df = pd.DataFrame(data, columns=["link", "title", "date", "text"])


genai.configure(api_key="AIzaSyANmCjwB6DgM8MJgSsNEmReLKzZlStEQfE")
model = genai.GenerativeModel("gemini-1.5-flash")

article = df.iloc[10,0]
response = model.generate_content(f"make the facts presented in this article as a character dialogue between spongebob and patrick, {article}")
print(response.text)
