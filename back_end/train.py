#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# author:
# datetime:2021/9/11 9:17
# software: PyCharm
# filename:train.py
"""
import json
import os

from bert4keras.backend import keras
from bert4keras.optimizers import Adam
from bert4keras.snippets import DataGenerator, sequence_padding
from bert4keras.tokenizers import Tokenizer
from sklearn.metrics import classification_report

from bert_model import build_bert_model
from process_data import load_data

# 定义超参数和配置文件
from config import bert_config_path

class_nums = 11
maxlen = 60
batch_size = 5
epochs = 16

dict_path = os.path.join(bert_config_path, 'vocab.txt')
config_path = os.path.join(bert_config_path, 'bert_config_rbt3.json')
checkpoint_path = os.path.join(bert_config_path, 'bert_model.ckpt')
# config_path = 'D:/学习资料/model/chinese_rbt3_L-3_H-768_A-12/bert_config_rbt3.json'
# checkpoint_path = 'D:/学习资料/model/chinese_rbt3_L-3_H-768_A-12/bert_model.ckpt'
# dict_path = 'D:/学习资料/model/chinese_rbt3_L-3_H-768_A-12/vocab.txt'

tokenizer = Tokenizer(dict_path)


class data_generator(DataGenerator):
    """数据生成器"""
    def __iter__(self, random=False):
        batch_token_ids, batch_segment_ids, batch_labels = [], [], []
        for is_end, (text, label) in self.sample(random=random):
            token_ids, segment_ids = tokenizer.encode(text, max_length=maxlen)
            batch_token_ids.append(token_ids)
            batch_segment_ids.append(segment_ids)
            batch_labels.append([label])
            if len(batch_token_ids) == self.batch_size or is_end:
                batch_token_ids = sequence_padding(batch_token_ids)
                batch_segment_ids = sequence_padding(batch_segment_ids)
                batch_labels = sequence_padding(batch_labels)
                yield [batch_token_ids, batch_segment_ids], batch_labels
                batch_token_ids, batch_segment_ids, batch_labels = [], [], []


def train():
    train_data = load_data('./data/train.csv')
    test_data = load_data('./data/test.csv')

    # 转换数据集
    train_generator = data_generator(train_data, batch_size=batch_size)
    test_generator = data_generator(test_data, batch_size=batch_size)

    model = build_bert_model(config_path, checkpoint_path, class_nums)
    model.compile(
        loss='sparse_categorical_crossentropy',
        optimizer=Adam(5e-6),
        metrics=['accuracy']
    )

    earlystop = keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=3,
        verbose=2,
        mode='min'
    )

    best_model_filepath = './checkpoint/best_model.weight'
    checkpoint = keras.callbacks.ModelCheckpoint(
        best_model_filepath,
        monitor='val_loss',
        verbose=1,
        save_best_only=True,
        mode='min'
    )

    model.fit_generator(
        train_generator.forfit(),
        steps_per_epoch=len(train_generator),
        epochs=epochs,
        validation_data=test_generator.forfit(),
        validation_steps=len(test_generator),
        shuffle=True,
        callbacks=[earlystop, checkpoint]
    )

    # model.load_weights(best_model_filepath)
    # test_pred = []
    # test_true = []
    # for x, y in test_generator:
    #     p = model.predict(x).argmax(axis=1)
    #     test_pred.extend(p)
    #
    # test_true = test_data[:, 1].tolist()
    # print(set(test_true))
    # print(set(test_pred))
    #
    # # 读取labels名称
    # with open('./data/labels', 'r', encoding='utf-8') as f:
    #     lines = f.read()
    #     label_dict = json.loads(lines)
    #     labels = list(label_dict.keys())
    #
    # target_names = [line.strip() for line in labels]
    # print(classification_report(test_true, test_pred, target_names=target_names))


if __name__ == '__main__':

    train()
