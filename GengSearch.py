from email import message
import ssl
from bs4 import BeautifulSoup
import imgkit
import requests
import time
import simuse
import os

def log(SearchUrl='Error',infoUrl='Error',runingtime=0,target='None',mebmerID='None'):
    date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    target=str(target)
    mebmerID=str(mebmerID)
    runingtime=str(runingtime)
    loginfo='\n'+'-------------------------------------------------------------------------'+'\n'
    loginfo=loginfo+'Date:'+date+'\n'
    loginfo=loginfo+'SenderGroup:'+target+'\n'
    loginfo=loginfo+'SenderID:'+mebmerID+'\n'
    loginfo=loginfo+'SearchUrl:'+SearchUrl+'\n'
    loginfo=loginfo+'InfoUrl:'+infoUrl+'\n'
    loginfo=loginfo+'RuningTime:'+runingtime+' S'+'\n'
    logfile=open('log.txt','a',encoding='utf-8')
    logfile.write(loginfo)
    logfile.close()
    print('save log')
  
def Search(Searchinfo):
    try:
        print('Get mission')
        start=time.perf_counter()
        cookiefile=open('cookie.txt','r',encoding='utf-8')
        cookie=cookiefile.read()
        cookiefile.close()
        #print(cookie)
        try:       
            cookie = dict([l.split("=", 1) for l in cookie.split("; ")])
        except:
            print('can not find cookie.txt')
            cookie={}
        SearchUrl='https://jikipedia.com/search?phrase='
        Searchgroup=Searchinfo['Searchgroup']
        Searchsender=Searchinfo['Searchsender']
        Searchinfo=Searchinfo['Searchkey']
        SearchUrl=SearchUrl+Searchinfo
        SearchUrl=SearchUrl+'&category=definition'
        Searchlist=requests.get(SearchUrl,cookies=cookie)
        Searchlist=Searchlist.text
        #print(type(Searchlist))
        Searchhtmlfile=open('temp/Searchlist.html','w',encoding='utf-8')
        Searchhtmlfile.write(Searchlist)
        Searchhtmlfile.close()
        idnum=Searchlist.find('div data-id=')
        #print(idnum)
        idnum1=Searchlist.find('"',idnum)
        #print(idnum1)
        idnum1+=1
        idnum2=Searchlist.find('"',idnum1)
        #print(idnum2)
        idnum1=int(idnum1)
        idnum2=int(idnum2)
        Searchid=Searchlist[idnum1:idnum2]
        print('Searchid:',Searchid)
        infoUrl='https://jikipedia.com/definition/'
        infoUrl=infoUrl+Searchid
        print('infoUrl:',infoUrl)
        infolist=requests.get(infoUrl,cookies=cookie)
        infolist=infolist.text
        soup = BeautifulSoup(infolist, "lxml")
        title=soup.select('.title-container')[0]
        body=soup.select('.content')[0]
        try:
            img=soup.select('.show')[0]
        except:
            img=''
        title=str(title)
        title='<center>'+title+'</center>'
        body=str(body)
        img=str(img)
        if img.find('show image button image')==-1:
            img=''        
        img='<center>'+img+'</center>'
        headfile=open('head.html','r',encoding='utf-8')
        head=headfile.read()
        headfile.close()
        head=head+'\n'
        html=head+title+'\n'+body+'\n'+img+'\n'
        #print(html)
        htmlfile=open('temp/Searchinfo.html','w',encoding='utf-8')
        htmlfile.write(html)
        htmlfile.close()
        path_wkimg='wkhtmltopdf/bin/wkhtmltoimage.exe'
        cfg = imgkit.config(wkhtmltoimage=path_wkimg)
        imgkit.from_file('temp/Searchinfo.html', 'temp/Searchinfo_img.jpg', config=cfg)
        end = time.perf_counter()
        runingtime=end-start
        print('Success')
        print('RuningTime:',runingtime)
        log(SearchUrl,infoUrl,runingtime,Searchgroup,Searchsender)
    except:
        print('Error')
        log(target=Searchgroup,mebmerID=Searchsender)
    finally:
        print('\nListing……')

def Listing(data):
    #print('listing...')
    message=simuse.Fetch_Message(data)
    SearchList=[]
    Searchdict={}
    if type(message)==type(0):
        #print('not')
        return SearchList
    for i in message:
        checktext='none'
        if i['type']=='GroupMessage':
            messagechain_list=i['messagechain']
            messagechain_infodict=messagechain_list[1]
            if messagechain_infodict['type']=='Plain':
                checktext=messagechain_infodict['text']
        if checktext[:4]=='梗查询 ':
            Searchdict.update(Searchkey=checktext[4:])
            Searchdict.update(Searchsender=i['sender'])
            Searchdict.update(Searchgroup=i['group'])
            SearchList.append(Searchdict.copy())
        elif checktext=='来点梗':
            Searchdict.update(Searchkey=' ')
            Searchdict.update(Searchsender=i['sender'])
            Searchdict.update(Searchgroup=i['group'])
            SearchList.append(Searchdict.copy())            
    #print(SearchList)
    return SearchList        

def GengSearch(data):
    SearchList=[]
    SearchList=Listing(data)
    #print(SearchList)
    SearchListcheck=[]
    if SearchList!=SearchListcheck:
        for i in SearchList:
            Search(i)
            imgpath=os.getcwd()
            imgpath=imgpath+r'\\temp\\Searchinfo_img.jpg'
            simuse.Send_Message(data,i['Searchgroup'],1,imgpath,2,path=1)
    
def main():
    data=simuse.Get_data()
    #print(data)
    data=simuse.Get_Session(data)
    print(data)
    print('data Get Success')
    print('Listing……')
    while 1:
        GengSearch(data)
        time.sleep(2)

        
main()





