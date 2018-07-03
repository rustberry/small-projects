import requests
from lxml import etree
import time

def login(url, pwd, userName, session):
    loginData = {'form_email': userName, 'form_password': pwd,}
    loginHeaders = {
        'Host': 'accounts.douban.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.douban.com/accounts/login',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    l = session.post(url, data=loginData, headers = loginHeaders)
    
    if l.status_code == requests.codes.ok or l.status_code == requests.codes.found:
        print("Login Successfully")
    else:
        print("Failed to Login")
        session.close()


    
def main():
    pwd = ''
    userName = ''
    loginUrl = 'https://accounts.douban.com/login'
    totalPageNum = 5  # 用户在网页端显示一共有多少页广播
    targetUserUrl = ''
    broadcastUrl = 'https://www.douban.com/people/targetUserUrl/statuses?p='
    
    s = requests.Session()
    time.sleep(3)
    login(loginUrl, pwd, userName, session=s)
    time.sleep(2)
    brodHeaders = {
        'Host': 'www.douban.com',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    
    file = open('vivhDoubanStatuses.txt', 'a', encoding='utf-8')
    try:
        for i in range(1, totalPageNum+1):
            time.sleep(3)
            r = s.get(broadcastUrl+str(i), headers=brodHeaders)
            e = etree.HTML(r.text)
            bq = e.xpath('//*/blockquote')
            lenBq = len(bq)
            if lenBq == 0:
                print("Page {page} contains no statuses. When was that day?".format(page=i))
                continue
            for j in range(lenBq-1):
                try:
                    if bq[j].text == '\n  \n\n  ':
                        t = (bq[j]).xpath('p')[0].text
                        file.write(t + '\n')
                    else:
                        file.write(bq[j].text + '\n')
                    print("Scraping page {page}, status number {count}".format(page=i, count=j))
                except TypeError as e:
                    print(e)
                    continue
    except Exception as e:
        print('Error:', e)
        print('Page: {}, Statuses: {}'.format(i, j))
    finally:
        file.close()
    
if __name__ == '__main__':
    main()
