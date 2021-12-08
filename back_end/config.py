#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# author:
# datetime:2021/9/6 14:09
# software: PyCharm
# filename:config.py
"""
import os

root_path = os.path.abspath(os.path.dirname(__file__))
# data_path
data_path = './data/问题汇总(2)(1).xls'
columns_path = './data/columns'
labels_path = './data/labels'
# 分类模型bert_cnn模型路径
intent_path = os.path.join(root_path, 'checkpoint/')
# 预训练模型路径
bert_config_path = 'D:/学习资料/model/chinese_rbt3_L-3_H-768_A-12'
similar_config_path = 'D:/学习资料/model/chinese_simbert_L-6_H-384_A-12'
