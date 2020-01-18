#@author:shangzeng
import asyncio
import aiohttp
import netaddr
import base64
import time
import re


class WebBannerScanC(object):
    '''接受IP段并返回扫描信息，以数组形式返回'''
    def __init__(self,ip,ports):
        self.ip = ip
        self.ports = ports
        self.headers = {'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
        self.timeout = 5
        self.tasks = []

    async def http_response(self,url):  
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url=url,headers=self.headers,timeout=self.timeout,verify_ssl=False) as response:
                    if response:    
                        html = await response.text(encoding='utf-8')   
                        code = response.status
                        header = response.headers['Server'][:20]
                        title = re.findall(r'<title>(.*)</title>', html)
                        return url,code,header,title
            except Exception as r:
                pass

    def web_c(self):
        ips = netaddr.IPNetwork(self.ip)
        for ip in ips:
            for port in self.ports:
                url = "http://"+str(ip)+":"+str(port)
                self.tasks.append(asyncio.ensure_future(self.http_response(url)))  
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(asyncio.gather(*self.tasks))  
        return result

def ips():
    f = open('ip.txt', 'r')
    a = f.readlines()
    f.close()
    return a



if __name__ == '__main__':
    print(base64.b64decode("ICAgICAgICAgICAgICBfICAgICAgIF8gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICB8IHwgICAgIHwgfCAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIApfXyAgICAgIF9fX19ffCB8X18gICB8IHxfXyAgIF9fIF8gXyBfXyAgXyBfXyAgIF9fXyBfIF9fICAgX19fICBfX18gX18gXyBfIF9fICAKXCBcIC9cIC8gLyBfIFwgJ18gXCAgfCAnXyBcIC8gX2AgfCAnXyBcfCAnXyBcIC8gXyBcICdfX3wgLyBfX3wvIF9fLyBfYCB8ICdfIFwgCiBcIFYgIFYgLyAgX18vIHxfKSB8IHwgfF8pIHwgKF98IHwgfCB8IHwgfCB8IHwgIF9fLyB8ICAgIFxfXyBcIChffCAoX3wgfCB8IHwgfAogIFxfL1xfLyBcX19ffF8uX18vICB8Xy5fXy8gXF9fLF98X3wgfF98X3wgfF98XF9fX3xffCAgICB8X19fL1xfX19cX18sX3xffCB8X3wKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIA==").decode("utf-8"))
    time1 = time.time()
    port = [80,8080,81,8081,7001,8000,8088,8888,9090,8090,88,8001,82,9080]
    for ip in ips():
        ip = ip.strip("\n")
        test = WebBannerScanC(ip,port)
        result = test.web_c()
        for save in result:
            if save != None:  
                with open('save.txt', mode='a', encoding='utf-8') as f:
                    f.write(str(save)+"\n")



        time2 = time.time()
        print(ip+"  查询完成，目前共耗时"+str(time2-time1))
    print("全部完成！")

