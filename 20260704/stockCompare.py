import sys
import time
import yfinance as yf
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton, QGroupBox, QFormLayout,
    QStatusBar, QGridLayout, QFrame, QSizePolicy, QLineEdit,
    QCompleter, QTabWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QSplitter,
)
from PySide6.QtCore import Qt, Slot, QStringListModel, QSize, QThread, Signal
from PySide6.QtGui import QFont, QColor, QPalette, QIcon

plt = __import__("matplotlib.pyplot", fromlist=["rcParams"])
plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei", "Arial Unicode MS", "Heiti TC"]
plt.rcParams["axes.unicode_minus"] = False

# ── 台灣上市櫃股票清單（含代號與中文名稱） ──
STOCK_POOL = {
    # 半導體
    "2330.TW": "台積電", "2303.TW": "聯電", "2454.TW": "聯發科", "3711.TW": "日月光投控",
    "3034.TW": "聯詠", "2401.TW": "凌陽", "3443.TW": "創意", "3661.TW": "世芯-KY",
    "6531.TW": "愛普", "8016.TW": "矽創", "6239.TW": "力成", "6147.TW": "頎邦",
    "5347.TW": "世界", "6488.TW": "環球晶", "3532.TW": "台勝科", "6271.TW": "同欣電",
    "6770.TW": "力積電", "3189.TW": "景碩", "3374.TW": "精材", "6231.TW": "系微",
    "4961.TW": "天鈺", "4966.TW": "譜瑞-KY", "5269.TW": "祥碩", "6415.TW": "矽力*-KY",
    "6515.TW": "穎崴", "6526.TW": "達發", "6643.TW": "M31", "6732.TW": "昇佳電子",
    "6756.TW": "威鋒電子", "3035.TW": "智原",
    # 面板
    "2409.TW": "友達", "3481.TW": "群創", "6116.TW": "彩晶",
    # 電腦周邊
    "2357.TW": "華碩", "2353.TW": "宏碁", "2377.TW": "微星", "2376.TW": "技嘉",
    "2382.TW": "廣達", "3231.TW": "緯創", "2324.TW": "仁寶", "2356.TW": "英業達",
    "2385.TW": "群光", "3005.TW": "神基", "3017.TW": "奇鋐", "3324.TW": "雙鴻",
    "3515.TW": "華擎", "4938.TW": "和碩", "6277.TW": "宏正", "2301.TW": "光寶科",
    "2308.TW": "台達電", "2317.TW": "鴻海", "2332.TW": "友訊", "2347.TW": "聯強",
    # IC 通路
    "3036.TW": "文曄", "3702.TW": "大聯大", "8072.TW": "陞達",
    # 光電
    "3008.TW": "大立光", "3406.TW": "玉晶光", "4919.TW": "新唐", "3673.TW": "宸鴻",
    "6456.TW": "GIS-KY", "5264.TW": "鎧勝-KY",
    # 電信
    "2412.TW": "中華電", "4904.TW": "遠傳", "3045.TW": "台灣大",
    # 金融
    "2881.TW": "富邦金", "2882.TW": "國泰金", "2883.TW": "開發金", "2884.TW": "玉山金",
    "2885.TW": "元大金", "2886.TW": "兆豐金", "2887.TW": "台新金", "2888.TW": "新光金",
    "2889.TW": "國票金", "2890.TW": "永豐金", "2891.TW": "中信金", "2892.TW": "第一金",
    "5880.TW": "合庫金", "2834.TW": "臺企銀", "2801.TW": "彰銀", "2812.TW": "台中銀",
    # 航運
    "2603.TW": "長榮", "2609.TW": "陽明", "2610.TW": "華航", "2618.TW": "長榮航",
    "2637.TW": "慧洋-KY", "5608.TW": "四維航", "2605.TW": "新興", "2606.TW": "裕民",
    # 鋼鐵
    "2002.TW": "中鋼", "2014.TW": "中鴻", "2031.TW": "新光鋼", "2006.TW": "東和鋼鐵",
    # 塑膠
    "1301.TW": "台塑", "1303.TW": "南亞", "1326.TW": "台化", "1304.TW": "台聚",
    "1309.TW": "台達化", "1310.TW": "台苯",
    # 紡織
    "1402.TW": "遠東新", "1476.TW": "儒鴻", "1477.TW": "聚陽",
    # 水泥
    "1101.TW": "台泥", "1102.TW": "亞泥",
    # 食品
    "1216.TW": "統一", "1227.TW": "佳格", "1215.TW": "卜蜂",
    # 百貨
    "2912.TW": "統一超", "2903.TW": "遠百",
    # 電機
    "1504.TW": "東元", "1513.TW": "中興電", "1519.TW": "華城", "1527.TW": "鑽全",
    "1582.TW": "信錦", "1590.TW": "亞德客-KY",
    # 汽車
    "2201.TW": "裕隆", "2204.TW": "中華", "2227.TW": "裕日車",
    # 生技
    "4126.TW": "太景*-KY", "4137.TW": "麗豐-KY", "4162.TW": "智擎", "4174.TW": "浩鼎",
    "6472.TW": "保瑞", "6491.TW": "晶碩", "6576.TW": "逸達", "8404.TW": "百和興業",
    # 油電
    "6505.TW": "台塑化",
    # 營建
    "2501.TW": "國建", "2515.TW": "中工", "2548.TW": "華固",
    # 電子零組件
    "2313.TW": "華通", "2327.TW": "國巨", "2368.TW": "金像電", "2383.TW": "台光電",
    "2379.TW": "瑞昱", "2388.TW": "威盛", "2451.TW": "創見", "2474.TW": "可成",
    "3006.TW": "晶豪科", "3013.TW": "晟銘電", "3023.TW": "信邦", "3026.TW": "禾伸堂",
    "3037.TW": "欣興", "3044.TW": "健鼎", "3217.TW": "優群", "3338.TW": "泰碩",
    "3504.TW": "揚明光", "3653.TW": "健策", "4915.TW": "致伸", "4994.TW": "傳奇",
    "5007.TW": "三星", "5469.TW": "瀚宇博", "5483.TW": "中美晶", "6121.TW": "新普",
    "6269.TW": "台郡", "8046.TW": "南電",
    # 通信網路
    "2345.TW": "智邦", "3380.TW": "明泰", "3596.TW": "智易", "4906.TW": "正文",
    "5388.TW": "中磊",
    # 上櫃（.TWO）
    "1565.TWO": "精華", "1785.TWO": "光洋科", "1795.TWO": "美時", "1815.TWO": "富采",
    "3081.TWO": "聯亞", "3105.TWO": "穩懋", "3152.TWO": "璟德", "3218.TWO": "大學光",
    "3260.TWO": "威剛", "3285.TWO": "微端", "3293.TWO": "鈊象", "3317.TWO": "尼克森",
    "3325.TWO": "旭品", "3363.TWO": "上詮", "3376.TWO": "新日興", "3402.TWO": "漢科",
    "3444.TWO": "利機", "3491.TWO": "昇達科", "3508.TWO": "位速", "3529.TWO": "力旺",
    "3537.TWO": "堡達", "3548.TWO": "兆利", "3552.TWO": "同致", "3587.TWO": "閎康",
    "3615.TWO": "安可", "3624.TWO": "光頡", "3630.TWO": "新鉅科", "3663.TWO": "鑫科",
    "3675.TWO": "德微", "3680.TWO": "家登", "3691.TWO": "碩禾", "4105.TWO": "東洋",
    "4114.TWO": "健喬", "4163.TWO": "鐿鈦", "4168.TWO": "台灣東洋", "4198.TWO": "欣大健康",
    "4306.TWO": "炎洲", "4401.TWO": "東隆興", "4433.TWO": "興采", "4506.TWO": "崇友",
    "4526.TWO": "東台", "4533.TWO": "協易機", "4541.TWO": "晟田", "4543.TWO": "萬在",
    "4551.TWO": "智伸科", "4552.TWO": "力達-KY", "4563.TWO": "百德", "4568.TWO": "科際精密",
    "4707.TWO": "磐亞", "4711.TWO": "永純", "4714.TWO": "永捷", "4721.TWO": "美琪瑪",
    "4722.TWO": "國精化", "4736.TWO": "泰博", "4743.TWO": "合一", "4747.TWO": "強生",
    "4763.TWO": "材料-KY", "4764.TWO": "雙鍵", "4908.TWO": "前鼎", "4912.TWO": "聯德控股-KY",
    "4927.TWO": "泰鼎-KY", "4931.TWO": "新盛力", "4942.TWO": "嘉彰", "4950.TWO": "牧東",
    "4953.TWO": "緯軟", "4967.TWO": "十銓", "4971.TWO": "IET-KY", "4972.TWO": "湯石",
    "4974.TWO": "亞泰", "4987.TWO": "科誠", "4991.TWO": "環宇-KY", "5009.TWO": "榮剛",
    "5011.TWO": "久威", "5014.TWO": "建錩", "5015.TWO": "華祺", "5016.TWO": "久裕",
    "5203.TWO": "訊連", "5289.TWO": "宜鼎", "5299.TWO": "杰力", "5306.TWO": "桂盟",
    "5345.TWO": "天揚", "5351.TWO": "鈺創", "5371.TWO": "中光電", "5403.TWO": "中菲",
    "5412.TWO": "明基材", "5425.TWO": "台半", "5434.TWO": "崇越", "5460.TWO": "同協",
    "5478.TWO": "智冠", "5489.TWO": "彩富", "5490.TWO": "同亨", "5493.TWO": "三聯",
    "5512.TWO": "力麒", "5514.TWO": "三豐", "5519.TWO": "隆大", "5520.TWO": "力泰",
    "5523.TWO": "豐謙", "5530.TWO": "龍巖", "5536.TWO": "聖暉", "5543.TWO": "桓鼎-KY",
    "5604.TWO": "中連", "5609.TWO": "中菲行", "5701.TWO": "劍湖山", "5704.TWO": "老爺知",
    "5864.TWO": "致和證", "5871.TWO": "中租-KY", "5903.TWO": "全家", "5904.TWO": "寶雅",
    "5905.TWO": "南仁湖", "6005.TWO": "群益證", "6015.TWO": "宏遠證", "6016.TWO": "康和證",
    "6020.TWO": "大展證", "6023.TWO": "元大期", "6024.TWO": "群益期", "6101.TWO": "寬魚國際",
    "6104.TWO": "創惟", "6108.TWO": "競國", "6111.TWO": "大宇資", "6114.TWO": "久威",
    "6118.TWO": "建達", "6122.TWO": "擎邦", "6123.TWO": "產晶", "6125.TWO": "廣運",
    "6126.TWO": "信音", "6127.TWO": "九豪", "6128.TWO": "上福", "6130.TWO": "亞元",
    "6133.TWO": "金橋", "6134.TWO": "萬旭", "6136.TWO": "富爾特", "6138.TWO": "茂達",
    "6140.TWO": "訊達", "6143.TWO": "振曜", "6144.TWO": "得利影", "6146.TWO": "耕興",
    "6147.TWO": "頎邦", "6148.TWO": "驊宏資", "6150.TWO": "撼訊", "6151.TWO": "晉倫",
    "6152.TWO": "百一", "6153.TWO": "嘉聯益", "6154.TWO": "順發", "6155.TWO": "鈞寶",
    "6156.TWO": "松上", "6158.TWO": "禾昌", "6160.TWO": "欣技", "6161.TWO": "捷波",
    "6163.TWO": "華電網", "6165.TWO": "浪凡", "6166.TWO": "凌華", "6167.TWO": "眾達-KY",
    "6168.TWO": "宏齊", "6170.TWO": "統振", "6171.TWO": "亞銳士", "6173.TWO": "信昌電",
    "6174.TWO": "安碁", "6175.TWO": "立敦", "6176.TWO": "瑞儀", "6177.TWO": "達麗",
    "6178.TWO": "立碁", "6179.TWO": "亞通", "6180.TWO": "橘子", "6182.TWO": "合晶",
    "6183.TWO": "關貿", "6184.TWO": "大豐電", "6185.TWO": "幃翔", "6186.TWO": "新潤",
    "6187.TWO": "萬潤", "6188.TWO": "廣明", "6189.TWO": "豐藝", "6190.TWO": "萬泰科",
    "6191.TWO": "精成科", "6192.TWO": "巨路", "6194.TWO": "育富", "6195.TWO": "詩肯",
    "6196.TWO": "帆宣", "6197.TWO": "佳必琪", "6198.TWO": "瑞筑", "6199.TWO": "晶華",
    "6201.TWO": "亞弘電", "6202.TWO": "盛群", "6203.TWO": "海韻電", "6204.TWO": "艾華",
    "6205.TWO": "詮欣", "6206.TWO": "飛捷", "6207.TWO": "雷科", "6208.TWO": "日揚",
    "6209.TWO": "今國光", "6210.TWO": "慶生", "6211.TWO": "福登", "6212.TWO": "理銘",
    "6213.TWO": "聯茂", "6214.TWO": "精誠", "6215.TWO": "和椿", "6216.TWO": "居易",
    "6217.TWO": "中探針", "6218.TWO": "豪勉", "6219.TWO": "富旺", "6220.TWO": "岳豐",
    "6221.TWO": "晉泰", "6222.TWO": "上揚", "6223.TWO": "旺矽", "6224.TWO": "聚鼎",
    "6225.TWO": "天瀚", "6226.TWO": "光鼎", "6227.TWO": "茂綸", "6228.TWO": "全譜",
    "6229.TWO": "研通", "6230.TWO": "超眾", "6231.TWO": "系微", "6233.TWO": "旺玖",
    "6234.TWO": "高僑", "6235.TWO": "華孚", "6236.TWO": "康呈", "6237.TWO": "國碩",
    "6238.TWO": "勝麗", "6239.TWO": "力成", "6240.TWO": "松崗", "6241.TWO": "易通展",
    "6242.TWO": "立康", "6243.TWO": "迅杰", "6244.TWO": "茂迪", "6245.TWO": "立端",
    "6246.TWO": "臺龍", "6247.TWO": "淇譽電", "6248.TWO": "沛波", "6250.TWO": "宇加",
    "6251.TWO": "定穎", "6252.TWO": "海灣", "6253.TWO": "創源", "6254.TWO": "岳豐",
    "6255.TWO": "奈米醫材", "6256.TWO": "安國", "6257.TWO": "矽格", "6258.TWO": "金士頓",
    "6259.TWO": "百徽", "6260.TWO": "尚立", "6261.TWO": "久元", "6263.TWO": "普萊德",
    "6264.TWO": "富裔", "6265.TWO": "方土昶", "6266.TWO": "泰詠", "6268.TWO": "台表科",
    "6269.TWO": "台郡", "6270.TWO": "倍微", "6271.TWO": "同欣電", "6272.TWO": "驊訊",
    "6274.TWO": "台燿", "6275.TWO": "元山", "6276.TWO": "名鐘", "6278.TWO": "台表科",
    "6279.TWO": "胡連", "6280.TWO": "致新", "6281.TWO": "聯電", "6282.TWO": "康舒",
    "6283.TWO": "淳安", "6284.TWO": "大中", "6285.TWO": "啟碁", "6286.TWO": "立錡",
    "6287.TWO": "元隆", "6288.TWO": "聯鈞", "6289.TWO": "華上", "6290.TWO": "良維",
    "6291.TWO": "沛亨", "6292.TWO": "迅德", "6293.TWO": "敏成", "6294.TWO": "智基",
    "6295.TWO": "兆遠", "6296.TWO": "東捷", "6297.TWO": "宏致", "6298.TWO": "崧騰",
    "6299.TWO": "大田", "6300.TWO": "日勝化", "6301.TWO": "華宏", "6302.TWO": "易華電",
    "6508.TWO": "惠光", "6509.TWO": "聚和", "8008.TWO": "建國", "8024.TWO": "佑華",
    "8027.TWO": "鈦昇", "8028.TWO": "昇陽半", "8032.TWO": "光菱", "8033.TWO": "雷虎",
    "8034.TWO": "榮群", "8039.TWO": "台虹", "8040.TWO": "九暘", "8042.TWO": "金山電",
    "8043.TWO": "蜜望實", "8044.TWO": "網家", "8047.TWO": "星雲", "8048.TWO": "德勝",
    "8049.TWO": "晶采", "8050.TWO": "廣積", "8053.TWO": "巨有", "8054.TWO": "安馳",
    "8059.TWO": "凱碩", "8064.TWO": "東捷", "8066.TWO": "來思達", "8067.TWO": "志旭",
    "8068.TWO": "全達", "8069.TWO": "元太", "8070.TWO": "長華", "8071.TWO": "能率網通",
    "8072.TWO": "陞達", "8074.TWO": "鉅橡", "8076.TWO": "伍豐", "8077.TWO": "冠華",
    "8079.TWO": "誠遠", "8080.TWO": "印鉐", "8081.TWO": "致和", "8082.TWO": "眾星",
    "8083.TWO": "瑞穎", "8084.TWO": "巨虹", "8085.TWO": "福華", "8086.TWO": "宏捷科",
    "8087.TWO": "華鎂鑫", "8088.TWO": "品安", "8089.TWO": "康全電", "8090.TWO": "永彰",
    "8091.TWO": "翔名", "8092.TWO": "建暐", "8093.TWO": "保銳", "8094.TWO": "達邦蛋白",
    "8096.TWO": "擎亞", "8097.TWO": "常珵", "8098.TWO": "慶康", "8099.TWO": "大世科",
    "8101.TWO": "華冠", "8102.TWO": "沛波", "8103.TWO": "瀚荃", "8104.TWO": "錸寶",
    "8105.TWO": "凌巨", "8107.TWO": "大億金茂", "8109.TWO": "博大", "8110.TWO": "華東",
    "8111.TWO": "立碁", "8112.TWO": "至上", "8114.TWO": "振樺電", "8115.TWO": "義隆",
    "8116.TWO": "奇偶", "8119.TWO": "公準", "8121.TWO": "越峰", "8131.TWO": "福懋科",
    "8147.TWO": "正淩", "8150.TWO": "南茂", "8155.TWO": "博智", "8163.TWO": "達方",
    "8176.TWO": "智捷", "8183.TWO": "精星", "8201.TWO": "無敵", "8210.TWO": "勤誠",
    "8211.TWO": "利機", "8213.TWO": "志超", "8215.TWO": "明基材", "8222.TWO": "寶一",
    "8227.TWO": "巨有科技", "8234.TWO": "新漢", "8240.TWO": "華宏", "8249.TWO": "菱光",
    "8255.TWO": "朋程", "8261.TWO": "富鼎", "8266.TWO": "中日新", "8271.TWO": "宇瞻",
    "8272.TWO": "全景軟體", "8277.TWO": "商丞", "8279.TWO": "生展", "8281.TWO": "歐普羅",
    "8287.TWO": "英格爾", "8289.TWO": "泰藝", "8291.TWO": "尚茂", "8298.TWO": "威睿",
    "8299.TWO": "大慶證", "8341.TWO": "日友", "8349.TWO": "恒耀", "8354.TWO": "冠好",
    "8358.TWO": "金居", "8360.TWO": "柏承", "8367.TWO": "建新國際", "8370.TWO": "欣天然",
    "8374.TWO": "羅昇", "8383.TWO": "千附", "8390.TWO": "金益鼎", "8401.TWO": "白紗科",
    "8403.TWO": "盛弘", "8409.TWO": "商之器", "8410.TWO": "森田", "8415.TWO": "大國鋼",
    "8416.TWO": "實威", "8420.TWO": "明揚", "8421.TWO": "旭源", "8422.TWO": "可寧衛",
    "8423.TWO": "保綠", "8424.TWO": "惠普", "8426.TWO": "紅木", "8427.TWO": "東生華",
    "8429.TWO": "金麗科", "8430.TWO": "春源", "8431.TWO": "匯鑽科", "8432.TWO": "東台",
    "8433.TWO": "弘帆", "8435.TWO": "鉅邁", "8436.TWO": "大江", "8437.TWO": "大地-KY",
    "8438.TWO": "昶昕", "8440.TWO": "綠電", "8442.TWO": "富邦媒", "8443.TWO": "阿瘦",
    "8444.TWO": "綠河-KY", "8446.TWO": "華研", "8450.TWO": "霹靂", "8454.TWO": "富邦媒",
    "8455.TWO": "大拓-KY", "8462.TWO": "柏文", "8463.TWO": "潤泰材", "8464.TWO": "億豐",
    "8465.TWO": "中揚光", "8466.TWO": "美吉吉-KY", "8467.TWO": "波力-KY", "8472.TWO": "夠麻吉",
    "8473.TWO": "山林水", "8476.TWO": "台境", "8477.TWO": "創業家", "8478.TWO": "三貝德",
    "8480.TWO": "泰昇-KY", "8481.TWO": "政伸", "8482.TWO": "商億-KY", "8487.TWO": "愛爾達",
    "8488.TWO": "吉源-KY", "8489.TWO": "三貝德", "8490.TWO": "佐登-KY", "8491.TWO": "永冠-KY",
    "8492.TWO": "聯德", "8493.TWO": "力士", "8494.TWO": "漢來", "8495.TWO": "經緯航",
    "8496.TWO": "台翰", "8497.TWO": "意德士", "8498.TWO": "鼎基", "8499.TWO": "鼎炫-KY",
}

