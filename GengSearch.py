import json
import os
import platform
import time
import traceback

import requests

import imgkit
import simuse
from bs4 import BeautifulSoup

print('Version 1.3.2')


class platform():
    plat = platform.system()

    def wkimgpath(self):
        if self.plat == 'Windows':
            wkimgpath = 'wkhtmltopdf/bin/wkhtmltoimage.exe'
        else:
            wkimgpath = 'wkhtmltoimage'
        #print(wkimgpath)
        return wkimgpath

    def imgpath(self):
        if self.plat == 'Windows':
            imgpath = os.getcwd()
            imgpath = imgpath + r'\\temp\\Searchinfo_img.jpg'
        else:
            imgpath = os.path.dirname(os.path.realpath(__file__))
            imgpath = imgpath + '/temp/Searchinfo_img.jpg'
        #print(imgpath)
        return imgpath


class rescontrol():
    groupcontrol = {}
    membercontrol = {}

    def addgroup(self, group):
        self.groupcontrol[group] = int(time.time())

    def addmember(self, member):
        self.membercontrol[member] = int(time.time())

    def timegroup(self, group):
        if group in self.groupcontrol.keys():
            nowtime = int(time.time())
            subtime = nowtime - self.groupcontrol[group]
            return subtime
        else:
            return -1

    def timemember(self, member):
        if member in self.membercontrol.keys():
            nowtime = int(time.time())
            subtime = nowtime - self.membercontrol[member]
            return subtime
        else:
            return -1

    def sendgrouptext(self, data, group, rescontrol):
        grouptext = rescontrol['grouptext']
        simuse.Send_Message(data, group, 1, grouptext, 1)

    def sendmembertext(self, data, group, member, rescontrol):
        membertext = rescontrol['membertext']
        subtime = int(rescontrol['member']) - self.timemember(member)
        subtime = str(subtime)
        membertext = membertext.replace('{}', subtime)
        messagechain = []
        messageinfo1 = {'type': 'At', 'display': ''}
        messageinfo1['target'] = member
        messageinfo2 = {'type': 'Plain'}
        messageinfo2['text'] = '\n' + membertext
        messagechain.append(messageinfo1.copy())
        messagechain.append(messageinfo2.copy())
        simuse.Send_Message_Chain(data, group, 1, messagechain)


def DelError(Errortitle, Errortext):
    print(Errortitle)
    print('错误详情:')
    print(Errortext)
    log(target=Errortitle, mebmerID=Errortext)


def log(SearchUrl='Error',
        infoUrl='Error',
        runingtime=0,
        target='None',
        mebmerID='None'):
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    target = str(target)
    mebmerID = str(mebmerID)
    runingtime = str(runingtime)
    loginfo = '\n' + '-------------------------------------------------------------------------' + '\n'
    loginfo = loginfo + 'Date:' + date + '\n'
    loginfo = loginfo + 'SenderGroup:' + target + '\n'
    loginfo = loginfo + 'SenderID:' + mebmerID + '\n'
    loginfo = loginfo + 'SearchUrl:' + SearchUrl + '\n'
    loginfo = loginfo + 'InfoUrl:' + infoUrl + '\n'
    loginfo = loginfo + 'RuningTime:' + runingtime + ' S' + '\n'
    logfile = open('log.txt', 'a', encoding='utf-8')
    logfile.write(loginfo)
    logfile.close()
    print('save log')


