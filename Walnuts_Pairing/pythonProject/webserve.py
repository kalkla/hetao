# -*- coding: utf-8 -*-
"""
Web服务：接收客户端传来的单个核桃的六张图片数据，
执行与桌面应用相同的完整流程，并返回结果。
"""

import os
import base64
import shutil
import sqlite3
import jwt
import datetime
import hashlib
import mimetypes
from functools import wraps
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  # 添加CORS支持
from werkzeug.utils import secure_filename
from apscheduler.schedulers.background import BackgroundScheduler

from Walnuts_Pairing.pythonProject import similar
# 导入项目中的其他模块
from imageLoad import load_images_from_folder
import similar
from getData import filter_details_by_threshold
from Configdeal import get_config_value
import Sqldeal  # 导入Sqldeal模块以复用其功能
from vector_db import VectorDB

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # 在生产环境中应该使用更安全的密钥

# 配置CORS，允许来自所有来源的请求
CORS(app, resources={r"/*": {"origins": "*"}})

# --- 配置 ---
TEMP_IMAGES_FOLDER = 'temp_images'
os.makedirs(TEMP_IMAGES_FOLDER, exist_ok=True)

# 设置上传文件夹
app.config['UPLOAD_FOLDER'] = TEMP_IMAGES_FOLDER

# 数据库路径
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'example.db')

# 初始化向量数据库
VECTOR_DB_PATH = 'vector_features.db'
vector_db = VectorDB(VECTOR_DB_PATH) if os.path.exists(VECTOR_DB_PATH) else None


# 定时清理临时图片文件夹的任务
def cleanup_temp_images():
    """清理超过30分钟的临时图片文件和目录"""
    now = datetime.datetime.now()
    cutoff = now - datetime.timedelta(minutes=30)

    if not os.path.exists(TEMP_IMAGES_FOLDER):
        return

    deleted_files = []
    errors = []

    for filename in os.listdir(TEMP_IMAGES_FOLDER):
        file_path = os.path.join(TEMP_IMAGES_FOLDER, filename)
        try:
            if os.path.isfile(file_path):
                mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                if mtime < cutoff:
                    os.remove(file_path)
                    deleted_files.append(file_path)
            elif os.path.isdir(file_path):
                mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                if mtime < cutoff:
                    shutil.rmtree(file_path)
                    deleted_files.append(file_path)
        except Exception as e:
            errors.append((file_path, str(e)))

    # 打印清理结果
    if deleted_files:
        print(f"已清理 {len(deleted_files)} 个临时文件/目录")
    if errors:
        print(f"清理过程中遇到 {len(errors)} 个错误")


# 启动定时任务调度器
scheduler = BackgroundScheduler()
scheduler.add_job(func=cleanup_temp_images, trigger="interval", minutes=5)
scheduler.start()


# 确保在应用关闭时正确关闭调度器
@app.teardown_appcontext
def shutdown_scheduler(exception=None):
    if scheduler.running:
        scheduler.shutdown()


# 确保数据目录存在
ROOT_FOLDER = 'data'
os.makedirs(ROOT_FOLDER, exist_ok=True)

G_THRESHOLD = get_config_value('G') or 0.9
YUZHI_THRESHOLD = get_config_value('yuppie') or 0.8


# JWT装饰器 (修改为与webserve2一致)
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # 添加详细的请求信息日志，帮助诊断问题
        print(f"请求路径: {request.path}")
        print(f"请求头: {dict(request.headers)}")

        # 检查Authorization头
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            print(f"Authorization头: {auth_header}")

            # 验证Bearer格式
            if not auth_header.startswith('Bearer '):
                print("Authorization头格式错误，缺少Bearer前缀")
                return jsonify({'success': False, 'message': 'Token格式错误，应为Bearer token'}), 401

            try:
                token = auth_header.split(" ")[1]
                print("成功提取token")
            except IndexError:
                print("Authorization头格式错误，无法提取token")
                return jsonify({'success': False, 'message': 'Token格式错误，Bearer后缺少token值'}), 401
        else:
            print("请求中未包含Authorization头")

        if not token:
            # 提供更详细的错误信息，指导客户端如何正确使用token
            return jsonify({
                'success': False,
                'message': '缺少访问令牌，请在请求头中添加Authorization: Bearer <token>',
                'error_code': 'AUTH_TOKEN_MISSING'
            }), 401

        try:
            print("尝试解码token...")
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['sub']  # 修改为与webserve2一致，使用'sub'而不是'open_id'
            print(f"Token解码成功，用户: {current_user}")
        except jwt.ExpiredSignatureError:
            print("Token已过期")
            return jsonify({
                'success': False,
                'message': '令牌已过期，请重新登录获取新token',
                'error_code': 'TOKEN_EXPIRED'
            }), 401
        except jwt.InvalidTokenError as e:
            print(f"Token无效: {str(e)}")
            return jsonify({
                'success': False,
                'message': '无效令牌，请检查token是否正确',
                'error_code': 'INVALID_TOKEN'
            }), 401
        except Exception as e:
            print(f"Token处理过程中发生错误: {str(e)}")
            return jsonify({
                'success': False,
                'message': '令牌验证失败',
                'error_code': 'TOKEN_VERIFICATION_FAILED'
            }), 401

        return f(current_user, *args, **kwargs)

    return decorated


