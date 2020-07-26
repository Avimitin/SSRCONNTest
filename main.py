#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# author: avimitin
# date: 2020.5.21
import subprocess
import os
import json
import wget
import zipfile


def main():
    # 测试是否有测速主程序
    try_speedtest()
    # 获取订阅链接
    sub = get_sub_link()
    # 进入测速程序目录
    os.chdir("./SSRSpeed-2.6.4")
    # print(os.getcwd())
    # ss_url = 'https://sub.O-Proxy.com/xxx'
    ssr_url = sub['SSR']
    shell = 'python3 ./main.py -M "pingonly" --exclude "官网" --exclude "如果发现" --yes -u %s' % ssr_url
    os.system(shell)


def get_sub_link():
    if not os.path.exists('config/sub_link.json'):
        print('+-----------------------------------------+')
        sub_type = input('选择你的链接类型(SSR)：').upper()
        sub_link = input('输入你的订阅链接：')
        print('+-----------------------------------------+')
        sub = {sub_type: sub_link}
        with open('config/sub_link.json', 'w+', encoding='UTF-8') as sub_file:
            json.dump(sub, sub_file)
    else:
        with open('config/sub_link.json', 'r+', encoding='UTF-8') as sub_file:
            sub = json.load(sub_file)
        print("找到订阅链接，进行下一步")
    return sub


'''
def alert():
    print('+-----------------------------------------------------------------+')
    print('您尚未安装SSRSpeed，请执行以下命令:')
    print('wget https://github.com/NyanChanMeow/SSRSpeed/archive/2.6.4.zip')
    print('unzip 2.6.4.zip')
    print('cp SSRSpeed-2.6.4 ./SSRCONNTest')
    print('+-----------------------------------------------------------------+')
'''

def try_speedtest():
    is_exist = False
    
    for file in os.listdir('./'):
        if "SSRSpeed" in file:
            is_exist = True
        else:
            pass
    
    if is_exist == False:
        print("没有找到SpeedTest，下载中...\n")
        wget.download("https://github.com/NyanChanMeow/SSRSpeed/archive/2.6.4.zip")
        print("下载完成，正在解压...\n")
        files = zipfile.ZipFile("./SSRSpeed-2.6.4.zip", "r")
        for file_name in files.namelist():
            files.extract(file_name, "./")
        files.close()
        print("解压完成，正在清理...\n")
        os.remove("./SSRSpeed-2.6.4.zip")
        modify_file()
        print("清理完成")
    else:
        print("找到SSRSpeed，进行下一步")
        return


def modify_file():
    is_exist = False
    
    with open("./SSRSpeed-2.6.4/main.py", 'r', encoding='UTF-8') as main_file:
        program = main_file.readlines()
        for line in program:
            if 'input("Press' in line:
                print("正在修改程序...")
                is_exist = True
                break
        
    if not is_exist:
        return

    with open("./SSRSpeed-2.6.4/main.py", 'w', encoding='utf-8') as new_file:
        for line in program:
            if 'input("Press' in line:
                continue
            else:
                new_file.writelines(line)
        print("修改完成")

if __name__ == '__main__':
    main()
