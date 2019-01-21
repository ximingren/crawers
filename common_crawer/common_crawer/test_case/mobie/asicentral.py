import requests

if __name__ == '__main__':
    headers={
        'Cookie':"""AuthCookie=eyJhbGciOiJSU0EtT0FFUCIsImVuYyI6IkEyNTZHQ00iLCJrZXlpZCI6IkNPTk4ifQ.Nt_-cHtL8DrAKesJfqaZvLauaMmYDZg6u8oIN5iUeBK8-SZ4wUS6UP-vlPc5FbPJXZLMR4JhuyFwJkGoIVsjSXndoya3qmOqDC36a1zZNuth9KAuIomkXW7R5WAAfWSX6AKGK60FcbuCRbVy-Z6HI6pFaaKmdMBa6w2M95VVlKc.kMoQX2jwK1JxIO_b.jzeoAc7PNsuRs21W6idc4e_GDhepU5OttPeeieoVvV0Lz-34XnfGfqgTdwABWeDmnNTnftroEuOB5D9CSWHvZgMvAvpfdi-ODbNH1_Vd9CUiUdWlsWFoUTPGvryeCBfYu8ks9PBxhkLMx8RGkSrLAjJkxkefkTPyOZbLVn94NxZQoYKtzu57apuXWgHPWHdSLLhrVvvFsg61gO5MJax9klXr_5BuRdjGQj3ovISbIeECAYB1TDgqqhBSKiA8GDo17qAoIhY9dv4OycfzRUjtLb9U_AIwnEVQyxtbMkNDB7frca5UTxb_VIR2bKn05Wvw5aml2m_s8GwIkZ-bgj1mgnUKeGKy9I-9MjoIXEt79D5vV5m_gtohbBJoWy33O2kpegupx_7ogJj9HALNaRp5Hsrw3oPcB2pZ6VpumLqnnh6VeUUX99Yu6nQe1acb8BbkDSNXCnwcr6wZntAPPmLT7kqYnhEP4Cic5TYLCKzt0bfrr4USXcIM5erqXYmPcYdqiBySIZCgCBA6hWY.2iAPEhsBJaatPNRIPnrWdA; RefreshCookie=cf4223ef-5541-4bd2-8497-e63e1a5fe7ed; ASP.NET_SessionId=hhfl2bdyoeivvbffepvopf0t; _ga=GA1.2.1426702415.1540205747; _gid=GA1.2.6260567.1540205747"""
    }
    res=requests.get("https://translate.google.cn/translate_a/single?client=t&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&otf=1&ssel=0&tsel=0&kc=1&tk=923355.561632&q=a"
                     )
    print(res.text)
