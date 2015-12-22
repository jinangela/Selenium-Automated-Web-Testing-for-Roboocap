#!/usr/bin/python
# -*- coding: utf-8 -*-
## 快速生产-上传配置图纸-上传多张图纸

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

f = open("C:\\Users\\Administrator\\Desktop\\learn_python\\Selenium1\\order-info.txt",'a')
f.write(time.strftime(ISOTIMEFORMAT,time.localtime()))
f.write(u''.join(u"\t快速生产-上传配置图纸-上传多张图纸").encode('utf-8'))
f.write(u''.join(u"\t账号：jms_test").encode('utf-8'))
f.write('\n\n')

# 登录
while True:
	try:
		browser.find_element_by_name("username").clear() # 清空用户名输入框，防止浏览器自动填充
		browser.find_element_by_name("username").send_keys(u"jms_test")
		browser.find_element_by_name("password").send_keys("forget@1t")
		browser.find_element_by_id("text_login").click()
		browser.set_page_load_timeout(60) # 1分钟内未登录成功即为超时
		browser.switch_to.default_content # 跳转到图纸室
		break
	except TimeoutException:
		print "啊哦，超时了！即将重试……"
		time.sleep(2)

# 检测URL是否已经发生变化
while True:
	if browser.current_url != url:
		break # 说明已成功跳转到图纸室
	time.sleep(1) # 否则等待1秒

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

# 上传多张图纸，上传的同时选择配置
file_list = ["1278_0_20mmbox.stl","1334_0_MarsBase_waterstorage.STL","14303829918605020.stl","1410587887402684744.STL","14110509732038630898.STL",\
"14162822731628411061.stl","1417848498574959174.stl","14208844761507865345.stl","1430382939371311859.stl","1430382944314873357.stl",\
"14309042721475161403.stl","14321152701553900666.stl","1432281592469984352.stl","14322835061104361894.stl","1432344608926086198.stl",\
"1432738881831267669.stl","14327394791625924388.stl","1433987611759123027.stl","14340073111112743688.stl","14349796591742613012.stl"]
file_path = "C:\\Users\\Administrator\\Desktop\\learn_python\\Selenium1\\stl\\"  # 注意\需要转义，用\\
number_index = random.randint(1,20) # 上传图纸数目
file_index = random.sample(file_list,number_index)

for i in range(number_index):
	file_path_upload = file_path + file_index[i]
	browser.find_element_by_class_name("webuploader-element-invisible").send_keys(file_path_upload)
	time.sleep(1) # 等待操作完成
	f.write(u''.join(u"已上传：" + file_index[i]).encode('utf-8'))
	f.write('\n')
	
	xpath1 = "//li[@id='WU_FILE_" + str(i) + "']/div[@class='uflist-bottom']/div[@class='configure']" \
	+ "/ul/li/ol[@class='rbc-clear rbc-img form-item']/li[@title=\""
	xpath11 = "//li[@id='WU_FILE_" + str(i) + "']/div[@class='uflist-bottom']/div[@class='configure']" \
	+ "/ul/li/ol[@class='rbc-clear rbc-img form-item materials']/li[@title=\""
	xpath2 = "//li[@id='WU_FILE_" + str(i) + "']/div[@class='uflist-bottom']/div[@class='configure']/ul/li"
	button_xpath = "//li[@id='WU_FILE_" + str(i) + "']/div[@class='uflist-bottom']/div[@class='uflist-button mt10 mb10 config-close']" \
	+ "/button[@value='保存配置']"
	
	# 选择生产设备（3D打印机）
	browser.find_element_by_xpath(xpath1 + "3D打印机\"]").click()

	# 选择材质
	material_list = ["ABS","PLA"]
	# material_index = random.randint(0,1)
	material_xpath = xpath11 + material_list[1] + "\"]"
	browser.find_element_by_xpath(material_xpath).click()
	browser.switch_to.default_content # 等待颜色出来

	# 选择颜色
	color_list = ["天依蓝","DarkSalmon","Crimson","Pink","DeepPink","Tomato","PeachPuff","Orchid","Fuchsia","DarkMagenta","LawnGreen","LightGreen",\
	"Green","Teal","PaleTurquoise","SteelBlue","RoyalBlue"]
	# color_index = random.randint(0,16)
	color_xpath = xpath1 + color_list[0] + "\"]"
	time.sleep(2) # 现在选了材质才能选颜色，因此需要等待一会儿
	browser.find_element_by_xpath(color_xpath).click()

	# 选择工艺
	technology_list = ["不做处理","化学抛光","磨砂抛光"]
	technology_index = random.randint(0,2)
	technology_xpath = xpath1 + technology_list[technology_index] + "\"]"
	browser.find_element_by_xpath(technology_xpath).click()
	
	# 填写数量（选填）
	quantity_number = random.randint(0,1000) # 随机决定是否更改数量，等于0则不更改，使用默认值1，否则更改
	if quantity_number != 0:
		quantity = browser.find_element_by_xpath(xpath2 + '/div[@class="price form-item"]/input[@form-key="quantity"]')
		quantity.clear() # 一定要先清空，否则会在1之后输入，如果输入的是3位数，就会自动修正成1000
		quantity.send_keys(quantity_number)
	
	# 填写图纸补充说明（选填）
	# intro_index = random.randint(0,1) # 随机决定是否填写图纸补充说明，等于1则填写，等于0则不填写
	intro_index = 1
	intro_num = random.randint(1,200)
	if intro_index == 1:
		browser.find_element_by_xpath(xpath2 + '/div[@form-key="comment"]/textarea').send_keys(u"测试数据"*intro_num)
	
	"""
	# 插入附件（选填）
	attach_number = random.randint(0,8) # 随机决定是否插入附件，等于0则不插入附件，否则插入数量为attach_number的附件
	attach_files = ["scrapy.pdf","3fd15360d78d6f8d8cb10d3c.gif","53f60624e8d0836cd507428b.gif","4d086e061d950a7bf524513b0ad162d9f2d3c938.jpg",\
	"DSC_0396.JPG","test.png","selenium-java-2.46.0.zip","selenium-remote-control-1.0.3.rar"]
	if attach_number != 0:
		attach_index = random.sample(attach_files,attach_number)
		for k in range(attach_number):
			try:
				attach_path = "C:\\Users\\Administrator\\Desktop\\learn_python\\Test2\\attach\\" + attach_index[k]
				attach_element = browser.find_element_by_xpath(xpath2 + "/div[@class=\"form-item\"]\
				/div[@class=\"mt10 mb10\"]/a[@id='WU_FILE_" + str(i) + "-attach']")
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
			except TimeoutException:
				print "啊哦，上传附件超时了！"
				pass
	"""
	
	time.sleep(1) # 等待操作完成
	browser.find_element_by_xpath(button_xpath).click() # 点击“保存配置”按钮
	time.sleep(1)

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

element = browser.find_element_by_xpath('//div[@class="left-content"]/p').text
string = u''.join(element).encode('utf-8').strip()
f.write(string)
f.write('\n=======================\n')

f.write('\n')
f.close()
browser.quit()
