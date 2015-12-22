#!/usr/bin/python
# -*- coding: utf-8 -*-
## 从图纸详情页面点击立即询价

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

browser.get(url_login)
time.sleep(3) # 等待页面加载完成

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

browser.get("http://www.roboocap.net/index.php?route=model/info&mid=1998")
time.sleep(3)

browser.find_element_by_xpath('//a[@href="javascript:add2Quote(\'1998\')"]').click()
time.sleep(3)

# 选择配置
# 选择生产设备（3D打印机）
browser.find_element_by_xpath('//li[@title="3D打印机"]').click()

# 选择材质
material_list = ["ABS","PLA"]
material_index = random.randint(0,1)
material_xpath = "//li[@title=\"" + material_list[material_index] + "\"]"
browser.find_element_by_xpath(material_xpath).click()

# 选择颜色
color_list = ["天依蓝","DarkSalmon","Crimson","Pink","DeepPink","Tomato","PeachPuff","Orchid","Fuchsia","DarkMagenta","LawnGreen","LightGreen",\
"Green","Teal","PaleTurquoise","SteelBlue","RoyalBlue"]
color_index = random.randint(0,16)
color_xpath = "//li[@title=\"" + color_list[color_index] + "\"]"
browser.find_element_by_xpath(color_xpath).click()

# 选择工艺
technology_list = ["不做处理","化学抛光","磨砂抛光"]
technology_index = random.randint(0,2)
technology_xpath = "//li[@title=\"" + technology_list[technology_index] + "\"]"
browser.find_element_by_xpath(technology_xpath).click()

"""
# 填写数量（选填）
quantity_number = random.randint(0,1000) # 随机决定是否更改数量，等于0则不更改，使用默认值1，否则更改
if quantity_number != 0:
	quantity = browser.find_element_by_xpath('//input[@form-key="quantity"]')
	quantity.clear() # 一定要先清空，否则会在1之后输入，如果输入的是3位数，就会自动修正成1000
	quantity.send_keys(quantity_number)

# 填写图纸补充说明（选填）
intro_index = random.randint(0,1) # 随机决定是否填写图纸补充说明，等于1则填写，等于0则不填写
if intro_index == 1:
	browser.find_element_by_xpath('//div[@form-key="comment"]/textarea').send_keys(u"测试数据")

# 插入附件（选填）
attach_number = random.randint(0,8) # 随机决定是否插入附件，等于0则不插入附件，否则插入数量为attach_number的附件
attach_files = ["scrapy.pdf","3fd15360d78d6f8d8cb10d3c.gif","53f60624e8d0836cd507428b.gif","4d086e061d950a7bf524513b0ad162d9f2d3c938.jpg",\
"DSC_0396.JPG","test.png","selenium-java-2.46.0.zip","selenium-remote-control-1.0.3.rar"]
if attach_number != 0:
	attach_index = random.sample(attach_files,attach_number)
	for i in range(attach_number):
		attach_path = "C:\\Users\\Administrator\\Desktop\\learn_python\\Selenium1\\attach\\" + attach_index[i]
		attach_element = browser.find_element_by_xpath('//a[@id="WU_FILE_0-attach"]')
		th = threading.Thread(target = _action_on_trigger_element, args = [attach_element]) # 没看懂这个thread
		th.start()
		time.sleep(1)
		
		# Call WindowFinder Class
		win = WindowFinder()
		win.find_window_wildcard(".*OPEN.*")
		# win.set_foreground() # 待解决问题：如何Focus在“打开”对话框窗口？（否则一旦离开去做别的事情，就无法成功上传附件）
		key = "{ENTER}"
		SendKeys.SendKeys(attach_path)
		SendKeys.SendKeys(key)
		if attach_path[-3:] == "rar" or attach_path[-3:] == "zip":
			time.sleep(150)
		else:
			time.sleep(3)
"""
time.sleep(3) # 等待操作完成
browser.find_element_by_xpath('//button[@value="保存配置"]').click() # 点击“保存配置”按钮

# 填写询价手机号码（选填）
phone_index = random.randint(0,1) # 随机决定是否填写询价手机号码，等于1则填写，等于0则不填写
if phone_index == 1:
	browser.find_element_by_id("commit-phone").send_keys("18100614031")
time.sleep(3) # 等待操作完成

# 提交询价工单
browser.find_element_by_id("commit-button").click()
browser.set_page_load_timeout(60) # 1分钟内未跳转即为超时
browser.switch_to.default_content # 跳转到询价后页面
time.sleep(3) # 等待操作完成

file = open("C:\\Users\\Administrator\\Desktop\\learn_python\\Selenium1\\order-info.txt",'a')
file.write(time.strftime(ISOTIMEFORMAT,time.localtime()))
file.write('\n')
order_info = browser.find_element_by_xpath('//div[@class="left-content"]/p').text
order_info_string = u''.join(order_info).encode('utf-8').strip()
file.write(order_info_string + '\n')
file.write("==========\n")
file.close()

browser.quit()