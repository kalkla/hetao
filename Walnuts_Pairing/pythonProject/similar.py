# similar.py
import cv2
import numpy as np
from skimage.feature import local_binary_pattern
from vector_db import VectorDB
import os

# 假设向量数据库路径在项目根目录
VECTOR_DB_PATH = 'vector_features.db'
vector_db = VectorDB(VECTOR_DB_PATH) if os.path.exists(VECTOR_DB_PATH) else None


def extract_texture_features(image):
    """提取纹理特征"""
    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image

    # 使用LBP算法提取纹理特征
    radius = 3
    n_points = 8 * radius
    lbp = local_binary_pattern(gray, n_points, radius, method='uniform')

    # 计算直方图作为特征向量
    hist, _ = np.histogram(lbp.ravel(), bins=np.arange(0, n_points + 3), range=(0, n_points + 2))
    hist = hist.astype("float")
    hist /= (hist.sum() + 1e-7)  # 归一化

    return hist.tolist()


def extract_edge_features(image):
    """提取边缘特征"""
    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image

    # Canny边缘检测
    edges = cv2.Canny(gray, 50, 150)

    # 计算边缘密度和方向直方图
    edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])

    # 计算梯度方向直方图
    grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    magnitude = np.sqrt(grad_x ** 2 + grad_y ** 2)
    angle = np.arctan2(grad_y, grad_x) * 180 / np.pi

    # 只考虑边缘点的角度
    mask = edges > 0
    angles = angle[mask]
    magnitudes = magnitude[mask]

    # 计算角度直方图
    hist, _ = np.histogram(angles, bins=36, range=(-180, 180), weights=magnitudes)
    hist = hist.astype("float")
    hist /= (hist.sum() + 1e-7)  # 归一化

    # 将边缘密度和直方图合并为特征向量
    features = [edge_density] + hist.tolist()
    return features


def extract_color_features(image):
    """提取颜色特征"""
    # 转换到HSV色彩空间
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 计算各个通道的直方图
    hist_h = cv2.calcHist([hsv], [0], None, [180], [0, 180])
    hist_s = cv2.calcHist([hsv], [1], None, [256], [0, 256])
    hist_v = cv2.calcHist([hsv], [2], None, [256], [0, 256])

    # 归一化
    cv2.normalize(hist_h, hist_h, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    cv2.normalize(hist_s, hist_s, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    cv2.normalize(hist_v, hist_v, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

    # 合并为单一特征向量
    features = hist_h.flatten().tolist() + hist_s.flatten().tolist() + hist_v.flatten().tolist()
    return features


def calulate_similarity(image1, image2):
    """计算两张图片的相似度"""
    # 将图像转换为灰度图
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY) if len(image1.shape) == 3 else image1
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY) if len(image2.shape) == 3 else image2

    # 纹理相似度计算
    lbp1 = local_binary_pattern(gray1, 8, 1, method='uniform')
    lbp2 = local_binary_pattern(gray2, 8, 1, method='uniform')
    hist1, _ = np.histogram(lbp1.ravel(), bins=np.arange(0, 11), range=(0, 10))
    hist2, _ = np.histogram(lbp2.ravel(), bins=np.arange(0, 11), range=(0, 10))
    texture_similarity = cv2.compareHist(hist1.astype(np.float32), hist2.astype(np.float32), cv2.HISTCMP_CORREL)

    # 边缘相似度计算
    edges1 = cv2.Canny(gray1, 50, 150)
    edges2 = cv2.Canny(gray2, 50, 150)
    edge_similarity = np.sum((edges1 > 0) & (edges2 > 0)) / (np.sum((edges1 > 0) | (edges2 > 0)) + 1e-7)

    # 颜色相似度计算（使用HSV色彩空间）
    hsv1 = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(image2, cv2.COLOR_BGR2HSV)
    hist_h1 = cv2.calcHist([hsv1], [0], None, [50], [0, 180])
    hist_h2 = cv2.calcHist([hsv2], [0], None, [50], [0, 180])
    color_similarity = cv2.compareHist(hist_h1, hist_h2, cv2.HISTCMP_CORREL)

    # 综合相似度计算
    similarity = (texture_similarity + edge_similarity + color_similarity) / 3

    return {
        'similarity': float(similarity),
        'texture_similarity': float(texture_similarity),
        'edge_similarity': float(edge_similarity),
        'color_similarity': float(color_similarity)
    }


def calulate_all_similarity(image_list1, image_list2):  # 比较两个核桃图片序列的相似度
    if not image_list1 or not image_list2:
        return {
            'similarity': 0.0,
            'texture_similarity': 0.0,
            'edge_similarity': 0.0,
            'color_similarity': 0.0,
            'details': []
        }

    best_results = []
    for image1 in image_list1:
        max_similarity = -1.0
        best_result = None
        for image2 in image_list2:
            sim_result = calulate_similarity(image1, image2)
            if sim_result['similarity'] > max_similarity:
                max_similarity = sim_result['similarity']
                best_result = sim_result
        if best_result:
            best_results.append(best_result)

    if not best_results:
        return {
            'similarity': 0.0,
            'texture_similarity': 0.0,
            'edge_similarity': 0.0,
            'color_similarity': 0.0,
            'details': []
        }

    # 计算平均相似度
    length = len(best_results)
    avg_similarity = sum([result['similarity'] for result in best_results]) / length
    avg_texture = sum([result['texture_similarity'] for result in best_results]) / length
    avg_edge = sum([result['edge_similarity'] for result in best_results]) / length
    avg_color = sum([result['color_similarity'] for result in best_results]) / length

    return {
        'similarity': avg_similarity,
        'texture_similarity': avg_texture,
        'edge_similarity': avg_edge,
        'color_similarity': avg_color,
        'details': best_results
    }
