import docker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

# add path to driver !!!
client = docker.from_env()
driver = webdriver.Firefox(executable_path='/home/ritka-admin/PycharmProjects/pythonProject/geckodriver')
action = ActionChains(driver=driver)

# variables for names and credentials
username = 'kekkek'
email = 'kekkek@admin.ru'
password = 12345678
repository = 'my_repo'
commit_file_name = 'first_commit'
commit_body = 'writing code'


def find_and_click(find_by, value):
    by = find_by.lower()
    if by == "tag":
        elem = driver.find_element(by=By.TAG_NAME, value=value)
        action.click(elem)
        action.perform()
    elif by == "css":
        elem = driver.find_element(by=By.CSS_SELECTOR, value=value)
        action.click(elem)
        action.perform()
    elif by == "link_text":
        elem = driver.find_element(by=By.LINK_TEXT, value=value)
        action.click(elem)
        action.perform()
    else:
        print('acceptable find_bys: tag, css, link_text')


def find_and_send_keys(find_by, value, key_value):
    by = find_by.lower()
    if by == "id":
        elem = driver.find_element(by=By.ID, value=value)
        elem.send_keys(str(key_value))
    elif by == "link_text":
        elem = driver.find_element(by=By.LINK_TEXT, value=value)
        elem.send_keys(str(key_value))
    elif by == "css":
        elem = driver.find_element(by=By.CSS_SELECTOR, value=value)
        elem.send_keys(str(key_value))
    else:
        print('acceptable find_bys: id, link_text, css')


def wait_until_displayed(find_by, value):
    by = find_by.lower()
    if by == "css":
        WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, value)))
    elif by == "link_text":
        WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.LINK_TEXT, value)))
    else:
        print('acceptable find_bys: link_text, css')