# -*- coding: utf-8 -*-
"""
ffys.fun 飞飞影视‑Chaquopy Python Spider
现象：分类显示，但首页无数据，优化网络请求
分类ID：电影20，剧集21，动漫22，综艺23
"""
import sys
sys.path.append('..')

try:
    from base.spider import Spider
except ImportError:
    import types
    base_mod = types.ModuleType('base')
    spider_mod = types.ModuleType('base.spider')
    class Spider:pass
    spider_mod.Spider = Spider
    base_mod.spider = spider_mod
    sys.modules['base'] = base_mod
    sys.modules['base.spider'] = spider_mod

import json
import ssl
import urllib.request
import urllib.error
from urllib.parse import quote


class Spider(Spider):
    HOST = "https://www.ffys.fun"
    UA = "Mozilla/5.0 (Android 14; Mobile) Chrome/128.0.0.0 Mobile Safari/537.36"

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
            "User-Agent": self.UA,
            "Referer": self.HOST + "/",
            "Accept": "application/json",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        # ssl关闭证书校验
        self._ssl_ctx = ssl.create_default_context()
        self._ssl_ctx.check_hostname = False
        self._ssl_ctx.verify_mode = ssl.CERT_NONE

    def getDependence(self):return []
    def isVideoFormat(self, url):pass
    def manualVideoCheck(self):pass
    def action(self, action):pass
    def destroy(self):pass

    def _fetch(self, url, timeout=15):
        """优先urllib，部分Chaquopy内置fetch异常直接废弃不用"""
        try:
            req = urllib.request.Request(url, headers=self.headers)
            opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=self._ssl_ctx))
            with opener.open(req, timeout=timeout) as resp:
                raw = resp.read()
                return raw.decode("utf-8", errors="ignore")
        except urllib.error.HTTPError as e:
            try:
                return e.read().decode("utf-8", errors="ignore")
            except:
                return ""
        except Exception:
            return ""

    @staticmethod
    def _fix_pic(url):
        if not url:return ""
        url = url.strip()
        if url.startswith("http"):return url
        if url.startswith("//"):return "https:" + url
        return ""

    def homeContent(self, filter):
        result = {"class": self.CATEGORIES, "filters": {}, "list": []}
        resp_text = self._fetch(f"{self.HOST}/api/home")
        if not resp_text:
            return result
        try:
            js = json.loads(resp_text)
            data_arr = js.get("data", [])
            for item in data_arr:
                result["list"].append({
                    "vod_id": str(item.get("id", "")),
                    "vod_name": item.get("title", ""),
                    "vod_pic": self._fix_pic(item.get("pic", "")),
                    "vod_remarks": item.get("update", "")
                })
        except Exception:
            pass
        return result

    def homeVideoContent(self):
        result = {"list": []}
        resp_text = self._fetch(f"{self.HOST}/api/home")
        if resp_text:
            try:
                js = json.loads(resp_text)
                arr = js.get("data", [])
                for it in arr[:24]:
                    result["list"].append({
                        "vod_id": str(it.get("id")),
                        "vod_name": it.get("title", ""),
                        "vod_pic": self._fix_pic(it.get("pic", "")),
                        "vod_remarks": it.get("update", "")
                    })
            except Exception:
                pass
        return result

    def categoryContent(self, tid, pg, filter, extend):
        result = {"list": [], "page": int(pg), "pagecount":9999,"limit":30,"total":9999}
        api_url = f"{self.HOST}/api/cate?type={tid}&page={pg}"
        resp_text = self._fetch(api_url)
        if not resp_text:
            return result
        try:
            js = json.loads(resp_text)
            data_arr = js.get("data", [])
            for item in data_arr:
                result["list"].append({
                    "vod_id": str(item.get("id", "")),
                    "vod_name": item.get("title", ""),
                    "vod_pic": self._fix_pic(item.get("pic", "")),
                    "vod_remarks": item.get("update", "")
                })
        except Exception:
            pass
        return result

    def detailContent(self, ids):
        result = {"list": []}
        if not ids:return result
        vid = ids[0]
        resp_text = self._fetch(f"{self.HOST}/api/detail?id={vid}")
        if not resp_text:return result
        try:
            js = json.loads(resp_text)
            d = js.get("data", {})
            vod = {
                "vod_id": str(d.get("id")),
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
            for idx,line in enumerate(play_list):
                ep_parts = []
                for ep in line.get("list", []):
                    ep_parts.append(f"{ep.get('name','')}${ep.get('url','')}")
                if ep_parts:
                    play_from_arr.append(line.get("name",f"线路{idx+1}"))
                    play_url_arr.append("#".join(ep_parts))
            vod["vod_play_from"] = "$$$".join(play_from_arr)
            vod["vod_play_url"] = "$$$".join(play_url_arr)
            result["list"] = [vod]
        except Exception:
            pass
        return result

    def searchContent(self, key, quick):
        result = {"list": []}
        resp_text = self._fetch(f"{self.HOST}/api/search?wd={quote(key)}&page=1")
        if not resp_text:return result
        try:
            js = json.loads(resp_text)
            for item in js.get("data", []):
                result["list"].append({
                    "vod_id": str(item.get("id")),
                    "vod_name": item.get("title", ""),
                    "vod_pic": self._fix_pic(item.get("pic", "")),
                    "vod_remarks": item.get("update", "")
                })
        except Exception:
            pass
        return result

    def playerContent(self, flag, id, vipFlags):
        return {
            "parse":0,
            "playUrl":"",
            "jx":0,
            "url":id,
            "header":{"User-Agent":self.UA,"Referer":self.HOST}
        }

    def localProxy(self, param):
        return [200, "video/MP2T", {"url":"","header":"","param":"","type":"string","after":""},""]
