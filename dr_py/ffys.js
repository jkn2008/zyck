/**
ffys.fun 飞飞影视 dr‑py脚本
分类ID：20电影，21剧集，22动漫，23综艺
*/
const HOST = "https://www.ffys.fun";
const UA = "Mozilla/5.0 (Android) AppleWebKit/537.36 Chrome/128.0 Mobile Safari/537.36";

class Spider {
    getName() {
        return "飞飞影视";
    }

    init(extend) {
        this.headers = {
            "User‑Agent": UA,
            "Referer": HOST + "/",
            "Accept": "application/json"
        }
    }

    homeContent(filter) {
        let classes = [
            {"type_name":"电影","type_id":"20"},
            {"type_name":"剧集","type_id":"21"},
            {"type_name":"动漫","type_id":"22"},
            {"type_name":"综艺","type_id":"23"}
        ];
        let res = req(HOST + "/api/home", this.headers);
        let list = [];
        if(res.code ===200){
            let json = JSON.parse(res.content);
            let arr = json.data || [];
            for(let item of arr){
                list.push({
                    vod_id: item.id + "",
                    vod_name: item.title,
                    vod_pic: this.fixPic(item.pic),
                    vod_remarks: item.update || ""
                })
            }
        }
        return {
            class: classes,
            filters: {},
            list: list
        }
    }

    homeVideoContent() {
        let res = req(HOST + "/api/home", this.headers);
        let list = [];
        if(res.code ===200){
            let json = JSON.parse(res.content);
            let arr = json.data || [];
            for(let item of arr.slice(0,24)){
                list.push({
                    vod_id: item.id + "",
                    vod_name: item.title,
                    vod_pic: this.fixPic(item.pic),
                    vod_remarks: item.update || ""
                })
            }
        }
        return {list:list}
    }

    categoryContent(tid, pg, filter, extend) {
        let url = `${HOST}/api/cate?type=${tid}&page=${pg}`;
        let res = req(url, this.headers);
        let list = [];
        if(res.code ===200){
            let json = JSON.parse(res.content);
            let arr = json.data || [];
            for(let item of arr){
                list.push({
                    vod_id: item.id + "",
                    vod_name: item.title,
                    vod_pic: this.fixPic(item.pic),
                    vod_remarks: item.update || ""
                })
            }
        }
        return {
            list: list,
            page: parseInt(pg),
            pagecount:9999,
            limit:30,
            total:9999
        }
    }

    detailContent(ids) {
        let vid = ids[0];
        let res = req(`${HOST}/api/detail?id=${vid}`, this.headers);
        let list = [];
        if(res.code === 200){
            let json = JSON.parse(res.content);
            let d = json.data;
            let vod = {
                vod_id: d.id + "",
                vod_name: d.title,
                vod_pic: this.fixPic(d.pic),
                vod_year: d.year||"",
                vod_area: d.area||"",
                vod_actor: d.actor||"",
                vod_director: d.director||"",
                vod_content: d.desc||"",
                vod_remarks: d.update||""
            }
            let fromArr = [];
            let urlArr = [];
            let playList = d.playList || [];
            for(let idx=0; idx<playList.length; idx++){
                let line = playList[idx];
                let eps = [];
                for(let ep of line.list){
                    eps.push(`${ep.name}$${ep.url}`);
                }
                fromArr.push(line.name || `线路${idx+1}`);
                urlArr.push(eps.join("#"));
            }
            vod.vod_play_from = fromArr.join("$$$");
            vod.vod_play_url = urlArr.join("$$$");
            list.push(vod);
        }
        return {list:list}
    }

    searchContent(key, quick) {
        let url = `${HOST}/api/search?wd=${encodeURIComponent(key)}&page=1`;
        let res = req(url, this.headers);
        let list = [];
        if(res.code ===200){
            let json = JSON.parse(res.content);
            let arr = json.data || [];
            for(let item of arr){
                list.push({
                    vod_id: item.id + "",
                    vod_name: item.title,
                    vod_pic: this.fixPic(item.pic),
                    vod_remarks: item.update||""
                })
            }
        }
        return {list:list}
    }

    playerContent(flag, id, vipFlags) {
        return {
            parse:0,
            jx:0,
            url:id,
            header:{
                "User‑Agent":UA,
                "Referer":HOST
            }
        }
    }

    fixPic(u){
        if(!u) return "";
        u = u.trim();
        if(u.startsWith("http")) return u;
        if(u.startsWith("//")) return "https:" + u;
        return HOST + u;
    }
}
