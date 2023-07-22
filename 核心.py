import flet as ft
import time
import 模块
import os

def main(页面):
    页面.title = 'OpenFrp Client'
    页面.window_width = 500
    页面.window_height = 300

    def btn_click(占位符):
        if 文本框_账户.value:
            账户 = 文本框_账户.value
        else:
            文本框_账户.error_text = "这里需要填写用户名或者邮箱。"
            页面.update()
        if 文本框_密码.value:
            密码 = 文本框_密码.value
        else:
            文本框_密码.error_text = "这里需要填写密码。"
            页面.update()
        if 文本框_账户.value:
            if 文本框_密码.value:
                授权值, 会话值, 登录成功 = 模块.登录(账户, 密码)
                if 登录成功:
                    页面.clean()
                    账户数据 = 模块.获取账户信息(授权值, 会话值)
                    用户名文本 = ft.Text(value='你好，' + 账户数据['data']['username'] + '。')
                    页面.window_width = 1000
                    页面.window_height = 800
                    def 签到(占位符):
                        签到数据 = 模块.签到(授权值, 会话值)
                        if 签到数据['data'] == '你今天已经签到过啦':
                            签到提示 = ft.Text(value="你今天已经签到过了馁。")
                            页面.add(签到提示)
                            time.sleep(3)
                            页面.remove(签到提示)
                        else:
                            签到提示 = ft.Text(value="签到失败。细节：" + 签到数据['msg'])
                            页面.add(签到提示)
                            time.sleep(3)
                            页面.remove(签到提示)
                            print(签到数据)
                    页面.add(用户名文本, ft.ElevatedButton("签到", on_click=签到))
                    隧道数据 = 模块.获取隧道列表(授权值, 会话值)
                    if 隧道数据['data']['total'] == 0:
                        页面.add(ft.Text(value='你目前还没有隧道诶。'))
                    else:
                        页面.add(ft.Text(value='你目前有 ' + str(隧道数据['data']['total']) + ' 条隧道诶。'))
                        def button_clicked(e):
                            output_text.value = f"正在启动 {color_dropdown.value} 。"
                            页面.update()
                            次数 = 0
                            while 次数 != 隧道数据['data']['total']:
                                if color_dropdown.value == 隧道数据['data']['list'][次数]['proxyName']:
                                    模块.启动隧道(账户数据['data']['token'], 隧道数据['data']['list'][次数]['id'])
                                次数 = 次数 + 1
                        次数 = 0
                        隧道选项 = []
                        while 次数 != 隧道数据['data']['total']:
                            print(隧道数据['data']['list'][次数])
                            选项 = ft.dropdown.Option(隧道数据['data']['list'][次数]['proxyName'])
                            隧道选项.append(选项)
                            次数 = 次数 + 1
                        output_text = ft.Text()
                        submit_btn = ft.ElevatedButton(text="启动", on_click=button_clicked)
                        color_dropdown = ft.Dropdown(
                            width = 300,
                            options = 隧道选项
                        )
                        页面.add(color_dropdown, submit_btn, output_text)
                else:
                    页面.controls.append(ft.Text(value="账户名称或者密码错误了哦。", color='red'))
                    页面.update()

    文本框_账户 = ft.TextField(label="用户名或邮箱")
    文本框_密码 = ft.TextField(label="密码")
    提示 = ft.Text(value="演示账户是 test@test.com ，密码相同。")
    页面.controls.append(提示)
    页面.add(文本框_账户, 文本框_密码, ft.ElevatedButton("登录！", on_click=btn_click))
    页面.update()

ft.app(target=main)
