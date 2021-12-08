# coding=gbk
import pymysql
import pandas as pd

def get_db_data():
    # 打开数据库连接
    db = pymysql.connect(host='202.112.23.252', user='root', password='bdcc.11235813', database='bdcc', port=53306)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = f"SELECT * FROM error_question"

    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        db.close()
        return results
    except:
        print("Error: unable to fetch data")
        db.close()
        return None

def get_message():
    # 打开数据库连接
    db = pymysql.connect(host='202.112.23.252', user='root', password='bdcc.11235813', database='bdcc', port=53306)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = f"SELECT * FROM message"

    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        db.close()
        return results
    except:
        print("Error: unable to fetch data")
        db.close()
        return None

if __name__ == '__main__':
    results = get_db_data()
    data = pd.DataFrame()
    for i in range(len(results)):
        data.loc[i, 'message_id'] = results[i][0]
        data.loc[i, 'question_id'] = results[i][1]
        data.loc[i, 'user_id'] = results[i][2]
        data.loc[i, 'identity_id'] = results[i][3]
        data.loc[i, 'create_time'] = results[i][4]
        data.loc[i, 'content'] = results[i][5]

    print(data)