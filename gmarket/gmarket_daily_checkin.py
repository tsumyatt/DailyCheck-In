from bs4 import BeautifulSoup
from urllib import request, parse
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

def checkin_gmarket(id, password):
    gmarket_global_cookies = 'charset=enUS;' \
                             'shipnation=KR;'

    # 로그인 페이지 요청
    login_page_url = "https://signinssl.gmarket.co.kr/login/login?url=http://www.gmarket.co.kr/"
    login_page_request = request.Request(login_page_url, headers=common_http_header)
    login_page_response = request.urlopen(login_page_request, context=ssl_context)
    login_page_html = login_page_response.read()
    login_page_cookies = login_page_response.getheader('Set-Cookie')

    # GUID 생성 관련 페이지 요청
    setguid_url = "http://pds.gmarket.co.kr/cookiemanager/getguids/montelena"
    setguid_request = request.Request(setguid_url, headers=common_http_header)
    setguid_response = request.urlopen(setguid_request, context=ssl_context)
    setguid_cookies = setguid_response.getheader('Set-Cookie')

    # 로그인에 필요한 쿠키 정보 모아놓기
    parsed_login_page_html = BeautifulSoup(login_page_html, "html.parser", from_encoding='utf-8')
    login_verification_token = \
        parsed_login_page_html.select("#defaultForm > input[type=hidden]:nth-child(1)")[0].attrs['value']
    login_verification_token2 = \
        login_page_cookies[login_page_cookies.find('__RequestVerificationToken=') + 27:
                           login_page_cookies.find(';', login_page_cookies.find('__RequestVerificationToken='))]
    cguid = setguid_cookies[setguid_cookies.find('cguid=') + 6:
                            setguid_cookies.find(';', setguid_cookies.find('cguid='))]
    pguid = setguid_cookies[setguid_cookies.find('pguid=') + 6:
                            setguid_cookies.find(';', setguid_cookies.find('pguid='))]
    sguid = setguid_cookies[setguid_cookies.find('sguid=') + 6:
                            setguid_cookies.find(';', setguid_cookies.find('sguid='))]

    # 로그인 요청
    login_url = 'https://signinssl.gmarket.co.kr/LogIn/LogInProc'
    gmarket_global_cookies += '__RequestVerificationToken=' + login_verification_token2 + ';' \
                              'cguid=' + cguid + ';' \
                              'pguid=' + pguid + ';' \
                              'sguid=' + sguid + ';' \
                              'charset=' + 'enUS;' \
                              'shipnation=' + 'KR;'

    login_http_header = {
        'Cache-Control': 'max-age=0',
        'Referer': 'https://signinssl.gmarket.co.kr/login/login?url=http://www.gmarket.co.kr/',
        'Origin': 'https://signinssl.gmarket.co.kr',
        'Upgrade-Insecure-Requests': 1,
        'Cookie': gmarket_global_cookies
    }
    login_http_header.update(common_http_header)
    login_http_body = parse.urlencode({
        '__RequestVerificationToken': login_verification_token,
        'command': 'login',
        'valid_url': '',
        'valid_key': '',
        'member_type': 'MEM',
        'type': '',
        'untrustCheck': '? 1 : 0',
        'FailCheck': '0',
        'url': 'http%3a%2f%2fwww.gmarket.co.kr%2f',
        'PrmtDisp': '',
        'PrmtreferURL': 'http%3a%2f%2fwww.gmarket.co.kr%2f',
        'FromWhere': 'G',
        'socialType': '',
        'socialSessionId': '',
        'member_yn': 'Y',
        'id': id,
        'pwd': password,
        'buyer_nm': '',
        'buyer_tel_no1': '',
        'buyer_tel_no2': '',
        'buyer_tel_no3': '',
        'nonmem_passwd': ''
    }).encode()
    login_request = request.Request(login_url, headers=login_http_header, data=login_http_body)
    login_response = request.urlopen(login_request, context=ssl_context)
    login_cookie = login_response.getheader('Set-Cookie')
    gmarket_global_cookies += login_cookie[login_cookie.find('user%5Finfo='):
                                           login_cookie.find(';', login_cookie.find('user%5Finfo=')) + 1]

    # 룰렛 돌리기 요청
    checkin_http_header = {
        'Cache-Control': 'max-age=0',
        'Referer': 'http://promotion.gmarket.co.kr/Event/AttendRoulette_none.asp',
        'Upgrade-Insecure-Requests': 1,
        'Cookie': gmarket_global_cookies
    }
    checkin_http_header.update(common_http_header)
    checkin_request = request.Request('http://promotion.gmarket.co.kr/Event/AttendApply.asp?actType=attToday',
                                      headers=checkin_http_header)
    checkin_response = request.urlopen(checkin_request, context=ssl_context)

    # 룰렛 돌리기 요청 2
    checkin_http_header_2 = {
        'Cache-Control': 'max-age=0',
        'Referer': 'http://promotion.gmarket.co.kr/Event/AttendRoulette_none.asp',
        'Upgrade-Insecure-Requests': 1,
        'Cookie': gmarket_global_cookies
    }
    checkin_http_header_2.update(common_http_header)
    checkin_request_2 = request.Request('http://eventnet.gmarket.co.kr/PluszoneEventPlatform/Attendance',
                                        headers=checkin_http_header_2)
    checkin_response_2 = request.urlopen(checkin_request_2, context=ssl_context)

    print("Gmarket daily check-in succeed!")

if __name__ == '__main__':
    checkin_gmarket(sys.argv[1], sys.argv[2])