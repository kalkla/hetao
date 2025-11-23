
# 本函数实现从原始的similar的数据中提取想要的数据并返回
# author：张
# qq：750123348
#变量：data_dict：similar返回值，具体格式下方已给出，G：浮点数范围可以通过配置软件扩大或缩小分为但是不建议这么做，最好是0-1的浮点数
#返回值：列表       result = [
            #     similarity,总体相似度
            #     texture_similarity,纹理相似度
            #     edge_similarity,边缘相似度
            #     color_similarity,颜色相似度
            #     count_above_threshold,对应面总相似度大于G的个数
            # ]

def filter_details_by_threshold(data_dict, G):
    # 提取前四项
    similarity = data_dict['similarity']
    texture_similarity = data_dict['texture_similarity']
    edge_similarity = data_dict['edge_similarity']
    color_similarity = data_dict['color_similarity']

    # 计算details中similarity大于G的个数
    count_above_threshold = sum(1 for detail in data_dict['details'] if detail['similarity'] > G)

    # 将结果合并到一个列表中
    result = [
        similarity,
        texture_similarity,
        edge_similarity,
        color_similarity,
        count_above_threshold
    ]

    return result

#
# # 示例字典
# data_dict = {
#     'similarity': 0.8868673490597471,
#     'texture_similarity': 0.8807445168495178,
#     'edge_similarity': 0.8140716552734375,
#     'color_similarity': 0.9657858750562859,
#     'details': [
#         {'similarity': 0.8919369376195655, 'texture_similarity': 0.86846143, 'edge_similarity': 0.8203887939453125,
#          'color_similarity': 0.9869605888405998},
#         {'similarity': 0.9066652837747645, 'texture_similarity': 0.88707757, 'edge_similarity': 0.836090087890625,
#          'color_similarity': 0.9968281934721208},
#         {'similarity': 0.8747529018887806, 'texture_similarity': 0.85855657, 'edge_similarity': 0.7873077392578125,
#          'color_similarity': 0.9783943977859404},
#         {'similarity': 0.8615908578366945, 'texture_similarity': 0.86475486, 'edge_similarity': 0.8640899658203125,
#          'color_similarity': 0.8559277520569889},
#         {'similarity': 0.8961633051721773, 'texture_similarity': 0.9039337, 'edge_similarity': 0.7957000732421875,
#          'color_similarity': 0.988856138374961},
#         {'similarity': 0.8900948080664998, 'texture_similarity': 0.901683, 'edge_similarity': 0.780853271484375,
#          'color_similarity': 0.9877481798071042}
#     ]
# }
