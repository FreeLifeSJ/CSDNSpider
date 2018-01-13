class Get_First_Url:
    def __init__(self, url2):
        self.url = url2
        print('\n')
        print('开始获取第一篇博客地址')
        print('博客主页地址： ' + self.url)
        '''
        这是注释
        '''
        user_agents = [
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
            'Opera/9.25 (Windows NT 5.1; U; en)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
            'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
            'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
            "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
            "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
        ]
        agent = random.choice(user_agents)
        req = urllib2.Request(self.url)
        req.add_header('User-Agent', agent)
        req.add_header('Host', 'blog.csdn.net')
        req.add_header('Accept', '*/*')
        req.add_header('Referer', 'http://blog.csdn.net/mangoer_ys?viewmode=list')
        req.add_header('GET', url)
        html = urllib2.urlopen(req)
        page = html.read().decode('utf-8')
        self.page = page
        self.beginurl = self.getFirstUrl()

    # 得到其博客主页的第一篇文章
    def getFirstUrl(self):
        bs = BeautifulSoup(self.page)
        html_content_list = bs.find('span', class_='link_title')
        self.type = 1
        if (html_content_list == None):
            html_content_list = bs.find('h3', class_='list_c_t')  # 不同的主题
            self.type = 2
            if (html_content_list == None):
                return "nourl"

        try:
            return 'http://blog.csdn.net' + html_content_list.a['href']
        except Exception, e:
            return "nourl"
