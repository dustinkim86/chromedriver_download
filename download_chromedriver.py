"""
selenium을 위한 Chrome driver 자동 download
"""


import json
import os.path
import plistlib
from urllib import request
from sys import platform
from bs4 import BeautifulSoup
import zipfile
import os


def check_download_path():
    """
    Check chromedriver folder
    """
    if "chromedriver" in os.listdir():
        os.path.join(os.getcwd(), "/chromedriver")
    else:
        os.makedirs("chromedriver")
        download_path = os.path.join(os.getcwd(), "/chromedriver")
        return download_path


def check_browser_ver():
    """
    Check chromedriver version
    """
    try:
        url = 'http://omahaproxy.appspot.com/all.json'
        resp = request.urlopen(url)
        data = json.loads(resp.read())
        for each in data:
            if each.get("os") == "mac":
                versions = each.get("versions")
                for version in versions:
                    if version.get("channel") == "stable":
                        latest = (version.get("current_version"))
                        return f"{latest.split('.')[0]}.{latest.split('.')[1]}.{latest.split('.')[2]}"
    except Exception:
        print("You do not have Chrome browser.")


def check_os():
    """
    Check OS
    """
    if platform == 'linux' or platform == 'linux2':
        os_name = 'linux64'
    elif platform == 'darwin':
        os_name = 'mac64'
    elif platform == 'win32' or platform == 'win64':
        os_name = 'win32'
    os_name_path = f"chromedriver_{os_name}.zip"
    return os_name_path


def get_download_url():
    """
    Get chromedriver download url
    """
    os_name_path = check_os()
    url = "https://chromedriver.chromium.org/downloads"
    resp = request.urlopen(url)
    soup = BeautifulSoup(resp, 'html.parser')
    links = [a['href'] for a in soup.select('a[href]')]
    for link in links:
        if latest in link:
            return link.replace('index.html?path=', '') + os_name_path


def download_and_unzip(down_url):
    """
    File download & Unzip
    """
    os_name_path = check_os()
    user_os = os_name_path.split('_')[1].split('.')[0]
    request.urlretrieve(down_url, "chromedriver.zip")
    if user_os in ['mac64', 'linux64']:
        os.system('unzip chromedriver.zip -d ./chromedriver')
        os.system('rm chromedriver.zip')
    elif user_os == 'win32':
        os.system('tar -xf chromedriver.zip')
        os.system('move chromedriver.exe ./chromedriver')
        os.system('del chromedriver.zip')




if __name__ == '__main__':
    download_path = check_download_path()
    latest = check_browser_ver()
    down_url = get_download_url()
    download_and_unzip(down_url)
