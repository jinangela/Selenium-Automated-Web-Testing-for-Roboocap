#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import random
import threading
import win32gui
import re
import SendKeys
import os

ISOTIMEFORMAT='%Y-%m-%d %X'
url_login = "http://admin.oneooone.com/index.php?route=common/login"

browser = webdriver.Chrome()
browser.maximize_window() # 最大化浏览器

browser.get(url_login)
time.sleep(3) # 等待页面加载完成

# 登录
while True:
	try:
		# 清空输入框，防止浏览器自动填充
		browser.find_element_by_name("username").clear()
		browser.find_element_by_name("password").clear()
		
		browser.find_element_by_name("username").send_keys("test")
		browser.find_element_by_name("password").send_keys("222222")
		browser.find_element_by_xpath('//button[@class="btn btn-primary"]').click()
		browser.set_page_load_timeout(60) # 1分钟内未登录成功即为超时
		browser.switch_to.default_content # 跳转到首页
		break
	except TimeoutException:
		print u"啊哦，超时了！即将重试……"
		time.sleep(2)

# 检测URL是否已经发生变化
while True:
	if browser.current_url != url_login:
		break # 说明已成功跳转
	time.sleep(1) # 否则等待1秒

# 进入 工单管理
browser.find_element_by_xpath('//button[@class="btn btn-primary navbar-btn"]').click()
time.sleep(3)
browser.set_page_load_timeout(60) # 1分钟内未跳转即为超时
browser.switch_to.default_content # 跳转到工单管理页面

# 查看全部工单
browser.find_element_by_xpath('//div[@class="status-list"]/a[9]').click()
time.sleep(3)

# 打开文件填写测试日期
file = open("C:\\Users\\Administrator\\Desktop\\learn_python\\Selenium2\\settings_and_gcode_info.txt",'a')
file.write(time.strftime(ISOTIMEFORMAT,time.localtime()))
file.write('\n')

