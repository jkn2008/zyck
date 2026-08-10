/**
 * ffys.fun 飞飞影视 drpy2脚本
 * 仅支持本地Drpy2后端服务，浏览器drpy2.min.js会跨域403
 */
const UA = "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36";
const host = "https://www.ffys.fun";

// 获取首页推荐
async function home() {
    const list = [];
    try {
        const res = await fetch(`${host}/api/home`, {
            headers: { "User-Agent": UA, "Referer": host }
        });
        const json = await res.json();
        if (json && json.data) {
            json.data.forEach((item) => {
                list.push({
                    vod_id: item.id,
                    vod_name: item.title,
                    vod_pic: item.pic,
                    vod_remarks: item.update || "",
                    vod_year: item.year || "",
                });
            });
        }
    } catch (e) {
        console.log("首页接口异常", e);
    }
    return setVod(list);
}

// 获取分类列表
async function category(tid, pg) {
    const list = [];
    try {
        const res = await fetch(`${host}/api/cate?type=${tid}&page=${pg}`, {
            headers: { "User-Agent": UA, "Referer": host }
        });
        const json = await res.json();
        if (json && json.data) {
            json.data.forEach((item) => {
                list.push({
                    vod_id: item.id,
                    vod_name: item.title,
                    vod_pic: item.pic,
                    vod_remarks: item.update || "",
                });
            });
        }
    } catch (e) {
        console.log("分类接口异常", e);
    }
    return setVod(list);
}

// 搜索
async function search(wd, pg) {
    const list = [];
    try {
        const res = await fetch(`${host}/api/search?wd=${encodeURIComponent(wd)}&page=${pg}`, {
            headers: { "User-Agent": UA, "Referer": host }
        });
        const json = await res.json();
        if (json && json.data) {
            json.data.forEach((item) => {
                list.push({
                    vod_id: item.id,
                    vod_name: item.title,
                    vod_pic: item.pic,
                    vod_remarks: item.update || "",
                });
            });
        }
    } catch (e) {
        console.log("搜索接口异常", e);
    }
    return setVod(list);
}

// 详情 + 播放集数
async function detail(id) {
    let vodInfo = {};
    let playList = [];
    try {
        const res = await fetch(`${host}/api/detail?id=${id}`, {
            headers: { "User-Agent": UA, "Referer": host }
        });
        const json = await res.json();
        if (json && json.data) {
            const d = json.data;
            vodInfo = {
                vod_id: d.id,
                vod_name: d.title,
                vod_pic: d.pic,
                vod_actor: d.actor || "",
                vod_director: d.director || "",
                vod_year: d.year || "",
                vod_area: d.area || "",
                vod_class: d.type || "",
                vod_remarks: d.update || "",
                vod_content: d.desc || "",
            };
            // 组装播放线路
            if (d.playList && Array.isArray(d.playList)) {
                d.playList.forEach((line, idx) => {
                    let episodes = [];
                    if(line.list){
                        line.list.forEach(ep=>{
                            episodes.push(`${ep.name}$${ep.url}`);
                        })
                    }
                    playList.push({
                        name: line.name || `线路${idx+1}`,
                        list: episodes.join("#")
                    })
                })
            }
            vodInfo.vod_play_from = playList.map(i=>i.name).join("$$$");
            vodInfo.vod_play_url = playList.map(i=>i.list).join("$$$");
        }
    } catch (e) {
        console.log("详情接口异常", e);
    }
    return setDetail(vodInfo);
}

// 固定格式导出
export default {
    home,
    category,
    search,
    detail
};