def save_images_to_temp_folder(images_data, walnut_id):
    """
    将图片数据保存到临时文件夹 (修改为与webserve2一致)
    images_data: 可以是Base64编码的图片数据数组或fileId数组，或包含base64_data/fileId的字典数组
    """
    temp_folder = os.path.join(TEMP_IMAGES_FOLDER, walnut_id)
    os.makedirs(temp_folder, exist_ok=True)

    for i, img_data in enumerate(images_data):
        try:
            # 处理字典类型的图片数据
            if isinstance(img_data, dict):
                # 优先使用base64_data字段
                if 'base64_data' in img_data:
                    base64_str = img_data['base64_data']
                    # Base64编码格式
                    # 检查是否包含MIME类型头（如：data:image/jpeg;base64,）
                    if ',' in base64_str:
                        header, img_data_part = base64_str.split(',', 1)
                        # 提取MIME类型
                        mime_type = header.split(';')[0].split(':')[1]
                        guessed_ext = mimetypes.guess_extension(mime_type)
                        ext = guessed_ext if guessed_ext else '.png'
                    else:
                        # 没有MIME类型头，使用默认扩展名
                        ext = '.png'
                        img_data_part = base64_str

                    img_bytes = base64.b64decode(img_data_part)
                    # 获取时间戳部分（walnut_id格式：YYYYMMDDHHMMSS_编号_尺寸）
                    timestamp_part = walnut_id.split('_')[0]
                    filename = f"{timestamp_part}_{i + 1}{ext}"
                    filepath = os.path.join(temp_folder, filename)
                    with open(filepath, 'wb') as f:
                        f.write(img_bytes)
                # 其次使用fileId字段
                elif 'fileId' in img_data:
                    file_id = img_data['fileId']
                    # 检查是否是fileId格式（包含upload_前缀）
                    if isinstance(file_id, str) and file_id.startswith('upload_'):
                        # fileId格式：upload_timestamp_randomhex_filename
                        import glob
                        search_pattern = os.path.join(TEMP_IMAGES_FOLDER, '**', f"{file_id}*")
                        image_files = glob.glob(search_pattern, recursive=True)
                        if image_files:
                            # 复制文件到临时目录并使用新命名规则
                            src_path = image_files[0]
                            # 获取时间戳部分（walnut_id格式：YYYYMMDDHHMMSS_编号_尺寸）
                            timestamp_part = walnut_id.split('_')[0]
                            # 从原始文件路径中提取扩展名
                            _, src_ext = os.path.splitext(src_path)
                            filename = f"{timestamp_part}_{i + 1}{src_ext}"
                            dst_path = os.path.join(temp_folder, filename)
                            import shutil
                            shutil.copy(src_path, dst_path)
                            # 删除原始上传的文件
                            os.remove(src_path)
            # 保持原有的字符串类型处理
            elif isinstance(img_data, str):
                # 检查是否是fileId格式（包含upload_前缀）
                if img_data.startswith('upload_'):
                    # fileId格式：upload_timestamp_randomhex_filename
                    import glob
                    search_pattern = os.path.join(TEMP_IMAGES_FOLDER, '**', f"{img_data}*")
                    image_files = glob.glob(search_pattern, recursive=True)
                    if image_files:
                        # 复制文件到临时目录并使用新命名规则
                        src_path = image_files[0]
                        # 获取时间戳部分（walnut_id格式：YYYYMMDDHHMMSS_编号_尺寸）
                        timestamp_part = walnut_id.split('_')[0]
                        # 从原始文件路径中提取扩展名
                        _, src_ext = os.path.splitext(src_path)
                        filename = f"{timestamp_part}_{i + 1}{src_ext}"
                        dst_path = os.path.join(temp_folder, filename)
                        import shutil
                        shutil.copy(src_path, dst_path)
                        # 删除原始上传的文件
                        os.remove(src_path)
                else:
                    # Base64编码格式
                    # 检查是否包含MIME类型头（如：data:image/jpeg;base64,）
                    if ',' in img_data:
                        header, img_data_part = img_data.split(',', 1)
                        # 提取MIME类型
                        mime_type = header.split(';')[0].split(':')[1]
                        guessed_ext = mimetypes.guess_extension(mime_type)
                        ext = guessed_ext if guessed_ext else '.png'
                    else:
                        # 没有MIME类型头，使用默认扩展名
                        ext = '.png'
                        img_data_part = img_data

                    img_bytes = base64.b64decode(img_data_part)
                    # 获取时间戳部分（walnut_id格式：YYYYMMDDHHMMSS_编号_尺寸）
                    timestamp_part = walnut_id.split('_')[0]
                    filename = f"{timestamp_part}_{i + 1}{ext}"
                    filepath = os.path.join(temp_folder, filename)
                    with open(filepath, 'wb') as f:
                        f.write(img_bytes)
        except Exception as e:
            print(f"保存图片 {i} 时出错: {e}")
    return temp_folder


