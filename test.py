import sys
import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


browser = webdriver.Firefox()
browser.get("https://ru.wikipedia.org/wiki/C%2B%2B")

paragraphs = browser.find_elements(By.TAG_NAME, "p")
main_articles = browser.find_elements(By.TAG_NAME, "div")


dict_main_articles = {} # {num: [title, link]}
cnt = 1
for m_article in main_articles:
    class_elem = m_article.get_attribute("class")
    if class_elem == "hatnote navigation-not-searchable ts-main":
        title = m_article.find_element(By.TAG_NAME, "a").text
        link = m_article.find_element(By.TAG_NAME, "a").get_attribute("href")
        dict_main_articles[cnt] = [title, link]
        cnt += 1

print(dict_main_articles)