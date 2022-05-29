import qrcode_terminal
import os, time, requests, json, urllib, hashlib

def tvsign(params, appkey='4409e2ce8ffd12b8', appsec='59b43e04ad6965f34319062b478f83dd'):
    '为请求参数进行 api 签名'
    params.update({'appkey': appkey})
    params = dict(sorted(params.items())) # 重排序参数 key
    query = urllib.parse.urlencode(params) # 序列化参数
    sign = hashlib.md5((query+appsec).encode()).hexdigest() # 计算 api 签名
    params.update({'sign':sign})
    return params

# 获取二维码
loginInfo = requests.post('https://passport.bilibili.com/x/passport-tv-login/qrcode/auth_code',params=tvsign({
    'local_id':'0',
    'ts':int(time.time())
})).json()

# 生成二维码
qrcode_terminal.draw(loginInfo['data']['url'])

while True:
    pollInfo = requests.post('https://passport.bilibili.com/x/passport-tv-login/qrcode/poll',params=tvsign({
        'auth_code':loginInfo['data']['auth_code'],
        'local_id':'0',
        'ts':int(time.time())
    })).json()
    
    if pollInfo['code'] == 0:
        loginData = pollInfo['data']
        break
        
    elif pollInfo['code'] == -3:
        print('API校验密匙错误')
        raise
    
    elif pollInfo['code'] == -400:
        print('请求错误')
        raise
        
    elif pollInfo['code'] == 86038:
        print('二维码已失效')
        raise
        
    elif pollInfo['code'] == 86039:
        time.sleep(5)
    
    else:
        print('未知错误')
        raise

print(f"登录成功, 有效期至{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + int(loginData['expires_in'])))}")

saveInfo = {
    'update_time':int(time.time()+0.5),
    'token_info':loginData['token_info'],
    'cookie_info':loginData['cookie_info']
}
with open('info.json','w+') as f:
    f.write(json.dumps(saveInfo,ensure_ascii=False,separators=(',',':')))
    f.close()
