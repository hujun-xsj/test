import requests

def get_proxy():
    return requests.get("http://101.35.19.102:5010/get/").json()

def delete_proxy(proxy):
    requests.get("http://101.35.19.102:5010/delete/?proxy={}".format(proxy))

# your spider code

def getHtml():
    # ....
    retry_count = 5
    proxy = get_proxy().get("proxy")
    while retry_count > 0:
        try:
            html = requests.get('http://www.baidu.com', proxies={"http": "http://{}".format(proxy)})
            # 使用代理访问
            print("尝试次数:"+str(6-retry_count))
            print("代理ip:{}".format(proxy))
            return html
        except Exception:
            retry_count -= 1
    # 删除代理池中代理
    delete_proxy(proxy)
    return None
if __name__ == '__main__':
    print(getHtml().text)