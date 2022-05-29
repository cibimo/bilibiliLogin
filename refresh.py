import os, time, requests, json, urllib, hashlib

def tvsign(params, appkey='4409e2ce8ffd12b8', appsec='59b43e04ad6965f34319062b478f83dd'):
    '为请求参数进行 api 签名'
    params.update({'appkey': appkey})
    params = dict(sorted(params.items())) # 重排序参数 key
    query = urllib.parse.urlencode(params) # 序列化参数
    sign = hashlib.md5((query+appsec).encode()).hexdigest() # 计算 api 签名
    params.update({'sign':sign})
    return params
    
saveInfo = json.loads(open('info.json').read())

rsp_data = requests.post("https://passport.bilibili.com/api/v2/oauth2/refresh_token",params=tvsign({
    'access_key':saveInfo['token_info']['access_token'], 
    'refresh_token':saveInfo['token_info']['refresh_token'],
    'ts':int(time.time())
}),headers={'Content-type': "application/x-www-form-urlencoded"}).json()


if rsp_data['code'] == 0:
    print(f"刷新成功, 有效期至{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(rsp_data['ts'] + int(rsp_data['data']['token_info']['expires_in'])))}")

    saveInfo = {
        'update_time':rsp_data['ts'],
        'token_info':rsp_data['data']['token_info'],
        'cookie_info':rsp_data['data']['cookie_info']
    }
    with open('info.json','w+') as f:
        f.write(json.dumps(saveInfo,ensure_ascii=False,separators=(',',':')))
        f.close()
else:
    print('刷新失败')
