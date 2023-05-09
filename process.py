from androguard.misc import APK
import json
import os
import re
import pymysql
def get_premission(filePath):
    apk = APK(filePath)
    return (apk.get_permissions())

def insert(data):
    db_params = {
        "host": "localhost",
        "user": "app",
        "password": "app123",
        "database": "app"
    }
    # 连接到数据库
    conn = pymysql.connect(**db_params)
    cursor = conn.cursor()

    # 构造SQL语句
    table_name = "app_consistency"
    columns = ", ".join(data.keys())
    values = ", ".join(["%s"] * len(data))
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
    # 执行SQL语句
    cursor.execute(sql, list(data.values()))
    # 提交事务并关闭连接
    conn.commit()
    conn.close()

def compare(policyPath,filename,premission_dict):
    with open(os.path.join(policyPath, filename),'r',encoding='utf-8') as f:
        content = f.read()
    with open('columns_name.json', encoding='utf-8') as file:
        columns = json.load(file)
        columns['id'] = filename.split(".")[0]
        score = 0
        for premission in premission_dict:
            count = premission_dict[premission][-1]
            for key in premission_dict[premission][:-2]:
                if(len(re.findall(key, content))>0):
                    count = 0
                    break
            if(count!=0):
                with open('classify.json', encoding='utf-8') as file:
                    class_dict = json.load(file)
                    cnt = 0
                    for word in class_dict[premission_dict[premission][-2]][:-1]:
                        if (len(re.findall(word, content)) > 0):
                            cnt = 1
                    if(cnt == 0):
                        count = count + class_dict[premission_dict[premission][-2]][-1]
                        columns[premission.rsplit(".", 1)[-1]] = 2
                    else:
                        columns[premission.rsplit(".", 1)[-1]] = 1
            else:
                columns[premission.rsplit(".", 1)[-1]] = 0
            score = score + count
        columns['score'] = int(100 - score * 0.87)
        print(columns)
        insert(columns)

def traverse_dir(dirPath,policyPath):
    num = 0
    for filename in os.listdir(dirPath):
        if filename.endswith('.apk'):
            premission_list = get_premission(os.path.join(dirPath, filename))
            with open('android_premission.json', encoding='utf-8') as f:
                premission_dict = {}
                json_dict = json.load(f)
                for premission in premission_list:
                    try:
                        if premission in json_dict.keys():
                            premission_dict[premission] = json_dict[premission]
                    except:
                        pass
                num = num +1
                compare(policyPath,filename.split(".")[0]+'.txt',premission_dict)
                print(num)
if __name__ == '__main__':
    # traverse_dir(r'G:\app',r'G:\policy')
    traverse_dir(r'E:\app\test', r'E:\app\test')