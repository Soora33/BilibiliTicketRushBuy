import datetime
import random
import time

import cv2
import yaml
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# 初始化抢购信息(都是必填)
# 地址
url = "https://show.bilibili.com/platform/detail.html?id=98212&from=pc_ticketlist"
# 抢购时间
TargetTime = "2025-02-24 11:19:00.00000000"  # 设置抢购时间
# 场地
Session = '1'  # 场次设置：修改引号内部的数字，数字对应第选项的序号，选项序号从左到右从1开始依次排列
# 价格
Price = '3'  # 价格设置：设置方法与场次设置一样
# 选座 id 同时再页面也要点
id = '2_22'
# id = '11_16'

def init():
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
    WebDriver = webdriver.Chrome(options)  # 使用可视化游览器

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

    WebDriver.get(url)  # 输入目标购买页面

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
    wait = WebDriverWait(WebDriver, 30)  # 增加等待超时时间至30秒
    while True:
        try:
            # --- 点击购买按钮 ---
            buy_button = wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, "product-buy.enable"))
            )
            buy_button.click()
            print("进入购买页面成功")

            # --- 处理可能的分场次/座位选择 ---
            try:

                # 原逻辑保持（等待元素可点击）
                WebDriverWait(WebDriver, 1).until(
                    EC.element_to_be_clickable((By.ID, '3111'))
                ).click()

                WebDriverWait(WebDriver, 1).until(
                    EC.element_to_be_clickable((By.ID, id))
                ).click()
            except TimeoutException:
                print("未检测到需要选择的场次/座位，继续流程")

            WebDriverWait(WebDriver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'finish-btn.active'))
            ).click()
            print("选座创建完成，准备付款")

            # --- 提交订单 ---
            WebDriverWait(WebDriver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'confirm-paybtn.active'))
            ).click()

            print("订单创建完成，请在一分钟内付款")

            return

        except TimeoutException as e:
            WebDriver.refresh()  # 刷新页面重试

        except Exception as e:
            WebDriver.refresh()


if __name__ == '__main__':
    init()
    choose_info()
    wait()
    buy()

