# -*- coding: utf-8 -*-
"""
TP‑3 Spider脚本，type=3，TP3引擎专用
站点：ffys.fun
现象：分类正常展示，列表无数据
TP3禁止使用urllib，全部使用引擎内置http()
分类ID：20电影,21剧集,22动漫,23综艺
"""
class Spider:
    HOST = "https://www.ffys.fun"
    UA = "Mozilla/5.0 (Android; Mobile) Chrome/130.0.0.0 Safari/537.36"

    def getName(self):
        return "飞飞影视"

    def init(self, extend=""):
        self.header = {
            "User‑Agent": self.UA,
            "Referer": self.HOST + "/",
            "Accept": "application/json;charset=utf‑8"
        }

    def homeContent(self, filter):
        result = {
            "class": [
                {"type_name": "电影", "type_id": "20"},
                {"type_name": "剧集", "type_id": "21"},
                {"type_name": "动漫", "type_id": "22"},
                {"type_name": "综艺", "type_id": "23"},
            ],
            "filters": {},
            "list": []
        }
        # TP3内置http请求函数
        resp = self.http(f"{self.HOST}/api/home", self.header)
        if resp["code"] != 200:
            return result
        try:
            js = self.jsonLoads(resp["content"])
            data_list = js.get("data", [])
            for item in data_list:
                result["list"].append({
                    "vod_id": str(item.get("id")),
                    "vod_name": item.get("title", ""),
                    "vod_pic": self.fixImg(item.get("pic", "")),
                    "vod_remarks": item.get("update", "")
                })
        except Exception:
            pass
        return result

    def homeVideoContent(self):
        result = {"list": []}
        resp = self.http(f"{self.HOST}/api/home", self.header)
        if resp["code"] != 200:
            return result
        try:
            js = self.jsonLoads(resp["content"])
            arr = js.get("data", [])
            for item in arr[:24]:
                result["list"].append({
                    "vod_id": str(item.get("id")),
                    "vod_name": item.get("title", ""),
                    "vod_pic": self.fixImg(item.get("pic", "")),
                    "vod_remarks": item.get("update", "")
                })
        except Exception:
            pass
        return result

    def categoryContent(self, tid, pg, filter, extend):
        result = {
            "list": [],
            "page": int(pg),
            "pagecount": 9999,
            "limit": 30,
            "total": 9999
        }
        api_url = f"{self.HOST}/api/cate?type={tid}&page={pg}"
        resp = self.http(api_url, self.header)
        if resp["code"] != 200:
            return result
        try:
            js = self.jsonLoads(resp["content"])
            data_list = js.get("data", [])
            for item in data_list:
                result["list"].append({
                    "vod_id": str(item.get("id")),
                    "vod_name": item.get("title", ""),
                    "vod_pic": self.fixImg(item.get("pic", "")),
                    "vod_remarks": item.get("update", "")
                })
        except Exception:
            pass
        return result

    def detailContent(self, ids):
        result = {"list": []}
        vid = ids[0]
        resp = self.http(f"{self.HOST}/api/detail?id={vid}", self.header)
        if resp["code"] != 200:
            return result
        try:
            js = self.jsonLoads(resp["content"])
            d = js["data"]
            vod = {
                "vod_id": str(d["id"]),
                "vod_name": d.get("title", ""),
                "vod_pic": self.fixImg(d.get("pic", "")),
                "vod_year": d.get("year", ""),
                "vod_area": d.get("area", ""),
                "vod_actor": d.get("actor", ""),
                "vod_director": d.get("director", ""),
                "vod_content": d.get("desc", ""),
                "vod_remarks": d.get("update", ""),
                "vod_play_from": "",
                "vod_play_url": ""
            }
            froms = []
            urls = []
            playList = d.get("playList", [])
            for idx, pl in enumerate(playList):
                ep_array = []
                for ep in pl.get("list", []):
                    ep_array.append(f"{ep['name']}${ep['url']}")
                froms.append(pl.get("name", f"线路{idx+1}"))
                urls.append("#".join(ep_array))
            vod["vod_play_from"] = "$$$".join(froms)
            vod["vod_play_url"] = "$$$".join(urls)
            result["list"].append(vod)
        except Exception:
            pass
        return result

    def searchContent(self, key, quick):
        result = {"list": []}
        from urllib.parse import quote
        url = f'{self.HOST}/api/search?wd={quote(key)}&page=1'
        resp = self.http(url, self.header)
        if resp["code"] != 200:
            return result
        try:
            js = self.jsonLoads(resp["content"])
            arr = js.get("data", [])
            for item in arr:
                result["list"].append({
                    "vod_id": str(item.get("id")),
                    "vod_name": item.get("title", ""),
                    "vod_pic": self.fixImg(item.get("pic", "")),
                    "vod_remarks": item.get("update", "")
                })
        except Exception:
            pass
        return result

    def playerContent(self, flag, id, vipFlags):
        return {
            "parse": 0,
            "jx": 0,
            "url": id,
            "header": self.header
        }

    def fixImg(self, url):
        if not url:
            return ""
        url = url.strip()
        if url.startswith("http"):
            return url
        if url.startswith("//"):
            return "https:" + url
        return self.HOST + url
