import time

import aiohttp
import asyncio


# task是coroutine对象的进一步封装
# 可以通过调用loop.create_task来创建task
# ensure_future()也可以创建task
# add_done_callback 设置回调函数
# 也可以不用回调函数,直接result()
# 如果要实现异步处理，要有挂起的操作。
# await 可以将耗时等待的操作挂起,后面跟的是 coroutine
import grequests
import requests

async def get(url):
    session=aiohttp.ClientSession()
    response=await session.get(url) # 挂起后，事件循环会寻找未被挂起的协程继续执行。
    print(response)
    print(response.url)
    result=await response.text() #不懂的是为什么这里也要awiat
    await session.close()
    return result

async def request(x):
    print(x)
    url='https://juejin.im/post/5b430456e51d45198a2ea433'
    res=await get(url)
    res=requests.get(url)
    return res

def callback(request,execption):
    print(request)
    print(execption)
def aio_test():
    start=time.time()
    # coroutine=request(1) # 返回coroutine协程
    tasks= [asyncio.ensure_future(request(_))for _ in range(10)] # 如果没用的变量取名为_
    # task.add_done_callback(callback)
    loop=asyncio.get_event_loop() # 事件循环loop
    # loop.run_until_complete(task) #注册协程,将coroutine封装成了task对象
    loop.run_until_complete(asyncio.wait(tasks)) # 如果想要多任务的话，首先将列表传递给wait方法，然后注册到事件循环中
    end=time.time()
    print(end-start)
    for task in tasks:
        print(task.result())

if __name__ == '__main__':
    tasks=[grequests.get('https://www.baidu.com')for _ in range(10)]
    a=grequests.imap(tasks,50,exception_handler=callback)
    print(next(a))
    for i in a:
        print(i)
# "bad handshake: SysCallError(-1, 'Unexpected EOF'
# 还有ahttp,asyncio