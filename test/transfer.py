import pymysql
import json
db_params = {
    "host": "localhost",
    "user": "app",
    "password": "app123",
    "database": "app"
}


def update(id, risk):
    # Connect to the database
    conn = pymysql.connect(**db_params)
    try:
        # Update the table
        with conn.cursor() as cursor:
            # Execute the SQL statement
            sql = "UPDATE app_comp SET breakPolicy=%s, breakPolicyDetectionTime=NOW() WHERE id=%s"
            cursor.execute(sql, (risk, id))

        # Commit the changes
        conn.commit()

    finally:
        # Close the connection
        conn.close()

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
    table_name = "app_consist"
    columns = ", ".join(data.keys())
    values = ", ".join(["%s"] * len(data))
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
    # 执行SQL语句
    cursor.execute(sql, list(data.values()))
    # 提交事务并关闭连接
    conn.commit()
    conn.close()
def transfer():
    # 连接到数据库
    conn = pymysql.connect(**db_params)
    cursor = conn.cursor()

    # 执行查询语句
    query = 'SELECT * FROM app_consistency'
    cursor.execute(query)

    # 获取查询结果
    result = cursor.fetchall()

    # 关闭游标和连接
    cursor.close()
    conn.close()
    levellist = []
    with open('../android_premission.json', encoding='utf-8') as f:
        premission_dict = {}
        pre_dict = json.load(f)
        for pre in pre_dict:
            levellist.append(pre_dict[pre][-1])
    # 将结果存储到列表中
    with open('../columns_name.json', encoding='utf-8') as file:
        data = json.load(file)
    cnt = 0
    for row in result:
        columns = []
        columns.append(list(row)[0])
        for i, element in enumerate(list(row)[1:-1]):
            if element < 1:
                columns.append(element)
            else:
                if element == levellist[i]:
                    columns.append(1)
                else:
                    columns.append(2)
                    cnt = cnt + 1
        columns.append(list(row)[-1])
        for i, pre in enumerate(data):
            data[pre] = columns[i]
        data['score'] = int(100 - columns[-1] * 0.87)
        insert(data)
    print(cnt)

if __name__ == '__main__':
    data = [0,0,0,0]
    conn = pymysql.connect(**db_params)
    cursor = conn.cursor()

    # 执行查询语句
    query = 'SELECT * FROM app_consist'
    cursor.execute(query)

    # 获取查询结果
    result = cursor.fetchall()

    # 关闭游标和连接
    cursor.close()
    conn.close()
    for row in result:
        if(list(row)[-1] <60):
            risk = "差"
            data[3] = data[3]+1
        elif(list(row)[-1] <75):
            risk = "合格"
            data[2] = data[2] + 1
        elif(list(row)[-1] < 85):
            risk = "良好"
            data[1] = data[1] + 1
        else:
            risk = "优秀"
            data[0] = data[0] +1
    cnt = 0
    c= 0
    for row in result:
        for i in list(row)[1:-1]:
            if i >0:
                cnt = cnt+1
            if i == 0:
                c = c+ 1
    print(c)
    print(cnt)
    print(cnt - 5312)
    print(5312)
    print(data)
    # 输出结果
