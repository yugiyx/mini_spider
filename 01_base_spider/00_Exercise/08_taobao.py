from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
wait = WebDriverWait(browser, 10)
url = 'https://www.jd.com/'
key_words = 'python'


def index_page(page):

    print('正在爬取第', page, '页')
    try:
        browser.get(url)
        input = wait.until(EC.presence_of_element_located((By.ID, 'key')))
        submit = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#search > div > div.form > button')))
        input.send_keys(key_words)
        submit.click()
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR,
                '#J_bottomPage > span.p-skip > em:nth-child(1) > b')))
    finally:
        browser.close()


def main():
    index_page(1)


if __name__ == '__main__':
    main()
