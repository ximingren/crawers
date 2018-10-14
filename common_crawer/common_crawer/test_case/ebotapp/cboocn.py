from lxml import etree
import requests


def get_office(data, style):
    if style == 1:
        hk_am_rank = []
        hk_am_boxOffice_total = []
        hk_am_oneWeekOffice = []
        hk_am_parts = int(len(data) / 5)
        for i in range(hk_am_parts):
            week_boxOffice = data[5 * i:5 * (i + 1)]
            hk_am_rank.append(week_boxOffice[0] + "(" + week_boxOffice[1] + ")" + ":" + week_boxOffice[2])
            hk_am_oneWeekOffice.append(week_boxOffice[0] + "(" + week_boxOffice[1] + ")" + ":" + week_boxOffice[3])
            hk_am_boxOffice_total.append(week_boxOffice[0] + "(" + week_boxOffice[1] + ")" + ":" + week_boxOffice[4])
        return hk_am_rank[::-1], hk_am_oneWeekOffice[::-1], hk_am_boxOffice_total[::-1]
    else:
        inland_days = []
        inland_boxOffice_total = []
        inland_oneWeekOffice = []
        inland_avePeople = []
        parts = int(len(data) / 6)
        for i in range(parts):
            week_boxOffice = data[6 * i:6 * (i + 1)]
            inland_avePeople.append(week_boxOffice[0] + "(" + week_boxOffice[1] + ")" + ":" + week_boxOffice[2])
            inland_oneWeekOffice.append(week_boxOffice[0] + "(" + week_boxOffice[1] + ")" + ":" + week_boxOffice[3])
            inland_boxOffice_total.append(week_boxOffice[0] + "(" + week_boxOffice[1] + ")" + ":" + week_boxOffice[4])
            inland_days.append(week_boxOffice[0] + "(" + week_boxOffice[1] + ")" + ":" + week_boxOffice[5])
        return inland_avePeople[::-1], inland_oneWeekOffice[::-1], inland_boxOffice_total[::-1], inland_days[::-1]

def get_block_office(tree):
    boxOffice_block=tree.xpath(
            '//div[@class="ziliaofr"]/div[@class="cont"]/p/span/text()')
    if boxOffice_block[0]=='累计票房':
        boxOffice_total =boxOffice_block[1][:-1]
        return boxOffice_total,None
    else:
        boxOffice_total = boxOffice_block[3][:-1]
        now_boxOffice =boxOffice_block[1][:-1]
        return boxOffice_total,now_boxOffice

if __name__ == '__main__':
    res = requests.get('http://www.cbooo.cn/m/13')
    tree = etree.HTML(res.text)
    name = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath(
        '//div[@class="ziliaofr"]/div[@class="cont"]/h2//text()')))))
    enName = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath(
        '//div[@class="ziliaofr"]/div[@class="cont"]/p[1]//text()')))))

    boxOffice_total,now_boxOffice=get_block_office(tree)

    genre = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath(
        '//div[@class="ziliaofr"]/div[@class="cont"]/p[3]//text()')))))
    genre = genre[genre.find("：") + 1:]
    runTime = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath(
        '//div[@class="ziliaofr"]/div[@class="cont"]/p[4]//text()')))))
    runTime = runTime[runTime.find("：") + 1:].strip('')
    releaseDate = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath(
        '//div[@class="ziliaofr"]/div[@class="cont"]/p[5]//text()')))))
    releaseDate = releaseDate[releaseDate.find("：") + 1:]
    standard = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath(
        '//div[@class="ziliaofr"]/div[@class="cont"]/p[6]//text()')))))
    standard = standard[standard.find("：") + 1:]
    country = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath(
        '//div[@class="ziliaofr"]/div[@class="cont"]/p[7]//text()')))))
    country = country[country.find("：") + 1:]
    field = tree.xpath('//dl[@class="dltext"]/dt/text()')
    director = ''.join(
        list(filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath('//dl[@class="dltext"]/dd[1]//text()')))))
    starring = ','.join(
        list(filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath('//dl[@class="dltext"]/dd[2]//text()')))))
    production_co = ','.join(
        list(filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath('//dl[@class="dltext"]/dd[3]//text()')))))
    distribution_co = ','.join(
        list(filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath('//dl[@class="dltext"]/dd[4]//text()')))))
    inland_boxOffice = list(filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath(
        '//*[@id="tabcont2"]/table[1]//tr[position()>1]//text()'))))
    hk_boxOffice = list(filter(lambda t: t != '',
                               map(lambda x: x.strip(), tree.xpath('//*[@id="tabcont2"]/table[2]/tbody//tr//text()'))))
    am_boxOffice = list(filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath(
        '//*[@id="tabcont2"]/table[3]//tr[position()>1]//text()'))))
    if '内地票房' in ''.join(tree.xpath('//*[@id="tabcont2"]/h4[1]//text()')):
        print('内地票房',1)
    elif '内地票房' in ''.join(tree.xpath('//*[@id="tabcont2"]/h4[2]//text()')):
        print('内地票房', 2)
    elif '内地票房' in ''.join(tree.xpath('//*[@id="tabcont2"]/h4[3]//text()')):
        print('内地票房', 3)
    if '香港票房' in ''.join(tree.xpath('//*[@id="tabcont2"]/h4[1]//text()')):
        print('香港票房',1)
    elif '香港票房' in ''.join(tree.xpath('//*[@id="tabcont2"]/h4[2]//text()')):
        print('香港票房', 2)
    elif '香港票房' in ''.join(tree.xpath('//*[@id="tabcont2"]/h4[3]//text()')):
        print('香港票房', 3)
    if '北美票房' in ''.join(tree.xpath('//*[@id="tabcont2"]/h4[1]//text()')):
        print('北美票房',1)
    elif '北美票房' in ''.join(tree.xpath('//*[@id="tabcont2"]/h4[2]//text()')):
        print('北美票房', 2)
    elif '北美票房' in ''.join(tree.xpath('//*[@id="tabcont2"]/h4[3]//text()')):
        print('北美票房', 3)
    avg, week, total, days = get_office(inland_boxOffice, 0)
    hk_rank, hk_week, hk_total = get_office(hk_boxOffice, 1)
    am_rank, am_week, am_total = get_office(am_boxOffice, 1)
    print(name, enName)
    print(boxOffice_total)
    print(now_boxOffice)
    print(genre)
    print(runTime)
    print(releaseDate)
    print(standard)
    print(country)
    print(director)
    print(starring)
    print(production_co)
    print(distribution_co)
    print(avg, week, total, days)
    print(hk_rank, hk_week, hk_total)
    print(am_rank, am_week, am_total)
