# File: test_case_textbox.py

"""
Test Case: Gửi form Text Box với dữ liệu khác
Steps:
1. Truy cập trang https://demoqa.com/text-box
2. Nhập dữ liệu mới vào các trường
3. Nhấn nút Submit
4. Kiểm tra từng dòng kết quả hiển thị
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://demoqa.com/text-box")

# Nhập thông tin khác
driver.find_element(By.ID, "userName").send_keys("Tran Thi B")
driver.find_element(By.ID, "userEmail").send_keys("tranthib@example.com")
driver.find_element(By.ID, "currentAddress").send_keys("789 Quang Trung")
driver.find_element(By.ID, "permanentAddress").send_keys("101 Le Loi")

# Submit
driver.find_element(By.ID, "submit").click()
time.sleep(2)

# Kiểm tra kết quả từng dòng
name_result = driver.find_element(By.ID, "name").text
email_result = driver.find_element(By.ID, "email").text

assert "Tran Thi B" in name_result
assert "tranthib@example.com" in email_result

print("✅ Test case với dữ liệu khác đã pass!")

driver.quit()
