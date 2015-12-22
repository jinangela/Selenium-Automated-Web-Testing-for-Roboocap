from selenium import webdriver

driver = webdriver.PhantomJS(executable_path='C:\\Python27\\Scripts\\phantomjs-2.0.0-windows\\bin\\phantomjs.exe')
driver.set_window_size(1120,550)
driver.get("https://duckduckgo.com/")
driver.find_element_by_id('search_form_input_homepage').send_keys("realpython")
driver.find_element_by_id("search_button_homepage").click()
print driver.current_url
driver.quit()