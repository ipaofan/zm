# coding:utf8
import mitmproxy.http

cookie_mitmproxy = 'gdt_cookie_mitmproxy.txt'
class Counter:

    def response(self, flow: mitmproxy.http.HTTPFlow):
        url1 = flow.request.url
        cookies = dict(flow.request.cookies)
        if 'g_tk' in url1 and 'owner' in url1 and 'ptui_loginuin' in str(cookies):
            dict1 = {'url':url1,'cookies':cookies}
            with open(cookie_mitmproxy,'a') as f:
                f.write(str(dict1)+'\n')
            print(url1)
            print(cookies)
            print('*' * 100)

addons = [
    Counter()
]
