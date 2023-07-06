from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import spacy
import time
from fastapi import FastAPI
import uvicorn

app=FastAPI()

@app.get("/")
def get_hun_sum(youtubelink: str=None):
  output=""
  hun_sum=""
  if youtubelink is None:
    output={"Example":"GET youtubelink"}
  else:
    hun_sum=  yt_summary_hun(youtubelink)
    if (hun_sum == "") :
        output="There is no Youtube narration"
    output={"Hungarian summary": hun_sum}
  return output

def open_driver():
  # Not showing the browser itself, this is the HEADLESS mode
  global driver
  options = webdriver.ChromeOptions()
  options.add_argument('--headless')
  options.add_argument('--disable-gpu')
  driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
  driver.implicitly_wait(5)

def TranslateText_EN_HU(source_text):
  driver.get("https://www.deepl.com/translator#en/hu/"+source_text)

  # Target textarea hidden, make it visible
  translated=driver.find_element(By.CLASS_NAME,"lmt__target_textarea")
  driver.execute_script("arguments[0].style.visibility = 'visible'",translated)

  try:
    WebDriverWait(driver, 15).until(
      lambda driver: driver.find_element(By.CLASS_NAME,"lmt__target_textarea").text.strip() != ''
      # lambda driver: driver.find_element(By.CLASS_NAME,"(//div[@class='lmt__textarea lmt__textarea_dummydiv'])[2]").text.strip() != ''
    )
  except:
    pass

  #Get translation
  target_text=driver.find_elements(By.CLASS_NAME,"lmt__textarea")[1].text
  # target_text=driver.find_element(By.XPATH,"(//div[@class='lmt__textarea lmt__textarea_dummydiv'])[2]").text
  return target_text

# python3 -m spacy download en_core_web_sm

def full_text_translate(fulltext):
  nlp=spacy.load("en_core_web_sm")
  doc = nlp(fulltext.replace("\n\n","\n"))
  sentences=list(doc.sents)

  output_text=''

  for sentence in sentences:
    translated=TranslateText_EN_HU(sentence.text)
    output_text+= translated
  
  return output_text

def close_driver():
  driver.close()

def yt_summary_hun(yt_link):
    if not yt_link:
        return "Invalid YouTube link" 
    
    open_driver()
    try:
        yt_link = yt_link[8:]
        driver.get(f"https://summarize.tech/{yt_link}")
        summary = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div/section/p')
        summary_hun = full_text_translate(summary.text)
        return summary_hun
    finally:
        close_driver()

# print(yt_summary_hun("https://youtu.be/eedaafutru4"))
