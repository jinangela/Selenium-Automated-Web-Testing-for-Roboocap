#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
import time

driver = webdriver.PhantomJS(executable_path='C:\\Python27\\Scripts\\phantomjs-1.9.7-windows\\phantomjs.exe')
driver.set_window_size(1400,1000)

url = "http://lsy.roboocap.net/index.php?route=account/login"
driver.get(url)
time.sleep(3) # 等待页面加载完成

# 检查是否成功进入用户登录页面
if driver.current_url=="http://lsy.roboocap.net/index.php?route=account/login":
	print u"成功进入用户登录页面！"
else:
	print u"未进入用户登录页面，请检查！"

# 登录
driver.find_element_by_name("username").clear() # 清空用户名输入框，防止浏览器自动填充
driver.find_element_by_name("username").send_keys("jms_1001")
driver.find_element_by_name("password").send_keys("forgive@h1m")
driver.find_element_by_id("text_login").click()
driver.set_page_load_timeout(60) # 1分钟内未登录成功即为超时
driver.switch_to_default_content() # 跳转到图纸室

# 检测URL是否已经发生变化
while True:
	if driver.current_url != url:
		print u"登录成功！"
		break # 说明已成功跳转到图纸室
	time.sleep(1) # 否则等待1秒

# 获取cookie
cookie = ";".join([item["name"]+"="+item["value"] for item in driver.get_cookies()]) # 还没看懂这个list的添加方法
driver.get_screenshot_as_file('C:\\Users\\Administrator\\Desktop\\learn python\\Test2\\test.png')

driver.find_element_by_xpath('//a[@href="index.php?route=model/info&mid=1977"]').click()
driver.set_page_load_timeout(60) # 1分钟内未跳转即为超时
driver.switch_to_default_content() # 跳转到图纸详情页面

driver.find_element_by_xpath('//a[@href="javascript:add2Quote(1977)"]').click()
driver.set_page_load_timeout(60) # 1分钟内未跳转即为超时
driver.switch_to_default_content() # 跳转到配置页面

"""
# 进入快速生产-上传配置图纸页面
driver.get("http://lsy.roboocap.net/index.php?route=model/produce")
# 检查是否成功进入快速生产-上传配置图纸页面
if driver.current_url=="http://lsy.roboocap.net/index.php?route=model/produce":
	print u"成功进入快速生产-上传配置图纸页面！"
else:
	print u"未进入上传配置图纸页面，请检查！"

# phantomjs自带bug：无法使用send_keys上传文件
# 上传图纸
file_path = "C:\\Users\\Administrator\\Desktop\\learn python\\Test2\\stl\\14349796591742613012.stl" # 注意\需要转义，用\\
driver.find_element_by_class_name("webuploader-element-invisible").send_keys(file_path)
time.sleep(5) # 等待操作完成
# 待解决问题：一次上传多张图纸？

print u"上传成功！"

# 设定配置
# 难点：需要解析js加载动态页面
driver.find_element_by_xpath('//li[@title="3D打印机"]').click() # 选择生产设备（3D打印机）

driver.find_element_by_partial_link_text("abs_icon.jpg").click() # 选择材质 # 待解决问题：随机选择
driver.find_element_by_partial_link_text("#66CCFF").click() # 选择颜色 # 待解决问题：随机选择
driver.find_element_by_partial_link_text("white.jpg").click() # 选择工艺 # 待解决问题：随机选择
driver.find_element_by_class_name("save button-static p0 ma0 float-right").click() # 点击“保存配置”按钮

time.sleep(3) # 等待操作完成

# 检查是否选中相应选项
if driver.find_element_by_xpath('//li[@title="3D打印机"]').get_attribute("class") == "rbc-selected":
	print u"已选中相应选项！"
else:
	print u"未选中相应选项，请检查！"
"""

driver.quit()

