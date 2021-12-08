#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# author:
# datetime:2021/9/9 14:42
# software: PyCharm
# filename:similar.py
"""
import os
import flask
from flask import Flask, jsonify

from bert4keras.models import build_transformer_model
from bert4keras.tokenizers import Tokenizer
from keras import Model
import numpy as np
import tensorflow as tf
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from keras.backend.tensorflow_backend import set_session

from config import similar_config_path

global bert_model, graph
graph = tf.get_default_graph()
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)
set_session(sess)

'''句子相似度计算'''
# bert配置
# config_path = 'D:/学习资料/model/chinese_simbert_L-6_H-384_A-12/bert_config.json'
# checkpoint_path = 'D:/学习资料/model/chinese_simbert_L-6_H-384_A-12/bert_model.ckpt'
# dict_path = 'D:/学习资料/model/chinese_simbert_L-6_H-384_A-12/vocab.txt'
config_path = os.path.join(similar_config_path, 'bert_config.json')
checkpoint_path = os.path.join(similar_config_path, 'bert_model.ckpt')
dict_path = os.path.join(similar_config_path, 'vocab.txt')

# 建立分词器
tokenizer = Tokenizer(dict_path, do_lower_case=True)

# 建立加载模型
bert = build_transformer_model(
    config_path,
    checkpoint_path,
    with_pool='linear',
    application='unilm',
    return_keras_model=False,
)

bert_model = Model(bert.model.input, bert.model.output)

# 建立分词器
tokenizer = Tokenizer(dict_path, do_lower_case=True)


# 利用模型，向量化句子
def similarity(sent1, sent2, mode='cos'):
    '''
    计算句子相似度
    :param sent1:句子1向量
    :param sent2:句子2向量
    :param mode:欧几里得距离（eu或者余弦距离（cos）
    :return:
    '''
    token_ids1, segment_ids1 = tokenizer.encode(sent1)
    token_ids2, segment_ids2 = tokenizer.encode(sent2)

    vec1 = bert_model.predict([np.array([token_ids1]), np.array([segment_ids1])])[0]
    vec2 = bert_model.predict([np.array([token_ids2]), np.array([segment_ids2])])[0]
    if mode == 'eu':
        return euclidean_distances(vec1, vec2)[0][0]
    if mode == 'cos':
        return cosine_similarity(vec1, vec2)[0][0]


if __name__ == '__main__':
    # sent1 = '南信工胡老师在用户管理看到部分用户的有效期是没过期的时间，显示是过期的状态。'
    # sent2 = '南信工胡老师在用户管理看到部分用户的有效期是没过期的时间'
    # # sent1 = ''
    # # sent2 = ''
    # # score = similarity(sent1, sent2)

    # print(sent1 + '与' + sent2 + '的余弦相似度为：' + str(score))
    app = Flask(__name__)

    @app.route('/api/similar', methods=['POST', 'GET'])
    def similar():
        data = {'success': 0}
        result = None

        text_json = flask.request.get_json()['text_json']

        for i in range(len(text_json)):
            sent1 = text_json[i]['sent1']
            sent2 = text_json[i]['sent2']
            with graph.as_default():
                set_session(sess)
                score = similarity(sent1, sent2)
                text_json[i]['score'] = float(score)
        # data['score'] = float(score)
        data['data'] = text_json
        data['success'] = 1
        return jsonify(data)
    app.run(host='127.0.0.1', port=6002)



