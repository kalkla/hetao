import sys
import os

# 确保能导入Configdeal
from Configdeal import get_config_value

# 测试读取配置项
print("当前工作目录:", os.getcwd())
appid = get_config_value('wechat_appid')
secret = get_config_value('wechat_secret')

print(f'微信APPID: {appid}')
print(f'微信APP Secret: {secret}')