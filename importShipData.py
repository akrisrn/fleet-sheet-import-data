# coding=utf-8
import json
import sys

import MySQLdb
from langconv import ConverterHandler

from pb import progressbar

reload(sys)
sys.setdefaultencoding("utf-8")

db_host = ''
db_port = 3306
db_user = ''
db_password = ''
db_name = ''


def convert(word):
    pair = {
        "Bismarck": "俾斯麦",
        "Prinz Eugen": "欧根亲王",
        "Graf Zeppelin": "齐柏林伯爵",
        "Zara": "扎拉",
        "Pola": "波拉",
        "Iowa": "衣阿华",
        "あきつ丸": "秋津丸",
        "Littorio": "利托里奥",
        "Italia": "意大利",
        "Roma": "罗马",
        "Warspite": "厌战",
        "Aquila": "天鹰",
        "QF 2ポンド8連装ポンポン砲": "QF2磅 8连装砰砰炮",
        "改良型艦本式タービン": "改良型舰政本部式涡轮",
        "強化型艦本式缶": "强化型舰政本部式锅炉",
        "飛び魚": "飞鱼",
        "タービン": "涡轮",
        "深海缶": "深海锅炉",
        "ソナー": "声呐",
        "連絡": "联络",
        "バルジ": "突出部",
        "ドラム缶": "运输桶",
        "新型高温高圧缶": "新型高温高压锅炉",
        "ダズル迷彩": "炫目迷彩",
        "レーダー": "雷达",
        "レーダ―": "雷达",
        "仕様": "式样",
        "プリエーゼ式水中防御隔壁": "普列赛水下防御隔壁",
        "秋刀魚の缶詰": "秋刀鱼罐头",
        "機銃": "机枪",
        "海外艦との接触": "和海外舰的接触",
        "予行": "预行",
        "弾": "弹",
        "応": "应",
        "聴": "听",
        "観": "观",
        "発": "发",
        "闘": "斗",
        "関": "关",
        "駆": "驱",
        "軽": "轻",
        "讐": "仇",
        "両": "两",
        "撃": "击",
        "帯": "带",
        "弐": "二",
        "壊": "坏",
        "囲": "围",
        "収": "收",
        "付": "附",
        "叡": "睿",
        "黒": "黑",
        "蔵": "藏",
        "浜": "滨",
        "暁": "晓",
        "満": "满",
        "皐": "皋",
        "単": "单",
        "砲": "炮",
        "戦": "战",
        "対": "对",
    }
    if word in pair.keys():
        word = pair[word]
    return word


def convert_name(word):
    name = ConverterHandler('zh-hans').convert(convert(word))
    return name


def remark_name(word):
    name = ""
    for w in word:
        if u'\u0041' <= w <= u'\u005a':
            name = word.lower()
            break
    if word == "Верный":
        name = "响改二"
    if word == "まるゆ":
        name = "马鹿油,马路油"
    if word == "まるゆ改":
        name = "马鹿油改,马路油改"
    if word == "Libeccio":
        name += ",西南风"
    if word == "Libeccio改":
        name += ",西南风改"
    if word == "驱逐舰":
        name = "驱逐"
    if word == "轻巡洋舰":
        name = "轻巡"
    if word == "重雷装巡洋舰":
        name = "雷巡"
    if word == "重巡洋舰":
        name = "重巡"
    if word == "航空巡洋舰":
        name = "航巡"
    if word == "轻空母":
        name = "轻母"
    if word == "高速战舰":
        name = "高战"
    if word == "低速战舰":
        name = "低战"
    if word == "航空战舰":
        name = "航战"
    if word == "正规空母":
        name = "正航"
    if word == "潜水舰":
        name = "潜艇"
    if word == "潜水空母":
        name = "潜母"
    if word == "补给舰":
        name = "补给"
    if word == "水上机母舰":
        name = "水母"
    if word == "扬陆舰":
        name = "扬陆"
    if word == "装甲空母":
        name = "装母"
    if word == "工作舰":
        name = "工作"
    if word == "潜水母舰":
        name = "潜母舰"
    if word == "练习巡洋舰":
        name = "练巡"
    return name


def read_json():
    fp = open('START2.json', 'r')
    data = json.loads(fp.read())
    fp.close()
    return data


def read_ships():
    return read_json()["api_data"]["api_mst_ship"]


