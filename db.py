# 数据库连接和操作的工具方法
import pymysql
def get_connection():
    # TODO:数据库连接
    db=pymysql.connect(host='localhost',
                      user='app',
                      password='app123',
                      database='app')
    cursor = db.cursor()
    return db, cursor


# 在table_name表中data_keys列插入data_list字典列表的值
# data_list中每个元素是一个字典，字典的键和datakeys列表对应
def insert(table_name, data_keys, data_list):
    db, cursor=get_connection()
    cols = ", ".join('{}'.format(k) for k in data_keys)
    val_cols = ', '.join('%({})s'.format(k) for k in data_keys)
    sql="insert into {}(%s) values(%s)".format(table_name)
    res_sql = sql % (cols, val_cols)
    num=0
    for data in data_list:
        try:
            num+=cursor.execute(res_sql, data)
        except:
            pass
    db.commit()
    db.close()
    return num

# 查询table_name表中data_keys列
# cond是条件字典，默认以and连接
def query(data_keys, table_name, cond=None):
    # def query(table_name, data_keys):
    db, cursor=get_connection()
    sql="select %s from %s"
    cols=", ".join('{}'.format(k) for k in data_keys)
    query_sql = sql % (cols,table_name)
    if cond!=None:
        where=" and ".join("{}='{}'".format(k,cond[k]) for k in cond.keys())
        query_sql+=(" where %s" % where)
    cursor.execute(query_sql)
    db.close()
    return cursor

# 按条件字典cond，删除table_name表中元素
# 若字典未空，删除表中所有行
def delete(table_name,cond=None):
    db, cursor=get_connection()
    sql="delete  from %s"
    delete_sql=sql % table_name
    if cond!=None:
        where=" and ".join("{}='{}'".format(k,cond[k]) for k in cond.keys())
        delete_sql+=(" where %s" % where)
    num = cursor.execute(delete_sql)
    db.commit()
    db.close()
    return num

# 按条件字典cond更新table_name
# 更新后的值由modify_key_values字典定义
def update(table_name, modify_key_values, cond):
    db, cursor=get_connection()
    set_values=", ".join("{}='{}'".format(k, modify_key_values[k]) for k in modify_key_values)
    where=" and ".join("{}='{}'".format(k,cond[k]) for k in cond.keys())
    sql="update {} set %s where %s".format(table_name)
    update_sql = sql % (set_values, where)
    num=cursor.execute(update_sql)
    db.commit()
    db.close()
    return num

def execue(sql, param):
    db, cursor=get_connection()
    sql = sql.format(param)
    cursor.execute(sql)
    db.commit()
    db.close()
    return cursor