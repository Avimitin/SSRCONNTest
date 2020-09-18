#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# author: avimitin
# date: 2020.5.21
import sys
import os
import json
import zipfile
import platform
import time
from bin.options import OPT


def main(name,
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
         skip_requirements_check=True,
         platform_confirm=True):

    if platform_confirm and "Linux" not in platform.platform():
        print("暂时不支持除了 Linux 以外的平台")
        return

    # 测试是否有测速主程序
    find_speed_test()

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

    opt = OPT(name, paolu, debug, test_method, test_mode, confirmation, result_color, import_file, guiConfig,
              url, filter, group, remarks, efliter, egfilter, erfilter, sort_method, group_override, use_ssr_CSharp, skip_requirements_check)

    sys.path.append(os.getcwd()+r"\SSRSpeed")
    os.chdir("SSRSpeed")

    from bin.SSRSpeed import main
    filename, pTime = main.start(opt)
    unixTime = int(time.mktime(time.strptime(pTime, "%Y-%m-%d-%H-%M-%S")))

    sys.path.append(os.getcwd()+r"\web")
    import utils.database.ResultHandler as Result
    r = Result.ResultHandler()
    r.add_new_result(opt.name, filename, unixTime)
    result = r.get_result_by_keyword(time=unixTime)
    return result


def get_sub_link():
    if not os.path.exists('configs/sub_link.json'):
        print('+-----------------------------------------+')
        sub_type = input('选择你的链接类型(SSR)：').upper()
        sub_link = input('输入你的订阅链接：')
        print('+-----------------------------------------+')
        sub = {sub_type: sub_link}
        with open('configs/sub_link.json', 'w+', encoding='UTF-8') as sub_file:
            json.dump(sub, sub_file)
    else:
        with open('configs/sub_link.json', 'r+', encoding='UTF-8') as sub_file:
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


def find_speed_test():
    is_exist = False

    for file in os.listdir('./'):
        if "SSRSpeed" in file:
            is_exist = True
        else:
            pass

    if not is_exist:
        print("没有找到SpeedTest，解压中...\n")
        files = zipfile.ZipFile("resource/SSRSpeed.zip", "r")
        for file_name in files.namelist():
            files.extract(file_name, "./")
        files.close()
        print("解压完成")
    else:
        print("找到SSRSpeed，进行下一步")
        return


'''
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
'''

if __name__ == '__main__':
    main(name="OxygenProxy", test_mode="pingonly", egfilter=["官网", "如果发现"], filter=["深港专线01"], confirmation=True, url="https://sub.o-proxy.info/o/FccSbmDQvkIIFSeF?sub=1", platform_confirm=False)
