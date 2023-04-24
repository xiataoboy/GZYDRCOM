# # 导入ping模块
# import platform
# import subprocess
#
# # ping测试函数
# def ping(host):
#     """
#     Return True if host (str) responds to a ping request.
#     """
#     # 根据不同操作系统，组装ping命令
#     param = '-n' if platform.system().lower() == 'windows' else '-c'
#     # 定义ping命令
#     command = ['ping', param, '1', host]
#     try:
#         # 执行ping命令
#         output = subprocess.check_output(command, timeout=5)
#         # 打印结果
#         print(f'{host} 能上网')
#         exit()
#         return True
#     except subprocess.TimeoutExpired:
#         # 超时说明不能上网
#         print(f'{host} 不能上网')
#         return False
#     except Exception as e:
#         # 其他异常说明不能上网
#         print(f'ping测试出错：{e}')
#         return False
#
# # 测试能否上网
# if ping('www.baidu.com'):
#     print('此电脑已经联网，程序结束运行')
# else:
#     print('此电脑未联网，开始运行赣职院(教学楼)Drcom登陆脚本')
#

import requests
import configparser
import os
import base64
from time import sleep
import logging

print('--------------------------------------------------------------------')
print('                        赣职院(教学楼)Drcom登陆脚本                              ')
print('                      -= By 小涛——XiaoTao出品 =-')
print('                         QQ： 3205584606                                ')
print('                      〓作者博客：www.xt6a.com〓                     ')
print('--------------------------------------------------------------------')
print('\n' * 1)

log_file = 'drcom.log'
logging.basicConfig(filename=log_file, level=logging.INFO,
format='认证时间：%(asctime)s - 返回结果：%(message)s')
# 读取账号密码
cfg = configparser.ConfigParser()
# 判断配置文件是否存在
if os.path.isfile("config.ini"):
    # 当文件存在时，读取账号密码
    cfg.read("config.ini")
    if cfg.has_section('GZY_DRCOM'):  # 判断是否有对应的GZY_DRCOM
        user_account = cfg.get('GZY_DRCOM', 'user_account')
        user_password_encrypted = cfg.get('GZY_DRCOM', 'user_password_encrypted')
        user_password = base64.b64decode(user_password_encrypted).decode('utf-8')
    else:
        # 当'GZY_DRCOM' GZY_DRCOM不存在时，提示文件不完整，并结束程序
        print("当前配置文件不完整，请尝试删除目录下的config.ini文件后重试")
        sleep(3)
        exit()
else:
    # 当文件不存在时，要求用户输入账号密码
    user_account = input("请输入您的账号：")
    user_password = input("输入您的密码：")
    print("密码已自动加密")
    # 加密密码
    user_password_encrypted = base64.b64encode(user_password.encode('utf-8')).decode('utf-8')
    # 将账号密码写入配置文件
    cfg['GZY_DRCOM'] = {
        'user_account': user_account,
        'user_password_encrypted': user_password_encrypted
    }
    # 保存配置文件
    with open('config.ini', 'w') as configfile:
        cfg.write(configfile)

# 请求接口
url = 'http://192.168.100.2:801/eportal/portal/login'
params = {
    'callback': 'dr1003',
    'login_method': 1,
    'user_account': user_account,
    'user_password': user_password
}

response = requests.get(url, params=params)

# 写入日志
if response.status_code == 200:
    logging.info({response.text})
else:
    logging.error(f'{user_account} 登陆失败，无法访问到该页面！')

# 输出页面返回页面的内容
print("页面返回结果：")
print(response.text)

# 保留控制台3秒再关闭
sleep(3)