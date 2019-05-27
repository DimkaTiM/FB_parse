import Pa
import sys
import time
import random
import base64
import requests
import selenium
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def main(FB):
    link = "https://www.facebook.com/{}".format(FB)
    opts = Options()
    opts.add_argument("user-agent=" + random.choice(Pa.usr_agents))
    opts.add_argument("--disable-notifications")
    driver = webdriver.Chrome(executable_path="chromedriver")# export PATH=$PATH:/home/timoxinda/
     #ChromeDriverManager().install())
    print(opts, driver)

    username = "login"
    password = str(Pa.password())

    driver.get('https://www.facebook.com/')
    UN = driver.find_element_by_id('email')
    UN.send_keys(username)
    PS = driver.find_element_by_id('pass')
    PS.send_keys(password)
    LI = driver.find_element_by_id('loginbutton')
    LI.click()
    driver.get(link)

    print(" - " * 1000)

    for i in range(0):
        SCROLL_PAUSE_TIME = 0.5
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    con = driver.page_source
    soup = BeautifulSoup(con, "html.parser")
    print(soup)
    print("--" * 100)
    #parametrs

    data = {"name":"", # Имя
            "from":"", # родной город
            "town":"", # город проживания
            "work":"", # работа
            "edu" :"", # образование
            "sub" :"", # пописчики
            "love":"", # любовь
          "Joined":"", # присоединился с
            "flag":""  # флаг
    }
    # атрибут тега
    id_tag = {"from":"sp_PcNl_Pzo88k sx_0b2fa6",
              "town":"sp_PcNl_Pzo88k sx_adab17",
              "work":"sp_PcNl_Pzo88k sx_15b8d3",
              "edu" :"sp_PcNl_Pzo88k sx_edc6b1",
              "sub" :"sp_PcNl_Pzo88k sx_92cb95",
              "love":"sp_PcNl_Pzo88k sx_86a8ae",
            "Joined":"sp_PcNl_Pzo88k sx_5a6fbb"
    }

    data["name"] = soup.find("a", {"class": "_2nlw _2nlv"}).get_text() #имя пользователя
    try:
        data["flag"] = str(soup.find("div", {"id": "owned_pages_container_id"}).get_text()) # флажок в профиле
    except:
        pass
    soup = soup.find_all("li", {"class": "_1zw6 _md0 _5h-n _5vb9"})

    # прохожусь по каждому типу, который я до этого не получил
    for num, key in enumerate(id_tag):
        for i in soup:
            try:
                if i.find("i", {"class": "_3-90 _8o _8s lfloat _ohe img " + id_tag[key]}):
                    data[key] += "* " + i.find("div", {"class": "_50f3"}).get_text()
            except:
                pass
    # все принтую
    for num, key in enumerate(data):
        if data[key] != "":
            print(key + "     " + data[key])
        else:
            print(key + "   " + "Null")

if __name__ == "__main__":
    a = datetime.datetime.now()
    link = sys.argv[1]
    main(link)
    print()
    print(datetime.datetime.now() - a)
