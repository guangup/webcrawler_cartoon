from  selenium import webdriver
from selenium.common.exceptions import TimeoutException
from multiprocessing import Pool
import os
import requests

from bs4 import BeautifulSoup


class getcartoon():
    def __init__(self,path,url_website):
        self.path=path
        self.title=''
        self.pic_url_list=[]
        self.url_list=[]
        self.picurl_webpic_list=[]
        self.url_list.append(path)
        self.total_url_list=[]
        self.url_website=url_website
        self.number=0
        self.wholetitle=''

    def total_chapter(self):
        path=self.path
        url=self.url_website+path
        response=requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        #print(soup)
        self.wholetitle=str(soup.title.text).split('|')[0]
        finaltitle=self.wholetitle
        print('文件夹名字是:',finaltitle)
        self.mkdir_method(finaltitle)

        a=soup.find_all('dd')
        for i in a:
            for child in i.children:
                if str(child).find('http')!=-1:
                    url_tmp=str(child['href'])
                    print(url_tmp)
                    if len(self.total_url_list)==0:
                        self.total_url_list.append(url_tmp)
                    else:
                        num=len(self.total_url_list)-1
                        path_before=self.total_url_list[num].split('/')[3:]
                        #print('path_before is:',path_before)
                        path_now=url_tmp.split('/')[3:]
                        #print('path_now is :',path_now)
                        if path_before==path_now:
                            print("已经添加")
                        else:
                            self.total_url_list.append(url_tmp)
        print("===========================")
        for i in self.total_url_list:
            print(i)
        print('此漫画目前篇章数量:',len(self.total_url_list))



    def Each_chapter(self,number):
        self.number=number
        driver=webdriver.Firefox()
        driver.set_page_load_timeout(3)
        i=0
        for url in self.total_url_list:
            i=i+1
            if self.number<i+1:
                path=url.split('.com')[1]
                url=url.split(path)[0]
                while path!='/exit/exit.htm':
                   c=0
                   while c <3:
                        try:
                            print('这是马上要访问的页面:',url+path)
                            driver.get(url+path)
                        except TimeoutException:
                            print('！！！！！！time out after 10 seconds when loading page！！！！！！')
                            # 当页面加载时间超过设定时间，通过js来stop，即可执行后续动作
                            driver.execute_script("window.stop()")
                        context=driver.page_source
                        soup = BeautifulSoup(context, 'lxml')
                        #print(soup)
                        self.title=str(soup.title.text)
                        try:
                            nowpic=str(soup.find('a').contents[0]).split('"')[1]
                            nexturl=str(soup.find_all('a')[0]['href'])
                            print('这个漫画叫',self.title)
                            print('这个页面是',nowpic)
                            #print(nexturl)
                            down_url_dire={'pic_url':nowpic,'web_url':path}
                            path=nexturl
                            dirpath='%s/%s'%(self.wholetitle,self.title)
                            self.mkdir_method(dirpath)
                            self.download_pic(down_url_dire)
                            break
                        except:
                            print("获取图片地址失败,第%s次!!"%(str(c+1)))
                            c+=1




                #self.pic_url_list.append(nowpic)
            print("============begin==============")
            print(self.picurl_webpic_list)
            print("============over==============")






    def mkdir_method(self,dirpath):
        #print(self.title)
        #print(type(self.title))
        if os.path.exists(dirpath):
            print('%s目录已经存在!!!'%(dirpath))
        else:
           os.mkdir(dirpath)

    def download_pic(self,directory_key):
        download_link=directory_key['pic_url']
        num=directory_key['web_url'].split('/')[-1].split('.')[0]
        #print(num)
        print('准备下载目录是:',download_link)
        #time.sleep(random.randint(1,10))
        fname='%s/%s/%s.jpg'%(self.wholetitle,self.title,num)
        print(fname)
        if os.path.exists(fname):
            print('%s文件已经存在!!!'%(fname))
        else:
            b=0
            while b < 10:
              try:
                r=requests.get(download_link,timeout=3)
                print("图片地址读取成功!!")
                with open (fname,"wb") as code:
                    code.write(r.content)
                    code.close()
                    print("保存成功!!")
                    break
              except requests.exceptions.RequestException:
                print("下载失败,重新下载,第%s次!!"%(str(b+1)))
                b=b+1



'''
    total_html = sel.find('div', id='play_0')
    total_chapter = []
    for i in total_html.find_all('li'):
        href = i.a['href']
        every_url = 'http://www.gugumh.com' + href
        total_chapter.append(every_url)

    print(total_chapter)
'''
if __name__=='__main__':
    #海贼王 path='/comiclist/4/'
    #鬼灭之刃 path='/comiclist/2126/'
    path_dire={
        '海贼王':'/comiclist/4/',
        '鬼灭之刃':'/comiclist/2126/',
        '一拳超人':'/comiclist/2035/'
    }
    print("漫画爬虫程序,作者:guang")
    print("本程序仅适用于http://comic3.ikkdm.com")
    print("===================================")
    print("漫画目录如下:")
    for i in path_dire:
        print(i)
    print("===================================")
    name = input("请输入漫画名字 ：")
    url_website='http://comic3.ikkdm.com'
    guimian=getcartoon(path_dire[name],url_website)
    guimian.total_chapter()
    number=input("你希望从第几话开始 ：")
    pool=Pool()
    guimian.Each_chapter(int(number))
    #pool.map(guimian.Each_chapter,[i for i in range(int(number))])