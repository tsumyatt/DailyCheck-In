from bs4 import BeautifulSoup
from urllib import request, parse
from jsbn import RSAKey
import ssl
import sys

common_http_header = {
    'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;'
              'q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'utf-8',
    'Accept-Language': 'ko,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': 1
}

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)



def checkin_11st(id, password):
    r = RSAKey.encrypt("ggomdyu")
    print("11st daily check-in succeed!")

if __name__ == '__main__':
    checkin_11st("", "")