STOCK_NAMES = {v: k for k, v in STOCK_POOL.items()}


class DataLoader(QThread):
    finished = Signal(pd.DataFrame, pd.DataFrame, pd.DataFrame)
    error = Signal(str)

    def __init__(self, ticker_symbols, name_list):
        super().__init__()
        self.ticker_symbols = ticker_symbols
        self.name_list = name_list

    def run(self):
        try:
            data = yf.download(
                self.ticker_symbols,
                start="2026-01-01",
                interval="1d",
                auto_adjust=True,
                progress=False,
            )
            close = data["Close"]
            close = close.rename(columns=dict(zip(self.ticker_symbols, self.name_list)))
            returns = close.pct_change().dropna()
            corr = returns.corr()
            self.finished.emit(close, returns, corr)
        except Exception as e:
            self.error.emit(str(e))


class SearchableCombo(QWidget):
    def __init__(self, label_text, items_dict, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        self.label = QLabel(label_text)
        self.label.setStyleSheet("font-weight: 600; color: #334155; font-size: 12px;")
        layout.addWidget(self.label)

        self.combo = QComboBox()
        self.combo.setEditable(True)
        self.combo.setInsertPolicy(QComboBox.NoInsert)
        self.combo.setMinimumHeight(34)
        self.combo.setStyleSheet("""
            QComboBox {
                background-color: #ffffff;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                padding: 4px 8px;
                font-size: 13px;
                color: #1e293b;
            }
            QComboBox:focus {
                border-color: #7c3aed;
            }
            QComboBox:hover {
                border-color: #94a3b8;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                selection-background-color: #7c3aed;
                selection-color: #ffffff;
                color: #1e293b;
                font-size: 12px;
            }
        """)

        self.items_dict = items_dict
        sorted_items = sorted(items_dict.items(), key=lambda x: x[1])
        for code, name in sorted_items:
            self.combo.addItem(f"{name} ({code})", code)

        self.completer = QCompleter([self.combo.itemText(i) for i in range(self.combo.count())])
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchContains)
        self.combo.setCompleter(self.completer)

        layout.addWidget(self.combo)

    def current_code(self):
        return self.combo.currentData()

    def set_by_code(self, code):
        for i in range(self.combo.count()):
            if self.combo.itemData(i) == code:
                self.combo.setCurrentIndex(i)
                return


class StockCompareApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("台股相關係數分析器")
        self.setMinimumSize(1100, 750)
        self.resize(1200, 800)

        self.close_data = None
        self.returns_data = None
        self.corr_data = None

        self._setup_style()
        self._setup_ui()

    def _setup_style(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8fafc;
            }
            QWidget#centralWidget {
                background-color: #f8fafc;
            }
            QLabel {
                color: #334155;
                font-family: "Microsoft JhengHei", "Arial Unicode MS", sans-serif;
            }
            QGroupBox {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 16px;
                font-weight: 600;
                color: #475569;
                font-family: "Microsoft JhengHei", sans-serif;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 10px;
                padding: 0 6px;
                background-color: #ffffff;
            }
            QPushButton#analyzeBtn {
                background-color: #7c3aed;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 10px 32px;
                font-weight: 700;
                font-size: 14px;
                font-family: "Microsoft JhengHei", sans-serif;
                min-height: 20px;
            }
            QPushButton#analyzeBtn:hover {
                background-color: #8b5cf6;
            }
            QPushButton#analyzeBtn:pressed {
                background-color: #6d28d9;
            }
            QPushButton#analyzeBtn:disabled {
                background-color: #cbd5e1;
                color: #94a3b8;
            }
            QStatusBar {
                background-color: #f1f5f9;
                color: #64748b;
                border-top: 1px solid #e2e8f0;
                font-family: "Microsoft JhengHei", sans-serif;
            }
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 4px;
                gridline-color: #f1f5f9;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 4px 8px;
            }
            QHeaderView::section {
                background-color: #f8fafc;
                color: #475569;
                font-weight: 600;
                border: none;
                border-bottom: 2px solid #e2e8f0;
                padding: 6px 8px;
                font-size: 12px;
            }
        """)

    def _setup_ui(self):
        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(16)

        # ── Header ──
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(2)

        title = QLabel("台股相關係數分析器")
        title.setStyleSheet("font-size: 22px; font-weight: 700; color: #0f172a;")
        subtitle = QLabel("資料來源：Yahoo Finance ｜ 2026/01/01 至今 ｜ 選擇 4 檔股票並點擊分析")
        subtitle.setStyleSheet("font-size: 12px; color: #64748b;")

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addWidget(header)

        # ── Stock selector row ──
        selector_card = QFrame()
        selector_card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
            }
        """)
        selector_layout = QHBoxLayout(selector_card)
        selector_layout.setContentsMargins(16, 20, 16, 20)
        selector_layout.setSpacing(12)

        default_codes = ["2330.TW", "2303.TW", "2454.TW", "2317.TW"]
        self.stock_selectors = []
        for i in range(4):
            sel = SearchableCombo(f"股票 {['一', '二', '三', '四'][i]}", STOCK_POOL)
            sel.set_by_code(default_codes[i])
            self.stock_selectors.append(sel)
            selector_layout.addWidget(sel)

        self.analyze_btn = QPushButton("開始分析")
        self.analyze_btn.setObjectName("analyzeBtn")
        self.analyze_btn.setMinimumWidth(140)
        self.analyze_btn.clicked.connect(self.on_analyze)
        selector_layout.addWidget(self.analyze_btn)

        main_layout.addWidget(selector_card)

        # ── Content area ──
        content = QSplitter(Qt.Horizontal)
        content.setHandleWidth(2)
        content.setStyleSheet("""
            QSplitter::handle {
                background-color: #e2e8f0;
            }
        """)

        # Left: heatmap + table
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(12)

        heatmap_group = QGroupBox("相關係數熱力圖")
        heatmap_layout = QVBoxLayout(heatmap_group)
        self.canvas_frame = QFrame()
        self.canvas_frame.setMinimumHeight(320)
        self.canvas_frame.setStyleSheet("background-color: #ffffff; border-radius: 6px;")
        self.figure = Figure(figsize=(5, 4), dpi=100, facecolor="#ffffff")
        self.figure.set_facecolor("#ffffff")
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor("#ffffff")
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self.canvas_frame)
        self._draw_placeholder()
        canvas_layout = QVBoxLayout(self.canvas_frame)
        canvas_layout.setContentsMargins(4, 4, 4, 4)
        canvas_layout.addWidget(self.canvas)
        heatmap_layout.addWidget(self.canvas_frame)
        left_layout.addWidget(heatmap_group)

        # Right: tabs for close / returns / correlation table
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                background-color: #ffffff;
                padding: 4px;
            }
            QTabBar::tab {
                background-color: #f1f5f9;
                color: #64748b;
                border: 1px solid #e2e8f0;
                border-bottom: none;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                padding: 8px 18px;
                margin-right: 3px;
                font-weight: 500;
                font-family: "Microsoft JhengHei", sans-serif;
                font-size: 12px;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                color: #0f172a;
                border-bottom: 1px solid #ffffff;
                font-weight: 600;
            }
            QTabBar::tab:hover:!selected {
                background-color: #ffffff;
                color: #334155;
            }
        """)

        # Tab 1: correlation table
        self.corr_table = QTableWidget()
        self.corr_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.corr_table.setSelectionMode(QTableWidget.NoSelection)
        self.tabs.addTab(self.corr_table, "相關係數矩陣")

        # Tab 2: close price
        self.price_table = QTableWidget()
        self.price_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.price_table.setSelectionMode(QTableWidget.NoSelection)
        self.tabs.addTab(self.price_table, "收盤價")

        # Tab 3: returns
        self.return_table = QTableWidget()
        self.return_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.return_table.setSelectionMode(QTableWidget.NoSelection)
        self.tabs.addTab(self.return_table, "日報酬率")

        right_layout.addWidget(self.tabs)
        content.addWidget(left_panel)
        content.addWidget(right_panel)
        content.setSizes([550, 450])
        main_layout.addWidget(content, 1)

        # ── Status bar ──
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就緒 — 請選擇 4 檔股票後點擊「開始分析」")

        # ── Info text ──
        info = QLabel("💡 相關係數越接近 1 表示走勢越同步，越接近 -1 表示相反，接近 0 則無關。")
        info.setStyleSheet("color: #64748b; font-size: 12px; padding: 4px 0;")
        main_layout.addWidget(info)

    def _draw_placeholder(self):
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor("#ffffff")
        self.ax.text(0.5, 0.5, "請選擇股票並點擊「開始分析」",
                     ha="center", va="center", fontsize=14, color="#94a3b8",
                     transform=self.ax.transAxes)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        for spine in self.ax.spines.values():
            spine.set_visible(False)
        self.canvas.draw()

    def _draw_heatmap(self, corr):
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor("#ffffff")

        names = list(corr.columns)
        vals = corr.values

        im = self.ax.imshow(vals, cmap="RdYlBu", vmin=-1, vmax=1, aspect="equal")

        self.ax.set_xticks(range(len(names)))
        self.ax.set_yticks(range(len(names)))
        self.ax.set_xticklabels(names, fontsize=10, color="#334155")
        self.ax.set_yticklabels(names, fontsize=10, color="#334155")

        for i in range(len(names)):
            for j in range(len(names)):
                val = vals[i, j]
                text_color = "white" if abs(val) > 0.55 else "#1e293b"
                self.ax.text(j, i, f"{val:.4f}", ha="center", va="center",
                             fontsize=13, fontweight="bold", color=text_color)

        cbar = self.figure.colorbar(im, ax=self.ax, shrink=0.85, pad=0.04)
        cbar.set_label("相關係數", fontsize=10, color="#475569")
        cbar.ax.yaxis.set_tick_params(color="#475569")
        plt.setp(cbar.ax.get_yticklabels(), color="#475569")

        self.ax.set_title("日報酬率相關係數熱力圖", fontsize=13, fontweight="bold",
                          color="#0f172a", pad=12)
        self.figure.tight_layout()
        self.canvas.draw()

    def _fill_table(self, table, data, fmt=".2f"):
        table.setRowCount(0)
        table.setColumnCount(0)
        if data is None or data.empty:
            return
        rows = data.tail(30)
        table.setRowCount(len(rows))
        table.setColumnCount(len(data.columns))
        table.setHorizontalHeaderLabels(list(data.columns))
        table.setVerticalHeaderLabels([str(getattr(d, 'date', lambda: str(d))()) for d in rows.index])

        for i, (_, row) in enumerate(rows.iterrows()):
            for j, val in enumerate(row):
                display = f"{val:{fmt}}" if pd.notna(val) else "N/A"
                item = QTableWidgetItem(display)
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                if j % 2 == 0:
                    item.setBackground(QColor("#f8fafc"))
                table.setItem(i, j, item)

        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.viewport().update()

    def _fill_corr_table(self, corr):
        self.corr_table.setRowCount(0)
        self.corr_table.setColumnCount(0)
        names = list(corr.columns)
        self.corr_table.setRowCount(len(names))
        self.corr_table.setColumnCount(len(names))
        self.corr_table.setHorizontalHeaderLabels(names)
        self.corr_table.setVerticalHeaderLabels(names)

        for i in range(len(names)):
            for j in range(len(names)):
                val = corr.iloc[i, j]
                item = QTableWidgetItem(f"{val:.4f}")
                item.setTextAlignment(Qt.AlignCenter)
                if val > 0.7:
                    bg = QColor("#dc2626")
                    fg = QColor("#ffffff")
                elif val > 0.4:
                    bg = QColor("#f59e0b")
                    fg = QColor("#ffffff")
                else:
                    bg = QColor("#f1f5f9")
                    fg = QColor("#334155")
                item.setBackground(bg)
                item.setForeground(fg)
                font = QFont("Consolas", 11, QFont.Bold)
                item.setFont(font)
                self.corr_table.setItem(i, j, item)

        self.corr_table.horizontalHeader().setStretchLastSection(True)
        self.corr_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    @Slot()
    def on_analyze(self):
        codes = []
        names = []
        for sel in self.stock_selectors:
            code = sel.current_code()
            if not code:
                self.status_bar.showMessage("請確實選擇 4 檔不同的股票")
                return
            codes.append(code)
            names.append(STOCK_POOL.get(code, code))

        if len(set(codes)) < 4:
            self.status_bar.showMessage("請選擇 4 檔不同的股票（不可重複）")
            return

        self.analyze_btn.setEnabled(False)
        self.analyze_btn.setText("資料下載中…")
        self.status_bar.showMessage("正在從 Yahoo Finance 下載股價資料…")

        self.loader = DataLoader(codes, names)
        self.loader.finished.connect(self.on_data_loaded)
        self.loader.error.connect(self.on_data_error)
        self.loader.start()

    @Slot(pd.DataFrame, pd.DataFrame, pd.DataFrame)
    def on_data_loaded(self, close, returns, corr):
        self.close_data = close
        self.returns_data = returns
        self.corr_data = corr

        self._draw_heatmap(corr)
        self._fill_corr_table(corr)
        self._fill_table(self.price_table, close, ".2f")
        self._fill_table(self.return_table, returns, ".4f")

        self.analyze_btn.setEnabled(True)
        self.analyze_btn.setText("開始分析")
        self.status_bar.showMessage(
            f"分析完成！資料區間：{returns.index[0].date()} ~ {returns.index[-1].date()}，共 {len(returns)} 個交易日"
        )

    @Slot(str)
    def on_data_error(self, msg):
        self.analyze_btn.setEnabled(True)
        self.analyze_btn.setText("開始分析")
        self.status_bar.showMessage(f"資料下載失敗：{msg}")


def main():
    app = QApplication(sys.argv)
    font = QFont("Microsoft JhengHei", 10)
    font.setStyleHint(QFont.SansSerif)
    app.setFont(font)
    window = StockCompareApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
