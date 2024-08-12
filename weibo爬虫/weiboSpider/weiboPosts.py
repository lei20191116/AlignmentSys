import re
import sys
import time
import json
import traceback

import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from weiboSpider.get_cookie import get_cookie


class GetWeiboPosts:
    browser_options = Options()
    browser_options.add_argument('--disable-gpu')
    browser_options.add_argument("--headless")

    def __init__(self):

        self.user_id_list = []
        self.user_posts = {}

    def scraping(self, UID):
        # 爬取单个User的微博动态时间
        users_posts_info = {}
        postsTimes = []
        print("浏览器已成功创建。")
        user_a_lists = []
        selector = self.deal_html("https://weibo.cn/u/{}?filter=1".format(UID))
        if not selector.xpath('//span[@class="ct"]'):
            print("nothing")
        else:
            user_a_lists = selector.xpath('//span[@class="ct"]/text()')


        for uaer_a in user_a_lists:
            match = re.search(r"(.+?)来自", uaer_a)
            if match:
                datetime_str = match.group(1)

                if re.search(r"(\d{2}月\d{2}日 \d{2}:\d{2})", datetime_str):
                    date_str = datetime_str.strip()
                    # 提取月份、日期和时间
                    month = date_str[:2]
                    day = date_str[3:5]
                    time = date_str[6:]
                    datetime_str = "2023-{}-{} {}".format(month, day, time)
                # time_content = match.group(1)
                postsTimes.append(datetime_str)
                print(datetime_str)
        users_posts_info[UID] = postsTimes
        # self.userPosts(users_posts_info)
        return users_posts_info

    def deal_html(self, url):
        """处理html"""
        try:
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
            headers = {
                'User_Agent': user_agent,
                'Cookie': "_T_WM=200718b690ce5368351fea4b20846ac2; SCF=AujJP-0jBMKic1zJAhHoPtoc-JpI8TsiTpTg04MU_h12lxQhf0SfCQuryAa8lkZSQq2DBfTZ2pQ_G3Wrk6eODRc.; SUB=_2A25IObyPDeRhGeFI61YQ9C7JzT6IHXVrxcTHrDV6PUJbktAGLVDZkW1NfXoyKRiEZi81GytzLgq5rD9lDI0D-ki7; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Whn_lUNQ4qbcIhn4-p.DvaN5JpX5K-hUgL.FoMcehBpSh5fSoz2dJLoI7D4qPLDwgYpeoec; SSOLoginState=1698548960; ALF=1701140960"}
            html = requests.get(url, headers=headers).content
            selector = etree.HTML(html)
            return selector
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    def userPosts(self, users_posts_info):
        with open('UserPosts/userPostsInformation.json', 'w') as f:
            f.seek(0, 2)  # 将文件指针移动到文件末尾
            json.dump(users_posts_info, f)
        # 补充一下将爬取到的用户ID和时间整理成和Twitter同样的格式
        return

    def getUserName(self, file_name):
        # 先找一下有没有UID的大量数据，如果有就直接用，如果没有就自己获取下，转为List[UID1，UID2,。。。]格式，
        self.user_id_list = []
        with open(file_name, 'rb') as f:
            try:
                lines = f.read().splitlines()
                lines = [line.decode('utf-8-sig') for line in lines]
            except UnicodeDecodeError:
                sys.exit(u'%s文件应为utf-8编码，请先将文件编码转为utf-8再运行程序' % file_name)
            for line in lines:
                info = line.split(' ')
                if len(info) > 0 and info[0].isdigit():
                    user_id = info[0]
                    if user_id not in self.user_id_list:
                        self.user_id_list.append(user_id)

    def dynamicUser(self, current_index, final_index):

        with open('UserPosts/userName.json', 'r') as file:
            data = json.load(file)
        while current_index < final_index:
            end_index = min(current_index + 10, len(data))
            users_batch = data[current_index:end_index]
            print("current_index:----------", current_index)
            for u in users_batch:
                users_posts_info = self.scraping(u)
                print(users_posts_info)

                with open('UserPosts/userPostsInformation{}-{}.json'.format(current_index,u), 'w') as f:
                    print("read")
                    f.seek(0, 2)  # 将文件指针移动到文件末尾
                    json.dump(users_posts_info, f)
            current_index += 10

    def main(self, current_index, final_index):
        self.dynamicUser(current_index, final_index)


if __name__ == '__main__':
    gt = GetWeiboPosts()
    current_index = 1
    final_index = 21
    gt.main(current_index, final_index)
