#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
import time
import random
import threading
import win32gui
import re
import SendKeys

def _action_on_trigger_element(_element):
	_element.click()

class WindowFinder:
    # Class to find and make focus on a particular Native OS dialog/Window
    def __init__ (self):
        self._handle = None

    def find_window(self, class_name, window_name = None):
    # Pass a window class name & window name directly if known to get the window
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
    # Call back func which checks each open window and matches the name of window using reg ex
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) != None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
    # This function takes a string as input and calls EnumWindows to enumerate through all open windows
        # self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
    # Get the focus on the desired open window
        win32gui.SetForegroundWindow(self._handle)

browser = webdriver.Chrome()
browser.maximize_window() # 最大化浏览器

url = "http://www.roboocap.net/index.php?route=account/login"
browser.get(url)
time.sleep(3) # 等待页面加载完成

# 登录
browser.find_element_by_name("username").clear() # 清空用户名输入框，防止浏览器自动填充
browser.find_element_by_name("username").send_keys("jms_1001")
browser.find_element_by_name("password").send_keys("forgive@h1m")
browser.find_element_by_id("text_login").click()
browser.set_page_load_timeout(60) # 1分钟内未登录成功即为超时
browser.switch_to.default_content # 跳转到图纸室

# 检测URL是否已经发生变化
while True:
	if browser.current_url != url:
		break # 说明已成功跳转到图纸室
	time.sleep(1) # 否则等待1秒

# 获取cookie
cookie = ";".join([item["name"]+"="+item["value"] for item in browser.get_cookies()]) # 还没看懂这个list的添加方法

# 点击“传图生产”进入上传配置图纸页面
browser.find_element_by_class_name("upload").click()
browser.set_page_load_timeout(60) # 1分钟内未跳转即为超时
browser.switch_to.default_content # 跳转到上传配置图纸页面

# 检测URL是否已经发生变化
while True:
	if browser.current_url == "http://www.roboocap.net/index.php?route=model/produce":
		break # 说明已成功跳转到上传配置图纸页面
	time.sleep(1) # 否则等待1秒

time.sleep(3) # 等待页面加载完成

file_list = ["order_model_id.png","test.py","超大.stl","一张空图纸.jpg"] # 中文名有问题
# 上传1张图纸
def file_upload(file_index):
	file_path = "C:\\Users\\Administrator\\Desktop\\learn_python\\Test2\\stl_exception\\" + file_list[file_index] # 注意\需要转义，用\\
	browser.find_element_by_class_name("webuploader-element-invisible").send_keys(file_path)
	time.sleep(2) # 等待操作完成
	return

for file_index in range(3):
	file_upload(file_index)
	if file_list[file_index] != "超大.stl": # 上传的文件格式有问题
		if browser.find_element_by_xpath('//div[@class="lightbox-body"]/section[@class="section-inputfields"]/p').text \
		== u"支持上传的文件格式是 stl，" + file_list[file_index] + u" 将不会上传。":
			browser.find_element_by_id("confirmBox").click() # 点击“确定”
		else:
			print u"出错了！请检查"
	else: # 上传的文件超出512MB
		if browser.find_element_by_xpath('//div[@class="lightbox-body"]/section[@class="section-inputfields"]/p').text \
		== u"可以上传的文件大小最大是512 MB，大小超出的文件 " + file_list[file_index] + u" 将不会上传。":
			browser.find_element_by_id("confirmBox").click() # 点击“确定”
		else:
			print u"出错了！请检查"

browser.quit()
		
		

browser.quit()
print u"一张图纸上传成功，已生成询价工单！"