def read_equipment():
    return read_json()["api_data"]["api_mst_slotitem"]


def read_ship_type():
    return read_json()["api_data"]["api_mst_stype"]


def read_map_info():
    return read_json()["api_data"]["api_mst_mapinfo"]


def read_mission():
    return read_json()["api_data"]["api_mst_mission"]


def gen_st_and_key(o):
    for key in o[20].keys():
        word = o[20][key]
        if isinstance(word, list):
            for i in range(len(word)):
                ke = key + "_" + str(i)
                st = ke + " INT"
                yield st, ke
        elif isinstance(word, dict):
            for i in word.keys():
                ke = key + "_" + str(i)
                st = ke + " INT"
                yield st, ke
        else:
            if isinstance(word, int):
                st = key + " INT"
            elif isinstance(word, float):
                st = key + " FLOAT"
            elif isinstance(word, unicode):
                st = key + " VARCHAR(255)"
            else:
                st = key + " INT"
            yield st, key


def gen_word_and_key(o, is_equip=False):
    if is_equip:
        if "api_cost" not in o:
            o["api_cost"] = 0
        if "api_distance" not in o:
            o["api_distance"] = 0
    for key in o.keys():
        word = o[key]
        if isinstance(word, list):
            for i in range(len(word)):
                yield word[i], key
        elif isinstance(word, dict):
            for i in word.keys():
                yield word[i], key
        else:
            yield word, key


def gen_create_ships_table_stn(ships):
    stn = ""
    keys = ""
    for st, key in gen_st_and_key(ships):
        stn += st + ","
        keys += key + ","
    keys += "api_name_s,api_remark"
    stn = "CREATE TABLE IF NOT EXISTS ships (" + stn + \
          "api_name_s VARCHAR(255),api_remark VARCHAR(255));"
    return stn, keys


def gen_insert_ships_stn(ships, keys):
    for ship in ships:
        val = ""
        name = ""
        remark = ""
        for word, key in gen_word_and_key(ship):
            if key == "api_id" and word == 501:
                return
            if key == "api_name":
                name = convert_name(word)
                remark = remark_name(word)
            if isinstance(word, unicode):
                val += "'" + word + "',"
            else:
                val += str(word) + ","
        val += "'" + name + "','" + remark + "'"
        yield "insert into ships (" + keys + ") values (" + val + ")"


def gen_create_equipment_table_stn(equipment):
    stn = ""
    keys = ""
    for st, key in gen_st_and_key(equipment):
        stn += st + ","
        keys += key + ","
    keys += "api_name_s,api_remark"
    stn = "CREATE TABLE IF NOT EXISTS equipment (" + stn + \
          "api_name_s VARCHAR(255),api_remark VARCHAR(255));"
    return stn, keys


def gen_insert_equipment_stn(equipment, keys):
    for equip in equipment:
        val = ""
        name = ""
        remark = ""
        for word, key in gen_word_and_key(equip, True):
            if key == "api_name":
                name = convert_name(word)
                remark = remark_name(name)
            if isinstance(word, unicode):
                val += "'" + word + "',"
            else:
                val += str(word) + ","
        val += "'" + name + "','" + remark + "'"
        yield "insert into equipment (" + keys + ") values (" + val + ")"


def gen_create_ship_type_table_stn(ship_type):
    stn = ""
    keys = ""
    for st, key in gen_st_and_key(ship_type):
        stn += st + ","
        keys += key + ","
    keys += "api_name_s,api_remark"
    stn = "CREATE TABLE IF NOT EXISTS ship_type (" + stn + \
          "api_name_s VARCHAR(255),api_remark VARCHAR(255));"
    return stn, keys


def gen_insert_ship_type_stn(ship_type, keys):
    high_speed = True
    for s_type in ship_type:
        val = ""
        name = ""
        remark = ""
        for word, key in gen_word_and_key(s_type):
            if key == "api_name":
                name = convert_name(word)
                if name == "战舰":
                    name = ("高速" if high_speed else "低速") + name
                    high_speed = not high_speed
                remark = remark_name(name)
            if isinstance(word, unicode):
                val += "'" + word + "',"
            else:
                val += str(word) + ","
        val += "'" + name + "','" + remark + "'"
        yield "insert into ship_type (" + keys + ") values (" + val + ")"


