class CSDN_Blog_Spider:
    def __init__(self, url2, type):
        self.url = url2
        self.type = type
        if type == 4:
            global WAIT_URL
            WAIT_URL = url2
            print '已记录待爬下一篇地址' + url2
            print('正在爬取网页地址： ' + self.url)
        else:
            print('正在爬取网页地址： ' + self.url)
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
        self.articalid = self.getArticleId()
        self.authorid = self.getAuthorId()
        self.linkurl = self.getLinkUrl()
        self.blogname = self.getBlogName()
        self.title = self.getTitle()
        print('文章标题是 ' + self.title)
        self.content = self.getContent()
        self.time = self.getTime()
        self.imgurl = self.getImg()
        if self.query():
            self.saveToLeanCloud()

    # 获取文章id
    def getArticleId(self):
        location = -1
        locationList = []
        isStop = True
        while isStop:
            location = self.url.find('/', location + 1)
            if location == -1:
                isStop = False
            else:
                locationList.append(location)

        artical_id = self.url[(locationList[-1] + 1):]
        return artical_id

    # 获取文章link url
    def getLinkUrl(self):
        location = -1
        locationList = []
        isStop = True
        while isStop:
            location = self.url.find('/', location + 1)

            if location == -1:
                isStop = False
            else:
                locationList.append(location)

        link_url = self.url[locationList[2]:]
        return link_url

    # 获得作者id
    def getAuthorId(self):
        location = -1
        locationList = []
        isStop = True
        while isStop:
            location = self.url.find('/', location + 1)

            if location == -1:
                isStop = False
            else:
                locationList.append(location)

        # 第二次和第三次斜杠之间
        author_id = self.url[(locationList[2] + 1):locationList[3]]
        return author_id

    def getTitle(self):
        bs = BeautifulSoup(self.page)

        location = -1
        locationList = []
        isStop = True
        while isStop:
            location = bs.title.string.find('-', location + 1)

            if location == -1:
                isStop = False
            else:
                locationList.append(location)
        # 截取倒数第三次横杆出现前面的字符
        new_title = bs.title.string[:locationList[-3]]
        return new_title.strip()

    def getBlogName(self):
        bs = BeautifulSoup(self.page)
        if self.type == 2:
            html_content_list = bs.find_all('h2', class_='blog_l_t')
            return html_content_list[0].string
        else:
            html_content_list = bs.find('a', href=('http://blog.csdn.net/' + self.authorid))
            return str(html_content_list.string)

    def getTime(self):
        bs = BeautifulSoup(self.page)
        if (self.type == 2):
            html_content_list = bs.findAll('div', class_='date')
            newtime = html_content_list[0].span.string + '-' + html_content_list[0].em.string
            html_content_list = bs.findAll('div', class_='date_b')
            new_time = newtime + '-' + html_content_list[0].string
            return new_time
        else:
            html_content_list = bs.find('span', class_='link_postdate')
            return str(html_content_list.string)

    def getImg(self):
        bs = BeautifulSoup(self.page)
        blog_userface_list = bs.find('div', id='blog_userface')
        if (blog_userface_list == None):
            blog_userface_list = bs.find('div', class_='mess')

        try:
            return blog_userface_list.img['src']
        except Exception, e:
            return " "

    def getContent(self):
        bs = BeautifulSoup(self.page)
        html_content_list = bs.findAll('div', {'id': 'article_content', 'class': 'article_content'})
        if (html_content_list == None or len(html_content_list) == 0):
            html_content_list = bs.find_all('div', {'id': 'article_content', 'class': 'skin_detail'})
        html_content = str(html_content_list[0])
        content = html_content
        if '$numbering.append' in content:
            location = -1
            locationList = []
            isStop = True
            while isStop:
                location = content.find('script', location + 1)  # script

                if location == -1:
                    isStop = False
                else:
                    locationList.append(location)

            mylenth = len(locationList)
            newContent = content[:(locationList[mylenth - 3] - 1)] + content[(locationList[mylenth - 1] + 7):]
        else:
            newContent = content

        return newContent

    # 查询是否存在该文章
    def query(self):
        QueryObject = leancloud.Object.extend('CSDNBlogList')
        query_object = leancloud.Query(QueryObject)
        # 先判断文章id是否存在
        query_list = query_object.equal_to('articleid', self.articalid).find()
        if len(query_list) == 0:
            print '数据库没有，可上传'
            return True
        elif query_list[0].get('authorid') == self.authorid:  # 再判断是否等于数据库中该文章的作者id
            print '数据库数据重复'
            return False
        elif query_list[0].get('blogname') == '':
            print '标题为空，可上传'
            return True

    # 数据存入leancloud
    def saveToLeanCloud(self):
        TestObject = Object.extend('CSDNBlogList')
        test_object = TestObject()
        test_object.set('authorid', self.authorid)
        test_object.set('articleid', self.articalid)
        test_object.set('title', self.title)
        test_object.set('blogname', self.blogname)
        test_object.set('content', self.content)
        test_object.set('time', self.time)
        test_object.set('img', self.imgurl)
        try:
            test_object.save()
            print '存储成功'
        except LeanCloudError, e:
            print e

    def saveFile(self):
        outfile = open(r'D:\123.txt', 'a')
        outfile.write(self.title)

    def getNextArticle(self):
        bs2 = BeautifulSoup(self.page)
        html = bs2.find('li', class_='prev_article')
        if html == None:
            print '没有上一篇'
            return None
        else:
            return None  # 不读取上一篇，直接去往下遍历读取最新的文章(注释掉这句则会读取上一篇)
            print '有上一篇，地址：' + 'http://blog.csdn.net' + html.a['href']
            return 'http://blog.csdn.net' + html.a['href']

    def getLastArticle(self):  # 下一篇
        bs2 = BeautifulSoup(self.page)
        html = bs2.find('li', class_='next_article')
        if html == None:
            global WAIT_URL
            WAIT_URL = None
            print '没有下一篇'
        else:
            print '有下一篇，地址：' + 'http://blog.csdn.net' + html.a['href']
            global WAIT_URL
            WAIT_URL = 'http://blog.csdn.net' + html.a['href']

    def getLastArticleUrl(self):  # 下一篇
        bs2 = BeautifulSoup(self.page)
        html = bs2.find('li', class_='next_article')
        if html == None:
            print '没有下一篇'
            return None
        else:
            print '有下一篇，地址：' + 'http://blog.csdn.net' + html.a['href']
            return 'http://blog.csdn.net' + html.a['href']
