#已开源至Github:AYOMITA(阿尤米塔)

class request(object):#请求器，框架的一部分
    def __init__(self):
        self.MY = str(self.__class__.__name__) + ':'
        self.max_error = 10
        self.time_out = 10
        self.header = {'cookie':'YOUR_COOKIE!!!!!!!',
                       'referer':'https://s.weibo.com/',
                       }

    def STD(self,string):#自定义统一输出
        out = output()
        string = self.MY + string
        out.put(string)

    def get(self,url):
        from fake_useragent import UserAgent
        import requests
        import time
        import random
        step = 0
        MAX_ERROR = self.max_error
        self.STD('Request接收数据:{},进入随机休眠.'.format(url))
        time.sleep(random.randint(3,8)*random.random())
        self.STD('请求数据:' + str(url))
        while True:
            if step == MAX_ERROR:
                self.STD(str(url) + '请求失败.共重试' + str(MAX_ERROR) + '次')
                return 'Error'
            else:
                try:
                    self.header['User-Agent'] = UserAgent().random
                    req = requests.get(url,headers=self.header,timeout=3)
                    self.STD('已收到来自'+str(url)+'的数据,状态码识别为:'+str(req.status_code)+',数据长度为:'+str(len(req.text)))
                    if req.status_code == 404:
                        self.STD('链接失效无法获取,已跳转异常.')
                        return 404
                    req.close()
                    return req
                except EOFError:
                    time.sleep(random.randint(3,8)*random.random())
                    step += 1
                    self.STD('EOF连接错误,重试次数:'+str(step))
                    continue
                except ConnectionRefusedError:
                    time.sleep(random.randint(3,8)*random.random())
                    step += 1
                    self.STD('目标拒绝连接,重试次数:'+str(step))
                    return 'refused'
                except TimeoutError:
                    time.sleep(random.randint(3,8)*random.random())
                    step += 1
                    self.STD('超时连接,重试次数:'+str(step))
                    continue
                except:
                    time.sleep(random.randint(3,8)*random.random())
                    step += 1
                    self.STD('未知连接错误,重试次数:'+str(step))
                    continue

class weibo_hot_spider(object):
    def __init__(self):
        self.MY = str(self.__class__.__name__) + ':'
        self.url_lib = {'hot':'https://s.weibo.com/top/summary?cate=realtimehot&sudaref=s.weibo.com&display=0&retcode=6102','hot_id':'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D{}%26t%3D0&page_type=searchall','get_com':'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0'}
        self.class_name_lib = {'td_class':'td-02','name_class':'name'}
        self.cookie = 'SINAGLOBAL=7454122815301.589.1686663142082; _s_tentry=-; Apache=503981901177.2506.1686905627231; ULV=1686905627297:5:5:5:503981901177.2506.1686905627231:1686897438082; SUB=_2A25JiFPCDeRhGeFG6VoS-CvJzDyIHXVq_MIKrDV8PUNbmtANLRDnkW9NefcNtxMrR2ltHa7HKkKyY7ECSKOKq0hk; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF9kXfG-O-wLN2dXafQ_BjZ5JpX5KzhUgL.FoMReon01h-fS052dJLoIpnLxKqL1heLBK5LxK-LBo5L1KBEeh27eK5t; ALF=1718441745; SSOLoginState=1686905746'

    def STD(self,string):#自定义统一输出
        out = output()
        string = self.MY + string
        out.put(string)

    def get_hot_list(self):
        req = request()
        exp = explor()
        import datetime
        from bs4 import BeautifulSoup
        csv_date = str(datetime.datetime.now().strftime('%F'))
        csv_time = str(datetime.datetime.now().strftime('%T'))
        self.STD('组件注册完毕,开始获取热搜榜.')
        hot_s_content = req.get(self.url_lib['hot'])
        if hot_s_content == 'Error':
            self.STD('获取失败.')
            return None
        soup = BeautifulSoup(hot_s_content.text,'html.parser') #仅做技术展示,后续数据解析获取不使用BeautifulSoup而是使用api接口
        items = soup.find_all('td', class_='td-02')
        hot_data_list = []
        for i in items:
            date = str(datetime.datetime.now().strftime('%F'))
            time = str(datetime.datetime.now().strftime('%T'))
            try:
                it_title = i.find('a',target='_blank').text
                it_url = req.header['referer'] + i.find('a',target='_blank')['href']
            except:
                continue
            try:
                count = i.find('span').text
                count = ''.join(filter(str.isdigit,count))
            except:
                count = 'Top'
            it_dict = {}
            it_dict['date'] = date
            it_dict['time'] = time
            it_dict['title'] = it_title
            it_dict['count'] = count
            it_dict['url'] = it_url
            hot_data_list.append(it_dict)
        csv_name = str('hot\\D' + str(csv_date) + 'T' + str(csv_time) + '.csv')
        #D:\learn\weibo\csv\hot
        self.STD('储存csv文件:'+str(csv_name))
        exp.csv_save('hot',csv_name,['date', 'time', 'title','count','url'],hot_data_list)
        return None

    def get_hot_pl(self,hot_name_list):#获取热搜有关的微博的所有评论
        import os
        import datetime
        exp = explor()
        self.STD('获取评论任务启动.')#由于使用BeautifulSoup单独解析网页速度较慢，此处采用api
        def get_weibo_id(hot_name):#获取单个热搜的相关微博ID
            import json
            req = request()
            self = weibo_hot_spider()
            url = self.url_lib['hot_id'].format(hot_name)
            response = req.get(url)
            if response.status_code == 200:
                data = json.loads(response.text)['data']
                weibo_ids = []
                for item in data['cards']:
                    if 'mblog' in item:
                        weibo_ids.append(item['mblog']['id'])
                self.STD('['+str(hot_name)+']的相关微博id:'+str(weibo_ids))
                return weibo_ids
            else:
                return None
        def get_comments(weibo_id):#获取每一个微博的评论表
            import json
            req = request()
            M_self = weibo_hot_spider()
            del req.header['cookie']
            del req.header['referer']
            response = req.get(M_self.url_lib['get_com'].format(weibo_id,weibo_id))
            self.STD('获取ID为:['+str(weibo_id)+']的评论列表.')
            if response.status_code == 200:
                try:
                    data = json.loads(response.text)['data']
                except:
                    return None
                comments = []
                for item in data['data']:
                    comment = {}
                    comment['text'] = item['text']
                    comment['user'] = item['user']['screen_name']
                    comment['time'] = item['created_at']
                    comments.append(comment)
                self.STD('ID:[%s]获取到%s个评论.'%(weibo_id,len(comments)))
                return comments
            else:
                return None
        
        weibo_pl_dict = {}
        for item_name in hot_name_list:
            weibo_pl_dict[item_name] = (get_weibo_id(item_name))
            pl_list = []
            for item_id in weibo_pl_dict[item_name]:
                commot_list = get_comments(item_id)
                if commot_list == None:
                    continue
                else:
                    for item_comm in commot_list:
                        pl_list.append(item_comm)
            weibo_pl_dict[item_name] = pl_list
        
        csv_date = str(datetime.datetime.now().strftime('%F'))
        csv_time = str(datetime.datetime.now().strftime('%T'))
        csv_lib_path = explor().return_csv_lib_path()

        dir_name = str('D'+csv_date+'T'+csv_time)
        name_not_allow_list = ['/','/',':','*','?','"','<','>','|']
        for i in name_not_allow_list:
            dir_name = dir_name.replace(i,'_')
        dir_path = str(str(csv_lib_path)+'pl\\'+str(dir_name))
        os.mkdir(dir_path)

        for item_hot in weibo_pl_dict.keys():
            pl_list_connect = weibo_pl_dict[item_hot]
            csv_name = str(str(item_hot) + '.csv')
            exp.csv_save('pl\\'+dir_name,csv_name,['user', 'time', 'text'],pl_list_connect)
        return None

    def run_get_hot_pl(self):
        exp = explor()
        hot_csv_list = exp.get_list()


