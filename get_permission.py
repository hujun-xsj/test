import os
from tqdm import tqdm
from androguard.misc import APK

from db import execue, insert
from util import permission_list

def get_permissions(uuid):
    apk_filepath="F:/app/{}.apk".format(uuid)
    a = APK(apk_filepath)
    prelist = a.get_permissions()
    permission_apply = [i[i.rfind(".")+1:] for i in prelist if i.startswith("android.permission")]
    permission_vector = list(map(lambda x: int(x in permission_apply),permission_list))
    return (permission_vector)

def update_single_app_permissoin(uuid):
    pers = get_permissions(uuid)
    per_info={i:j for i,j in zip(permission_list, pers)}
    per_info['id']=uuid
    insert("app_permission", ["id"]+permission_list, [per_info])


def isAnalysize(x, have_analysize):
    return x not in have_analysize

def get_toAnalysize_apk_id():
    sql = "select id from app_permission"
    c = execue(sql,None)
    have_analysize= list(map(lambda x:x[0], c.fetchall()))
    have_download = list(map(lambda x:x.split('.')[0], os.listdir("F://app")))
    urls=list(filter(lambda x: isAnalysize(x, have_analysize), have_download))
    return urls


# 更新权限表
if __name__=="__main__":
    toAnalysize=get_toAnalysize_apk_id()
    for uuid in tqdm(toAnalysize):
        update_single_app_permissoin(uuid)