# 查看用户名为jms_1001、琉璃和海盗不乖的所有工单
for i in range(9): # 页码
	if i == 1:
		# 进入下一页
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(3)
		browser.find_element_by_xpath('//div[@class="plinks"]/a[1]').click()
		time.sleep(3)
	if i > 1:
		# 进入下一页
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(3)
		browser.find_element_by_xpath('//div[@class="plinks"]/a[13]').click()
		time.sleep(3)
	for j in range(20): # 行数
		element = browser.find_element_by_xpath('//div[' + str(j+1) + ']/div[@class="middle"][2]').text
		if element == "jms_1001" or element == u"琉璃" or element == u"海盗不乖":
			if browser.find_element_by_xpath('//div[' + str(j+1) + ']/div[@class="large"][1]').text != u"正在报价":
				element = browser.find_element_by_xpath('//div[' + str(j+1) + ']/div[@class="middle"][1]').text
				string = u''.join(u"工单编号：" + element).encode('utf-8')
				file.write(string + '\t')
				element = browser.find_element_by_xpath('//div[' + str(j+1) + ']/div[@class="middle"][2]').text
				string = u''.join(u"用户昵称：" + element).encode('utf-8')
				file.write(string + '\t')
				element = browser.find_element_by_xpath('//div[' + str(j+1) + ']/div[@class="large"][1]').text
				string = u''.join(u"工单状态：" + element).encode('utf-8')
				file.write(string + '\n\n')
				
				element = browser.find_element_by_xpath('//div[' + str(j+1) + ']/div[@class="last"]/a[@class="action tr glyphicon glyphicon-wrench"]')
				if j > 9:
					browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
					time.sleep(3)
					element.click()
					time.sleep(3) # 进入工单概要
				else:
					element.click()
					time.sleep(3)
				
				# 读取图纸配置
				file.write(u''.join(u"用户选择的图纸配置：").encode('utf-8') + '\n')
				for it_user in range(20): # 最多上传20张图纸
					try:
						for k in range(6):
							string = u''.join(browser.find_element_by_xpath('//div[@class="paper"][' + str(it_user+1) + ']/div[' + str(k+1) + ']').text).encode('utf-8')
							file.write(string + '\n')
						file.write('\n')
					except NoSuchElementException:
						break
				file.write('==========\n')
				
				# 读取生产配置与Gcode信息
				browser.find_element_by_xpath('//div[@class="handle-list"]/a[2]').click()
				time.sleep(3)
				file.write(u''.join(u"生产配置与Gcode信息：").encode('utf-8') + '\n')
				for it_paper in range(20): # 最多上传20张图纸
					try:
						string = u''.join(browser.find_element_by_xpath('//table[@id="option-value"][' + str(it_paper+1) + ']/thead/tr/td[@class="left"][1]').text).encode('utf-8')
						file.write(string + '\t')
						string = u''.join(browser.find_element_by_xpath('//table[@id="option-value"][' + str(it_paper+1) + ']/thead/tr/td[@class="left"][2]').text).encode('utf-8')
						file.write(string + '\n')
						for it in range(4):
							try:
								string = u''.join(browser.find_element_by_xpath('//table[@id="option-value"][' + str(it_paper+1) + ']/tfoot/tr[' + str(it+1) + ']/td[@class="left"]').text).encode('utf-8')
								file.write(string + '\n')
							except NoSuchElementException:
								file.write(u''.join(u"没有找到配置信息，请检查该工单！\n").encode('utf-8'))
						file.write('\n')
					except NoSuchElementException:
						break
				file.write('==========\n')
				
				# 读取询价结果
				browser.find_element_by_xpath('//div[@class="handle-list"]/a[3]').click()
				time.sleep(3)
				file.write(u''.join(u"图纸询价结果：").encode('utf-8') + '\n')
				for it_paper in range(20): # 最多上传20张图纸
					# xpath = 
					try:
						string = u''.join(browser.find_element_by_xpath('//table[@id="option-value"][' + str(it_paper+1) + ']/thead/tr/td[@class="left"][1]').text).encode('utf-8')
						file.write(string + '\t')
						string = u''.join(browser.find_element_by_xpath('//table[@id="option-value"][' + str(it_paper+1) + ']/thead/tr/td[@class="left"][2]').text).encode('utf-8')
						file.write(string + '\n')
						string = u''.join(browser.find_element_by_xpath('//table[@id="option-value"][' + str(it_paper+1) + ']/tfoot/tr/td[@class="left"][1]').text).encode('utf-8')
						file.write(string + '\n')
						
						try:
							if browser.find_element_by_xpath('//table[@id="option-value"][' + str(it_paper+1) + ']/tfoot/tr/td[@class="left"][2]').is_displayed() == True:
								file.write(u''.join(u"生产性分析：").encode('utf-8'))
								"""
								# 难点：获取下拉框中被选中项的值
								# 如果知道图纸编号与order_model_id的关系，可以用javascript直接获取
								# 笨办法：用catch exception的办法遍历所有index查找selected —— 失败，因为selected不是紧跟index的（即中间不是空格）
								for it_index in range(5):
									try:
										string = u''.join(browser.find_element_by_xpath('//table[@id="option-value"][' + str(it_paper+1) + \
										']/tfoot/tr/td[@class="left"][2]/div[@class="td-right select-status"]/select[@class="status"]\
										/option[@value="' + str(it_index) + '" selected]').text).encode('utf-8')
										file.write(string + '\n')
										break
									except NoSuchElementException:
										pass
								"""
								select = Select(browser.find_element_by_xpath('//table[@id="option-value"][' + str(it_paper+1) + \
								']/tfoot/tr/td[@class="left"]/div[@class="td-right select-status"]/select[@class="status"]'))
								string = u''.join(select.first_selected_option.text).encode('utf-8')
								file.write(string + '\n')
								
								# 查看报价
								try:
									if browser.find_element_by_xpath('//table[@id="option-value"][' + str(it_paper+1) + \
									']/tfoot/tr/td[@class="left"]/div[@class="td-right price-hide"]').is_displayed() == True:
										string = u''.join(browser.find_element_by_xpath('//table[@id="option-value"][' + str(it_paper+1) + \
										']/tfoot/tr/td[@class="left"]/div[@class="td-right price-hide"]/input').get_attribute("value")).encode('utf-8')
										file.write(u''.join(u"报价：").encode('utf-8'))
										file.write(string + '\n')
								except NoSuchElementException:
									pass
								
								# 查看图纸错误信息或图纸修改建议
								try:
									xpath1 = '//table[@id="option-value"][' + str(it_paper+1) + \
									']/tfoot/tr/td[@class="left"]/div[@class="td-right repair-hide"]/p'
									if browser.find_element_by_xpath(xpath1).is_displayed() == True:
										xpath2 = '//table[@id="option-value"][' + str(it_paper+1) + \
										']/tfoot/tr/td[@class="left"]/div[@class="td-right repair-hide"]/textarea'
										string = u''.join(browser.find_element_by_xpath(xpath2).text).encode('utf-8')
										if browser.find_element_by_xpath(xpath1).text == u"图纸错误信息":
											file.write(u''.join(u"图纸错误信息：").encode('utf-8'))
											file.write(string + '\n')
										if browser.find_element_by_xpath(xpath1).text == u"图纸修改建议":
											file.write(u''.join(u"图纸修改建议：").encode('utf-8'))
											file.write(string + '\n')
								except NoSuchElementException, e:
									print e
								
						except NoSuchElementException:
							file.write(u''.join(u"没有找到询价结果，请检查该工单！\n").encode('utf-8'))
						file.write('\n')
					except NoSuchElementException:
						break
				file.write('========================================\n')
				
				# 返回全部工单
				browser.find_element_by_xpath('//button[@class="btn btn-primary navbar-btn"]').click()
				time.sleep(3)
				browser.find_element_by_xpath('//div[@class="status-list"]/a[9]').click()
				time.sleep(3)
				
				# 返回当前循环所在页面
				if i > 0:
					browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
					time.sleep(3)
					browser.find_element_by_xpath('//div[@class="plinks"]/a[' + str(i) + ']').click()
					time.sleep(3)

file.close()
browser.quit()