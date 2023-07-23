import os
import time
import zipfile
import datetime
import requests
import threading
import configparser
config = configparser.ConfigParser()

print('BugCraft OpenFrp Client - 你好！这个客户端“使用 OpenFrp OPENAPI”。')
print('请使用“help”了解它可以做什么。')

配置文件名 = 'config.ini'
if os.path.exists(配置文件名):
    print('找到了配置文件，所以先读取一下配置吧。')
    config.read(配置文件名)
else:
    print('找不到配置文件诶……所以先写一个吧。')
    config['账户相关'] = {'账号': 'test@test.com', '密码': 'test@test.com'}
    用户名 = config.get('账户相关', '账号')
    密码 = config.get('账户相关', '密码')
    with open(配置文件名, 'w') as configfile:
        config.write(configfile)

if os.path.exists('frpc.exe'):
    已安装 = True
else:
    已安装 = False

def 下载_frpc():
    if 已安装 == False:
        print('找不到 frpc 诶……所以嘛……')
        print('下载一下，马上搞定。')
        frpc_下载地址 = 'https://sq.oss.imzzh.cn/client/OpenFRP_0.49.0_5cc2e1cc_20230618/frpc_windows_amd64.zip'
        response = requests.get(frpc_下载地址, stream=True)
        if response.status_code == 200:
            with open('frpc.zip', 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print("下载好了馁……")
            print('下载下来是一个压缩包，先解压一下。')
            with zipfile.ZipFile('frpc.zip', 'r') as zip_ref:
                zip_ref.extractall()
            print('解压好了！那么就删除掉原来的压缩包吧。')
            os.remove('frpc.zip')
            os.rename('frpc_windows_amd64.exe', 'frpc.exe')
            print('安装好了，但是需要重启客户端才能使用。')
            print('五秒钟后退出。')
            time.sleep(5)
            exit()
        else:
            print("好像没下下来，不管了。没有下载成功。")
    else:
        print('你已经安装过了诶。')

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
    else:
        print('似乎不对劲……可能是因为账号或者密码错误了。')
    return 授权值, 会话值

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

def 启动隧道(密钥, 序号):
    if 已安装 == True:
        frpc = f"start frpc.exe -u {密钥} -p {序号}"
        os.system(frpc)
    else:
        print('因找不到 frpc 而不能启动隧道。请先运行“install”。')

def 获取节点列表(授权值, 会话值):
    url = "https://of-dev-api.bfsea.xyz/frp/api/getNodeList"
    headers = {
        "Authorization": 授权值
    }
    payload = {
        "session": 会话值
    }
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    return data

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

def 处理输入():
    已登录 = False
    while True:
        输入 = input()
        分解输入 = 输入.split()
        命令长度 = len(分解输入)
        命令已处理 = False
        if 输入 == 'help':
            命令已处理 = True
            帮助 = '''BugCraft OpenFrp Client - Help
    - help | 让我告诉你我可以做什么。
    - login 账号 密码 | 登录，不填写账号密码则使用配置中的登录信息。
    - start 隧道序号 | 启动隧道，需要附加隧道序号才能启动。
    - logout | 登出，同时修改配置中的登录信息为测试账户。
    - install | 安装 OpenFrp 的 frpc ，以便启动隧道。
    - signin | 签到，需要你已经登录了 OpenFrp 的账号。
    - about | 关于你的账户，可以获取你账号的一些信息。
    - proxy | 查看已创建的隧道列表。
    - node | 查看可用的节点列表。
    - new | 创建一个隧道。
    - edit | 修改一个隧道。
    - del 隧道序号 | 根据隧道序号删除一个隧道。
    - cls | 清空屏幕，这会清空已输出的内容。'''
            print(帮助)
        elif 分解输入[0] == 'login':
            命令已处理 = True
            if 已登录 == False:
                if 命令长度 == 3:
                    print('正在使用账号密码登录馁。')
                    授权值, 会话值 = 登录(分解输入[1], 分解输入[2])
                    config['账户相关'] = {'账号': 分解输入[1], '密码': 分解输入[2]}
                    with open(配置文件名, 'w') as configfile:
                        config.write(configfile)
                    print('登录信息已经保存起来了哦。')
                    已登录 = True
                if 命令长度 == 1:
                    print('正在使用配置中的登录信息登录。')
                    账号 = config.get('账户相关', '账号')
                    密码 = config.get('账户相关', '密码')
                    授权值, 会话值 = 登录(账号, 密码)
                    已登录 = True
                else:
                    print('这个命令不是这么用的哦。请使用“help”了解正确用法。')
            else:
                print('不能在已经登录的情况下再次登录哦。')
        elif 分解输入[0] == 'start':
            命令已处理 = True
            if 命令长度 == 2 and 分解输入[1].isdigit():
                if 已登录 == True:
                    序号 = 分解输入[1]
                    print('正在启动序号为 ' + 序号 + ' 的隧道。')
                    账户信息 = 获取账户信息(授权值, 会话值)
                    密钥 = 账户信息['data']['token']
                    启动隧道(密钥, 序号)
                else:
                    print('你需要登录才能启动隧道。')
            else:
                print('这个命令需要一个纯数字的参数。请使用“help”了解正确用法。')
        elif 输入 == 'logout':
            命令已处理 = True
            print('登出了你的账号。现在，你可以重新登录。')
            config['账户相关'] = {'账号': 'test@test.com', '密码': 'test@test.com'}
            with open(配置文件名, 'w') as configfile:
                config.write(configfile)
            授权值, 会话值 = '', ''
            已登录 = False
        elif 输入 == 'install':
            命令已处理 = True
            print('正在安装 OpenFrp 的 frpc 。')
            下载_frpc()
        elif 输入 == 'signin':
            命令已处理 = True
            if 已登录 == True:
                print('正在准备签到，稍等哦。')
                签到结果 = 签到(授权值, 会话值)
                print('签到结果是……')
                print(签到结果)
            else:
                print('没有办法签到，这是因为你还没有登录。')
                print('或者是因为你的账户已经被锁定了。')
        elif 输入 == 'about':
            命令已处理 = True
            if 已登录 == True:
                账户信息 = 获取账户信息(授权值, 会话值)
                if 账户信息['data'] != None:
                    print('成功获取账户信息。')
                    print('名字：' + 账户信息['data']['username'])
                    print('邮箱：' + 账户信息['data']['email'])
                    print('密钥：' + 账户信息['data']['token'])
                    print('权限：' + 账户信息['data']['friendlyGroup'])
                    print('序号：' + str(账户信息['data']['id']))
                    if 账户信息['data']['realname']:
                        print('实名：是')
                    else:
                        print('实名：否')
                else:
                    print('无法获取账户信息。')
            else:
                print('无法获取账户信息，你似乎没有登录诶。')
        elif 输入 == 'proxy':
            命令已处理 = True
            if 已登录 == True:
                隧道列表_json = 获取隧道列表(授权值, 会话值)
                隧道数量 = 隧道列表_json['data']['total']
                print('隧道数量：' + str(隧道数量))
                隧道列表 = 隧道列表_json['data']['list']
                次数 = 0
                while 次数 != 隧道数量:
                    隧道名称 = str(隧道列表[次数]['proxyName'])
                    在线状态 = str(隧道列表[次数]['online'])
                    if 在线状态 == 'True':
                        在线状态 = '\033[1;32m在线\033[0m'
                    else:
                        在线状态 = '\033[1;31m离线\033[0m'
                    print(f'=====[ {次数 + 1} - {隧道名称} - {在线状态} ]=====')
                    隧道序号 = str(隧道列表[次数]['id'])
                    print('隧道序号：' + 隧道序号)
                    隧道类型 = str(隧道列表[次数]['proxyType'])
                    print('隧道类型：' + 隧道类型)
                    本地地址 = str(隧道列表[次数]['localIp'])
                    print('本地地址：' + 本地地址)
                    本地端口 = str(隧道列表[次数]['localPort'])
                    print('本地端口：' + 本地端口)
                    远程端口 = str(隧道列表[次数]['remotePort'])
                    print('远程端口：' + 远程端口)
                    连接地址 = str(隧道列表[次数]['connectAddress'])
                    print('连接地址：' + 连接地址)
                    时间戳 = int(隧道列表[次数]['lastUpdate'])
                    时间 = datetime.datetime.fromtimestamp(时间戳)
                    时间 = 时间.strftime("%Y-%m-%d %H:%M:%S")
                    print('最近更改：' + 时间)
                    数据加密 = str(隧道列表[次数]['useEncryption'])
                    if 数据加密 == 'True':
                        数据加密 = '是'
                    else:
                        数据加密 = '否'
                    print('数据加密：' + 数据加密)
                    数据压缩 = str(隧道列表[次数]['useCompression'])
                    if 数据压缩 == 'True':
                        数据压缩 = '是'
                    else:
                        数据压缩 = '否'
                    print('数据压缩：' + 数据压缩)
                    次数 = 次数 + 1
            else:
                print('无法获取隧道列表，你似乎没有登录诶。')
        elif 输入 == 'node':
            命令已处理 = True
            if 已登录 == True:
                可用节点 = 获取节点列表(授权值, 会话值)
                可用节点 = 可用节点['data']
                节点数量 = 可用节点['total']
                print('节点数量：' + str(节点数量))
                可用节点 = 可用节点['list']
                次数 = 0
                while 次数 != 节点数量:
                    节点 = 可用节点[次数]
                    节点序号 = 节点['id']
                    节点名称 = 节点['name']
                    if 节点['status'] == 200:
                        节点状态 = '\033[1;32m正常\033[0m'
                        if 节点['fullyLoaded']:
                            节点状态 = '\033[1;31m满载\033[0m'
                    else:
                        节点状态 = '\033[1;31m异常\033[0m'
                    print(f'=====[ {节点序号} - {节点名称} - {节点状态} ]=====')
                    print('节点描述：' + 节点['description'])
                    支持协议 = 节点['protocolSupport']
                    协议列表 = ''
                    if 支持协议['tcp'] == True:
                        协议列表 = 协议列表 + 'TCP '
                    if 支持协议['udp'] == True:
                        协议列表 = 协议列表 + 'UDP '
                    if 支持协议['xtcp'] == True:
                        协议列表 = 协议列表 + 'XTCP '
                    if 支持协议['stcp'] == True:
                        协议列表 = 协议列表 + 'STCP '
                    if 支持协议['http'] == True:
                        协议列表 = 协议列表 + 'HTTP '
                    if 支持协议['https'] == True:
                        协议列表 = 协议列表 + 'HTTPS '
                    print('支持协议：' + 协议列表)
                    节点地址 = 节点['hostname']
                    if 节点地址 == '您无权查询此节点的地址':
                        节点地址 = '没有权限'
                    print('节点地址：' + 节点地址)
                    if 'normal' in 节点['group']:
                        需要特权 = '否'
                    else:
                        需要特权 = '是'
                    print('需要特权：' + 需要特权)
                    if 节点['needRealname']:
                        需要实名 = '是'
                    else:
                        需要实名 = '否'
                    print('需要实名：' + 需要实名)
                    次数 = 次数 + 1
            else:
                print('无法获取节点列表，你似乎没有登录诶。')
        elif 输入 == 'new':
            命令已处理 = True
            if 已登录 == True:
                if 命令长度 == 1:
                    节点名称 = input('隧道的名字是？')
                    节点序号 = int(input(f'要让 {节点名称} 用什么节点呢（填写节点序号）？'))
                    本地地址 = input('本地地址是什么？')
                    本地端口 = input('本地端口是多少？')
                    远程端口 = input('远程端口是多少？')
                    通信协议 = input('通信协议是什么（tcp/udp/http/https）？')
                    url = "https://of-dev-api.bfsea.xyz/frp/api/newProxy"
                    headers = {
                        "Authorization": 授权值
                    }
                    payload = {
    "session": 会话值,
    "node_id": 节点序号,
    "name": 节点名称,
    "type": 通信协议,
    "local_addr": 本地地址,
    "local_port": 本地端口,
    "remote_port": int(远程端口),
    "domain_bind": "",
    "dataGzip": "False",
    "dataEncrypt": "False",
    "url_route": "",
    "host_rewrite": "",
    "request_from": "",
    "request_pass": "",
    "custom": ""
}
                    response = requests.post(url, headers=headers, json=payload)
                    data = response.json()
                    if data['flag']:
                        print('修改或创建成功！')
                    else:
                        print('修改或创建失败。')
                    print('细节：' + data['msg'])
                else:
                    print('这个命令不是这样用的哦。')
            else:
                print('在创建隧道前，请先登录哦。')
        elif 输入 == 'edit':
            命令已处理 = True
            if 已登录 == True:
                if 命令长度 == 1:
                    节点名称 = input('隧道的名字是？')
                    节点序号 = int(input(f'要让 {节点名称} 用什么节点呢（填写节点序号）？'))
                    本地地址 = input('本地地址是什么？')
                    本地端口 = input('本地端口是多少？')
                    远程端口 = input('远程端口是多少？')
                    通信协议 = input('通信协议是什么（tcp/udp/http/https）？')
                    代理序号 = input('隧道序号是什么？')
                    url = "https://of-dev-api.bfsea.xyz/frp/api/editProxy"
                    headers = {
                        "Authorization": 授权值
                    }
                    payload = {
                        "name": 节点名称,
                        "node_id": 节点序号,
                        "local_addr": 本地地址,
                        "local_port": 本地端口,
                        "remote_port": 远程端口,
                        "domain_bind": "[]",
                        "dataGzip": False,
                        "dataEncrypt": False,
                        "custom": "",
                        "type": 通信协议,
                        "proxy_id": int(代理序号),
                        "session": 会话值
                    }
                    response = requests.post(url, headers=headers, json=payload)
                    data = response.json()
                    if data['flag']:
                        print('修改或创建成功！')
                    else:
                        print('修改或创建失败。')
                    print('细节：' + data['msg'])
                else:
                    print('这个命令不是这样用的哦。')
            else:
                print('在编辑隧道前，请先登录哦。')
        elif 分解输入[0] == 'del':
            命令已处理 = True
            if 命令长度 == 2 and 分解输入[1].isdigit():
                if 已登录 == True:
                    隧道序号 = 分解输入[1]
                    结果 = 删除隧道(授权值, 会话值, 隧道序号)
                    if 结果['flag']:
                        print('删除成功！')
                        print('细节：' + 结果['msg'])
                    else:
                        print('删除失败。')
                        print('细节：' + 结果['msg'])
                else:
                    print('删除隧道前需要先登录。')
            else:
                print('这个命令不是这样用的馁。')
        elif 输入 == 'cls':
            命令已处理 = True
            os.system('cls')
        elif 命令已处理 == False:
            print('不太理解你的意思。请使用“help”了解我可以做什么。')
            命令已处理 = True

输入线程 = threading.Thread(target=处理输入)
输入线程.start()
