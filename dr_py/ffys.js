/**
 * @title 飞飞影视
 * @type 0
 * @api https://www.ffys.fun
 */

const UA = "Mozilla/5.0 (Android TV) AppleWebKit/537.36 Chrome/126.0.0.0 Safari/537.36";
const siteUrl = "https://www.ffys.fun";

const cateMap = [
    { typeId: 1, typeName: "电影" },
    { typeId: 2, typeName: "剧集" },
    { typeId: 3, typeName: "动漫" },
    { typeId: 4, typeName: "综艺" },
    { typeId: 6, typeName: "爽剧" }
];

async function home() {
    let list = [];
    let res = await fetch(`${siteUrl}/api/home/recommend`, {
        headers: { "User-Agent": UA, "Referer": siteUrl }
    });
    let json = await res.json();
    if (json?.data) {
        list.push({
            title: "🔥首页推荐",
            data: json.data.map(item => formatVod(item))
        });
    }
    for (let c of cateMap) {
        let r = await fetch(`${siteUrl}/api/video/list?type=${c.typeId}&page=1&limit=12`, {
            headers: { "User-Agent": UA, "Referer": siteUrl }
        });
        let j = await r.json();
        if (j?.data?.list) {
            list.push({
                title: c.typeName,
                data: j.data.list.map(item => formatVod(item))
            });
        }
    }
    return setHome(list);
}

async function category(tid, pg) {
    let cid = Number(tid);
    let limit = 20;
    let res = await fetch(`${siteUrl}/api/video/list?type=${cid}&page=${pg}&limit=${limit}`, {
        headers: {
            "User-Agent": UA,
            "Referer": siteUrl
        }
    });
    let json = await res.json();
    let arr = [];
    if (json?.data?.list) {
        arr = json.data.list.map(item => formatVod(item));
    }
    return setVod(arr, pg < json?.data?.totalPage);
}

async function search(wd, pg) {
    let res = await fetch(`${siteUrl}/api/video/search?keyword=${encodeURIComponent(wd)}&page=${pg}&limit=20`, {
        headers: {
            "User-Agent": UA,
            "Referer": siteUrl
        }
    });
    let json = await res.json();
    let arr = [];
    if (json?.data?.list) {
        arr = json.data.list.map(item => formatVod(item));
    }
    return setVod(arr, pg < json?.data?.totalPage);
}

async function detail(id) {
    let res = await fetch(`${siteUrl}/api/video/detail?id=${id}`, {
        headers: {
            "User-Agent": UA,
            "Referer": siteUrl
        }
    });
    let json = await res.json();
    if (!json?.data) return setDetail({});
    let info = json.data;
    let vod = formatVod(info);

    let playList = [];
    if (info?.playList && Array.isArray(info.playList)) {
        for (let pl of info.playList) {
            let ep = [];
            for (let p of pl.playUrls) {
                ep.push(`${p.name}$${p.url}`);
            }
            playList.push(ep.join("#"));
        }
    }
    vod.vod_play_from = playList.map((_, i) => `线路${i + 1}`).join("$$$");
    vod.vod_play_url = playList.join("$$$");
    return setDetail(vod);
}

function formatVod(item) {
    return {
        vod_id: item.id,
        vod_name: item.title,
        vod_pic: item.image,
        vod_remarks: item.updateInfo || "",
        vod_year: item.year || "",
        vod_area: item.area || "",
        vod_class: item.typeName || "",
        vod_actor: item.actor || "",
        vod_director: item.director || "",
        vod_content: item.desc || ""
    };
}

async function getCategory() {
    return cateMap.map(x => {
        return {
            type_id: x.typeId,
            type_name: x.typeName
        };
    });
}
