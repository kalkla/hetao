#!/usr/bin/env python3
"""
测试用户信息完整度修复的脚本
"""

import requests
import json

# 测试登录请求
def test_login():
    url = "http://127.0.0.1:5000/api/login"
    
    # 测试参数1：仅提供code
    test_data1 = {
        "code": "test_code_123456"
    }
    
    try:
        print("测试1：仅提供code，数据库中无用户信息")
        response = requests.post(url, json=test_data1)
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        # 检查用户信息是否完整
        if "userInfo" in result:
            user_info = result["userInfo"]
            print(f"用户信息完整性检查:")
            print(f"  - nickName: {'完整' if 'nickName' in user_info and user_info['nickName'] != '' else '缺失或空'}")
            print(f"  - avatarUrl: {'完整' if 'avatarUrl' in user_info and user_info['avatarUrl'] != '' else '缺失或空'}")
            print(f"  - openId: {'完整' if 'openId' in user_info else '缺失'}")
        print()
        
        # 测试参数2：提供code和用户信息
        test_data2 = {
            "code": "test_code_123456",
            "nickName": "测试用户",
            "avatarUrl": "http://example.com/test_avatar.png"
        }
        
        print("测试2：提供code和完整用户信息")
        response = requests.post(url, json=test_data2)
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        # 检查用户信息是否完整
        if "userInfo" in result:
            user_info = result["userInfo"]
            print(f"用户信息完整性检查:")
            print(f"  - nickName: {'完整' if 'nickName' in user_info and user_info['nickName'] != '' else '缺失或空'}")
            print(f"  - avatarUrl: {'完整' if 'avatarUrl' in user_info and user_info['avatarUrl'] != '' else '缺失或空'}")
            print(f"  - openId: {'完整' if 'openId' in user_info else '缺失'}")
        print()
        
    except Exception as e:
        print(f"测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_login()