def Search(Searchinfo, plat):
    global control
    try:
        Searchsign = 1
        print('Get mission')
        start = time.perf_counter()
        try:
            cookiefile = open('cookie.txt', 'r', encoding='utf-8-sig')
        except:
            DelError('cookie文件打开错误', traceback.format_exc())
            Searchsign = 0
        cookie = cookiefile.read()
        cookiefile.close()
        #print(cookie)
        try:
            cookie = dict([l.split("=", 1) for l in cookie.split("; ")])
        except:
            print('can not find cookie.txt')
            cookie = {}
        SearchUrl = 'https://jikipedia.com/search?phrase='
        Searchgroup = Searchinfo['Searchgroup']
        Searchsender = Searchinfo['Searchsender']
        Searchinfo = Searchinfo['Searchkey']
        SearchUrl = SearchUrl + Searchinfo
        SearchUrl = SearchUrl + '&category=definition'
        try:
            Searchlist = requests.get(SearchUrl, cookies=cookie)
            Searchlist = Searchlist.text
        except:
            DelError('搜索请求错误/超时', traceback.format_exc())
            Searchsign = 0
        #print(type(Searchlist))
        try:
            Searchhtmlfile = open('temp/Searchlist.html',
                                  'w',
                                  encoding='utf-8')
            Searchhtmlfile.write(Searchlist)
            Searchhtmlfile.close()
        except:
            DelError('搜索列表保存错误', traceback.format_exc())
            Searchsign = 0
        try:
            idnum = Searchlist.find('div data-id=')
            #print(idnum)
            idnum1 = Searchlist.find('"', idnum)
            #print(idnum1)
            idnum1 += 1
            idnum2 = Searchlist.find('"', idnum1)
            #print(idnum2)
            idnum1 = int(idnum1)
            idnum2 = int(idnum2)
        except:
            DelError('无法定位到搜索列表的首个词条ID', traceback.format_exc())
            Searchsign = 0
        Searchid = Searchlist[idnum1:idnum2]
        print('Searchid:', Searchid)
        infoUrl = 'https://jikipedia.com/definition/'
        infoUrl = infoUrl + Searchid
        print('infoUrl:', infoUrl)
        try:
            infolist = requests.get(infoUrl, cookies=cookie)
            infolist = infolist.text
        except:
            DelError('词条页面打开错误/请求超时', traceback.format_exc())
            Searchsign = 0
        try:
            stylenum1 = infolist.find('<style')
            stylenum2 = infolist.find('</style')
            stylehtml = infolist[stylenum1:stylenum2 + 8]
        except:
            DelError('页面样式(style)获取失败', traceback.format_exc())
            Searchsign = 0
        try:
            stylefile = open('temp/head.html', 'w', encoding='utf-8')
            stylehtml = '<meta charset="UTF-8">' + '\n' + stylehtml
            stylefile.write(stylehtml)
            stylefile.close()
        except:
            DelError('head文件保存失败', traceback.format_exc())
            Searchsign = 0
        soup = BeautifulSoup(infolist, "lxml")
        title = soup.select('.title-container')[0]
        body = soup.select('.content')[0]
        try:
            img = soup.select('.show')[0]
        except:
            img = ''
        title = str(title)
        title = '<center>' + title + '</center>'
        body = str(body)
        img = str(img)
        if img.find('show image button image') == -1:
            img = ''
        img = '<center>' + img + '</center>'
        try:
            headfile = open('temp/head.html', 'r', encoding='utf-8')
            head = headfile.read()
            headfile.close()
        except:
            DelError('未找到head文件', traceback.format_exc())
            Searchsign = 0
        head = head + '\n'
        html = head + title + '\n' + body + '\n' + img + '\n'
        #print(html)
        try:
            htmlfile = open('temp/Searchinfo.html', 'w', encoding='utf-8')
            htmlfile.write(html)
            htmlfile.close()
        except:
            DelError('词条页面保存错误', traceback.format_exc())
            Searchsign = 0
        path_wkimg = plat.wkimgpath()
        try:
            cfg = imgkit.config(wkhtmltoimage=path_wkimg)
            imgkit.from_file('temp/Searchinfo.html',
                             'temp/Searchinfo_img.jpg',
                             config=cfg)
        except:
            DelError('html转换图片错误', traceback.format_exc())
            Searchsign = 0
        end = time.perf_counter()
        runingtime = end - start
        if Searchsign != 0:
            print('Success')
            control.addgroup(Searchgroup)  #记录该群时间戳
            control.addmember(Searchsender)  #记录该成员时间戳
            print('RuningTime:', runingtime)
        log(SearchUrl, infoUrl, runingtime, Searchgroup, Searchsender)
    except:
        DelError('Error', traceback.format_exc())
        log(target=Searchgroup, mebmerID=Searchsender)
        Searchsign = 0
    finally:
        print('\nListening……')
        return Searchsign


