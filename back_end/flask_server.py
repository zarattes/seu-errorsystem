#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
# author:
# datetime:2021/9/10 14:45
# software: PyCharm
# filename:flask_server.py
'''
import json
from datetime import datetime

import flask
import pandas as pd

import requests
import xlrd
from flask import Flask, jsonify
from xlutils.copy import copy

from config import data_path
import jieba
from bim25 import BM25_Model
import numpy as np
from py2mysql import get_db_data, get_message


def similar(text_json):
    url = 'http://127.0.0.1:6002/api/similar'
    data = {"text_json": text_json}
    headers = {'Content-Type': 'application/json;charset=utf8'}
    reponse = requests.post(url, data=json.dumps(data), headers=headers)
    if reponse.status_code == 200:
        reponse = json.loads(reponse.text)
        return reponse['data']
    else:
        return -1


def bert_classifier(text):
    url = 'http://127.0.0.1:6001/api/bert_recognize'
    data = {"text": text}
    headers = {'Content-Type': 'application/json;charset=utf8'}
    reponse = requests.post(url, data=json.dumps(data), headers=headers)
    if reponse.status_code == 200:
        reponse = json.loads(reponse.text)
        return reponse['data']
    else:
        return -1


def get_topk(sent, data, topk=10):
    # 计算已知句子top-k的相似句子
    # 读取文件
    # data = pd.read_excel(data_path, sheet_name='项目运维统计表')
    result = data.copy()
    request_data = []
    document = []
    for i, row in result.iterrows():
        sent2 = row['content']
        document.append(sent2)
    document_list_split = [list(jieba.cut(doc)) for doc in document]

    bm25_model = BM25_Model(document_list_split)
    query = list(jieba.cut(sent))
    scores = bm25_model.get_documents_score(query)
    document = [document[i] for i in np.array(scores).argsort()[-2 * topk:][::-1]]
    data = data[data.content.isin(document)]
    for s in document:
        text_json = {'sent1': sent, 'sent2': s}
        request_data.append(text_json)

    request_result = similar(request_data)
    df = pd.DataFrame.from_dict(request_result, orient='columns')
    combine_df = data.merge(df, left_on='content', right_on='sent2', how='left')
    # combine_df = pd.concat([data, df[['sent1', 'score']]], axis=1)
    # result.columns = ['score', 'sent1', '运维需求描述']
    # # 新增列,并赋值为None
    # result['score'] = None
    #
    # for i, row in result.iterrows():
    #     sent2 = row['运维需求描述']
    #     text_json = {'sent1': sent, 'sent2': sent2}
    #     score = similar(text_json)
    #     result['score'][i] = score

    # 按score排序
    res = combine_df.sort_values(by='score', ascending=False).drop_duplicates()

    res = res[:topk]
    return res


def format_date():
    time = datetime.now()
    curr_time = datetime.strftime(time, '%Y-%m-%d %H:%M:%S')
    year = str(time.year)
    month = str(time.month)
    return year, month, curr_time


def excelwrite(content_json):
    '''
    写入excel
    :param content_json: 需要写入的内容（list),元素为json
    :return:
    '''

    filename = data_path
    workbook = xlrd.open_workbook(filename, formatting_info=True)
    sheet = workbook.sheet_by_index(0)
    rowNum = sheet.nrows
    newbook = copy(workbook)
    newsheet = newbook.get_sheet(0)

    # 在末尾增加新行
    for i in range(len(content_json)):
        newsheet.write(rowNum + i, 0, content_json[i]['年度'])
        newsheet.write(rowNum + i, 1, content_json[i]['月份'])
        newsheet.write(rowNum + i, 2, content_json[i]['问题发生时间'])
        newsheet.write(rowNum + i, 3, content_json[i]['运维需求描述'])
        newsheet.write(rowNum + i, 4, content_json[i]['运维类别'])
        newsheet.write(rowNum + i, 5, content_json[i]['问题状态'])
        newsheet.write(rowNum + i, 6, content_json[i]['问题处理方式'])

    # 覆盖保存
    newbook.save(filename)


if __name__ == '__main__':
    app = Flask(__name__)

    results = get_db_data()
    data_top = pd.DataFrame()
    for i in range(len(results)):
        data_top.loc[i, 'id'] = results[i][0]
        data_top.loc[i, 'content'] = results[i][1]
        data_top.loc[i, 'user_id'] = results[i][2]
        data_top.loc[i, 'answer_status'] = results[i][3]
        data_top.loc[i, 'admin_id'] = results[i][4]
        data_top.loc[i, 'category_id'] = results[i][5]
    data_top = data_top.where(data_top.notnull(), None)

    message_df = get_message()
    messages = pd.DataFrame()
    for i in range(len(message_df)):
        messages.loc[i, 'message_id'] = message_df[i][0]
        messages.loc[i, 'question_id'] = message_df[i][1]
        messages.loc[i, 'user_id'] = message_df[i][2]
        messages.loc[i, 'identity_id'] = message_df[i][3]
        messages.loc[i, 'create_time'] = message_df[i][4]
        messages.loc[i, 'content'] = message_df[i][5]
    messages = messages.where(messages.notnull(), None)
    messages = messages[['question_id', 'content']]
    messages = messages.rename(columns={'question_id': "id", 'content': 'answer'})
    messages = messages.drop_duplicates(['id'])
    data_top = data_top.merge(messages, how='left')


    @app.route('/api/classifier', methods=['POST', 'GET'])
    def classifier():
        data = {'success': 0}
        result = []
        text = flask.request.get_json()['text']  # 获取文本（运维需求描述）
        print(text)
        # 计算数据库中相似的运维需求描述
        topk_similar = get_topk(text, data_top)
        topk_similar = topk_similar.reset_index(drop=True)
        print(topk_similar)

        # bert 模型预测运维类别
        bert_res = bert_classifier(text)
        bert_type = bert_res['name']
        print(bert_type)

        # 得到最终的运维类别及处理方式
        # temp = pd.DataFrame(columns=topk_similar.columns)
        year, month, curr_time = format_date()
        return_k = 5
        for i in range(return_k):
            res_json = {}
            res_json['年度'] = year
            res_json['月份'] = month
            res_json['问题发生时间'] = curr_time
            res_json['运维需求描述'] = text
            res_json['问题状态'] = '已完成'
            res_json['答案所对应问题编号'] = topk_similar.loc[i, 'id']
            res_json['问题处理方式'] = topk_similar.loc[i, 'answer']
            if bert_res['confidence'] > 0.6:
                res_json['运维类别'] = bert_type
            else:
                res_json['运维类别'] = topk_similar.loc[i, 'category_id']
            result.append(res_json)

        # for i, row in topk_similar.iterrows():
        #     temp = {}
        #     year, month, curr_time = format_date()
        #     temp['年度'] = year
        #     temp['月份'] = month
        #     temp['问题发生时间'] = curr_time
        #     temp['运维需求描述'] = text
        #     temp['问题状态'] = '已完成'
        #     temp['问题处理方式'] = row['问题处理方式']
        #     if row['运维类别'] == bert_type:
        #         temp['运维类别'] = bert_type
        #     # else:
        #     #     temp['运维类别'] = row['运维类别']
        #         result.append(temp)
        if len(result) == 0:
            result = topk_similar[:1].to_json(orient='index', force_ascii=False)
        excelwrite(result)
        data['data'] = result
        data['success'] = 1

        return jsonify(data)


    app.run(host='127.0.0.1', port=6003)
