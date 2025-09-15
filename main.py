import sys
import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


def get_paragraphs(link):
    """Функция для перехода по ссылке, запись абзацев и ссылок на связанные статьи"""
    if link is None:
        print("Ссылка не найдена")
        return None
    elif link == "end":
        return None
    else:
        browser.get(link)

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

    return {"paragraphs": paragraphs,
            "main_articles": dict_main_articles}


def print_texts(text_dict):
    """Функция для вывода абзацев в консоль и взаимодействия с пользователем"""

    if not text_dict:
        print("Статья закончилась. Завершение программы")
        browser.quit()
        sys.exit()

    paragraphs = text_dict.get("paragraphs")
    dict_main_articles = text_dict.get("main_articles")

    if not paragraphs:
        print("Не удалось получить текст стати")
        return None

    for paragraph in paragraphs:
        print(paragraph.text + "\n----------------------------")
        print("Чтобы читать дальше, нажмите 'enter'")
        print("Чтобы посмотреть список связанных статей, введите 'm'")
        print("Для выхода из программы введите 'q'\n----------------------------")

        user_input = input()
        if user_input == "q":
            browser.quit()
            sys.exit()
        elif user_input == "m":
            if dict_main_articles:
                cnt = 1
                for _ in range(len(dict_main_articles)):
                    print(f"{cnt}. {dict_main_articles[cnt][0]}")
                    cnt += 1

                print("Введите номер заголовка, чтобы перейти к статье или введите 'b', чтобы продолжить читать статью")
                user_input = input()
                if user_input == 'b':
                    continue
                else:
                    try:
                        link = dict_main_articles[int(user_input)][1]
                        return link
                    except:
                        print("Что-то пошло не так! Вернулись к статье\n")
                        continue
            else:
                print("В данное статье нет связанных статей. Продолжение основной статьи:\n")
                continue
        else:
            continue

    return "end"


browser = webdriver.Firefox()
browser.get("https://ru.wikipedia.org/wiki/Заглавная_страница")

search_box = browser.find_element(By.ID, "searchInput")
search_box.send_keys(input("Введите текст поискового запроса в Википедии: "))
search_box.send_keys(Keys.RETURN)

# Ожидаем загрузку страницы
new_url = cur_url = browser.current_url
while cur_url == new_url:
    new_url = browser.current_url

time.sleep(3)

# Поиск превью статей по запросу
articles = []
search_results = browser.find_elements(By.TAG_NAME, "li")
for elem in search_results:
    class_elem = elem.get_attribute("class")
    if class_elem == "mw-search-result mw-search-result-ns-0 searchresult-with-quickview":
        articles.append(elem)

# Перебор статей и выбор одной
if not articles:
    print("Не удалось найти статьи по запросу")
else:
    run = True
    while run:
        for article in articles:
            print(article.text + "\n----------------------------")
            print("Чтобы листать дальше, введите 'n'\n"
                  "Для выбора этой статьи введите 'enter'\n"
                  "Для выхода из программы введите 'q'\n----------------------------")
            user_input = input()
            if user_input == "n":
                continue
            elif user_input == "q":
                browser.quit()
                sys.exit()
            else:
                link = article.find_element(By.TAG_NAME, "a").get_attribute("href")
                run = False
                break


while True:
    try:
        content = get_paragraphs(link)
        link = print_texts(content)
    except SystemExit:
        sys.exit()
    except:
        print("Что-то пошло не так и страница не обработалась")
        browser.quit()
        break