def Listening(data, seting, blacklist=0):
    #print('Listening...')
    global control
    tritext = seting['tritext']
    rescontrol = seting['rescontrol']
    try:
        message = simuse.Fetch_Message(data)
        #print(message)
    except:
        DelError('Mirai未运行或未配置mah插件', traceback.format_exc())
        os.system('pause')
    SearchList = []
    Searchdict = {}
    if type(message) == type(0):
        #print('not')
        return SearchList
    for i in message:
        try:
            sign = 1
            checktext = 'none'
            if i['type'] == 'GroupMessage':
                messagechain_list = i['messagechain']
                messagechain_infodict = messagechain_list[1]
                if messagechain_infodict['type'] == 'Plain':
                    checktext = messagechain_infodict['text']
                if blacklist != 0:
                    for k in blacklist['group']:
                        if str(k) == str(i['group']):
                            sign = 0
                    for k in blacklist['member']:
                        if str(k) == str(i['sender']):
                            sign = 0
        except:
            continue
        for j in tritext['searchtext']:
            if checktext[:len(j)] == j:
                if control.timegroup(i['group']) <= int(
                        rescontrol['group']) and control.timegroup(
                            i['group']) != -1 and sign == 1:
                    sign = 0
                    control.sendgrouptext(data, i['group'], rescontrol)
                    log(SearchUrl='群搜索次数限制',
                        infoUrl='群搜索次数限制',
                        runingtime=0,
                        target=i['group'],
                        mebmerID=i['sender'])
                elif control.timemember(i['sender']) <= int(
                        rescontrol['member']) and control.timemember(
                            i['sender']) != -1 and sign == 1:
                    sign = 0
                    control.sendmembertext(data, i['group'], i['sender'],
                                           rescontrol)
                    log(SearchUrl='群成员搜索次数限制',
                        infoUrl='群成员搜索次数限制',
                        runingtime=0,
                        target=i['group'],
                        mebmerID=i['sender'])
                if sign == 1:
                    Searchdict.update(Searchkey=checktext[len(j):])
                    Searchdict.update(Searchsender=i['sender'])
                    Searchdict.update(Searchgroup=i['group'])
                    SearchList.append(Searchdict.copy())
                    sign = 0
                    break
            else:
                for k in tritext['randomtext']:
                    if checktext == k:
                        if control.timegroup(i['group']) <= int(
                                rescontrol['group']) and control.timegroup(
                                    i['group']) != -1 and sign == 1:
                            sign = 0
                            control.sendgrouptext(data, i['group'], rescontrol)
                            log(SearchUrl='群搜索次数限制',
                                infoUrl='群搜索次数限制',
                                runingtime=0,
                                target=i['group'],
                                mebmerID=i['sender'])
                        elif control.timemember(i['sender']) <= int(
                                rescontrol['member']) and control.timemember(
                                    i['sender']) != -1 and sign == 1:
                            sign = 0
                            control.sendmembertext(data, i['group'],
                                                   i['sender'], rescontrol)
                            log(SearchUrl='群成员搜索次数限制',
                                infoUrl='群成员搜索次数限制',
                                runingtime=0,
                                target=i['group'],
                                mebmerID=i['sender'])
                        if sign == 1:
                            Searchdict.update(Searchkey=' ')
                            Searchdict.update(Searchsender=i['sender'])
                            Searchdict.update(Searchgroup=i['group'])
                            SearchList.append(Searchdict.copy())
                            sign = 0
                            break
    #print(SearchList)
    return SearchList


def GengSearch(data, seting, plat):
    SearchList = []
    blacklist = seting['blacklist']
    if str(blacklist['switch']) == str(1):
        SearchList = Listening(data, seting, blacklist)
    else:
        SearchList = Listening(data, seting)
    #print(SearchList)
    SearchListcheck = []
    if SearchList != SearchListcheck:
        for i in SearchList:
            Searchsign = Search(i, plat)
            imgpath = plat.imgpath()
            if Searchsign == 1:
                simuse.Send_Message(data,
                                    i['Searchgroup'],
                                    1,
                                    imgpath,
                                    2,
                                    path=1)


def GetSeting():
    setingfile = open('seting.json', 'r', encoding='utf-8-sig')
    seting = setingfile.read()
    seting = json.loads(seting)
    return seting


def Checkset(seting):
    senddaily = seting['senddaily']
    blacklist = seting['blacklist']
    tritext = seting['tritext']
    rescontrol = seting['rescontrol']
    if len(tritext['searchtext']) == 0 or len(tritext['randomtext']) == 0:
        print("触发文本未配置")
        exit(0)
    if str(senddaily['switch']) == str(1):
        print('已开启每日梗发送')
        print('文本：', senddaily['text'])
        print('发送时间为每日', senddaily['hour'], '点')
        print('已开启发送的群：', senddaily['sendlist'])
    else:
        print('未开启每日发送')
    if str(blacklist['switch']) == str(1):
        print('已开启黑名单模式')
        print('黑名单列表(群)：', blacklist['group'])
        print('黑名单列表(成员)：', blacklist['member'])
    else:
        print('未开启黑名单模式')
    print('查询触发文本:')
    print(tritext['searchtext'])
    print(tritext['randomtext'])
    print('群冷却时间:', rescontrol['group'], '秒   文本:', rescontrol['grouptext'])
    print('群成员冷却时间:', rescontrol['member'], '秒   文本:',
          rescontrol['membertext'])


def Senddaily(data, plat, senddaily):
    hours = time.strftime("%H", time.localtime())
    days = time.strftime("%d", time.localtime())
    if str(senddaily['hour']).zfill(2) == hours:
        for i in senddaily['sendlist']:
            Searchdict = {}
            Searchdict.update(Searchkey=' ')
            Searchdict.update(Searchsender='None')
            Searchdict.update(Searchgroup=i)
            Search(Searchdict, plat)
            simuse.Send_Message(data, i, 1, senddaily['text'], 1)
            imgpath = plat.imgpath()
            simuse.Send_Message(data, i, 1, imgpath, 2, path=1)
        return days


def main():
    plat = platform()
    print("running from", plat.plat)
    data = simuse.Get_data()
    #print(data)
    data = simuse.Get_Session(data)
    seting = GetSeting()
    Checkset(seting)
    print(data)
    print('data Get Success')
    print('Listening……')
    daysign = None
    while 1:
        senddaily = seting['senddaily']
        if str(senddaily['switch']) == str(1):
            day = time.strftime("%d", time.localtime())
            if day != daysign:
                daysign = Senddaily(data, plat, seting['senddaily'])
        GengSearch(data, seting, plat)
        time.sleep(1)


control = rescontrol()
main()