def gen_create_map_info_table_stn(map_info):
    stn = ""
    keys = ""
    for st, key in gen_st_and_key(map_info):
        stn += st + ","
        keys += key + ","
    keys += "api_name_s,api_remark"
    stn = "CREATE TABLE IF NOT EXISTS map_info (" + stn + \
          "api_name_s VARCHAR(255),api_remark VARCHAR(255));"
    return stn, keys


def gen_insert_map_info_stn(map_info, keys):
    for info in map_info:
        val = ""
        name = ""
        remark = ""
        for word, key in gen_word_and_key(info):
            if key == "api_name":
                name = convert_name(word)
                remark = remark_name(name)
            if isinstance(word, unicode):
                val += "'" + word + "',"
            elif word is None:
                val += "0,"
            else:
                val += str(word) + ","
        val += "'" + name + "','" + remark + "'"
        yield "insert into map_info (" + keys + ") values (" + val + ")"


def gen_create_mission_table_stn(mission):
    stn = ""
    keys = ""
    for st, key in gen_st_and_key(mission):
        stn += st + ","
        keys += key + ","
    keys += "api_name_s,api_remark"
    stn = "CREATE TABLE IF NOT EXISTS mission (" + stn + \
          "api_name_s VARCHAR(255),api_remark VARCHAR(255));"
    return stn, keys


def gen_insert_mission_stn(mission, keys):
    for info in mission:
        val = ""
        name = ""
        remark = ""
        for word, key in gen_word_and_key(info):
            if key == "api_name":
                name = convert_name(word)
                remark = remark_name(name)
            if isinstance(word, unicode):
                val += "'" + word + "',"
            elif word is None:
                val += "0,"
            else:
                val += str(word) + ","
        val += "'" + name + "','" + remark + "'"
        yield "insert into mission (" + keys + ") values (" + val + ")"


def insert_db(mode=0):
    conn = MySQLdb.connect(host=db_host,
                           port=db_port,
                           user=db_user,
                           passwd=db_password,
                           db=db_name,
                           charset='utf8')
    cur = conn.cursor()
    left_just = 18
    if mode == 1 or mode == 0:
        cur.execute("drop table if exists ships")
        ships = read_ships()
        stn, keys = gen_create_ships_table_stn(ships)
        cur.execute(stn)
        ships_bar = progressbar(len(ships) - 215, "Insert ships".ljust(left_just))
        i = 0
        for stn in gen_insert_ships_stn(ships, keys):
            cur.execute(stn)
            i += 1
            ships_bar.progress(i)
    if mode == 2 or mode == 0:
        cur.execute("drop table if exists equipment")
        equipment = read_equipment()
        stn, keys = gen_create_equipment_table_stn(equipment)
        cur.execute(stn)
        equipment_bar = progressbar(len(equipment), "Insert equipment".ljust(left_just))
        i = 0
        for stn in gen_insert_equipment_stn(equipment, keys):
            cur.execute(stn)
            i += 1
            equipment_bar.progress(i)
    if mode == 3 or mode == 0:
        cur.execute("drop table if exists ship_type")
        ship_type = read_ship_type()
        stn, keys = gen_create_ship_type_table_stn(ship_type)
        cur.execute(stn)
        ship_type_bar = progressbar(len(ship_type), "Insert ship_type".ljust(left_just))
        i = 0
        for stn in gen_insert_ship_type_stn(ship_type, keys):
            cur.execute(stn)
            i += 1
            ship_type_bar.progress(i)
    if mode == 4 or mode == 0:
        cur.execute("drop table if exists map_info")
        map_info = read_map_info()
        stn, keys = gen_create_map_info_table_stn(map_info)
        cur.execute(stn)
        map_info_bar = progressbar(len(map_info), "Insert map_info".ljust(left_just))
        i = 0
        for stn in gen_insert_map_info_stn(map_info, keys):
            cur.execute(stn)
            i += 1
            map_info_bar.progress(i)
    if mode == 5 or mode == 0:
        cur.execute("drop table if exists mission")
        mission = read_mission()
        stn, keys = gen_create_mission_table_stn(mission)
        cur.execute(stn)
        mission_bar = progressbar(len(mission), "Insert mission".ljust(left_just))
        i = 0
        for stn in gen_insert_mission_stn(mission, keys):
            cur.execute(stn)
            i += 1
            mission_bar.progress(i)
    conn.commit()
    cur.close()
    conn.close()


insert_db(0)
