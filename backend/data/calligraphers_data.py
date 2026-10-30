# -*- coding: utf-8 -*-
"""历代著名书法家及作品数据

按朝代时间排序，包含书法家基本信息与代表作品。
"""

# 朝代列表（按时间排序）
DYNASTIES = [
    {"name": "秦", "sort_order": 1, "start_year": -221, "end_year": -206},
    {"name": "东汉", "sort_order": 2, "start_year": 25, "end_year": 220},
    {"name": "三国魏", "sort_order": 3, "start_year": 220, "end_year": 265},
    {"name": "东晋", "sort_order": 4, "start_year": 317, "end_year": 420},
    {"name": "唐", "sort_order": 5, "start_year": 618, "end_year": 907},
    {"name": "北宋", "sort_order": 6, "start_year": 960, "end_year": 1127},
    {"name": "南宋", "sort_order": 7, "start_year": 1127, "end_year": 1279},
    {"name": "元", "sort_order": 8, "start_year": 1271, "end_year": 1368},
    {"name": "明", "sort_order": 9, "start_year": 1368, "end_year": 1644},
    {"name": "清", "sort_order": 10, "start_year": 1644, "end_year": 1912},
    {"name": "近现代", "sort_order": 11, "start_year": 1912, "end_year": 2026},
]

