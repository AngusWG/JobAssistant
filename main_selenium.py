#!/usr/bin/python3
# encoding: utf-8 
# @Time    : 2018/9/21 0:09 
# @author  : zza
# @Email   : 740713651@qq.com
import re
import time

import selenium
from selenium import webdriver

import config


class LaGou():
    user_cookies = "C:\\Users\\74071\\AppData\\Local\\Google\\Chrome\\User Data"

    option = webdriver.ChromeOptions()
    option.add_argument(
        "--user-data-dir={}".format(user_cookies))  # 设置成用户自己的数据目录
    option.add_argument("--headless")
    browser = webdriver.Chrome(chrome_options=option)
    main_url = "https://www.lagou.com/zhaopin/"

    key_list = config.关键字.strip().split()
    key_matching_num = int(config.关键词匹配量)
    crawl_list = config.爬取列表.strip().split()
    want_salary_range = [i for i in range(*[int(i) for i in re.findall("(\d+)", config.期望薪资)])]

    def __init__(self):
        self.browser.get(self.main_url)

    def server(self):
        for i in self.crawl_list[:]:
            self.surf_pages(self.main_url + i)
        pass

    def __del__(self):
        # self.browser.quit()
        pass

    def surf_pages(self, target_url, page=1):
        self.browser.get(target_url + "/{}/".format(page))
        print(target_url + "/{}/".format(page))
        self.browser.implicitly_wait(15)
        elements = self.browser.find_elements_by_xpath('//*[@id="s_position_list"]/ul/li/div[1]/div[1]/div[1]/a/h3')
        main_handle = self.browser.current_window_handle
        for element in elements:
            element.click()
            self.browser.switch_to.window(self.browser.window_handles[-1])
            self.check_page()
            self.browser.close()
            self.browser.switch_to.window(main_handle)

        btn = self.browser.find_element_by_xpath('//*[contains(text(), "下一页")]')
        if btn.get_attribute("href") != 'javascript:;':
            self.surf_pages(target_url, page + 1)

    def check_page(self):
        # 工资检查
        element = self.browser.find_element_by_xpath('//span[@class="salary"]')
        text = element.text
        a = re.findall("(\d+)", text)
        salary_range = [i for i in range(*[int(i) for i in a])]
        # 元素检查
        element = self.browser.find_element_by_xpath('//*[@id="job_detail"]')
        text = element.text
        res = re.findall("|".join(self.key_list), text, flags=re.IGNORECASE)
        res = list(set([i.lower() for i in res]))
        print(self.browser.current_url, res, salary_range[0])
        if len(res) < self.key_matching_num or len(set(salary_range) & set(self.want_salary_range)) == 0:
            return
        self.send_resume()

    def send_resume(self):
        print("符合规则")
        try:
            self.browser.find_element_by_xpath('//*[contains(text(), "投个简历")]').click()
            time.sleep(1.5)
            self.browser.find_element_by_xpath('//*[contains(text(), "确认投递")]').click()
            time.sleep(1.5)
            print("已投")
            self.browser.find_element_by_xpath('//*[contains(text(), "我知道了")]').click()
        except (
                selenium.common.exceptions.NoSuchWindowException,
                selenium.common.exceptions.ElementNotVisibleException):
            # self.browser.save_screenshot(r"D:\学习用\Python\JobAssistant\a.png")
            pass
        except selenium.common.exceptions.NoSuchElementException:
            print("投过了 pass")


if __name__ == '__main__':
    # print("66666")
    LaGou().server()
