#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# author: avimitin
# date: 2020.5.21
import subprocess
import os
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

    if 'venv' in str(os.getcwd()):
        try:
            os.chdir('../SSRSpeed-2.6.4')
        except FileNotFoundError:
            print('+-----------------------------------------------------------------+')
            print('您尚未安装SSRSpeed，请执行以下命令:')
            print('wget https://github.com/NyanChanMeow/SSRSpeed/archive/2.6.4.zip')
            print('unzip 2.6.4.zip')
            print('cp SSRSpeed-2.6.4 ./SSRCONNTest')
            print('+-----------------------------------------------------------------+')
            return
    elif str(os.getcwd()) == '/root':
        try:
            os.chdir('~/SSRCONNTest/SSRSpeed-2.6.4')
        except FileNotFoundError:
            print('+-----------------------------------------------------------------+')
            print('您尚未安装SSRSpeed，或SSRCONNTest不在根目录下,请将项目放至根目录下或执行以下命令:')
            print('wget https://github.com/NyanChanMeow/SSRSpeed/archive/2.6.4.zip')
            print('unzip 2.6.4.zip')
            print('cp SSRSpeed-2.6.4 ./SSRCONNTest')
            print('+-----------------------------------------------------------------+')
            return
    else:
        try:
            os.chdir('./SSRSpeed-2.6.4')
        except FileNotFoundError:
            print('+-----------------------------------------------------------------+')
            print('您尚未安装SSRSpeed，请执行以下命令:')
            print('wget https://github.com/NyanChanMeow/SSRSpeed/archive/2.6.4.zip')
            print('unzip 2.6.4.zip')
            print('cp SSRSpeed-2.6.4 ./SSRCONNTest')
            print('+-----------------------------------------------------------------+')
            return

    print(os.getcwd())

    with open('main.py', 'r+', encoding='UTF-8') as file:
        lines = file.readlines()
        for x in lines:
            if 'input("Press' in lines:
                with open('main.py', 'w+', encoding='UTF-8') as new_file:
                    for x in lines:
                        if 'input("Press' in lines:
                            continue
                        else:
                            file.writelines(x)
            else:
                continue


def test():
    # ss_url = 'https://sub.O-Proxy.com/xxx'
    ssr_url = sub['SSR']
    shell = r'python3 ./main.py -M "pingonly" --exclude "官网" --exclude "如果发现" --yes -u %s' % ssr_url
    subprocess.run(shell, shell=True)


if __name__ == '__main__':
    main()
    test()
    
