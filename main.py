import sys
import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


browser = webdriver.Firefox()
browser.get("https://ru.wikipedia.org/wiki/Заглавная_страница")

def user_search_input() -> list:
    """Функция для поиска всех вариантов статей по поисковому запросу пользователя"""
    search_box = browser.find_element(By.ID, "searchInput")

    search_box.send_keys(input("Введите текст поискового запроса в Википедии: "))
    search_box.send_keys(Keys.RETURN)

    # Ожидаем загрузку страницы
    new_url = cur_url = browser.current_url
    while cur_url == new_url:
        new_url = browser.current_url

    time.sleep(5)

    articles = []
    search_results = browser.find_elements(By.TAG_NAME, "li")
    for elem in search_results:
        class_elem = elem.get_attribute("class")
        if class_elem == "mw-search-result mw-search-result-ns-0 searchresult-with-quickview":
            articles.append(elem)

    print(len(articles))
    return articles


def choosing_article(articles):
    """Функция для вывода превью или параграфов статей по очереди и выбор статьи пользователем"""
    if not articles:
        return None

    while True:
        for article in articles:
            print(article.text + "\n----------------------------")
            print("Чтобы листать дальше, введите 'n'\n"
                  "Для выбора этой статьи введите 'enter'\n"
                  "Для выхода из программы введите 'q'")
            user_input = input()
            if user_input == "n":
                continue
            elif user_input == "q":
                browser.quit()
                return None
            else:
                link = article.find_element(By.TAG_NAME, "a").get_attribute("href")
                return link


def get_paragraphs(link):
    """Функция для поиска параграфов и связных статей в статье"""
    if link is None:
        print("Ссылка не найдена")
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

    for paragraph in paragraphs:
        print(paragraph.text + "\n----------------------------")
        print("Чтобы читать дальше, нажмите 'enter'")
        print("Чтобы посмотреть список связанных статей, введите 'm'")
        print("Для выхода из программы введите 'q'")

        user_input = input()
        if user_input == "q":
            browser.quit()
            sys.exit()
        elif user_input == "m":
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
                    except:
                        print("Что-то пошло не так! Вернулись к статье\n")
                        continue
            else:
                print("В данное статье нет связанных статей. Продолжение основной статьи:\n")
                continue
        else:
            continue
    return None


def main_func():
    articles = user_search_input()
    link = choosing_article(articles)
    get_paragraphs(link)


main_func()

while True:
    user_input = input("Хотите что-то снова найти? (да / нет): ")
    if user_input == "да":
        main_func()
    elif user_input == "нет":
        break

print("Программа завершена")


