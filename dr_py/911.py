# -*- coding: utf-8 -*-
import json
import random
import re
import sys
import threading
import time
import requests
from base64 import b64decode, b64encode
from urllib.parse import urlparse, urljoin
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from bs4 import BeautifulSoup
sys.path.append('..')
from base.spider import Spider

class Spider(Spider):

    def init(self, extend="{}"):
        config = json.loads(extend)
        self.domin = config.get('site', "https://911blw.com")
        self.proxies = config.get('proxy', {}) or {}
        self.plp = config.get('plp', '')
        self.backup_urls = ["https://hlj.fun", "https://911bl16.com"]
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="134", "Google Chrome";v="134"',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        
        # 获取最佳主机
        self.host = self.host_late([self.domin] + self.backup_urls)
        self.headers.update({'Origin': self.host, 'Referer': f"{self.host}/"})
        
        # 缓存主机信息
        self.getcnh()

    def getName(self):
        return "911爆料网"

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def destroy(self):
        pass

    def homeContent(self, filter):
        result = {}
        classes = []
        
        # 分类列表（根据911爆料网的实际分类）
        categories = [
            {"type_id": "/category/jrgb/", "type_name": "最新爆料"},
            {"type_id": "/category/rmgb/", "type_name": "精选大瓜"},
            {"type_id": "/category/blqw/", "type_name": "猎奇吃瓜"},
            {"type_id": "/category/rlph/", "type_name": "TOP5大瓜"},
            {"type_id": "/category/ssdbl/", "type_name": "社会热点"},
            {"type_id": "/category/hjsq/", "type_name": "海角社区"},
            {"type_id": "/category/mrds/", "type_name": "每日大赛"},
            {"type_id": "/category/xyss/", "type_name": "校园吃瓜"},
            {"type_id": "/category/mxhl/", "type_name": "明星吃瓜"},
            {"type_id": "/category/whbl/", "type_name": "网红爆料"},
            {"type_id": "/category/bgzq/", "type_name": "反差爆料"},
            {"type_id": "/category/fljq/", "type_name": "网黄福利"},
            {"type_id": "/category/crfys/", "type_name": "午夜剧场"},
            {"type_id": "/category/thjx/", "type_name": "探花经典"},
            {"type_id": "/category/dmhv/", "type_name": "禁漫天堂"},
            {"type_id": "/category/slec/", "type_name": "吃瓜精选"},
            {"type_id": "/category/zksr/", "type_name": "重口调教"},
            {"type_id": "/category/crlz/", "type_name": "精选连载"}
        ]
        
        result['class'] = categories
        
        # 首页推荐内容
        html = self.fetch_page(f"{self.host}/")
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            articles = soup.select('article, .post-item, .article-item')
            result['list'] = self.getlist(articles)
        else:
            result['list'] = []
            
        return result

    def homeVideoContent(self):
        # 首页推荐视频
        html = self.fetch_page(f"{self.host}/category/jrgb/1/")
        videos = self.extract_content(html, f"{self.host}/category/jrgb/1/")
        return {'list': videos}

    def categoryContent(self, tid, pg, filter, extend):
        if '@folder' in tid:
            # 文件夹类型内容
            id = tid.replace('@folder', '')
            videos = self.getfod(id)
        else:
            # 普通分类内容
            url = f"{self.host}{tid}{pg}/" if pg != "1" else f"{self.host}{tid}"
            html = self.fetch_page(url)
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                articles = soup.select('article, .post-item, .article-item, ul.row li')
                videos = self.getlist(articles, tid)
            else:
                videos = []
                
        result = {}
        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = 1 if '@folder' in tid else 99999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def detailContent(self, ids):
        url = ids[0] if ids[0].startswith("http") else f"{self.host}{ids[0]}"
        html = self.fetch_page(url)
        
        if not html:
            return {'list': []}
            
        soup = BeautifulSoup(html, 'html.parser')
        vod = {'vod_play_from': '911爆料网'}
        
        try:
            # 提取标签信息
            clist = []
            tags = soup.select('.tags .keywords a, .tagcloud a, a[rel="tag"]')
            for tag in tags:
                title = tag.get_text(strip=True)
                href = tag.get('href', '')
                if href and title:
                    clist.append('[a=cr:' + json.dumps({'id': href, 'name': title}) + '/]' + title + '[/a]')
                    
            vod['vod_content'] = '点击展开↓↓↓\n'+' '.join(clist) if clist else soup.select_one('.post-content, .entry-content').get_text(strip=True)[:200] + '...'
        except:
            title_elem = soup.select_one('h1, .post-title, .entry-title')
            vod['vod_content'] = title_elem.get_text(strip=True) if title_elem else "无简介"
        
        try:
            # 提取播放列表（类似51吸瓜的dplayer方式）
            plist = []
            
            # 方式1：检查dplayer
            dplayers = soup.select('.dplayer, [data-config]')
            for c, player in enumerate(dplayers, start=1):
                config_str = player.get('data-config', '{}')
                try:
                    config = json.loads(config_str)
                    if 'video' in config and 'url' in config['video']:
                        plist.append(f"视频{c}${config['video']['url']}")
                except:
                    pass
            
            # 方式2：检查视频标签
            if not plist:
                video_tags = soup.select('video source, video[src]')
                for c, video in enumerate(video_tags, start=1):
                    src = video.get('src') or ''
                    if src:
                        plist.append(f"视频{c}${src}")
            
            # 方式3：检查iframe
            if not plist:
                iframes = soup.select('iframe[src]')
                for c, iframe in enumerate(iframes, start=1):
                    src = iframe.get('src', '')
                    if src and ('player' in src or 'video' in src):
                        plist.append(f"视频{c}${src}")
            
            # 方式4：从脚本中提取
            if not plist:
                scripts = soup.find_all('script')
                for script in scripts:
                    if script.string:
                        # 查找m3u8、mp4等视频链接
                        video_matches = re.findall(r'(https?://[^\s"\']*\.(?:m3u8|mp4|flv|ts|mkv)[^\s"\']*)', script.string)
                        for c, match in enumerate(video_matches, start=1):
                            plist.append(f"视频{c}${match}")
            
            vod['vod_play_url'] = '#'.join(plist) if plist else f"请检查页面，可能没有视频${url}"
            
        except Exception as e:
            print(f"详情页解析错误: {e}")
            vod['vod_play_url'] = f"解析错误${url}"
        
        return {'list': [vod]}

    def searchContent(self, key, quick, pg="1"):
        url = f"{self.host}/search/{key}/{pg}/"
        html = self.fetch_page(url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            articles = soup.select('article, .post-item, .article-item, ul.row li')
            videos = self.getlist(articles)
        else:
            videos = []
            
        return {'list': videos, 'page': pg, 'pagecount': 9999, 'limit': 90, 'total': 999999}

    def playerContent(self, flag, id, vipFlags):
        # 判断是否为直接播放的视频格式
        p = 0 if re.search(r'\.(m3u8|mp4|flv|ts|mkv|mov|avi|webm)', id) else 1
        return {'parse': p, 'url': f"{self.plp}{id}", 'header': self.headers}

    def localProxy(self, param):
        try:
            url = self.d64(param['url'])
            match = re.search(r"loadBannerDirect\('([^']*)'", url)
            if match:
                url = match.group(1)
                
            res = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=10)
            
            # 检查是否需要AES解密（根据文件类型判断）
            if url.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                # 普通图片直接返回
                return [200, res.headers.get('Content-Type'), res.content]
            else:
                # 加密内容进行AES解密
                return [200, res.headers.get('Content-Type'), self.aesimg(res.content)]
                
        except Exception as e:
            print(f"图片代理错误: {str(e)}")
            return [500, 'text/html', '']

    def e64(self, text):
        try:
            text_bytes = text.encode('utf-8')
            encoded_bytes = b64encode(text_bytes)
            return encoded_bytes.decode('utf-8')
        except Exception as e:
            print(f"Base64编码错误: {str(e)}")
            return ""

    def d64(self, encoded_text):
        try:
            encoded_bytes = encoded_text.encode('utf-8')
            decoded_bytes = b64decode(encoded_bytes)
            return decoded_bytes.decode('utf-8')
        except Exception as e:
            print(f"Base64解码错误: {str(e)}")
            return ""

    def aesimg(self, word):
        key = b'f5d965df75336270'
        iv = b'97b60394abc2fbe1'
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(word), AES.block_size)
        return decrypted

    def fetch_page(self, url, use_backup=False):
        original_url = url
        if use_backup:
            for backup in self.backup_urls:
                test_url = url.replace(self.domin, backup)
                try:
                    time.sleep(1)
                    res = requests.get(test_url, headers=self.headers, proxies=self.proxies, timeout=10)
                    res.raise_for_status()
                    res.encoding = "utf-8"
                    text = res.text
                    if len(text) > 1000:
                        print(f"[DEBUG] 使用备用 {backup}: {test_url}")
                        return text
                except:
                    continue
        
        try:
            time.sleep(1)
            res = requests.get(original_url, headers=self.headers, proxies=self.proxies, timeout=10)
            res.raise_for_status()
            res.encoding = "utf-8"
            text = res.text
            if len(text) < 1000:
                print(f"[DEBUG] 内容过短，尝试备用域名")
                return self.fetch_page(original_url, use_backup=True)
            return text
        except Exception as e:
            print(f"[ERROR] 请求失败 {original_url}: {e}")
            return None

    def getcnh(self):
        try:
            html = self.fetch_page(f"{self.host}/about.html")
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                link = soup.select_one('a[href]')
                if link:
                    url = link.get('href')
                    parsed_url = urlparse(url)
                    host = parsed_url.scheme + "://" + parsed_url.netloc
                    self.setCache('host_911blw', host)
        except Exception as e:
            print(f"获取主机信息错误: {str(e)}")

    def host_late(self, url_list):
        if not url_list:
            return self.domin
            
        results = {}
        threads = []

        def test_host(url):
            try:
                start_time = time.time()
                response = requests.head(url, headers=self.headers, proxies=self.proxies, timeout=1.0, allow_redirects=False)
                delay = (time.time() - start_time) * 1000
                results[url] = delay
            except Exception as e:
                results[url] = float('inf')

        for url in url_list:
            t = threading.Thread(target=test_host, args=(url,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        return min(results.items(), key=lambda x: x[1])[0]

    def getfod(self, id):
        url = f"{self.host}{id}"
        html = self.fetch_page(url)
        if not html:
            return []
            
        soup = BeautifulSoup(html, 'html.parser')
        videos = []
        
        # 查找文件夹内容
        content = soup.select_one('.post-content, .entry-content')
        if content:
            # 移除不需要的元素
            for elem in content.select('.txt-apps, .line, blockquote, .tags, .content-tabs'):
                elem.decompose()
                
            # 提取标题和链接
            headings = content.select('h2, h3, h4')
            paragraphs = content.select('p')
            
            for i, heading in enumerate(headings):
                title = heading.get_text(strip=True)
                if i < len(paragraphs):
                    link = paragraphs[i].select_one('a')
                    if link:
                        videos.append({
                            'vod_id': link.get('href', ''),
                            'vod_name': link.get_text(strip=True),
                            'vod_pic': f"{self.getProxyUrl()}&url={self.e64(link.get('data-img', ''))}",
                            'vod_remarks': title
                        })
        
        return videos

    def getlist(self, articles, tid=''):
        videos = []
        is_folder = '/mrdg' in tid
        
        for article in articles:
            try:
                # 标题
                title_elem = article.select_one('h2, h3, .headline, .title, a[title]')
                name = title_elem.get_text(strip=True) if title_elem else ""
                
                # 链接
                link_elem = article.select_one('a')
                href = link_elem.get('href', '') if link_elem else ""
                
                # 日期/备注
                date_elem = article.select_one('time, .date, .published')
                remarks = date_elem.get_text(strip=True) if date_elem else ""
                
                # 图片（使用吸瓜的方式）
                pic = None
                script_elem = article.select_one('script')
                if script_elem and script_elem.string:
                    base64_match = re.search(r'base64,[\'"]?([A-Za-z0-9+/=]+)[\'"]?', script_elem.string)
                    if base64_match:
                        encoded_url = base64_match.group(1)
                        pic = f"{self.getProxyUrl()}&url={self.e64(encoded_url)}"
                
                if not pic:
                    img_elem = article.select_one('img[data-xkrkllgl]')
                    if img_elem and img_elem.get('data-xkrkllgl'):
                        encoded_url = img_elem.get('data-xkrkllgl')
                        pic = f"{self.getProxyUrl()}&url={self.e64(encoded_url)}"
                
                if not pic:
                    img_elem = article.select_one('img')
                    if img_elem:
                        for attr in ["data-lazy-src", "data-original", "data-src", "src"]:
                            pic = img_elem.get(attr)
                            if pic:
                                pic = urljoin(self.host, pic)
                                break
                
                if name and href:
                    videos.append({
                        'vod_id': f"{href}{'@folder' if is_folder else ''}",
                        'vod_name': name.replace('\n', ' '),
                        'vod_pic': pic,
                        'vod_remarks': remarks,
                        'vod_tag': 'folder' if is_folder else '',
                        'style': {"type": "rect", "ratio": 1.33}
                    })
                    
            except Exception as e:
                print(f"列表项解析错误: {e}")
                continue
                
        return videos

if __name__ == "__main__":
    spider = Spider()
    spider.init('{"site": "https://911blw.com"}')
    
    # 测试首页
    result = spider.homeContent({})
    print(f"首页分类: {len(result['class'])} 个")
    print(f"首页内容: {len(result['list'])} 个")
    
    # 测试分类
    result = spider.categoryContent("/category/jrgb/", "1", False, {})
    print(f"分类内容: {len(result['list'])} 个")
    
    # 测试搜索
    result = spider.searchContent("测试", False, "1")
    print(f"搜索结果: {len(result['list'])} 个")