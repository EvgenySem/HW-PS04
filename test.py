from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


browser = webdriver.Firefox()
browser.get("")

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


if dict_main_articles:
    cnt = 1
    for el in range(len(dict_main_articles)):
        print(f"{cnt}. {dict_main_articles[cnt][0]}")
        cnt += 1

    print("Введите номер заголовка, чтобы перейти к статье или введите 'b', чтобы продолжить читать статью")
    user_input = input()
    if user_input == 'b':
        continue
    else:
        try:
            get_paragraphs(dict_main_articles[int(user_input)][1])