#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# author: avimitin
# date: 2020.5.21
import subprocess
import os
from apscheduler.schedulers.background import BlockingScheduler
import json


sub = None


def main():
    global sub
    if not os.path.exists('sub_link.json'):
        print('+-----------------------------------------+')
        sub_type = input('选择你的链接类型(SSR)：').upper()
        sub_link = input('输入你的订阅链接：')
        print('+-----------------------------------------+')
        sub = {sub_type: sub_link}
        with open('sub_link.json', 'w+', encoding='UTF-8') as sub_file:
            json.dump(sub, sub_file)
    else:
        with open('sub_link.json', 'r+', encoding='UTF-8') as sub_file:
            sub = json.load(sub_file)


def test():
    if 'venv' in str(os.getcwd()):
        os.chdir('../SSRSpeed-2.6.4')
    else:
        os.chdir('./SSRSpeed-2.6.4')
    # ss_url = 'https://sub.O-Proxy.com/xxx'
    ssr_url = sub['SSR']
    shell = r'python3 ./main.py -M "pingonly" --exclude "官网" --exclude "如果发现" --yes -u %s' % ssr_url
    subprocess.run(shell, shell=True)


if __name__ == '__main__':
    main()
    scheduler = BlockingScheduler()
    scheduler.add_job(test, 'interval', hours=3)
    print('+-------------------------+')
    print(' Program Start Schduling Now ')
    print('+-------------------------+')
    scheduler.start()
    
