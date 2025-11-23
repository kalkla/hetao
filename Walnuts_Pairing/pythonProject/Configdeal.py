import os
import yaml

def get_config_value(key):
    """从配置文件中读取指定键的值，如果不存在则返回 None"""
    # 尝试多种路径查找config.yaml
    paths_to_try = [
        'config.yaml',
        '../config.yaml',
        os.path.join(os.path.dirname(__file__), 'config.yaml'),
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yaml')
    ]
    
    for config_file in paths_to_try:
        try:
            with open(config_file, 'r') as file:
                config = yaml.safe_load(file)
                print(f"Found config file at: {config_file}")
                return config.get(key, None)
        except FileNotFoundError:
            print(f"Config file not found at: {config_file}")
            continue
    
    return None

# 示例调用
if __name__ == '__main__':
    # 读取 G 值
    G = get_config_value('G')
    print(f"G: {G}")

    # 读取 Goal 值
    Goal = get_config_value('Goal')
    print(f"Goal: {Goal}")

    # 读取 color 值
    color = get_config_value('color')
    print(f"Color: {color}")

    # 读取 data_folder 值
    data_folder = get_config_value('data_folder')
    print(f"Data Folder: {data_folder}")

    # 读取 edge 值
    edge = get_config_value('edge')
    print(f"Edge: {edge}")

    # 读取 root_folder 值
    root_folder = get_config_value('root_folder')
    print(f"Root Folder: {root_folder}")

    # 读取 texture 值
    texture = get_config_value('texture')
    print(f"Texture: {texture}")

    # 读取 yuzhi 值
    yuzhi = get_config_value('yuzhi')
    print(f"Yuzhi: {yuzhi}")