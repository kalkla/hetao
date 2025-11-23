import sys
import os

# 临时添加项目路径到Python环境变量
sys.path.append(os.path.join(os.path.dirname(__file__), 'pythonProject'))

from Configdeal import get_config_value

# 测试读取配置项
appid = get_config_value('wechat_appid')
secret = get_config_value('wechat_secret')

print(f'微信APPID: {appid}')
print(f'微信APP Secret: {secret}')