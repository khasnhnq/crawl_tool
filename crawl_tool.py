from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

def crawl_vnexpress_health():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    url = "https://vnexpress.net/suc-khoe"
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 10)

        # Mở rộng thêm bài bằng cách click nút "Xem thêm" (nếu có)
        for _ in range(3):  # Click 3 lần để lấy thêm nhiều bài viết
            try:
                load_more_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-readmore")))
                driver.execute_script("arguments[0].click();", load_more_btn)
                time.sleep(2)
            except:
                break  # Không còn nút hoặc có lỗi

        articles = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".item-news")))

        article_data = []
        for article in articles:
            try:
                title_element = article.find_element(By.CSS_SELECTOR, ".title-news a")
                title = title_element.text.strip()
                link = title_element.get_attribute("href")

                description_element = article.find_element(By.CSS_SELECTOR, ".description")
                description = description_element.text.strip() if description_element else ""

                article_data.append({"title": title, "link": link, "description": description})
            except Exception as e:
                print(f"Lỗi khi lấy bài viết: {e}")

        driver.quit()

        # Lưu vào CSV
        csv_filename = "vnexpress_health_articles.csv"
        with open(csv_filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["title", "link", "description"])
            writer.writeheader()
            writer.writerows(article_data)

        print(f"Đã lưu {len(article_data)} bài viết vào {csv_filename}")
        return article_data

    except Exception as e:
        print(f"Lỗi thu thập dữ liệu: {e}")
        driver.quit()
        return None

# Gọi hàm crawl
health_articles = crawl_vnexpress_health()