def init_database():
    """
    初始化数据库，确保所有必要的表存在
    """
    try:
        # 使用绝对路径确保正确的文件位置
        absolute_db_path = os.path.abspath(DATABASE_PATH)
        print(f"尝试连接数据库: {absolute_db_path}")

        # 确保数据库文件的目录存在
        db_dir = os.path.dirname(absolute_db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            print(f"创建数据库目录: {db_dir}")

        # 连接数据库
        conn = sqlite3.connect(absolute_db_path)
        print("数据库连接成功")

        c = conn.cursor()
        # 创建users表（如果不存在）
        c.execute('''
                  CREATE TABLE IF NOT EXISTS users
                  (
                      id
                      INTEGER
                      PRIMARY
                      KEY
                      AUTOINCREMENT,
                      open_id
                      TEXT
                      UNIQUE
                      NOT
                      NULL,
                      nick_name
                      TEXT,
                      avatar_url
                      TEXT,
                      created_at
                      TIMESTAMP
                      DEFAULT
                      CURRENT_TIMESTAMP,
                      updated_at
                      TIMESTAMP
                      DEFAULT
                      CURRENT_TIMESTAMP
                  )
                  ''')

        # 创建walnut_selection表（如果不存在）
        c.execute('''
                  CREATE TABLE IF NOT EXISTS walnut_selection
                  (
                      id
                      INTEGER
                      PRIMARY
                      KEY
                      AUTOINCREMENT,
                      walnut_name
                      TEXT
                      UNIQUE
                      NOT
                      NULL,
                      selected
                      BOOLEAN
                      DEFAULT
                      False,
                      over
                      BOOLEAN
                      DEFAULT
                      False,
                      created_at
                      TIMESTAMP
                      DEFAULT
                      CURRENT_TIMESTAMP,
                      updated_at
                      TIMESTAMP
                      DEFAULT
                      CURRENT_TIMESTAMP
                  )
                  ''')

        conn.commit()
        print("所有数据库表创建成功")
        conn.close()
    except Exception as e:
        print(f"数据库初始化错误: {str(e)}")
        raise  # 重新抛出异常以便上层捕获


def get_wechat_openid(code):
    """
    调用微信接口获取真实的openId
    使用微信小程序登录接口进行验证
    """
    print(f"get_wechat_openid called with code: '{code}'")
    import requests

    appid = get_config_value('wechat_appid') or 'your_wechat_appid_here'
    appsecret = get_config_value('wechat_secret') or 'your_wechat_appsecret_here'

    # 验证必要参数
    if not code:
        raise ValueError("缺少code参数")

    # 对测试用的模拟code仍返回mock openid
    if code.startswith('code_') or code.startswith('test_code_'):
        # 使用code生成一个固定的模拟openid，便于测试
        mock_openid = 'mock_' + hashlib.md5(code.encode()).hexdigest()
        print(f"使用模拟openid（测试code）: {mock_openid}")
        return mock_openid

    # 打印调试信息
    print(f"appid: '{appid}', appsecret: '{appsecret}'")
    # 检查是否配置了有效的appid和appsecret
    if appid in [None, '', 'your_wechat_appid_here'] or appsecret in [None, '', 'your_wechat_appsecret_here']:
        # 开发环境备用方案：返回模拟的openid
        print("警告：未配置有效的微信小程序appid和appsecret，使用模拟的openid进行开发测试")
        # 使用code生成一个固定的模拟openid，便于测试
        mock_openid = 'mock_' + hashlib.md5(code.encode()).hexdigest()
        print(f"使用模拟openid: {mock_openid}")
        return mock_openid

    # 生产环境：调用真实的微信接口
    try:
        # 调用微信登录接口
        url = f'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={appsecret}&js_code={code}&grant_type=authorization_code'

        # 设置超时，避免请求长时间挂起
        response = requests.get(url, timeout=10)

        # 检查HTTP状态码
        response.raise_for_status()  # 若HTTP状态码不是200，抛出HTTPError

        # 解析响应数据
        data = response.json()

        # 检查是否包含错误信息
        if 'errcode' in data and data['errcode'] != 0:
            raise Exception(f'微信登录失败: 错误码 {data["errcode"]}, 错误信息: {data["errmsg"]}')

        # 检查是否返回了openid
        if 'openid' not in data:
            raise Exception(f'微信登录接口未返回openid: {data}')

        return data['openid']

    except requests.RequestException as e:
        # 网络请求异常
        raise Exception(f'微信接口网络请求失败: {str(e)}')
    except Exception as e:
        # 其他异常
        raise Exception(f'微信登录验证失败: {str(e)}')


@app.route('/api/login', methods=['POST'])
def login():
    """
    微信登录接口
    使用真实的微信code获取openid进行用户认证
    """
    # 初始化数据库（确保users表存在）
    try:
        init_database()
    except Exception as e:
        print(f"数据库初始化失败: {str(e)}")
        return jsonify({'success': False, 'message': '服务器数据库初始化失败'}), 500

    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': '无效的请求数据'}), 400

        code = data.get('code')
        if not code:
            return jsonify({'success': False, 'message': '缺少code参数'}), 400

        # 调用微信接口获取openId和用户信息
        open_id = None
        user_info = None
        try:
            # 获取openid
            open_id = get_wechat_openid(code)
            print(f"login function got open_id: '{open_id}'")
            if not open_id:
                raise Exception("未获取到有效的openid")
            print(f"成功获取openid: {open_id}")

            # 模拟获取用户基本信息（需要微信用户信息接口权限）
            # 实际开发中需要使用access_token调用微信用户信息接口
            # 这里模拟获取用户信息
            user_info = {
                'nickname': f'用户_{open_id[:6]}',
                'avatar_url': 'http://example.com/default_avatar.png'
            }
        except Exception as e:
            # 记录微信登录错误
            print(f"微信登录验证错误: {str(e)}")
            return jsonify({'success': False, 'message': f'微信登录失败: {str(e)}'}), 401

        # 生成JWT token (修改为与webserve2一致)
        token = jwt.encode({
            'sub': open_id,  # 修改为与webserve2一致，使用'sub'而不是'open_id'
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        # 检查是否首次登录并获取用户信息
        conn = None
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            c = conn.cursor()
            c.execute("SELECT nick_name, avatar_url FROM users WHERE open_id = ?", (open_id,))
            user_data = c.fetchone()

            is_first_login = user_data is None

            # 构建用户信息
            if is_first_login:
                # 新用户：保存提供的信息，若为空则使用默认值
                nick_name = data.get('nickName', '') or '匿名用户'
                avatar_url = data.get('avatarUrl', '') or 'http://example.com/default_avatar.png'
                c.execute(
                    "INSERT INTO users (open_id, nick_name, avatar_url) VALUES (?, ?, ?)",
                    (open_id, nick_name, avatar_url)
                )
            else:
                # 现有用户：仅更新提供的非空信息
                current_nick_name = user_data[0]
                current_avatar_url = user_data[1]
                nick_name = data['nickName'] if 'nickName' in data and data['nickName'] else (
                            current_nick_name or '匿名用户')
                avatar_url = data['avatarUrl'] if 'avatarUrl' in data and data['avatarUrl'] else (
                            current_avatar_url or 'http://example.com/default_avatar.png')
                c.execute(
                    "UPDATE users SET nick_name = ?, avatar_url = ?, updated_at = CURRENT_TIMESTAMP WHERE open_id = ?",
                    (nick_name, avatar_url, open_id)
                )
            conn.commit()

            # 构建用户信息
            user_info = {
                'nickName': nick_name,
                'avatarUrl': avatar_url,
                'openId': open_id
            }

            if is_first_login:
                print(f"新用户注册成功: {open_id}")
            else:
                print(f"用户信息更新成功: {open_id}")
        finally:
            if conn:
                conn.close()
                print("数据库连接已关闭")

        print(f"登录成功: {open_id}, 是否首次登录: {is_first_login}")
        print(f"返回的用户信息: {user_info}")
        print(f"返回的token: {token}")
        # 修改响应格式与webserve2一致
        return jsonify({
            'success': True,
            'token': token,
            'isFirstLogin': is_first_login,
            'userInfo': user_info
        })

    except Exception as e:
        print(f"登录过程异常: {str(e)}")
        # 确保数据库连接关闭
        if 'conn' in locals() and conn:
            try:
                conn.close()
                print("错误处理中关闭数据库连接")
            except:
                pass
        return jsonify({'success': False, 'message': '登录过程中发生服务器错误'}), 500


# 添加获取用户信息接口 (与webserve2一致)
@app.route('/api/user/info', methods=['GET'])
@token_required
def get_user_info(current_user):
    """
    获取用户信息接口
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute("SELECT open_id, nick_name, avatar_url FROM users WHERE open_id = ?", (current_user,))
        user_data = c.fetchone()
        conn.close()

        if not user_data:
            return jsonify({'success': False, 'message': '用户不存在'}), 404

        # 构建返回的用户信息
        user_info = {
            'openId': user_data[0],
            'nickName': user_data[1] or '',  # 确保昵称非空
            'avatarUrl': user_data[2] or ''  # 确保头像URL非空
        }

        return jsonify({
            'success': True,
            'userInfo': user_info
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/logout', methods=['POST'])
@token_required
def logout(current_user):
    """
    用户登出接口
    """
    try:
        # JWT是无状态的，服务端不需要特殊处理
        # 客户端需要删除本地存储的token
        return jsonify({
            'success': True,
            'message': '登出成功'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/user/register', methods=['POST'])
@token_required
def register_user(current_user):
    """
    用户信息完善接口
    """
    try:
        data = request.get_json()
        nick_name = data.get('nickName')
        avatar_url = data.get('avatarUrl', '')

        if not nick_name:
            return jsonify({'success': False, 'message': '缺少用户昵称'}), 400

        # 保存用户信息到数据库
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO users (open_id, nick_name, avatar_url) VALUES (?, ?, ?)",
                  (current_user, nick_name, avatar_url))
        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'message': '用户信息完善成功',
            'userInfo': {
                'nickName': nick_name,
                'avatarUrl': avatar_url,
                'openId': current_user
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/collection', methods=['POST'])
@token_required
def collect_walnut(current_user):
    """
    核桃采集接口
    """
    try:
        data = request.get_json()
        images = data.get('images')
        size = data.get('size')
        angles = data.get('angles')

        if not images or len(images) != 6:
            return jsonify({'success': False, 'message': '需要提供6个角度的图片'}), 400

        if not size or not (33 <= size <= 42):
            return jsonify({'success': False, 'message': '尺寸应在33-42mm范围内'}), 400

        if not angles or len(angles) != 6:
            return jsonify({'success': False, 'message': '需要提供6个角度类型'}), 400

        # 生成唯一的核桃ID
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        walnut_id = f"{timestamp}_1_{size}"  # 格式: 时间戳_编号_尺寸

        # 保存图片到临时文件夹
        temp_folder = save_images_to_temp_folder(images, walnut_id)

        # 提取并存储特征到向量数据库
        if vector_db:
            try:
                # 加载图片
                walnut_images = load_images_from_folder(temp_folder)

                # 提取每个角度的特征并存储
                for i, image in enumerate(walnut_images):
                    # 提取特征
                    texture_feature = similar.extract_texture_features(image)
                    edge_feature = similar.extract_edge_features(image)
                    color_feature = similar.extract_color_features(image)

                    # 存储特征到向量数据库
                    angle_id = f"{walnut_id}_angle{i + 1}"
                    vector_db.store_features(angle_id, str(size), 'texture', texture_feature)
                    vector_db.store_features(angle_id, str(size), 'edge', edge_feature)
                    vector_db.store_features(angle_id, str(size), 'color', color_feature)
            except Exception as e:
                print(f"特征提取和存储出错: {e}")

        # 构建数据目录结构
        size_folder = os.path.join(ROOT_FOLDER, str(size))
        os.makedirs(size_folder, exist_ok=True)

        collection_folder = os.path.join(size_folder, walnut_id)
        os.makedirs(collection_folder, exist_ok=True)

        # 移动图片到正式目录
        for filename in os.listdir(temp_folder):
            src_path = os.path.join(temp_folder, filename)
            dst_path = os.path.join(collection_folder, filename)
            shutil.move(src_path, dst_path)

        # 清理临时文件夹
        shutil.rmtree(temp_folder, ignore_errors=True)

        # 添加到数据库
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO walnut_selection (walnut_name, selected, over) VALUES (?, ?, ?)",
                  (walnut_id, False, False))
        conn.commit()
        conn.close()

        # 修改响应格式与webserve2一致
        return jsonify({
            'success': True,
            'collection_id': walnut_id,
            'message': '采集成功'
        })

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


def compare_endpoint(temp_walnut_id, size, root_folder):
    """比较核桃相似度的核心逻辑"""
    # 构造临时文件夹路径
    temp_folder = os.path.join(TEMP_IMAGES_FOLDER, temp_walnut_id)

    # 获取阈值配置
    G_THRESHOLD = get_config_value('G') or 0.8

    try:
        # 加载新核桃的图片
        new_walnut_images = load_images_from_folder(temp_folder)
        if not new_walnut_images or len(new_walnut_images) < 6:
            print(f"加载新核桃图片失败或数量不足: {temp_folder}")
            return jsonify({
                'success': False,
                'message': '无法加载新核桃的图片',
                'top_results': []
            }), 500

        # 获取相同尺寸的所有核桃ID
        walnut_ids = vector_db.get_walnut_ids_by_size(str(size)) if vector_db else []

        comparison_results = []

        # 只遍历相同尺寸的核桃进行比较
        for walnut_id in walnut_ids:
            if walnut_id == temp_walnut_id:
                continue  # 跳过自身比较

            try:
                # 直接使用向量数据库计算相似度
                similarity_result = None
                if vector_db:
                    similarity_result = Sqldeal.calculate_similarity_from_vectors(
                        temp_walnut_id, str(size), walnut_id, str(size))

                # 如果向量数据库不可用，则使用原有方法作为备选
                if similarity_result is None:
                    # 构造现有核桃的路径
                    existing_walnut_path = os.path.join(root_folder, walnut_id)
                    if not os.path.exists(existing_walnut_path):
                        print(f"现有核桃路径不存在: {existing_walnut_path}")
                        continue

                    existing_walnut_images = load_images_from_folder(existing_walnut_path)
                    if not existing_walnut_images or len(existing_walnut_images) < 6:
                        print(f"加载现有核桃图片失败或数量不足: {existing_walnut_path}")
                        continue

                    similarity_result = calulate_all_similarity(new_walnut_images, existing_walnut_images)

                # 根据配置阈值G过滤结果
                if similarity_result is None:
                    print(f"计算相似度失败: {temp_walnut_id} vs {walnut_id}")
                    continue

                filtered_result = filter_details_by_threshold(similarity_result, G_THRESHOLD)

                # 收集结果
                result_entry = {
                    'id': walnut_id,
                    'similarity': round(filtered_result[0] * 100, 2),
                    'texture_similarity': round(filtered_result[1] * 100, 2),
                    'edge_similarity': round(filtered_result[2] * 100, 2),
                    'color_similarity': round(filtered_result[3] * 100, 2),
                    'details': filtered_result[4]
                }
                comparison_results.append(result_entry)

                # 输出单个核桃对比日志
                print(f"[对比日志] 核桃ID: {walnut_id}, 相似度: {filtered_result[0] * 100:.2f}%")
            except Exception as e:
                print(f"计算 {temp_walnut_id} 与 {walnut_id} 相似度时出错: {e}")

        # 清理临时文件
        if os.path.exists(temp_folder):
            try:
                shutil.rmtree(temp_folder)
            except:
                pass

        # 按相似度降序排序
        comparison_results.sort(key=lambda x: x['similarity'], reverse=True)

        # 取前三个结果
        top_three_results = comparison_results[:3]

        # 确保返回一个空数组而不是 undefined
        if not top_three_results:
            top_three_results = []

        # 修改响应格式与webserve2一致
        return jsonify({
            'success': True,
            'message': '对比完成',
            'top_results': top_three_results
        })

    except Exception as e:
        if 'temp_folder' in locals() and os.path.exists(temp_folder):
            try:
                shutil.rmtree(temp_folder)
            except:
                pass
        print(f"compare_endpoint 函数执行异常: {e}")
        return jsonify({
            'success': False,
            'message': '对比过程中发生错误',
            'top_results': []
        }), 500



@app.route('/compare', methods=['POST'])
@app.route('/api/compare', methods=['POST'])
@token_required
def compare_walnut(current_user):
    """
    核桃相似度比较接口
    """
    try:
        # 获取请求数据
        data = request.get_json()
        images = data.get('images')
        size = data.get('size')
        angles = data.get('angles', [])

        # 验证输入数据
        if not images or len(images) != 6:
            return jsonify({'success': False, 'message': '需要提供6个角度的图片'}), 400

        if not size or not (33 <= size <= 42):
            return jsonify({'success': False, 'message': '尺寸应在33-42mm范围内'}), 400

        if not angles or len(angles) != 6:
            return jsonify({'success': False, 'message': '需要提供6个角度类型'}), 400

        # 生成临时核桃ID
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        temp_walnut_id = f"{timestamp}_temp_{size}"

        # 保存图片到临时文件夹
        temp_folder = save_images_to_temp_folder(images, temp_walnut_id)

        # 提取并存储特征到向量数据库（如果是新核桃）
        if vector_db:
            try:
                # 加载图片
                walnut_images = load_images_from_folder(temp_folder)

                # 提取每个角度的特征并存储
                for i, image in enumerate(walnut_images):
                    # 提取特征
                    texture_feature = similar.extract_texture_features(image)
                    edge_feature = similar.extract_edge_features(image)
                    color_feature = similar.extract_color_features(image)

                    # 存储特征到向量数据库
                    angle_id = f"{temp_walnut_id}_angle{i + 1}"
                    vector_db.store_features(angle_id, str(size), 'texture', texture_feature)
                    vector_db.store_features(angle_id, str(size), 'edge', edge_feature)
                    vector_db.store_features(angle_id, str(size), 'color', color_feature)
            except Exception as e:
                print(f"特征提取和存储出错: {e}")

        # 获取数据根目录
        root_folder = get_config_value('root_folder') or 'data'
        root_folder = os.path.join(root_folder, str(size))

        # 执行比较逻辑
        return compare_endpoint(temp_walnut_id, size, root_folder)

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# 静态文件服务路由
@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    """
    提供上传文件的静态访问
    """
    # 安全地处理文件路径，避免路径遍历攻击
    import werkzeug
    filename = werkzeug.utils.secure_filename(filename)

    # 构建完整文件路径
    file_path = os.path.join(TEMP_IMAGES_FOLDER, filename)

    # 检查文件是否存在
    if not os.path.exists(file_path):
        # 尝试在子目录中查找
        for root, dirs, files in os.walk(TEMP_IMAGES_FOLDER):
            if filename in files:
                file_path = os.path.join(root, filename)
                break
        else:
            return jsonify({'success': False, 'message': '文件不存在'}), 404

    # 返回文件
    return send_from_directory(os.path.dirname(file_path), os.path.basename(file_path))


# 处理程序关闭事件
import atexit

atexit.register(lambda: scheduler.shutdown())


# 在 webserve.py 文件末尾添加以下代码（在 if __name__ == '__main__': 之前）

# 保留原有的接口以确保向后兼容
@app.route('/process_walnut', methods=['POST'])
def process_single_walnut():
    # 保留原有实现的占位符
    pass


@app.route('/confirm_pair', methods=['POST'])
def confirm_walnut_pair():
    # 保留原有实现的占位符
    pass


@app.route('/unpair', methods=['POST'])
def unpair_walnuts():
    # 保留原有实现的占位符
    pass


@app.route('/get_history', methods=['GET'])
def get_history_pairs():
    # 保留原有实现的占位符
    pass


@app.route('/get_similarities', methods=['GET'])
def get_current_similarities():
    # 保留原有实现的占位符
    pass


# 在开发环境中，可以临时允许跳过token验证
# 生产环境部署时，请确保移除以下装饰器中的条件逻辑
@app.route('/upload', methods=['POST'])
@token_required
def upload_images(current_user):
    """
    图片上传接口
    接口路径: /upload
    请求方式: POST
    是否需要认证: 是
    """
    try:
        # 添加详细的调试信息
        print(f"=== 上传请求详情 ===")
        print(f"请求文件: {request.files.keys() if request.files else '无文件'}")
        print(f"表单数据: {dict(request.form) if request.form else '无表单数据'}")

        # 使用get_json(silent=True)避免Content-Type错误
        json_data = request.get_json(silent=True)
        print(f"JSON数据: {list(json_data.keys()) if json_data else '无JSON数据'}")

        # 先处理JSON格式的请求
        if json_data:
            if 'image' in json_data:
                image_data = json_data['image']
                purpose = json_data.get('purpose', '')
                angle = json_data.get('angle', '')
                print(f"JSON上传: purpose={purpose}, angle={angle}")

                # 生成文件ID
                file_id = f"upload_{int(datetime.datetime.now().timestamp())}_{os.urandom(8).hex()}"

                # 确保上传目录存在
                upload_folder = os.path.join(TEMP_IMAGES_FOLDER, purpose if purpose else 'general')
                os.makedirs(upload_folder, exist_ok=True)

                # 检查是否包含Base64前缀
                if ',' in image_data:
                    header, image_data = image_data.split(',', 1)
                    print(f"Base64前缀: {header}")

                # 解码Base64图片数据
                image_bytes = base64.b64decode(image_data)

                # 确定文件扩展名
                ext = '.png'  # 默认使用png格式
                if ',' in json_data['image']:
                    header = json_data['image'].split(',')[0]
                    # 从header中提取MIME类型 (例如: 'data:image/jpeg;base64')
                    mime_type = header.split(';')[0].split(':')[1]
                    guessed_ext = mimetypes.guess_extension(mime_type)
                    if guessed_ext:
                        ext = guessed_ext

                # 保存图片到临时目录
                file_path = os.path.join(upload_folder, f"{file_id}{ext}")
                with open(file_path, 'wb') as f:
                    f.write(image_bytes)

                print(f"JSON上传成功: {file_path}")
                return jsonify({
                    'success': True,
                    'file_id': file_id,
                    'url': file_path
                }), 200

        # 兼容 'file' 和 'image' 两种字段名（表单上传）
        if 'file' in request.files:
            file = request.files['file']
        elif 'image' in request.files:
            file = request.files['image']
        else:
            print("错误：请求中没有'file'或'image'字段")
            return jsonify({'success': False, 'message': '缺少文件参数'}), 400
        print(f"文件信息: 名称={file.filename}, 类型={file.mimetype}")

        if file.filename == '':
            print("错误：文件名为空")
            return jsonify({'success': False, 'message': '未选择文件'}), 400

        # 获取上传目的（可选）
        purpose = request.form.get('purpose', '')
        # 不再严格验证purpose值，只在为空时使用默认值
        # if purpose not in ['', 'collection', 'comparison']:
        #     return jsonify({'success': False, 'message': '无效的用途标识'}), 400

        # 生成文件ID
        file_id = f"upload_{int(datetime.datetime.now().timestamp())}_{os.urandom(8).hex()}"

        # 确保上传目录存在
        upload_folder = os.path.join(TEMP_IMAGES_FOLDER, purpose if purpose else 'general')
        os.makedirs(upload_folder, exist_ok=True)

        # 保存文件
        filename = secure_filename(file.filename)
        filepath = os.path.join(upload_folder, f"{file_id}_{filename}")
        file.save(filepath)

        # 构建文件URL（实际环境中应该使用CDN或文件服务器地址）
        file_url = f"http://localhost:5000/uploads/{purpose if purpose else 'general'}/{file_id}_{filename}"

        return jsonify({
            'success': True,
            'file_id': file_id,
            'url': file_url
        })

    except Exception as e:
        print(f"文件上传失败: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


def process_walnut_images(images):
    # ... (原有代码保持不变)
    pass


if __name__ == '__main__':
    # 初始化数据库
    init_database()
    # 修改服务器地址：host='0.0.0.0' 表示监听所有网络接口，port=8080 表示使用8080端口 (与webserve2一致)
    app.run(debug=True, host='0.0.0.0', port=8080)
