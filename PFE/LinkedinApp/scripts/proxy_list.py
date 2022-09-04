import requests
from bs4 import BeautifulSoup
from random import choice
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

def get_proxies():
    proxieslist = []
    while len(proxieslist) != 1:
        url = "https://www.sslproxies.org/"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        PROXY = choice(list(map(lambda x: x[0] + ':' + x[1], list(
            zip(map(lambda x: x.text, soup.find_all('td')[::8]), map(lambda x: x.text, soup.find_all('td')[1::8]))))))

        print("checking proxy")
        driver_options = webdriver.ChromeOptions()
        driver_options.add_argument('--proxy-server=%s' % PROXY)

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=driver_options)
        print("trying :",PROXY)
        try:
            driver.get("http://www.guimp.com")
            print("Working proxy was found :", PROXY)
            proxieslist.append(PROXY)
            driver.close()
        except WebDriverException:
            print("Retrying...")
            driver.close()

        print(proxieslist)
    return proxieslist