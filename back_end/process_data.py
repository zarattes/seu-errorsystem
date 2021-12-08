#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# author:
# datetime:2021/9/6 9:52
# software: PyCharm
# filename:process_data.py
"""
import json
import random
import pandas as pd

from config import data_path, columns_path, labels_path
from py2mysql import get_db_data

class GenerateData():
    '''读取运维需求描述，运维类别'''

    def __init__(self, path, columns_path, labels_path):
        self.path = path
        # self.code_path = code_path
        self.columns_path = columns_path
        self.labels_path = labels_path

    def read_labels(self, labels_list):
        label_list = [line.strip() for line in labels_list]
        label2id = {label: idx for idx, label in enumerate(label_list)}
        return label2id

    def read_questions(self):
        """
        读取运维统计表
        :return:运维需求描述，类别和表的列名
        """
        questions = []
        # data = pd.read_excel(self.path, sheet_name='项目运维统计表')
        # data = data.where(data.notnull(), None)
        # data_col = data.columns.values  # ndarray
        results = get_db_data()
        data = pd.DataFrame()
        for i in range(len(results)):
            data.loc[i, 'id'] = results[i][0]
            data.loc[i, 'content'] = results[i][1]
            data.loc[i, 'user_id'] = results[i][2]
            data.loc[i, 'answer_status'] = results[i][3]
            data.loc[i, 'admin_id'] = results[i][4]
            data.loc[i, 'category_id'] = results[i][5]
        data = data.where(data.notnull(), None)
        data_col = data.columns.values  # ndarray

        # # 保存列名
        # for column in data_col:
        #     with open(self.columns_path, 'a', encoding='utf-8') as f:
        #         f.write(column + '\n')

        labels = list(set(data['category_id']))
        label2id = self.read_labels(labels)

        with open(self.labels_path, 'w', encoding='utf-8') as fp:
            fp.write(json.dumps(label2id, ensure_ascii=False, indent=3))

        for idx, row in data.iterrows():
            questions.append([row['content'], row['category_id'], label2id[row['category_id']]])

        df = pd.DataFrame(questions)
        df.columns = ['text', 'label_class', 'label']
        return df, data_col, label2id


def load_data(filename):
    """
    加载数据
    :param filename:
    :return:
    """
    df = pd.read_csv(filename, header=0)
    return df[['text', 'label']].values


if __name__ == '__main__':
    # data_path = './data/问题汇总(2)(1).xlsx'
    # columns_path = './data/columns'
    # labels_path = './data/labels'
    generate_data = GenerateData(data_path, columns_path, labels_path)
    data, columns, labels_dict = generate_data.read_questions()

    # 将columns写入文件
    for column in columns:
        with open(columns_path, 'a', encoding='utf-8') as f:
            f.write(column + '\n')

    data.to_csv('./data/data.csv', index=False)

    # 将labels写入文件
    res = data.sample(frac=1.0)
    # 拆分数据集
    train_num = int(0.9 * len(res))
    print(train_num)
    train, test = res[:train_num], res[train_num + 1:]

    train.to_csv('./data/train.csv', index=False)
    test.to_csv('./data/test.csv', index=False)
    print()
