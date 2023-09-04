"""
@Name:get_url.py
@Auth:89703 
@Date:2023/9/4
"""
import re
from time import sleep

import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By


class GetID:

    def get_cookie(self):
        # 获取牛客网的cookie，并保存为yaml文件
        options = webdriver.ChromeOptions()
        options.debugger_address = '127.0.0.1:9222'
        driver = webdriver.Chrome(options=options)
        file = open('cookies.yaml', 'w', encoding="utf-8")
        yaml.dump(driver.get_cookies(), file)
        file.close()

    def load_cookie(self):
        # 加载cookie
        return yaml.safe_load(open('cookies.yaml', encoding='utf-8'))

    def get_id(self):
        # 获取各个试题的访问url
        driver = webdriver.Chrome()
        driver.maximize_window()
        # 访问测试题的搜索结果页面
        driver.get('https://www.nowcoder.com/exam/company?currentTab=recommand&jobId=100&keyword=%E6%B5%8B%E8%AF%95&selectStatus=0')

        sleep(3)
        # 使用cookie登录
        for coookie in self.load_cookie():
            driver.add_cookie(coookie)
        sleep(5)
        # 刷新页面
        driver.refresh()
        sleep(5)
        # 进行滑动，使面试题全部加载完成
        driver.execute_script("window.scrollBy(0,10000)")
        sleep(5)
        driver.execute_script("window.scrollBy(0,10000)")
        sleep(5)
        driver.execute_script("window.scrollBy(0,10000)")
        sleep(5)
        driver.execute_script("window.scrollBy(0,10000)")
        sleep(5)
        url_list = []
        # 通过定位获取全部试题的'href'内容，组装成url
        ele_list = driver.find_elements(By.XPATH, '//*[@id="paperContent"]/div/div/div/a')
        for ele in ele_list:
            text = ele.get_attribute('href')

            url_list.append(text)
        print(url_list)
        # 关闭driver，回收资源
        driver.close()
        return url_list

    def get_url(self):
        # 将上述方法获取到的url，通过浏览器打开，获得我们实际需要的url，并取出testid和paperid，便于后续操作
        url_list = self.get_id()
        # 重新打开浏览器
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get('https://www.nowcoder.com/')
        # 重新登录牛客网
        for cookie in self.load_cookie():
            driver.add_cookie(cookie)
        sleep(3)
        driver.refresh()
        # for 循环遍历url_list
        for url in url_list:
            # 访问href生成的网址
            driver.get(url)

            sleep(2)
            # 获取我们真正需要的网址
            url_end = driver.current_url
            # 使用正则将testid和paperid提取出来
            match_exam_id = re.search(r'/(\d+)/detail\?pid=(\d+)', url_end)
            exam_id = match_exam_id.group(1)
            pid = match_exam_id.group(2)
            # 将testid和paperid组合成字典，并写入id.yaml
            dict = {
                exam_id: pid
            }
            with open('id.yaml', 'a', encoding='utf-8') as f:
                yaml.safe_dump(dict, f)
                # f.write(url_end)

if __name__ == '__main__':
    GetID().get_url()

