﻿var rule = {
    title: '可可影视[优]',
    host: 'https://www.keke8.app',
    //host: 'https://www.kkys01.com',
    // url: '/show/fyclass-----2-fypage.html',
    url: '/show/fyclass-fyfilter-fypage.html',
    filter_url: '{{fl.类型}}-{{fl.地区}}-{{fl.语言}}-{{fl.年份}}-{{fl.排序}}',
    searchUrl: '/search?k=**&page=fypage',
    searchable: 2,
    quickSearch: 0,
    filterable: 1,
    headers: {
        'User-Agent': 'MOBILE_UA',
    },
    class_parse: '#nav-swiper&&.nav-swiper-slide;a&&Text;a&&href;/(\\w+).html',
    cate_exclude: 'Netflix|今日更新|专题列表|排行榜',
    tab_exclude:'可可影视提供',
    tab_order: ['超清', '蓝光', '极速蓝光'],
    tab_remove:['4K(高峰不卡)'],
    play_parse: true,
    lazy: '',
    limit: 20,
    推荐: '.section-box:eq(2)&&.module-box-inner&&.module-item;*;*;*;*',
    double: false,
    一级: '.module-box-inner&&.module-item;.v-item-title:eq(1)&&Text;img:last-of-type&&data-original;.v-item-bottom&&span:eq(1)&&Text;a&&href',
    二级: {
        title: '.detail-pic&&img&&alt;.detail-tags&&a&&Text',
        img: '.detail-pic&&img&&data-original',
        desc: '.detail-info-row-main:eq(-2)&&Text;.detail-tags&&a&&Text;.detail-tags&&a:eq(1)&&Text;.detail-info-row-main:eq(1)&&Text;.detail-info-row-main&&Text',
        content: '.detail-desc&&Text',
        //tabs: '.source-item-label:nth-of-type(2)',
        tabs: 'body&&.source-item-label[id]',
        lists: '.episode-list:eq(#id) a',
    },
    搜索: '.search-result-list&&a;.title:eq(1)&&Text;*;.search-result-item-header&&Text;a&&href;.desc&&Text',
    // 图片替换:$js.toString(()=>{
    //     log(input);
    //    input = input.replace(rule.host,'https://vres.a357899.cn');
    // }),
    //图片替换: 'https://keke5.app=>https://vres.a357899.cn',
    预处理: $js.toString(() => {
        let html = request(rule.host);
        let scripts = pdfa(html, 'script');
        let img_script = scripts.find(it => pdfh(it, 'script&&src').includes('rdul.js'));
        if (img_script) {
            let img_url = img_script.match(/src="(.*?)"/)[1];
            //console.log(img_url);
            let img_html = request(img_url);
            let img_host = img_html.match(/'(.*?)'/)[1];
            log(img_host);
            rule.图片替换 = rule.host + '=>' + img_host;
        }
    }),
    filter: '{"1":[{"key":"类型","name":"类型","value":[{"n":"全部","v":""},{"n":"Netflix","v":"NETFLIX"},{"n":"剧情","v":"剧情"},{"n":"喜剧","v":"喜剧"},{"n":"动作","v":"动作"},{"n":"爱情","v":"爱情"},{"n":"恐怖","v":"恐怖"},{"n":"惊悚","v":"惊悚"},{"n":"犯罪","v":"犯罪"},{"n":"科幻","v":"科幻"},{"n":"悬疑","v":"悬疑"},{"n":"奇幻","v":"奇幻"},{"n":"冒险","v":"冒险"},{"n":"战争","v":"战争"},{"n":"历史","v":"历史"},{"n":"古装","v":"古装"},{"n":"家庭","v":"家庭"},{"n":"传记","v":"传记"},{"n":"武侠","v":"武侠"},{"n":"歌舞","v":"歌舞"},{"n":"短片","v":"短片"},{"n":"动画","v":"动画"},{"n":"儿童","v":"儿童"},{"n":"职场","v":"职场"}]},{"key":"地区","name":"地区","value":[{"n":"全部","v":""},{"n":"大陆","v":"中国大陆"},{"n":"香港","v":"中国香港"},{"n":"台湾","v":"中国台湾"},{"n":"美国","v":"美国"},{"n":"日本","v":"日本"},{"n":"韩国","v":"韩国"},{"n":"英国","v":"英国"},{"n":"法国","v":"法国"},{"n":"德国","v":"德国"},{"n":"印度","v":"印度"},{"n":"泰国","v":"泰国"},{"n":"丹麦","v":"丹麦"},{"n":"瑞典","v":"瑞典"},{"n":"巴西","v":"巴西"},{"n":"加拿大","v":"加拿大"},{"n":"俄罗斯","v":"俄罗斯"},{"n":"意大利","v":"意大利"},{"n":"比利时","v":"比利时"},{"n":"爱尔兰","v":"爱尔兰"},{"n":"西班牙","v":"西班牙"},{"n":"澳大利亚","v":"澳大利亚"},{"n":"其他","v":"其他"}]},{"key":"语言","name":"语言","value":[{"n":"全部","v":""},{"n":"国语","v":"国语"},{"n":"粤语","v":"粤语"},{"n":"英语","v":"英语"},{"n":"日语","v":"日语"},{"n":"韩语","v":"韩语"},{"n":"法语","v":"法语"},{"n":"其他","v":"其他"}]},{"key":"年份","name":"年份","value":[{"n":"全部","v":""},{"n":"2024","v":"2024"},{"n":"2023","v":"2023"},{"n":"2022","v":"2022"},{"n":"2021","v":"2021"},{"n":"2020","v":"2020"},{"n":"10年代","v":"2010_2019"},{"n":"00年代","v":"2000_2009"},{"n":"90年代","v":"1990_1999"},{"n":"80年代","v":"1980_1989"},{"n":"更早","v":"0_1979"}]},{"key":"排序","name":"排序","value":[{"n":"综合","v":"1"},{"n":"最新","v":"2"},{"n":"最热","v":"3"},{"n":"评分","v":"4"}]}],"2":[{"key":"类型","name":"类型","value":[{"n":"全部","v":""},{"n":"Netflix","v":"Netflix"},{"n":"剧情","v":"剧情"},{"n":"爱情","v":"爱情"},{"n":"喜剧","v":"喜剧"},{"n":"犯罪","v":"犯罪"},{"n":"悬疑","v":"悬疑"},{"n":"古装","v":"古装"},{"n":"动作","v":"动作"},{"n":"家庭","v":"家庭"},{"n":"惊悚","v":"惊悚"},{"n":"奇幻","v":"奇幻"},{"n":"美剧","v":"美剧"},{"n":"科幻","v":"科幻"},{"n":"历史","v":"历史"},{"n":"战争","v":"战争"},{"n":"韩剧","v":"韩剧"},{"n":"武侠","v":"武侠"},{"n":"言情","v":"言情"},{"n":"恐怖","v":"恐怖"},{"n":"冒险","v":"冒险"},{"n":"都市","v":"都市"},{"n":"职场","v":"职场"}]},{"key":"地区","name":"地区","value":[{"n":"地区","v":""},{"n":"大陆","v":"中国大陆"},{"n":"香港","v":"中国香港"},{"n":"韩国","v":"韩国"},{"n":"美国","v":"美国"},{"n":"日本","v":"日本"},{"n":"法国","v":"法国"},{"n":"英国","v":"英国"},{"n":"德国","v":"德国"},{"n":"台湾","v":"中国台湾"},{"n":"泰国","v":"泰国"},{"n":"印度","v":"印度"},{"n":"其他","v":"其他"}]},{"key":"语言","name":"语言","value":[{"n":"全部","v":""},{"n":"国语","v":"国语"},{"n":"粤语","v":"粤语"},{"n":"英语","v":"英语"},{"n":"日语","v":"日语"},{"n":"韩语","v":"韩语"},{"n":"法语","v":"法语"},{"n":"其他","v":"其他"}]},{"key":"年份","name":"年份","value":[{"n":"全部","v":""},{"n":"2024","v":"2024"},{"n":"2023","v":"2023"},{"n":"2022","v":"2022"},{"n":"2021","v":"2021"},{"n":"2020","v":"2020"},{"n":"10年代","v":"2010_2019"},{"n":"00年代","v":"2000_2009"},{"n":"90年代","v":"1990_1999"},{"n":"80年代","v":"1980_1989"},{"n":"更早","v":"0_1979"}]},{"key":"排序","name":"排序","value":[{"n":"综合","v":"1"},{"n":"最新","v":"2"},{"n":"最热","v":"3"},{"n":"评分","v":"4"}]}],"3":[{"key":"类型","name":"类型","value":[{"n":"全部","v":""},{"n":"Netflix","v":"Netflix"},{"n":"动态漫画","v":"动态漫画"},{"n":"剧情","v":"剧情"},{"n":"动画","v":"动画"},{"n":"喜剧","v":"喜剧"},{"n":"冒险","v":"冒险"},{"n":"动作","v":"动作"},{"n":"奇幻","v":"奇幻"},{"n":"科幻","v":"科幻"},{"n":"儿童","v":"儿童"},{"n":"搞笑","v":"搞笑"},{"n":"爱情","v":"爱情"},{"n":"家庭","v":"家庭"},{"n":"短片","v":"短片"},{"n":"热血","v":"热血"},{"n":"益智","v":"益智"},{"n":"悬疑","v":"悬疑"},{"n":"经典","v":"经典"},{"n":"校园","v":"校园"},{"n":"Anime","v":"Anime"},{"n":"运动","v":"运动"},{"n":"亲子","v":"亲子"},{"n":"青春","v":"青春"},{"n":"恋爱","v":"恋爱"},{"n":"武侠","v":"武侠"},{"n":"惊悚","v":"惊悚"}]},{"key":"地区","name":"地区","value":[{"n":"全部","v":""},{"n":"日本","v":"日本"},{"n":"大陆","v":"中国大陆"},{"n":"台湾","v":"中国台湾"},{"n":"美国","v":"美国"},{"n":"香港","v":"中国香港"},{"n":"韩国","v":"韩国"},{"n":"英国","v":"英国"},{"n":"法国","v":"法国"},{"n":"德国","v":"德国"},{"n":"印度","v":"印度"},{"n":"泰国","v":"泰国"},{"n":"丹麦","v":"丹麦"},{"n":"瑞典","v":"瑞典"},{"n":"巴西","v":"巴西"},{"n":"加拿大","v":"加拿大"},{"n":"俄罗斯","v":"俄罗斯"},{"n":"意大利","v":"意大利"},{"n":"比利时","v":"比利时"},{"n":"爱尔兰","v":"爱尔兰"},{"n":"西班牙","v":"西班牙"},{"n":"澳大利亚","v":"澳大利亚"},{"n":"其他","v":"其他"}]},{"key":"语言","name":"语言","value":[{"n":"全部","v":""},{"n":"国语","v":"国语"},{"n":"粤语","v":"粤语"},{"n":"英语","v":"英语"},{"n":"日语","v":"日语"},{"n":"韩语","v":"韩语"},{"n":"法语","v":"法语"},{"n":"其他","v":"其他"}]},{"key":"年份","name":"年份","value":[{"n":"全部","v":""},{"n":"2024","v":"2024"},{"n":"2023","v":"2023"},{"n":"2022","v":"2022"},{"n":"2021","v":"2021"},{"n":"2020","v":"2020"},{"n":"10年代","v":"2010_2019"},{"n":"00年代","v":"2000_2009"},{"n":"90年代","v":"1990_1999"},{"n":"80年代","v":"1980_1989"},{"n":"更早","v":"0_1979"}]},{"key":"排序","name":"排序","value":[{"n":"综合","v":"1"},{"n":"最新","v":"2"},{"n":"最热","v":"3"},{"n":"评分","v":"4"}]}],"4":[{"key":"类型","name":"类型","value":[{"n":"全部","v":""},{"n":"纪录","v":"纪录"},{"n":"真人秀","v":"真人秀"},{"n":"记录","v":"记录"},{"n":"脱口秀","v":"脱口秀"},{"n":"剧情","v":"剧情"},{"n":"历史","v":"历史"},{"n":"喜剧","v":"喜剧"},{"n":"传记","v":"传记"},{"n":"相声","v":"相声"},{"n":"节目","v":"节目"},{"n":"歌舞","v":"歌舞"},{"n":"冒险","v":"冒险"},{"n":"运动","v":"运动"},{"n":"Season","v":"Season"},{"n":"犯罪","v":"犯罪"},{"n":"短片","v":"短片"},{"n":"搞笑","v":"搞笑"},{"n":"晚会","v":"晚会"}]},{"key":"地区","name":"地区","value":[{"n":"全部","v":""},{"n":"大陆","v":"中国大陆"},{"n":"香港","v":"中国香港"},{"n":"台湾","v":"中国台湾"},{"n":"美国","v":"美国"},{"n":"日本","v":"日本"},{"n":"韩国","v":"韩国"},{"n":"其他","v":"其他"}]},{"key":"语言","name":"语言","value":[{"n":"全部","v":""},{"n":"国语","v":"国语"},{"n":"粤语","v":"粤语"},{"n":"英语","v":"英语"},{"n":"日语","v":"日语"},{"n":"韩语","v":"韩语"},{"n":"法语","v":"法语"},{"n":"其他","v":"其他"}]},{"key":"年份","name":"年份","value":[{"n":"全部","v":""},{"n":"2024","v":"2024"},{"n":"2023","v":"2023"},{"n":"2022","v":"2022"},{"n":"2021","v":"2021"},{"n":"2020","v":"2020"},{"n":"10年代","v":"2010_2019"},{"n":"00年代","v":"2000_2009"},{"n":"90年代","v":"1990_1999"},{"n":"80年代","v":"1980_1989"},{"n":"更早","v":"0_1979"}]},{"key":"排序","name":"排序","value":[{"n":"综合","v":"1"},{"n":"最新","v":"2"},{"n":"最热","v":"3"},{"n":"评分","v":"4"}]}],"6":[{"key":"类型","name":"类型","value":[{"n":"类型","v":""},{"n":"逆袭","v":"逆袭"},{"n":"甜宠","v":"甜宠"},{"n":"虐恋","v":"虐恋"},{"n":"穿越","v":"穿越"},{"n":"重生","v":"重生"},{"n":"剧情","v":"剧情"},{"n":"科幻","v":"科幻"},{"n":"武侠","v":"武侠"},{"n":"爱情","v":"爱情"},{"n":"动作","v":"动作"},{"n":"战争","v":"战争"},{"n":"冒险","v":"冒险"},{"n":"其它","v":"其它"}]},{"key":"排序","name":"排序","value":[{"n":"综合","v":"1"},{"n":"最新","v":"2"},{"n":"最热","v":"3"}]}]}',
    一级f: `js:
    let urls = [
    'https://keke5.app/show/1-----1-1.html',
    'https://keke5.app/show/2-----1-1.html',
    'https://keke5.app/show/3-----1-1.html',
    'https://keke5.app/show/4-----1-1.html',
    'https://keke5.app/show/6-----1-1.html',
    ];
    let filters = {};
    pdfa = jsp.pdfa;
    pdfh = jsp.pdfh;
    for(let url of urls){
    let fclass = url.match(/show\\/(\\d+)-/)[1];
    console.log(fclass);
    let html = request(url);
    let tabs = pdfa(html, '.filter-row');
    let data = [];
    for (let tab of tabs) {
        let title = pdfh(tab, 'strong&&Text').replace(':','');
        let lis = pdfa(tab, 'a');
        let _map = {key: title, name: title};
        let value = [];
        for (let li of lis) {
            let n = pdfh(li, 'a&&Text').trim();
            let v=n;
            if(/全部|地区|类型/.test(n)){
                v = '';
            }else if(/综合/.test(n)){
                v = '1';
            }else{
                v = pdfh(li,'a&&href');
                try {
                    v = v.match(/-(.*?)1-1\.html/)[1].replace(/-/g,'');
                }catch (e) {
                    v = v.match(/-(.*?)-1\.html/)[1].replace(/-/g,'');
                }
                v = decodeURIComponent(v);
            }
            value.push({
                'n': n, 'v': v
            });
        }
        _map['value'] = value;
        data.push(_map);
    }
    filters[fclass] = data;
    }
    VODS = [filters];
    console.log(gzip(JSON.stringify(filters)));
    `,
}