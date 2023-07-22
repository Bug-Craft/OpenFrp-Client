import requests
import os

def 登录(账号, 密码):
    print('正在尝试进行登录……')
    print('账号：' + 账号)
    print('密码：' + 密码)
    url = "https://of-dev-api.bfsea.xyz/user/login"
    payload = {
        "user": 账号,
        "password": 密码
    }
    response = requests.post(url, json=payload)
    data = response.json()
    授权值 = response.headers.get('Authorization')
    会话值 = data['data']
    if data['data'] != None:
        print('登录好了！')
        print('授权值是：' + 授权值)
        print('会话值是：' + 会话值)
        print('请记住：不要向他人泄露你的账号、密码，还有授权值和会话值。')
        return 授权值, 会话值, True
    else:
        print('似乎不对劲……可能是因为账号或者密码错误了。')
        return 授权值, 会话值, False

def 签到(授权值, 会话值):
    url = "https://of-dev-api.bfsea.xyz/frp/api/userSign"
    headers = {
        "Authorization": 授权值
    }
    payload = {
        "session": 会话值
    }
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    return data

def 获取账户信息(授权值, 会话值):
    url = "https://of-dev-api.bfsea.xyz/frp/api/getUserInfo"
    headers = {
        "Authorization": 授权值
    }
    payload = {
        "session": 会话值
    }
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    return data

def 启动隧道(密钥, 序号):
    frpc = f"start frpc.exe -u {密钥} -p {序号}"
    os.system(frpc)

def 删除隧道(授权值, 会话值, 隧道序号):
    url = "https://of-dev-api.bfsea.xyz/frp/api/removeProxy"
    headers = {
        "Authorization": 授权值
    }
    payload = {
        "proxy_id": 隧道序号,
        "session": 会话值
    }
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    return data

def 获取隧道列表(授权值, 会话值):
    url = "https://of-dev-api.bfsea.xyz/frp/api/getUserProxies"
    headers = {
        "Authorization": 授权值
    }
    payload = {
        "session": 会话值
    }
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    return data
