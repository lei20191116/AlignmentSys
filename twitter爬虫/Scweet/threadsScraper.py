import time
from queue import Queue

import pandas as pd

from Scweet.scweet import scrape
from Scweet.user import get_user_information, get_users_following, get_users_followers
from threading import Thread


def run_time(func):
    def wrapper(*args, **kw):
        start = time.time()
        func(*args, **kw)
        end = time.time()
        print('running', end - start, 's')

    return wrapper


class Spider():
    def __init__(self):
        self.qurl = Queue()
        self.data = pd.DataFrame()
        self.thread_num = 16

    def get_info(self):
        while not self.qurl.empty():
            date = self.qurl.get()
            print('crawling from {} to {}'.format(date[0],date[1]))
            data = scrape(words=["ChainInfo","chaindotinfo"], since=date[0], until=date[1], from_account=None, interval=1,
                          headless=True, display_type="Top", save_images=False,
                          resume=False, filter_replies=True, proximity=True)
    def produce_date(self):

        datelist = []
        for y in range(2021, 2022):
            for i in range(1, 13):
                date1 = "{y}-{m}-1".format(y=y, m=i)
                date2 = "{y}-{m}-14".format(y=y, m=i)
                datelist.append(date1)
                datelist.append(date2)
        # for i in range(len(datelist)):
        #     print(i)
        #     if i != 287:
        #         self.qurl.put((datelist[i], datelist[i + 1]))

        for i in range(1, 5):
            date1 = "2022-{m}-1".format(m=i)
            date2 = "2022-{m}-14".format(m=i)
            datelist.append(date1)
            datelist.append(date2)
        for i in range(len(datelist)-1):
            print(i)
            self.qurl.put((datelist[i], datelist[i + 1]))
    @run_time
    def run(self):

        self.produce_date()
        ths = []
        for _ in range(self.thread_num):
            th = Thread(target=self.get_info)
            th.start()
            ths.append(th)
        for th in ths:
            th.join()

        print('Data crawling is finished.')


if __name__ == '__main__':
    start = time.time()
    Spider().run()
    end = time.time()
    print(end - start)

env_path = ".env"
