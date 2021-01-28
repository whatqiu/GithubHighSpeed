# coding:utf8
import re
from os import name, system

import requests
from bs4 import BeautifulSoup

github = requests.get('https://github.com.ipaddress.com/')
github_ssl = requests.get('https://fastly.net.ipaddress.com/github.global.ssl.fastly.net')
github_cdn = requests.get('https://github.com.ipaddress.com/assets-cdn.github.com')
github_image = requests.get('https://githubusercontent.com.ipaddress.com/user-images.githubusercontent.com')
github_cdn.encoding = github_ssl.encoding = github.encoding = github_image.encoding = 'utf8'

gtext = BeautifulSoup(github.text, 'html.parser')
gstext = BeautifulSoup(github_ssl.text, 'html.parser')
gctext = BeautifulSoup(github_cdn.text, 'html.parser')
gitext = BeautifulSoup(github_image.text, 'html.parser')


def re_ip():
    return [
        re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
                   str(gtext.find('table', attrs={'class': 'dnsinfo'})))[0],
        re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
                   str(gstext.find('table', attrs={'class': 'dnsinfo'})))[0],
        re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
                   str(gctext.find('table', attrs={'class': 'dnsinfo'})))[0],
         re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
                   str(gitext.find('table', attrs={'class': 'dnsinfo'})))[0]
    ]


def re_hosts():
    score_ip = re_ip()
    return [score_ip[0] + ' github.com\n',
            score_ip[1] + ' assets-cdn.github.com\n',
            score_ip[2] + ' github.global.ssl.fastly.net\n',
            score_ip[3] + 'user-images.githubusercontent.com\n']


if __name__ == '__main__':
    if name == 'nt':
        with open(r'C:\Windows\System32\drivers\etc\hosts', 'r') as r:
            rl = r.readlines()
            with open(r'C:\Windows\System32\drivers\etc\hosts', 'w') as w:
                for str_rl in rl:
                    if str_rl.endswith(
                            'github.com' or 'assets-cdn.github.com' \
                            or 'github.global.ssl.fastly.net '):
                        rl.remove(str_rl)
                w.writelines(rl)
                w.writelines(re_hosts())
                system('ipconfig /flushdns')

    elif name == 'posix':
        with open(r'\etc\hosts', 'r') as r:
            rl = r.readlines()
            with open(r'\etc\hosts', 'w') as w:
                for str_rl in rl:
                    if str_rl.endswith(
                            'github.com' or 'assets-cdn.github.com' \
                            or 'github.global.ssl.fastly.net'):
                        rl.remove(str_rl)
                w.writelines(rl)
                w.writelines(re_hosts())
    exit(0)
