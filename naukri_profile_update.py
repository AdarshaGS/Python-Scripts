import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

EMAIL = "your_email@gmail.com"
PASSWORD = "your_password"

CHROMEDRIVER_PATH = "/opt/homebrew/bin/chromedriver"


def create_driver():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    return driver


def safe_click(driver, element):
    try:
        element.click()
    except:
        driver.execute_script("arguments[0].click();", element)


def login(driver, wait):
    driver.get("https://www.naukri.com")

    login_btn = wait.until(EC.element_to_be_clickable((By.ID, "login_Layer")))
    safe_click(driver, login_btn)

    form = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//form[@name='login-form']"))
    )

    email = form.find_element(By.XPATH, ".//input[@type='text']")
    password = form.find_element(By.XPATH, ".//input[@type='password']")

    email.send_keys(EMAIL)
    password.send_keys(PASSWORD)

    submit = form.find_element(By.XPATH, ".//button[@type='submit']")
    safe_click(driver, submit)

    time.sleep(5)


def update_date(driver, wait):
    driver.get("https://www.naukri.com/mnjuser/profile")
    time.sleep(5)

    if "login" in driver.current_url:
        raise Exception("Login failed")

    # -------- OPEN BASIC DETAILS --------
    edit_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "(//em[contains(@class,'edit')])[1]"))
    )

    driver.execute_script("arguments[0].scrollIntoView(true);", edit_btn)
    time.sleep(1)
    safe_click(driver, edit_btn)

    form = wait.until(
        EC.visibility_of_element_located((By.ID, "editBasicDetailsForm"))
    )

    time.sleep(3)

    # -------- GET CURRENT DAY --------
    current_day = int(driver.find_element(By.ID, "hid_lwdDay").get_attribute("value"))
    next_day = current_day + 1 if current_day < 31 else 1

    print("Current:", current_day, "Next:", next_day)

    # -------- OPEN DAY DROPDOWN --------
    day_input = wait.until(EC.element_to_be_clickable((By.ID, "lwdDayFor")))

    driver.execute_script("arguments[0].scrollIntoView(true);", day_input)
    time.sleep(1)
    safe_click(driver, day_input)

    # -------- SELECT DAY --------
    option = wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//a[@data-id='lwdDay_{next_day}']"))
    )

    driver.execute_script("arguments[0].scrollIntoView(true);", option)
    time.sleep(1)
    safe_click(driver, option)

    time.sleep(1)

    # -------- FORCE STATE CHANGE --------
    driver.execute_script("document.body.click();")
    time.sleep(2)

    # -------- VERIFY --------
    updated_day = int(driver.find_element(By.ID, "hid_lwdDay").get_attribute("value"))
    print("Updated:", updated_day)

    if updated_day != next_day:
        raise Exception("Date update failed")

    # -------- SAVE --------
    save_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "saveBasicDetailsBtn"))
    )

    driver.execute_script("arguments[0].scrollIntoView(true);", save_btn)
    time.sleep(1)
    safe_click(driver, save_btn)

    print("Saved successfully")
    time.sleep(5)


def run():
    driver = None
    try:
        print("Starting...")

        driver = create_driver()
        wait = WebDriverWait(driver, 20)

        login(driver, wait)
        update_date(driver, wait)

        print("Done. Closing...")

    except Exception as e:
        print("ERROR:", str(e))

    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    run()
