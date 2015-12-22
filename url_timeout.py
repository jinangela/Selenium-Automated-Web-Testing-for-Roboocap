#!/usr/bin/python
# -*- coding: utf-8 -*-
## 检测超时登录跳转是否正确

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
import time
import random
import threading
import win32gui
import re
import SendKeys

# 登录
def login(browser):
	browser.find_element_by_name("username").clear() # 清空用户名输入框，防止浏览器自动填充
	browser.find_element_by_name("username").send_keys("jms_1001")
	browser.find_element_by_name("password").send_keys("forgive@h1m")
	browser.find_element_by_id("text_login").click()
	browser.set_page_load_timeout(60) # 1分钟内未登录成功即为超时
	browser.switch_to.default_content # 跳转到图纸室
	return

# 退出登录
def logout():
	menu = browser.find_element_by_xpath('//li[@class="gnb top-account hold"]')
	ActionChains(browser).click_and_hold(menu).perform()
	browser.execute_script("document.getElementById('logout').click()")
	return

url = "http://www.roboocap.net/index.php?route=account/login"

urls = []
# 添加所有需要测试的页面
# urls.append("http://www.roboocap.net/index.php?route=model/room") # 图纸室
urls.append("http://www.roboocap.net/index.php?route=order/list") # 工单室
"""
order_status = [1,2,3,4,5,7]
for i in range(len(order_status)):
	urls.append("http://www.roboocap.net/index.php?route=order/list&status=" + str(order_status[i])) # 各种工单状态
urls.append("http://www.roboocap.net/index.php?route=model/info&mid=1977") # 图纸详情（先只测一个页面）
urls.append("http://www.roboocap.net/index.php?route=checkout/cart") # 购物车
urls.append("http://www.roboocap.net/index.php?route=model/produce") # 快速生产-上传配置图纸
urls.append("http://www.roboocap.net/index.php?route=model/roomUp") # 图纸室-上传图纸
urls.append("http://www.roboocap.net/index.php?route=order/list/detail&order_id=715") # 查看工单详情（先只测一个页面）
urls.append("http://www.roboocap.net/index.php?route=price/quoted/result&order_id=1027") # 报价结果（先只测一个页面）

urls.append("http://wlm.roboocap.net/index.php?route=checkout/checkout&order_type=quoted") # 配送&支付
urls.append("http://wlm.roboocap.net/index.php?route=checkout/checkout/payment&order_id=1028") # 等待支付（先只测一个页面）
urls.append("http://wlm.roboocap.net/index.php?route=order/edit/paymentmethod&order_id=1028") # 修改支付方式（先只测一个页面）
urls.append("http://wlm.roboocap.net/index.php?route=order/edit/address&order_id=1028") # 修改收货地址（先只测一个页面）
urls.append("http://wlm.roboocap.net/index.php?route=order/edit/invoice&order_id=1028") # 修改发票信息（先只测一个页面）
urls.append("http://wlm.roboocap.net/index.php?route=order/edit/comment&order_id=1028") # 修改工单备注（先只测一个页面）
urls.append("http://wlm.roboocap.net/index.php?route=order/edit/cancel&order_id=1028") # 取消工单（先只测一个页面）

urls.append("http://www.roboocap.net/index.php?route=order/list/progress&order_id=931") # 查看生产进度（先只测一个页面）
urls.append("http://www.roboocap.net/index.php?route=order/list/shipping&order_id=963") # 查看物流信息（先只测一个页面）
urls.append("http://www.roboocap.net/index.php?route=account/account_set/setting") # 设置
urls.append("http://www.roboocap.net/index.php?route=account/account_set/pwdReset") # 更改密码
urls.append("http://www.roboocap.net/index.php?route=account/account_set/shipping_address") # 寄送至
"""

drivers = []
for i in range(len(urls)):
	drivers.append(webdriver.Chrome())
	drivers[i].maximize_window()
	drivers[i].get(url)
	time.sleep(2) # 等待页面加载完成
	login(drivers[i])

	# 检测URL是否已经发生变化
	while True:
		if drivers[i].current_url != url:
			break # 说明已成功跳转到相应页面
		time.sleep(1) # 否则等待1秒
	
	drivers[i].get(urls[i])
	
time.sleep(3700)

for i in range(len(urls)):
	drivers[i].find_element_by_class_name("upload").click()
	if drivers[i].current_url == url: # 超时退出登录了
		login(drivers[i])
		time.sleep(2)
		drivers[i].find_element_by_class_name("upload").click()
		time.sleep(2)
		if drivers[i].current_url == url:
			print u"重新登录后点击按钮依然需要登录！"
		else:
			print u"测试通过！"
	else:
		print u"超时后未退出登录！URL：" + urls[i]
	drivers[i].quit()

# browser = webdriver.Chrome()
# browser.maximize_window()

# 根据头部有没有导航栏，分别进行检查
"""
try:
	if drivers[i].find_element_by_xpath('//li[@class="gnb top-account hold"]').is_displayed() == True:
		logout()
		# 重新登录
		login()
		time.sleep(2)
		# 判断是否是原页面
		if browser.current_url == urls[k]:
			print u"仍进入原页面"
		else:
			print u"未返回原页面，URL：" + urls[k]
except NoSuchElementException:
	# 重新打开窗口
	browser.quit()
	browser = webdriver.Chrome()
	browser.maximize_window()
	browser.get(urls[k])
	# 重新登录
	login()
	time.sleep(2)
	# 判断是否是原页面
	if browser.current_url == urls[k]:
		print u"仍进入原页面"
	else:
		print u"未返回原页面，URL：" + urls[k]
"""

# browser.find_element_by_xpath('//a[@url="http://wlm.roboocap.net/index.php?route=account/logout"]').click() # Element is not visible so it's not clickable