import datetime
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import cv2



def Init():
    ch_options = Options()
    ch_options.add_argument("--headless")
    global TargetTime
    TargetTime = "2025-02-24 12:00:00.00000000"  # 设置抢购时间

    global WebDriver
    WebDriver = webdriver.Chrome(options=ch_options)         #使用headless游览器，速度更快
    # WebDriver = webdriver.Chrome()  # 使用可视化游览器
    WebDriver.get("https://show.bilibili.com/platform/detail.html?id=98212&from=pc_ticketlist")  # 输入目标购买页面
    global Price, Session
    Session = '1'  # 场次设置：修改引号内部的数字，数字对应第选项的序号，选项序号从左到右从1开始依次排列
    Price = '3'  # 价格设置：设置方法与场次设置一样

    time.sleep(1)
    print("进入购票页面成功")

    WebDriver.find_element(By.CLASS_NAME, "nav-header-register").click()
    time.sleep(1)

    print("登录完成后关闭qrimg页面")
    WebDriver.save_screenshot('./QRcode.png')
    qrimg = cv2.imread('./QRcode.png')
    cv2.imshow("qrimg", qrimg)
    key = cv2.waitKey(10000)
    # WebDriver.find_element(By.CLASS_NAME, "bili-mini-close").click()
    #
    # print("请在10s内登录")
    # time.sleep(10)

def Select():
    print('select')
    while True:
        try:
            WebDriver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/div[2]/div[2]/div[4]/ul[1]/li[2]/div[' + Session + ']').click()
            WebDriver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/div[2]/div[2]/div[4]/ul[2]/li[2]/div[' + Price + ']').click()
            break
        except:
            print("等待刷新")


def Wait():
    print('wait')
    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        print(now + "     " + TargetTime)
        if now >= TargetTime:
            WebDriver.refresh()
            Select()
            break

def Buy():
    print("test1")
    while True:
        try:
            WebDriver.find_element(By.CLASS_NAME, "product-buy.enable").click()
            # time.sleep(5)
            print("进入购买页面成功")
        except:
            print("无法点击购买")

        try:
            # 输入联系人姓名
            name_input = WebDriver.find_element(By.XPATH, "//input[@placeholder='请输入联系人姓名']")
            name_input.clear()
            name_input.send_keys("xxx")

            # 输入联系人手机号
            phone_input = WebDriver.find_element(By.XPATH, "//input[@placeholder='请输入联系人手机号']")
            phone_input.clear()
            phone_input.send_keys("xxx")

            WebDriver.find_element(By.CLASS_NAME, "confirm-paybtn.active").click()

            # element = WebDriverWait(WebDriver, 10).until(
            #     EC.element_to_be_clickable((By.CLASS_NAME, "confirm-paybtn.active"))
            # )
            # element.click()

            print("订单创建完成，请在一分钟内付款")
            return
            # time.sleep(60)
        except:
            print("无法点击创建订单")


if __name__ == '__main__':
    Init()
    Select()
    Wait()
    Buy()

