# coding=gbk
import pymysql
import pandas as pd

def get_db_data():
    # �����ݿ�����
    db = pymysql.connect(host='202.112.23.252', user='root', password='bdcc.11235813', database='bdcc', port=53306)
    # ʹ��cursor()������ȡ�����α�
    cursor = db.cursor()

    # SQL ��ѯ���
    sql = f"SELECT * FROM error_question"

    try:
        # ִ��SQL���
        cursor.execute(sql)
        # ��ȡ���м�¼�б�
        results = cursor.fetchall()
        db.close()
        return results
    except:
        print("Error: unable to fetch data")
        db.close()
        return None

def get_message():
    # �����ݿ�����
    db = pymysql.connect(host='202.112.23.252', user='root', password='bdcc.11235813', database='bdcc', port=53306)
    # ʹ��cursor()������ȡ�����α�
    cursor = db.cursor()

    # SQL ��ѯ���
    sql = f"SELECT * FROM message"

    try:
        # ִ��SQL���
        cursor.execute(sql)
        # ��ȡ���м�¼�б�
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