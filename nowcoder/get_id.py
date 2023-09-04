"""
@Name:get_id.py
@Auth:89703 
@Date:2023/8/31
"""

# 该文件功能以及在get_url.py中实现
from time import sleep

import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By


class GetID:

    def get_cookie(self):
        options = webdriver.ChromeOptions()
        options.debugger_address = '127.0.0.1:9222'
        driver = webdriver.Chrome(options=options)
        file = open('cookies.yaml', 'w', encoding="utf-8")
        yaml.dump(driver.get_cookies(), file)
        file.close()

    def load_cookie(self):
        return yaml.safe_load(open('cookies.yaml', encoding='utf-8'))

    def get_id(self):
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get('https://www.nowcoder.com/exam/company?currentTab=recommand&jobId=100&keyword=%E6%B5%8B%E8%AF%95&selectStatus=0')

        sleep(3)
        for coookie in self.load_cookie():
            driver.add_cookie(coookie)
        sleep(5)
        driver.refresh()
        sleep(5)
        driver.execute_script("window.scrollBy(0,10000)")
        sleep(5)
        driver.execute_script("window.scrollBy(0,10000)")
        sleep(5)
        driver.execute_script("window.scrollBy(0,10000)")
        sleep(5)
        driver.execute_script("window.scrollBy(0,10000)")
        sleep(5)
        url_list = []
        ele_list = driver.find_elements(By.XPATH, '//*[@id="paperContent"]/div/div/div/a')
        for ele in ele_list:
            text = ele.get_attribute('href')

            url_list.append(text)
        print(url_list)
        driver.close()
        return url_list

    def get_url(self):
        url_list = self.get_id()
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get()
        for cookie in self.load_cookie():
            driver.add_cookie(cookie)
        sleep(3)
        driver.refresh()
        current_list = []
        for url in url_list:
            driver.get(url)
            sleep(5)
            current_url = driver.current_url
            current_list.append(current_url)
        print(current_list)




if __name__ == '__main__':

    GetID().load_cookie()

    GetID().get_url()