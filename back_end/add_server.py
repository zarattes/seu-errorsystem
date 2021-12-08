#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
# author:
# datetime:2021/9/29 15:33
# software: PyCharm
# filename:add_server.py
'''
import flask
import xlrd
from flask import Flask, jsonify
from xlutils.copy import copy

from config import data_path


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

    # 保存
    newbook.save(filename)


if __name__ == '__main__':
    app = Flask(__name__)

    @app.route('/api/add_data', methods=['POST', 'GET'])
    def classifier():
        data = {'success': 0}
        result = []
        text_json = flask.request.get_json()['text_json']  # 获取文本（运维需求描述）

        excelwrite(text_json)

        # data['data'] = result
        data['success'] = 1

        return jsonify(data)

    app.run(host='127.0.0.1', port=6004)
