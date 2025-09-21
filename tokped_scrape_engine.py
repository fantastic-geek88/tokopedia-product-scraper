from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd

driver_path = r"C:\Users\LENOVO\Documents\Python Data Analyst Project\tokopedia-product\chromedriver.exe"

options = webdriver.ChromeOptions()
# remove headless first so you can SEE Chrome
# options.add_argument("--headless")

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

# driver.get("https://www.tokopedia.com/search?q=geforce+rtx+3050")
driver.get("https://www.tokopedia.com/search?q=asus+vivobook")
# time.sleep(10)

wait = WebDriverWait(driver, 10)

wait.until(
    EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "#zeus-root div.css-jau1bt div.css-rjanld div:nth-child(3) a")
    )
)
time.sleep(10)

# ambil semua card produk (wrapper <a>)
cards = driver.find_elements(
    By.CSS_SELECTOR, "#zeus-root div.css-jau1bt div.css-rjanld div:nth-child(3) a"
)

data = []
for card in cards:
    try:
        title = card.find_element(
            By.CSS_SELECTOR, "div.y-oybT3IAd310DVdH3OwVg\\=\\= span"
        ).text
    except:
        title = None

    try:
        price = card.find_element(
            By.CSS_SELECTOR, "div.pBlp2erqYHW\\+p5z-rsznAA\\=\\= div"
        ).text
    except:
        price = None

    try:
        sales = card.find_element(
            By.CSS_SELECTOR, "span.u6SfjDD2WiBlNW7zHmzRhQ\\=\\="
        ).text
    except:
        sales = None

    try:
        seller = card.find_element(
            By.CSS_SELECTOR, "span.si3CNdiG8AR0EaXvf6bFbQ\\=\\="
        ).text
    except:
        seller = None

    try:
        link = card.get_attribute("href")
    except:
        link = None

    data.append(
        {"title": title, "price": price, "sales": sales, "seller": seller, "link": link}
    )

# masukin ke DataFrame
df = pd.DataFrame(data)
# print(df)

# export ke Excel
df.to_excel("tokopedia_products.xlsx", index=False)
print("✅ Data berhasil diexport ke tokopedia_products.xlsx")

driver.quit()
