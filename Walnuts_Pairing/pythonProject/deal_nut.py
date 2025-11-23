import cv2
import numpy as np

def crop_walnut(image):
    # 将图片转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 使用Canny边缘检测
    edges = cv2.Canny(gray, 50, 150)

    # 膨胀操作以增强边缘
    area = cv2.dilate(edges, None, iterations=2)

    # 寻找轮廓
    contours, _ = cv2.findContours(area, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 找到最大的轮廓（核桃）
    max_contour = max(contours, key=cv2.contourArea)

    # 计算边界矩形
    x, y, w, h = cv2.boundingRect(max_contour)

    # 裁剪核桃部分
    cropped_walnut = image[y:y+h, x:x+w]

    # 调整最大轮廓的坐标，使其与裁剪后的图像相对应
    max_contour = max_contour - [x, y]

    return cropped_walnut, max_contour

# 读取图像
image = cv2.imread('output1.png')
if image is None:
    raise FileNotFoundError("Image not found. Please check the file path.")

# 调用crop_walnut函数裁剪核桃部分
cropped_walnut, largest_contour = crop_walnut(image)

# 绘制轮廓到裁剪后的图像上
cv2.drawContours(cropped_walnut, [largest_contour], -1, (0, 255, 0), 2)  # 绿色轮廓

# 初始化最大距离和对应的点对
max_distance = 0
farthest_points = (None, None)

# 遍历轮廓中的所有点对，找到距离最远的一对
for i, point1 in enumerate(largest_contour):
    for j, point2 in enumerate(largest_contour):
        if i != j:  # 确保不是同一个点
            distance = np.linalg.norm(point1[0] - point2[0])  # 注意这里应该是 point1[0] 和 point2[0]
            if distance > max_distance:
                max_distance = distance
                farthest_points = (tuple(point1[0]), tuple(point2[0]))

# 检查是否找到了有效的点对
if all(farthest_points):
    # 画出最远的两点之间的线
    cv2.line(cropped_walnut, farthest_points[0], farthest_points[1], (0, 255, 0), 2)  # 红色线段

    # 计算整张图片的中点位置
    mid_y = cropped_walnut.shape[0] // 2
    cv2.line(cropped_walnut, (0, mid_y), (cropped_walnut.shape[1], mid_y), (0, 0, 255), 2)  # 水平红色线段

    # 检查两条线是否重合
    green_line_slope = (farthest_points[1][1] - farthest_points[0][1]) / (farthest_points[1][0] - farthest_points[0][0])
    green_line_intercept = farthest_points[0][1] - green_line_slope * farthest_points[0][0]

    # 检查绿线是否经过图像的中点
    if abs(mid_y - (green_line_slope * (cropped_walnut.shape[1] // 2) + green_line_intercept)) < 2:  # 允许一定的误差
        text = "OK"
        color = (0, 255, 0)
    else:
        text = "Error"
        color = (0, 0, 255)

    # 在图像上添加文本
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2
    text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
    text_x = (cropped_walnut.shape[1] - text_size[0]) // 2
    text_y = (cropped_walnut.shape[0] + text_size[1]) // 2
    cv2.putText(cropped_walnut, text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)

# 显示结果图像
cv2.imshow('Result with Farthest Points and Horizontal Line', cropped_walnut)
cv2.waitKey(0)
cv2.destroyAllWindows()