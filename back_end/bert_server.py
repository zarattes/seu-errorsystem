#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# author:
# datetime:2021/9/7 10:58
# software: PyCharm
# filename:bert_server.py
"""
import json

import flask
import pandas as pd
import os
import requests

import tensorflow as tf
from bert4keras.tokenizers import Tokenizer
from flask import Flask, request, jsonify
from keras.backend.tensorflow_backend import set_session
from keras.backend import clear_session

from bert_model import build_bert_model

from config import intent_path, bert_config_path, data_path

global graph, sess

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)
graph = tf.get_default_graph()
set_session(sess)

class_num = 11
max_len = 60


class BertIntentModel(object):
    def __init__(self):
        super(BertIntentModel, self).__init__()
        self.dict_path = os.path.join(bert_config_path, 'vocab.txt')
        self.config_path = os.path.join(bert_config_path, 'bert_config_rbt3.json')
        self.checkpoint_path = os.path.join(bert_config_path, 'bert_model.ckpt')

        with open('./data/labels', 'r', encoding='utf-8') as f:
            lines = f.read()
            label_dict = json.loads(lines)
            self.label_list = list(label_dict.keys())

        self.id2label = {idx: label for idx, label in enumerate(self.label_list)}

        self.tokenizer = Tokenizer(self.dict_path)
        self.model = build_bert_model(self.config_path, self.checkpoint_path, class_num)
        self.model.load_weights(os.path.join(intent_path, 'best_model.weight'))

    def predict(self, text):
        token_ids, segment_ids = self.tokenizer.encode(text, max_length=max_len)
        proba = self.model.predict([[token_ids], [segment_ids]])
        rst = {label: pro for label, pro in zip(self.label_list, proba[0])}
        rst = sorted(rst.items(), key=lambda kv: kv[1], reverse=True)
        name, confidence = rst[0]
        return {'name': name, "confidence": float(confidence)}


BIM = BertIntentModel()


if __name__ == '__main__':
    app = Flask(__name__)

    app = Flask(__name__)


    @app.route('/api/bert_recognize', methods=['GET', 'POST'])
    def bert_recognize():
        data = {'success': 0}
        result = None
        param = request.get_json()
        text = param['text']
        with graph.as_default():
            set_session(sess)
            result = BIM.predict(text)

        data['data'] = result
        data['success'] = 1

        return jsonify(data)
    app.run(host='127.0.0.1', port=6001)