class explor(object):#框架的一部分，由于存在强依赖，因此在这里保留
    def __init__(self) -> None:
        self.MY = str(self.__class__.__name__) + ':'

    def path_alive(self,path):
        import os
        if os.path.exists(path) is True:
            self.STD(str(path) + '已确定存在.')
            return None
        else:
            self.STD(str(path) + '不存在,已创建空白目标目录.')
            os.mkdir(path)
            return False
        
    def get_list(self,path):
        import os

        return None
    
    def csv_read(self,path):
        return None
    
    def csv_save(self,path,name,fieldnames,connect):
        import csv
        csv_lib_path = explor().return_csv_lib_path()
        name_not_allow_list = ['/','/',':','*','?','"','<','>','|']
        for i in name_not_allow_list:
            name = name.replace(i,'_')
        csv_name = path + '//'+ name
        with open(str(csv_lib_path+csv_name), 'w', newline='',encoding='gb18030') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(connect)

    def STD(self,string):#自定义统一输出
        out = output()
        string = self.MY + string
        out.put(string)

    def get_ini(self,section,key):
        self.STD('获取ini:'+str(key))
        import configparser
        global main_path
        config = configparser.ConfigParser()
        path = main_path + '/ini'
        config.read(path)
        return config.get(section,key)
    
    def return_main_path(self):
        global main_path
        return main_path
    
    def return_csv_lib_path(self):
        global csv_lib_path
        return csv_lib_path

    def start(self):
        self.STD('已开始探知环境.')
        global main_path
        global csv_lib_path
        csv_lib_path = main_path + self.get_ini('storge','csv_lib')
        self.STD('csv输出已确定:'+str(csv_lib_path))
        self.path_alive(csv_lib_path)
        return None

class due_bit(object):
    def __init__(self) -> None:
        self.MY = str(self.__class__.__name__) + ':'

    ok = weibo_hot_spider()
    global csv_lib_path
    csv_lib_path = 'D:\learn\weibo\csv//'
    ok.get_hot_pl(['庆余年2官宣阵容','11年前的今天太空迎来中国女性','嗯哼 追星成功太开心啦','吴倩方晒出院记录','国足vs缅甸'])
