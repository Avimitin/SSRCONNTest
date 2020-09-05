#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# author: avimitin
# date: 2020.5.21
import sys
import os
import json
import wget
import zipfile
import platform


class OPT:
    def __init__(self,
                 paolu=False,
                 debug=False,
                 test_method=None,
                 test_mode=None,
                 confirmation=True,
                 result_color=None,
                 import_file=False,
                 guiConfig=None,
                 url=None,
                 filter=None,
                 group=None,
                 remarks=None,
                 efliter=None,
                 egfilter=None,
                 erfilter=None,
                 sort_method=None,
                 group_override=None,
                 use_ssr_CSharp=False,
                 skip_requirements_check=True
                 ):
        self.paolu = paolu
        self.debug = debug
        self.test_method = test_method
        self.test_mode = test_mode
        self.confirmation = confirmation
        self.result_color = result_color
        self.import_file = import_file
        self.guiConfig = guiConfig
        self.url = url
        self.filter = filter
        self.group = group
        self.remarks = remarks
        self.efliter = efliter
        self.egfilter = egfilter
        self.erfilter = erfilter
        self.sort_method = sort_method
        self.group_override = group_override
        self.use_ssr_cs = use_ssr_CSharp
        self.skip_requirements_check = skip_requirements_check


def main():
    if "Linux" not in platform.platform():
        print("暂时不支持除了 Linux 以外的平台")
        return 
    # 测试是否有测速主程序
    try_speedtest()
    # 获取订阅链接
    sub = get_sub_link()
    ssr_url = sub['SSR']

    '''
    # 进入测速程序目录 
    # print(os.getcwd())
    # ss_url = 'https://sub.O-Proxy.com/xxx'
    shell = 'python ./main.py -M "pingonly" --exclude "官网" --exclude "如果发现" --yes -u %s' % ssr_url
    os.system(shell)
    '''

    opt = OPT(test_mode="pingonly", egfilter=["官网", "如果发现"], confirmation=True, url=ssr_url)

    sys.path.append(os.getcwd()+r"/SSRSpeed")
    os.chdir("SSRSpeed")

    from SSRSpeed import main
    main.start(opt)


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

    with open("SSRSpeed/main.py", 'r', encoding='UTF-8') as main_file:
        program = main_file.readlines()
        for line in program:
            if 'input("Press' in line:
                print("正在修改程序...")
                is_exist = True
                break

    if not is_exist:
        return

    with open("SSRSpeed/main.py", 'w', encoding='utf-8') as new_file:
        for line in program:
            if 'input("Press' in line:
                continue
            else:
                new_file.writelines(line)
        print("修改完成")


if __name__ == '__main__':
    main()
