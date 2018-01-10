from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import time

driver = webdriver.Chrome('C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe')
driver.get("https://www.attop.com/index.htm")

def StableClick(WebElem, driver):
    driver.execute_script("arguments[0].click();", WebElem)

def Login():
    driver.switch_to_frame("pageiframe")    #IMPORTANT, swith to the login iframe
    
    username = input("请输入用户名")
    userElem = driver.find_element_by_id('username')
    userElem.send_keys(username)
    paswd = input("请输入登录密码")
    paswdElem = driver.find_element_by_name('password')
    paswdElem.send_keys(paswd)
    vericode = input("请输入浏览器中显示的验证码")
    checkElem = driver.find_element_by_name('rand')
    checkElem.send_keys(vericode)
    
    loginElem_2 = driver.find_element_by_partial_link_text('登录')
    loginElem_2.click()
    
def BeginClass(): 
    driver.implicitly_wait(5)
    myAccount = driver.find_element_by_link_text("个人中心")
    driver.execute_script("arguments[0].click();", myAccount)
    myClass = driver.find_element_by_link_text("我的课程")
    driver.execute_script("arguments[0].click();", myClass)
    someClass_1 = driver.find_element_by_link_text("马克思主义基本原理概论")
    driver.execute_script("arguments[0].click();", someClass_1)
    driver.switch_to_window(driver.window_handles[1])   # switch to the new tab opened
    someClass_2 = driver.find_element_by_link_text("课程学习")
    driver.execute_script("arguments[0].click();", someClass_2)

def LectureFlag():
    timeState = driver.find_element_by_xpath("/html/body/div/div/div/div/div/ul/li").text   # see whether reached time limit
    checkState= driver.find_element_by_xpath("/html/body/div/div/div/div/div/ul/li[4]").text
    TimeFlag = ('OK' in timeState)  # '时间说明\n1 / 10 分钟' or 'OK\n时间说明'
    CheckFlag = ('OK' in checkState)    # will be True if in it
    ClassChecking()
    # print("the state of Flags: TimeFlag is %s, CheckFlag is" % TimeFlag, CheckFlag)
    # a = driver.find_element_by_xpath("/html/body/div/div/div/div/div/ul/li")
    # print(a)
    return TimeFlag, CheckFlag
    
def ClassChecking():
    '''
    click all the checks in one class page
    '''
    Checkbtn = driver.find_elements_by_class_name("BT_ping")
    # print("    now Checkbtn", Checkbtn[0].text, Checkbtn[0])
    # print(len(Checkbtn))
    num = 0
    for i in range(len(Checkbtn)):
        try:
            if '马上评价' in Checkbtn[i].text:
                driver.execute_script("arguments[0].click();", Checkbtn[i])
                driver.switch_to_frame("pageiframe")
                driver.find_element_by_class_name("ping_btn_2").click()
                num += 1
                print("items checked: %s, total items:" % num, len(Checkbtn))
                driver.implicitly_wait(7)
                driver.find_element_by_class_name("aui_state_highlight").click()
                driver.switch_to_default_content()
                exit = driver.find_element_by_class_name("aui_close")
                driver.execute_script("arguments[0].click();", exit)
        except NoSuchElementException as s:
            e = s
            print(e)
            driver.refresh()
            Checkbtn = driver.find_elements_by_class_name("BT_ping")
        except IndexError as d:
            e = d
            print("Now refreshing for the Checkbtn element.\n")
            driver.refresh()
            time.sleep(6)
            Checkbtn = driver.find_elements_by_class_name("BT_ping")
    
def TimingReaching():
    htmlElem = driver.find_element_by_tag_name("html")
    time.sleep(10)
    htmlElem.send_keys(Keys.DOWN)
    htmlElem.send_keys(Keys.DOWN)
    htmlElem.send_keys(Keys.UP)
    htmlElem.send_keys(Keys.DOWN)
    htmlElem.send_keys(Keys.UP)
    htmlElem.send_keys(Keys.UP)
    
def ShowHidden():    
    '''
    loop through elem with name: 'zj'
    click on each of them to show the hidden classes
    '''
    zj = driver.find_elements_by_name("zj")
    driver.implicitly_wait(3)
    for i in range(len(zj)):
        try:
            driver.execute_script("arguments[0].click();", zj[i])
        except Exception:
            print("ShowHidden Error")
            
def A():
    notice = ("Please note:\n"
    "Later the page will be scrolling up and down every 10 secs until Time Limit is reached.\n"
    "It's the normal behavior. Don't Panic.\n"
    "随后页面将每十秒上下翻动，这是正常现象，为了达到‘学习时间’。\n"
    "程序运行正常。")
    print(notice)
    i = 0
    TimeFlag, CheckFlag = LectureFlag()
    while not CheckFlag:
        ClassChecking()
        TimeFlag, CheckFlag = LectureFlag()
    print("\n\nAll items are checked.")
    while not TimeFlag:
        TimingReaching()
        TimeFlag, CheckFlag = LectureFlag()
        i += 1
        if i == 180:    # refresh to update, every 3 minutes.
            driver.refresh()
            i = 0
            
    driver.execute_script("alert('Finished! 本课已刷完！');")
        
            
            
if __name__ == '__main__':
    '''
    initiation 
    '''
    loginElem_1 = driver.find_element_by_partial_link_text('登录')
    driver.execute_script("arguments[0].click();", loginElem_1)   #click on the elem; but click() also works
    wait = WebDriverWait(driver, 10)
    
    Login()
    BeginClass()
    ShowHidden()