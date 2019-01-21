from fontTools.ttLib import TTFont

font1 = TTFont('./fonts/0daf468505636fa0f9ce913c6da43f412076.woff')
print(font1['glyf'].keys())
keys = font1['glyf'].keys()
values = list(' .0856239741')
# 构建基准 {name: num}
dict1 = dict((k,v) for k,v in zip(keys, values))
print(dict1)
font2 = TTFont('./fonts/03e4f54630a2443f3177df4623ee46682080.woff')
dict2 = {}
for key in font2['glyf'].keys():
    for k, v in dict1.items():
        # 通过比较 字形定义 填充新的name和num映射关系
        if font1['glyf'][k] == font2['glyf'][key]:
            dict2[key] = v.strip()
            break
print(dict2)