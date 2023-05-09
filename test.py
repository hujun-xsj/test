import pymysql
import json
db_params = {
    "host": "localhost",
    "user": "app",
    "password": "app123",
    "database": "app"
}
if __name__ == '__main__':
    conn = pymysql.connect(**db_params)
    cursor = conn.cursor()

    # 执行查询语句
    cursor.execute("SELECT MAX(score), MIN(score) FROM app_consistency")

    # 获取查询结果
    result = cursor.fetchone()

    # 计算最大值减去最小值
    score_range = result[0] - result[1]

    # 关闭游标和连接
    cursor.close()
    conn.close()
    print(0.87*score_range)
