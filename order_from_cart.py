#!/usr/bin/python
# -*- coding: utf-8 -*-

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
import os

ISOTIMEFORMAT='%Y-%m-%d %X'
url_login = "http://www.roboocap.net/index.php?route=account/login"
url_cart = "http://www.roboocap.net/index.php?route=checkout/cart"
url_model_room = "http://www.roboocap.net/index.php?route=model/room"

browser = webdriver.Chrome()
browser.maximize_window() # 最大化浏览器

browser.get(url_login)
time.sleep(3) # 等待页面加载完成

## 从购物车直接下单
def order_in_cart(browser):
	browser.find_element_by_xpath('//button[@class=" button p0 ma0 float-right button-checkout"]').click()
	time.sleep(3)
	browser.find_element_by_xpath('//button[@class="button mb10 p0 size1of1 generate-button"]').click()
	time.sleep(3)
	file = open("C:\\Users\\Administrator\\Desktop\\learn_python\\Selenium1\\order-info.txt",'a')
	file.write(time.strftime(ISOTIMEFORMAT,time.localtime()))
	file.write('\n')
	order_info = browser.find_element_by_xpath('//section[@class="left"]/p').text
	order_info_string = u''.join(order_info).encode('utf-8').strip()
	file.write(order_info_string + '\n')
	file.write("==========\n")
	file.close()
	return

def add_to_cart(browser,num_added = 0,order_num = 1):
	f = open("C:\\Users\\Administrator\\Desktop\\learn_python\\Selenium1\\models2.txt",'r')
	for eachLine in f.readlines():
		id = eachLine[-6:-2]
		xpath = '//a[@href="index.php?route=model/info&mid=' + id + '"]'
		while True:
			try:
				browser.find_element_by_xpath(xpath).click()
				time.sleep(3)
				break
			except TimeoutException:
				print u"啊哦，超时了！即将重试……"
				time.sleep(2)
		
		try:
			while num_added < order_num:
				try:
					browser.find_element_by_xpath('//a[@href="javascript:add2Cart()"]').click()
					time.sleep(1)
					browser.find_element_by_id("add2Cart").click()
					time.sleep(5)
					if browser.find_element_by_xpath('//div[@class="cart-info"]').text == u"已成功将图纸加入购物车":
						num_added += 1
						browser.back()
						if num_added < order_num:
							break
						else:
							f.close()
							return
					else:
						browser.back()
						break
				except TimeoutException:
					print u"啊哦，超时了！即将重试……"
					time.sleep(2)
		except NoSuchElementException:
			browser.back()

# 登录
while True:
	try:
		browser.find_element_by_name("username").clear() # 清空用户名输入框，防止浏览器自动填充
		browser.find_element_by_name("username").send_keys(u"琉璃")
		browser.find_element_by_name("password").send_keys("forget@1t")
		browser.find_element_by_id("text_login").click()
		browser.set_page_load_timeout(60) # 1分钟内未登录成功即为超时
		browser.switch_to.default_content # 跳转到图纸室
		break
	except TimeoutException:
		print u"啊哦，超时了！即将重试……"
		time.sleep(2)

# 检测URL是否已经发生变化
while True:
	if browser.current_url != url_login:
		break # 说明已成功跳转到图纸室
	time.sleep(1) # 否则等待1秒

# 先用随机数生成从购物车下单的图纸数
order_num = random.randint(1,5) # 暂时规定从购物车下单最多只能有五张图纸
print order_num

# 如果购物车中有图纸就直接下单，否则从图纸室中添加相应数量的图纸进购物车下单
browser.get(url_cart)
time.sleep(3)
try:
	num_in_cart = int(browser.find_element_by_class_name("subtotal").text[4:6].rstrip())
	if order_num <= num_in_cart:
		while True:
			try:
				order_in_cart(browser)
				break
			except TimeoutException:
				print u"啊哦，超时了！即将重试……"
				time.sleep(2)
	else:
		add_to_cart(browser,num_in_cart,order_num)
		browser.get(url_cart)
		while True:
			try:
				order_in_cart(browser)
				break
			except TimeoutException:
				print u"啊哦，超时了！即将重试……"
				time.sleep(2)
except NoSuchElementException:
	browser.get(url_model_room)
	num_added = 0
	add_to_cart(browser,num_added,order_num)
	browser.get(url_cart)
	while True:
		try:
			order_in_cart(browser)
			break
		except TimeoutException:
			print u"啊哦，超时了！即将重试……"
			time.sleep(2)

browser.quit()