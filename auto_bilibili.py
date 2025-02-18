import datetime
import time
import yaml
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import cv2

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# 初始化抢购信息(都是必填)
# 地址
# url = "https://show.bilibili.com/platform/detail.html?id=98212&from=pc_ticketlist"
# url = "https://show.bilibili.com/platform/detail.html?id=97102&from=pc_ticketlist"
url = "https://show.bilibili.com/platform/detail.html?id=96798&from=pc_ticketlist"
# 抢购时间
TargetTime = "2025-02-18 17:03:00.00000000"  # 设置抢购时间
# 场地
Session = '1'  # 场次设置：修改引号内部的数字，数字对应第选项的序号，选项序号从左到右从1开始依次排列
# 价格
Price = '4'  # 价格设置：设置方法与场次设置一样
# 填写人名字
name = 'xxx'
# 填写人手机号（格式必须正确）
phone = 'xxx'

def init():
    headless_options = Options()
    # 无头浏览器
    headless_options.add_argument("--headless")
    headless_options.add_argument("--window-size=1920,1080")
    headless_options.add_argument("--disable-gpu")

    options = Options()
    # 反反爬虫措施
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")

    user_agents = config["user-agent"]
    random_user_agent = random.choice(user_agents)
    options.add_argument(f'--user-agent={random_user_agent}')


    global WebDriver
    # WebDriver = webdriver.Chrome(options=headless_options)         #使用headless游览器，速度更快
    WebDriver = webdriver.Chrome(options)  # 使用可视化游览器
    WebDriver.get(url)  # 输入目标购买页面

    # 反反爬虫措施
    WebDriver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
    })
    script = 'Object.defineProperty(navigator,"webdriver",{get:() => false,});'
    WebDriver.execute_script(script)

    time.sleep(1)
    print("进入购票页面成功")

    WebDriver.find_element(By.CLASS_NAME, "nav-header-register").click()
    time.sleep(1)

    print("请在 10s 内登录")
    WebDriver.save_screenshot('./QRcode.png')
    qrimg = cv2.imread('./QRcode.png')
    cv2.imshow("qrimg", qrimg)
    key = cv2.waitKey(10000)

def choose_info():
    while True:
        try:
            WebDriver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/div[2]/div[2]/div[4]/ul[1]/li[2]/div[' + Session + ']').click()
            WebDriver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/div[2]/div[2]/div[4]/ul[2]/li[2]/div[' + Price + ']').click()
            break
        except:
            print("等待刷新")


def wait():
    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        print(now + "     " + TargetTime)
        if now >= TargetTime:
            WebDriver.refresh()
            choose_info()
            break

def buy():
    while True:
        try:
            WebDriver.find_element(By.CLASS_NAME, "product-buy.enable").click()
            print("进入购买页面成功")
        except:
            print("无法点击购买")

        try:
            try:
                name_input = WebDriver.find_element(By.XPATH, "//input[@placeholder='请输入联系人姓名']")
                name_input.clear()
                name_input.send_keys(name)

                phone_input = WebDriver.find_element(By.XPATH, "//input[@placeholder='请输入联系人手机号']")
                phone_input.clear()
                phone_input.send_keys(phone)
            except:
                pass

            WebDriver.find_element(By.CLASS_NAME, "confirm-paybtn.active").click()
            print("订单创建完成，请在一分钟内付款")
            return
        except:
            print("无法点击创建订单")


if __name__ == '__main__':
    init()
    choose_info()
    wait()
    buy()

