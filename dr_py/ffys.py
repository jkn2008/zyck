# -*- coding: utf-8 -*-
"""
ffys.fun 飞飞影视‑Chaquopy Python Spider
FongMi‑TVBox / OK‑TVBox
✅浏览器实测真实分类ID：电影20，剧集21，动漫22，综艺23
"""
import sys
sys.path.append('..')

# 本地调试模拟基类
try:
    from base.spider import Spider
except ImportError:
    import types
    base_mod = types.ModuleType('base')
    spider_mod = types.ModuleType('base.spider')
    class Spider:
        pass
    spider_mod.Spider = Spider
    base_mod.spider = spider_mod
    sys.modules['base'] = base_mod
    sys.modules['base.spider'] = spider_mod

import re
import json
import ssl
import urllib.request
import urllib.error
from urllib.parse import quote, unquote


class Spider(Spider):
    HOST = "https://www.ffys.fun"
    UA = "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"

    # ✅浏览器地址栏实测分类ID
    CATEGORIES = [
        {"type_name": "电影", "type_id": "20"},
        {"type_name": "剧集", "type_id": "21"},
        {"type_name": "动漫", "type_id": "22"},
        {"type_name": "综艺", "type_id": "23"},
    ]

    def getName(self):
        return "飞飞影视"

    def init(self, extend=""):
        self.headers = {
            "User‑Agent": self.UA,
            "Referer": self.HOST + "/",
            "Accept": "application/json,text/*;q=0.9,*/*;q=0.8"
        }
        self._ssl_ctx = ssl.create_default_context()
        self._ssl_ctx.check_hostname = False
        self._ssl_ctx.verify_mode = ssl.CERT_NONE

    def getDependence(self):
        return []

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def action(self, action):
        pass

    def destroy(self):
        pass

    def _fetch(self, url, headers=None, timeout=12):
        """GET 请求，优先框架fetch，回退urllib"""
        hdr = headers if headers else self.headers
        try:
            rsp = self.fetch(url, headers=hdr)
            if isinstance(rsp, str):
                return rsp
            if rsp and hasattr(rsp, "text"):
                return rsp.text
        except Exception:
            pass

        try:
            req = urllib.request.Request(url, headers=hdr)
            opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=self._ssl_ctx))
            with opener.open(req, timeout=timeout) as resp:
                raw = resp.read()
                return raw.decode("utf‑8", errors="ignore")
        except urllib.error.HTTPError as e:
            try:
                return e.read().decode("utf‑8", errors="ignore")
            except Exception:
                return ""
        except Exception:
            return ""

    @staticmethod
    def _fix_pic(url):
        if not url:
            return ""
        url = url.strip()
        if url.startswith("http"):
            return url
        if url.startswith("//"):
            return "https:" + url
        return ""

    # ========== 首页内容 ==========
    def homeContent(self, filter):
        result = dict()
        result["class"] = self.CATEGORIES
        result["filters"] = dict()

        resp_text = self._fetch(f"{self.HOST}/api/home")
        vod_list = []
        if resp_text:
            try:
                js = json.loads(resp_text)
                data_arr = js.get("data", [])
                for item in data_arr:
                    vod_list.append({
                        "vod_id": str(item.get("id", "")),
                        "vod_name": item.get("title", ""),
                        "vod_pic": self._fix_pic(item.get("pic", "")),
                        "vod_remarks": item.get("update", "")
                    })
            except Exception:
                pass
        result["list"] = vod_list
        return result

    # 首页轮播/推荐
    def homeVideoContent(self):
        result = {"list": []}
        resp_text = self._fetch(f"{self.HOST}/api/home")
        if resp_text:
            try:
                js = json.loads(resp_text)
                arr = js.get("data", [])
                lst = []
                for it in arr[:24]:
                    lst.append({
                        "vod_id": str(it.get("id")),
                        "vod_name": it.get("title", ""),
                        "vod_pic": self._fix_pic(it.get("pic", "")),
                        "vod_remarks": it.get("update", "")
                    })
                result["list"] = lst
            except Exception:
                pass
        return result

    # ========== 分类列表，tid=20/21/22/23 ==========
    def categoryContent(self, tid, pg, filter, extend):
        result = {
            "list": [],
            "page": int(pg) if pg else 1,
            "pagecount": 9999,
            "limit": 30,
            "total": 9999
        }
        api_url = f"{self.HOST}/api/cate?type={tid}&page={pg}"
        resp_text = self._fetch(api_url)
        if not resp_text:
            return result
        try:
            js = json.loads(resp_text)
            data_arr = js.get("data", [])
            out = []
            for item in data_arr:
                out.append({
                    "vod_id": str(item.get("id", "")),
                    "vod_name": item.get("title", ""),
                    "vod_pic": self._fix_pic(item.get("pic", "")),
                    "vod_remarks": item.get("update", "")
                })
            result["list"] = out
        except Exception:
            pass
        return result

    # ========== 详情页：信息 + 多线路集数 ==========
    def detailContent(self, ids):
        result = {"list": []}
        if not ids:
            return result
        vid = ids[0]
        api_url = f"{self.HOST}/api/detail?id={vid}"
        resp_text = self._fetch(api_url)
        if not resp_text:
            return result
        try:
            js = json.loads(resp_text)
            d = js.get("data", {})
            vod = {
                "vod_id": str(d.get("id", "")),
                "vod_name": d.get("title", ""),
                "vod_pic": self._fix_pic(d.get("pic", "")),
                "vod_year": d.get("year", ""),
                "vod_area": d.get("area", ""),
                "vod_actor": d.get("actor", ""),
                "vod_director": d.get("director", ""),
                "vod_content": d.get("desc", ""),
                "vod_remarks": d.get("update", ""),
                "vod_play_from": "",
                "vod_play_url": ""
            }
            play_from_arr = []
            play_url_arr = []
            play_list = d.get("playList", [])
            for idx, line in enumerate(play_list):
                line_name = line.get("name", f"线路{idx+1}")
                ep_list = line.get("list", [])
                ep_str_parts = []
                for ep in ep_list:
                    ep_name = ep.get("name", "")
                    ep_url = ep.get("url", "")
                    ep_str_parts.append(f"{ep_name}${ep_url}")
                if ep_str_parts:
                    play_from_arr.append(line_name)
                    play_url_arr.append("#".join(ep_str_parts))

            vod["vod_play_from"] = "$$$".join(play_from_arr)
            vod["vod_play_url"] = "$$$".join(play_url_arr)
            result["list"] = [vod]
        except Exception:
            pass
        return result

    # ========== 搜索 ==========
    def searchContent(self, key, quick):
        result = {"list": []}
        safe_key = quote(key)
        api_url = f"{self.HOST}/api/search?wd={safe_key}&page=1"
        resp_text = self._fetch(api_url)
        if not resp_text:
            return result
        try:
            js = json.loads(resp_text)
            data_arr = js.get("data", [])
            out = []
            for item in data_arr:
                out.append({
                    "vod_id": str(item.get("id", "")),
                    "vod_name": item.get("title", ""),
                    "vod_pic": self._fix_pic(item.get("pic", "")),
                    "vod_remarks": item.get("update", "")
                })
            result["list"] = out
        except Exception:
            pass
        return result

    # ========== 播放 ==========
    def playerContent(self, flag, id, vipFlags):
        real_url = id
        headers = {
            "User‑Agent": self.UA,
            "Referer": self.HOST
        }
        return {
            "parse": 0,
            "playUrl": "",
            "jx": 0,
            "url": real_url,
            "header": headers
        }

    def localProxy(self, param):
        action = {
            "url": "",
            "header": "",
            "param": "",
            "type": "string",
            "after": ""
        }
        return [200, "video/MP2T", action, ""]
