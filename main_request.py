from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pprint import pprint
import urllib.parse

source_text="Something happening in the dark outside"
url1="https://www.deepl.com/translator#en/hu/"+urllib.parse.quote(source_text)
session=HTMLSession()

"""Returns all form tags found on a web page's `url` """
# GET request
print(url1)
res = session.get(url1)
# for javascript driven website
res.html.render(sleep=1)
translated=res.html.find(".lmt__target_textarea", first=False)
pprint(translated[0])

# soup = BeautifulSoup(res.html.html, "html.parser")
# #pprint(soup.find_all("form"))
# file = open("out.html", "w")
# file.write(res.text)
# file.close()
