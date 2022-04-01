from test_case_qa_gitea.fixture import *
import pytest
import time
import requests
from selenium.webdriver.common.keys import Keys


# docker start
def test_docker_start():

    client.containers.run(image='gitea/gitea', detach=True, ports={'3000/tcp': 3000}, name='gitea')
    running_container_names = []

    i = 0
    while i < 12:       # waiting a minute for docker to start
        for container in client.containers.list(filters={'status': 'running'}):
            running_container_names.append(container.name)
        if 'gitea' in running_container_names:
            try:
                driver.get('http://localhost:3000/')
            except:
                time.sleep(5)
                driver.refresh()
            break
        else:
            print('Not up yet')
            time.sleep(5)
            i += 1


# initialize database. SQLite is a default option, no changes are needed.
def test_initialize_database():
    wait_until_displayed('css', 'input[id="db_path"]')
    action.send_keys(Keys.PAGE_DOWN)
    action.perform()
    time.sleep(1.5)
    find_and_click('css', 'button[class="ui primary button"]')
    time.sleep(3)
    i = 0
    while i < 12:
        try:
            requests.get('http://localhost:3000/user/login')
            break
        except:
            time.sleep(5)
    driver.get('http://localhost:3000/')


# tests in gitea web app
@pytest.mark.parametrize('selector',
                         ['div[id="navbar"]',
                          'img[class="logo"]',
                          'h1[class="ui icon header title"]',
                          'div[class="ui stackable middle very relaxed page grid"]'
                          ])
def test_checking_selectors_on_starter_page(selector):
    wait_until_displayed(find_by='css', value=selector)
    assert driver.find_element(by=By.CSS_SELECTOR, value=selector).is_displayed()


def test_user_register():
    find_and_click(find_by='link_text', value='Register')
    wait_until_displayed('css', 'form[class="ui form"]')
    find_and_send_keys('id', 'user_name', username)
    find_and_send_keys('id', 'email', email)
    find_and_send_keys('id', 'password', password)
    find_and_send_keys('id', 'retype', password)
    find_and_click('tag', 'button')
    wait_until_displayed('css', 'h4[class="ui top attached header df ac"]')
    assert driver.find_element(by=By.CSS_SELECTOR, value='div[class="ui positive message flash-success"]').is_displayed()


# after registration
def test_create_repo():
    # add url and sign in credentials if this func is not following right after the user_register
    find_and_click('link_text', 'New Repository')
    wait_until_displayed('css', 'form[class="ui form"]')
    find_and_send_keys('id', 'repo_name', repository)
    find_and_click('tag', 'h3')
    action.send_keys(Keys.PAGE_DOWN)
    action.perform()
    time.sleep(1.5)
    find_and_click('css', 'input[class="hidden"][name="auto_init"]')
    find_and_click('css', 'button[class="ui green button"]')
    wait_until_displayed('link_text', 'New File')
#     assert driver.find_element(by=By.LINK_TEXT, value=f'{repository}}').is_displayed()
    assert driver.current_url == f'http://localhost:3000/{username}/{repository}'


def test_new_commit():
    find_and_click('link_text', 'New File')
    # wait_until_displayed('css', 'div[class="monaco-aria-container"]')
    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'div[class="monaco-aria-container"]')))
    find_and_send_keys('css', 'input[id="file-name"]', commit_file_name)
    find_and_send_keys('css', 'textarea[class="inputarea monaco-mouse-cursor-text"]', commit_body)
    find_and_click('css', 'div[class="repo-icon mr-3"]')
    action.send_keys(Keys.PAGE_DOWN)
    action.perform()
    time.sleep(1.5)
    find_and_click('css', 'button[id="commit-button"]')
    wait_until_displayed('link_text', 'Raw')
    assert driver.current_url == f'http://localhost:3000/{username}/{repository}/src/branch/master/{commit_file_name}'


def test_checking_file():
    resp = requests.get(f'http://localhost:3000/{username}/{repository}/raw/branch/master/{commit_file_name}')
    assert str(resp.content) == f"b'{commit_body}'"


# close the browser
def test_driver_close():
    driver.quit()


# stop docker container
def test_docker_stop():
    ctnr = client.containers.list(filters={'status': 'running'})
    for each in ctnr:
        if each.name == 'gitea':
            each.stop()
        else:
            pass