# 书法家数据：dynasty 对应 DYNASTIES 中的 name
CALLIGRAPHERS = [
    # ===== 秦 =====
    {
        "name": "李斯",
        "dynasty": "秦",
        "birth_year": -280,
        "death_year": -208,
        "style": "小篆",
        "introduction": "秦代政治家、书法家。统一六国文字，创立小篆，被誉为「篆书之祖」。其书法结构匀称、笔法圆润，对后世书法发展影响深远。",
        "works": [
            {"name": "峄山刻石", "style": "小篆", "creation_year": -223, "description": "秦始皇东巡时所立，李斯书。笔法圆润挺拔，结构对称严谨，为小篆典范。"},
            {"name": "泰山刻石", "style": "小篆", "creation_year": -219, "description": "秦始皇登泰山封禅所立，李斯撰并书。字形端整，气魄宏大。"},
        ],
    },
    # ===== 东汉 =====
    {
        "name": "蔡邕",
        "dynasty": "东汉",
        "birth_year": 133,
        "death_year": 192,
        "style": "隶书",
        "introduction": "东汉文学家、书法家。通经史、善辞赋，工篆隶。创「飞白书」技法，隶书方正典雅。",
        "works": [
            {"name": "熹平石经", "style": "隶书", "creation_year": 175, "description": "蔡邕等奏请正定六经文字，刻石立于太学，为中国最早的官定儒家经本。隶书工整端庄。"},
        ],
    },
    # ===== 三国魏 =====
    {
        "name": "钟繇",
        "dynasty": "三国魏",
        "birth_year": 151,
        "death_year": 230,
        "style": "楷书",
        "introduction": "三国魏大臣、书法家。被后世尊为「楷书之祖」，与王羲之并称「钟王」。其楷书古朴自然，由隶入楷，开一代新风。",
        "works": [
            {"name": "宣示表", "style": "楷书", "creation_year": 220, "description": "钟繇代表作，楷书初创之作。用笔沉稳，结体扁方，犹存隶意，为楷书开山之作。"},
            {"name": "荐季直表", "style": "楷书", "creation_year": 221, "description": "钟繇上表荐举季直之作。笔画古拙，天真烂漫，被誉为「正书之祖」。"},
        ],
    },
    # ===== 东晋 =====
    {
        "name": "王羲之",
        "dynasty": "东晋",
        "birth_year": 303,
        "death_year": 361,
        "style": "行书",
        "introduction": "东晋书法家，被尊为「书圣」。其书法兼善隶、草、楷、行各体，自成一家，影响中国书法一千余年。代表作《兰亭序》被誉为「天下第一行书」。",
        "works": [
            {"name": "兰亭序", "style": "行书", "creation_year": 353, "description": "永和九年王羲之与友人会于会稽山阴兰亭，乘兴所作。被誉为「天下第一行书」，笔势飘逸，变化无穷。"},
            {"name": "快雪时晴帖", "style": "行书", "creation_year": 350, "description": "王羲之书札，内容为大雪初晴后的问候。笔画圆润流畅，乾隆誉为「三希」之首。"},
            {"name": "十七帖", "style": "草书", "creation_year": 345, "description": "王羲之草书代表作，为一组信札。草法严谨，气息平和，为今草典范。"},
        ],
    },
    {
        "name": "王献之",
        "dynasty": "东晋",
        "birth_year": 344,
        "death_year": 386,
        "style": "行草",
        "introduction": "东晋书法家，王羲之第七子。与父并称「二王」。其行草笔势飞动，气势豪迈，在乃父基础上更趋俊逸。",
        "works": [
            {"name": "中秋帖", "style": "行草", "creation_year": 370, "description": "王献之代表作，被乾隆列为「三希」之一。笔画连绵不断，气势纵横，为行草珍品。"},
            {"name": "鸭头丸帖", "style": "行草", "creation_year": 375, "description": "王献之行草书札，仅二行十五字。笔致洒脱，韵味悠长。"},
            {"name": "洛神赋十三行", "style": "楷书", "creation_year": 368, "description": "王献之小楷书曹植《洛神赋》，仅存十三行。字形秀逸，笔法精妙，为小楷神品。"},
        ],
    },
    # ===== 唐 =====
    {
        "name": "欧阳询",
        "dynasty": "唐",
        "birth_year": 557,
        "death_year": 641,
        "style": "楷书",
        "introduction": "唐代书法家，「初唐四大家」之首。楷书法度严谨，笔力险峻，世称「欧体」。与颜真卿、柳公权、赵孟頫并称「楷书四大家」。",
        "works": [
            {"name": "九成宫醴泉铭", "style": "楷书", "creation_year": 632, "description": "欧阳询晚年代表作，魏征撰文。结体险峻严谨，笔法刚劲，为欧体楷书巅峰之作。"},
            {"name": "化度寺碑", "style": "楷书", "creation_year": 631, "description": "欧阳询楷书，结字谨严，用笔沉厚，被誉为「楷书极则」。"},
        ],
    },
    {
        "name": "虞世南",
        "dynasty": "唐",
        "birth_year": 558,
        "death_year": 638,
        "style": "楷书",
        "introduction": "唐代书法家、政治家，「初唐四大家」之一。师承智永，楷书外柔内刚，含蓄蕴藉，深得二王神韵。",
        "works": [
            {"name": "孔子庙堂碑", "style": "楷书", "creation_year": 633, "description": "虞世南楷书代表作。笔画舒展，结体宽绰，气息温雅，为初唐楷书杰作。"},
        ],
    },
    {
        "name": "褚遂良",
        "dynasty": "唐",
        "birth_year": 596,
        "death_year": 658,
        "style": "楷书",
        "introduction": "唐代书法家，「初唐四大家」之一。楷书疏瘦劲健，变化丰富，融合隶意，自成「褚体」。对后世楷书发展影响极大。",
        "works": [
            {"name": "雁塔圣教序", "style": "楷书", "creation_year": 653, "description": "褚遂良晚年代表作，立于大雁塔下。笔画瘦劲，结体疏朗，灵动飘逸，为褚体巅峰。"},
            {"name": "倪宽赞", "style": "楷书", "creation_year": 650, "description": "褚遂良楷书墨迹，笔法精到，温润秀雅。"},
        ],
    },
    {
        "name": "颜真卿",
        "dynasty": "唐",
        "birth_year": 709,
        "death_year": 785,
        "style": "楷书",
        "introduction": "唐代杰出书法家。楷书雄强浑厚，气势磅礴，世称「颜体」。与柳公权并称「颜筋柳骨」。其行书《祭侄文稿》被誉为「天下第二行书」。",
        "works": [
            {"name": "多宝塔碑", "style": "楷书", "creation_year": 752, "description": "颜真卿早期楷书代表作。结体严密，用笔劲健，为学习颜体楷书的入门范本。"},
            {"name": "祭侄文稿", "style": "行书", "creation_year": 758, "description": "颜真卿悼念在安史之乱中殉国的侄子所作。情真意切，笔势激越，被誉为「天下第二行书」。"},
            {"name": "颜勤礼碑", "style": "楷书", "creation_year": 779, "description": "颜真卿晚年为其曾祖父所立神道碑。楷书浑厚大气，为颜体成熟期代表作。"},
        ],
    },
    {
        "name": "柳公权",
        "dynasty": "唐",
        "birth_year": 778,
        "death_year": 865,
        "style": "楷书",
        "introduction": "唐代书法家。楷书骨力道健，结构严紧，世称「柳体」。与颜真卿并称「颜筋柳骨」，同为「楷书四大家」之一。",
        "works": [
            {"name": "玄秘塔碑", "style": "楷书", "creation_year": 841, "description": "柳公权代表作。笔画挺拔，骨力遒劲，结构中宫收紧，为柳体楷书典范。"},
            {"name": "神策军碑", "style": "楷书", "creation_year": 843, "description": "柳公权晚年楷书，笔法更加精熟，骨力内含，为柳体精品。"},
        ],
    },
    {
        "name": "张旭",
        "dynasty": "唐",
        "birth_year": 675,
        "death_year": 750,
        "style": "狂草",
        "introduction": "唐代书法家，「草圣」。狂草纵横奔放，气势磅礴，与怀素并称「颠张醉素」。常于醉后挥毫，一气呵成。",
        "works": [
            {"name": "古诗四帖", "style": "狂草", "creation_year": 740, "description": "张旭狂草代表作，书古诗四首。笔势连绵，狂放不羁，为狂草巅峰之作。"},
            {"name": "肚痛帖", "style": "狂草", "creation_year": 738, "description": "张旭草书，仅六行三十字。由稳到狂，变化剧烈，尽显颠张之态。"},
        ],
    },
    {
        "name": "怀素",
        "dynasty": "唐",
        "birth_year": 737,
        "death_year": 799,
        "style": "狂草",
        "introduction": "唐代僧人书法家。狂草继承张旭又有发展，以「狂」继「颠」，笔法飞动，气势奔放。与张旭并称「颠张醉素」。",
        "works": [
            {"name": "自叙帖", "style": "狂草", "creation_year": 777, "description": "怀素自述学书经历之作。通篇狂草，连绵不绝，如骤雨旋风，为怀素代表作。"},
            {"name": "苦笋帖", "style": "草书", "creation_year": 785, "description": "怀素草书短札，笔势肥瘦相间，韵味清雅。"},
        ],
    },
    # ===== 北宋 =====
    {
        "name": "苏轼",
        "dynasty": "北宋",
        "birth_year": 1037,
        "death_year": 1101,
        "style": "行书",
        "introduction": "北宋文学家、书画家，「宋四家」之首。行书丰腴跌宕，天真烂漫，自言「我书意造本无法」。代表作《寒食帖》被誉为「天下第三行书」。",
        "works": [
            {"name": "寒食帖", "style": "行书", "creation_year": 1082, "description": "苏轼贬黄州时作，书寒食诗二首。情感起伏跌宕，笔法随情绪变化，被誉为「天下第三行书」。"},
            {"name": "赤壁赋", "style": "行楷", "creation_year": 1082, "description": "苏轼书《前赤壁赋》。行楷温润秀逸，字字如珠，为其书法精品。"},
        ],
    },
    {
        "name": "黄庭坚",
        "dynasty": "北宋",
        "birth_year": 1045,
        "death_year": 1105,
        "style": "行书",
        "introduction": "北宋诗人、书法家，「宋四家」之一。行书长枪大戟，气势雄健，自成一家。与苏轼并称「苏黄」。",
        "works": [
            {"name": "松风阁诗帖", "style": "行书", "creation_year": 1100, "description": "黄庭坚晚年行书代表作。笔画如长枪大戟，气势开阔，为黄体行书巅峰。"},
            {"name": "寒山子庞居士诗", "style": "行书", "creation_year": 1095, "description": "黄庭坚行书，笔法奇崛，结体纵横，尽显其书法个性。"},
        ],
    },
    {
        "name": "米芾",
        "dynasty": "北宋",
        "birth_year": 1051,
        "death_year": 1107,
        "style": "行书",
        "introduction": "北宋书画家，「宋四家」之一。行书骏快飞扬，沉著痛快，自谓「刷字」。性格狂放，人称「米颠」。",
        "works": [
            {"name": "蜀素帖", "style": "行书", "creation_year": 1088, "description": "米芾行书代表作，书于蜀素之上。笔法俊迈，风骨挺拔，被誉为「中华第一美帖」。"},
            {"name": "苕溪诗帖", "style": "行书", "creation_year": 1088, "description": "米芾自作诗，行书酣畅淋漓，跌宕多姿。"},
        ],
    },
    {
        "name": "蔡襄",
        "dynasty": "北宋",
        "birth_year": 1012,
        "death_year": 1067,
        "style": "楷书",
        "introduction": "北宋书法家，「宋四家」之一。书法浑厚端庄，传承晋唐法度。以楷书、行书著称，风格温润秀劲。",
        "works": [
            {"name": "澄心堂纸帖", "style": "行楷", "creation_year": 1063, "description": "蔡襄行楷代表作。笔画温润，结体端庄，尽显其浑厚典雅之风。"},
            {"name": "扈从帖", "style": "行书", "creation_year": 1060, "description": "蔡襄行书，笔法精到，气韵清雅。"},
        ],
    },
    # ===== 南宋 =====
    {
        "name": "陆游",
        "dynasty": "南宋",
        "birth_year": 1125,
        "death_year": 1210,
        "style": "行书",
        "introduction": "南宋诗人、书法家。诗名盖世，书法亦精。行草笔势奔放，气象开阔，有诗人之气。",
        "works": [
            {"name": "自书诗卷", "style": "行草", "creation_year": 1204, "description": "陆游晚年自书诗作。笔法老健，气势苍劲，为南宋书法珍品。"},
        ],
    },
    # ===== 元 =====
    {
        "name": "赵孟頫",
        "dynasty": "元",
        "birth_year": 1254,
        "death_year": 1322,
        "style": "楷书",
        "introduction": "元代书画家。楷书圆润遒美，世称「赵体」，与欧阳询、颜真卿、柳公权并称「楷书四大家」。倡导复古，回归晋唐，影响深远。",
        "works": [
            {"name": "洛神赋", "style": "行楷", "creation_year": 1300, "description": "赵孟頫书曹植《洛神赋》。行楷飘逸秀丽，笔法精绝，为赵体代表作。"},
            {"name": "胆巴碑", "style": "楷书", "creation_year": 1316, "description": "赵孟頫晚年楷书。笔画沉着稳健，结体端庄，为赵体楷书成熟之作。"},
            {"name": "妙严寺记", "style": "楷书", "creation_year": 1302, "description": "赵孟頫楷书碑记，笔法精到，温润秀美。"},
        ],
    },
    {
        "name": "鲜于枢",
        "dynasty": "元",
        "birth_year": 1246,
        "death_year": 1302,
        "style": "行草",
        "introduction": "元代书法家。与赵孟頫齐名，并称「南赵北鲜」。行草笔力遒健，气势雄放，得晋唐神韵。",
        "works": [
            {"name": "苏轼海棠诗", "style": "行书", "creation_year": 1295, "description": "鲜于枢行书苏轼诗。笔势跌宕，骨力遒劲，尽显北鲜之雄。"},
        ],
    },
    # ===== 明 =====
    {
        "name": "董其昌",
        "dynasty": "明",
        "birth_year": 1555,
        "death_year": 1636,
        "style": "行书",
        "introduction": "明代书画家。书法秀润虚灵，空灵淡雅，提倡「淡」的审美境界。对明末清初书法影响极大。",
        "works": [
            {"name": "岳阳楼记", "style": "行书", "creation_year": 1620, "description": "董其昌行书代表作。笔致空灵，墨色清润，尽显其淡雅书风。"},
            {"name": "蜀道难", "style": "行书", "creation_year": 1625, "description": "董其昌书李白诗，行书飘逸，气韵清雅。"},
        ],
    },
    {
        "name": "文徵明",
        "dynasty": "明",
        "birth_year": 1470,
        "death_year": 1559,
        "style": "行书",
        "introduction": "明代书画家，「吴门四家」之一。诗文书画皆精，行书、小楷尤为世重。书法温润秀雅，法度严谨。",
        "works": [
            {"name": "滕王阁序", "style": "行书", "creation_year": 1540, "description": "文徵明行书王勃名篇。笔法精到，气韵温润，为文氏行书精品。"},
            {"name": "归去来辞", "style": "小楷", "creation_year": 1535, "description": "文徵明小楷书陶渊明文。字字精工，法度森严，为明代小楷典范。"},
        ],
    },
    {
        "name": "祝允明",
        "dynasty": "明",
        "birth_year": 1461,
        "death_year": 1527,
        "style": "草书",
        "introduction": "明代书法家，「吴门四家」之一。狂草纵横捭阖，气势磅礴，与文徵明齐名。人称「祝京兆」。",
        "works": [
            {"name": "赤壁赋", "style": "草书", "creation_year": 1515, "description": "祝允明草书苏轼《赤壁赋》。狂草纵横，气势奔放，为明代草书杰作。"},
        ],
    },
    # ===== 清 =====
    {
        "name": "郑板桥",
        "dynasty": "清",
        "birth_year": 1693,
        "death_year": 1765,
        "style": "六分半书",
        "introduction": "清代书画家，「扬州八怪」之一。创「六分半书」，融合隶、楷、行、草于一体，参以画法，纵横错落，自成一格。",
        "works": [
            {"name": "难得糊涂", "style": "六分半书", "creation_year": 1755, "description": "郑板桥名言书法。融合诸体，朴拙奇崛，尽显其「难得糊涂」之人生哲学。"},
            {"name": "竹石图题跋", "style": "行书", "creation_year": 1760, "description": "郑板桥题画书法，以画法入书，错落有致。"},
        ],
    },
    {
        "name": "何绍基",
        "dynasty": "清",
        "birth_year": 1799,
        "death_year": 1873,
        "style": "行书",
        "introduction": "清代书法家。融碑帖于一炉，行书回腕执笔，笔势奇崛，气势雄浑，为晚清碑学代表。",
        "works": [
            {"name": "行书四条屏", "style": "行书", "creation_year": 1865, "description": "何绍基晚年行书。碑帖交融，笔力雄浑，为晚清行书巨制。"},
        ],
    },
    {
        "name": "吴昌硕",
        "dynasty": "清",
        "birth_year": 1844,
        "death_year": 1927,
        "style": "篆书",
        "introduction": "晚清民国书画家、篆刻家。篆书宗石鼓文，笔力浑厚苍劲，融金石气于书法，开海派画风之先。",
        "works": [
            {"name": "临石鼓文", "style": "篆书", "creation_year": 1915, "description": "吴昌硕临写石鼓文。笔力苍劲，气魄雄浑，为晚清篆书巅峰。"},
            {"name": "篆书对联", "style": "篆书", "creation_year": 1920, "description": "吴昌硕篆书联。浑厚朴拙，金石气十足。"},
        ],
    },
    # ===== 近现代 =====
    {
        "name": "于右任",
        "dynasty": "近现代",
        "birth_year": 1879,
        "death_year": 1964,
        "style": "标准草书",
        "introduction": "近现代书法家、政治家。创「标准草书」，以「易识、易写、准确、美丽」为原则，整理历代草书，影响深远。",
        "works": [
            {"name": "标准草书千字文", "style": "草书", "creation_year": 1936, "description": "于右任整理历代草书而成。规范草法，便于普及，为现代草书集大成之作。"},
            {"name": "草书对联", "style": "草书", "creation_year": 1950, "description": "于右任草书联。笔势奔放，气度恢宏。"},
        ],
    },
    {
        "name": "林散之",
        "dynasty": "近现代",
        "birth_year": 1898,
        "death_year": 1989,
        "style": "草书",
        "introduction": "现代书法家、诗人。草书以「瘦劲」著称，笔法多变，墨色丰富，被誉为「草圣」。",
        "works": [
            {"name": "草书论书诗", "style": "草书", "creation_year": 1980, "description": "林散之晚年草书。瘦劲飘逸，墨色枯润相间，为现代草书极品。"},
        ],
    },
    {
        "name": "启功",
        "dynasty": "近现代",
        "birth_year": 1912,
        "death_year": 2005,
        "style": "楷书",
        "introduction": "现代学者、书法家。楷书清秀劲挺，自成「启体」。以学者之书著称，结体精严，韵味清雅。",
        "works": [
            {"name": "论书绝句", "style": "行楷", "creation_year": 1985, "description": "启功自作论书绝句。行楷清秀挺拔，字字精到，为启体代表作。"},
            {"name": "楷书字帖", "style": "楷书", "creation_year": 1990, "description": "启功楷书范本。结体严谨，笔画清劲，广为流传。"},
        ],
    },
]
