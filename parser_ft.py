import requests
import json
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
def test(match_id):
    url = "https://1xstavka.ru/LiveFeed/GetGameZip?id="+str(match_id)+"&lng=ru&cfview=0&isSubGames=true&GroupEvents=true&allEventsGroupSubGames=true&countevents=250&partner=51&grMode=2&marketType=1"
    response = requests.get(url,verify=False)
    return json.loads(response.content)
def getP1Id(match_id):
    url = "https://1xstavka.ru/LiveFeed/GetGameZip?id="+str(match_id)+"&lng=ru&cfview=0&isSubGames=true&GroupEvents=true&allEventsGroupSubGames=true&countevents=250&partner=51&grMode=2&marketType=1"
    response = requests.get(url,verify=False, timeout = 30)
    data = json.loads(response.content)
    try:
        SG = data["Value"]["SG"]
    except:
        return False
    for item in SG:
        try:
            if item["P"] == 1 and 'TG' not in item:
                return item["I"]
        except:
            pass
    return False
def getStats(match_id):
    stats = {}
    t1_id = getP1Id(match_id)
    if not t1_id:
        return False
    url = "https://1xstavka.ru/LiveFeed/GetGameZip?id="+str(t1_id)+"&lng=ru&cfview=0&isSubGames=true&GroupEvents=true&allEventsGroupSubGames=true&countevents=250&partner=51&grMode=2&marketType=1"
    response = requests.get(url,verify=False, timeout = 30)
    data = json.loads(response.content)
    try:
        P1 = 0
        P2 = 0
        for kf in data["Value"]["GE"]:
            if kf["G"] == 1:
                for E in kf["E"]:
                    for item in E:
                        if item['T'] == 1:
                            P1 = item["C"]
                        if item['T'] == 3:
                            P2 = item["C"]
            if kf["G"] == 4:
                total = kf["E"][1][0]["C"]
        if (not P1) or (not P2):
            print("hm")
            print(P1)
            print(P2)
            return False
        stats.update({"P1":str(P1),"P2":str(P2),"total":str(total)})
    except Exception as e:
        print("kek")
        print(e)
        return False
    
    match_stats = {}
    match_stats_adv = {}
    for item in data["Value"]["SC"]["S"]:
        match_stats.update({item["Key"]:item["Value"]})
    for item in data["Value"]["SC"]["ST"][0]["Value"]:
        match_stats_adv.update({item["ID"]:{"S1":item["S1"],"S2":item["S2"]}})
    try:
        stats.update({"corners_1":match_stats["ICorner1"],"yellows_1":match_stats["IYellowCard1"],"reds_1":match_stats["IRedCard1"],"penalty_1":match_stats["IPenalty1"]})
        stats.update({"corners_2":match_stats["ICorner2"],"yellows_2":match_stats["IYellowCard2"],"reds_2":match_stats["IRedCard2"],"penalty_2":match_stats["IPenalty2"]})
        # first,second = map(lambda x: x.split(";"),match_stats["Stat"].split("-"))
        # stats.update({"attacks_1":first[0],"dang_attacks_1":first[1],"control_1":first[2],"good_hits_1":first[3],"hits_1":first[4]})
        # stats.update({"attacks_2":second[0],"dang_attacks_2":second[1],"control_2":second[2],"good_hits_2":second[3],"hits_2":second[4]})
        stats.update({"attacks_1":match_stats["Attacks1"],"dang_attacks_1":match_stats["DanAttacks1"],"control_1":match_stats_adv[29]["S1"],"good_hits_1":match_stats["ShotsOn1"],"hits_1":match_stats["ShotsOff1"]})
        stats.update({"attacks_2":match_stats["Attacks2"],"dang_attacks_2":match_stats["DanAttacks2"],"control_2":match_stats_adv[29]["S2"],"good_hits_2":match_stats["ShotsOn2"],"hits_2":match_stats["ShotsOff2"]})
    except Exception as e:
        return False
    if not(float(stats['P1'])>3.1 and float(stats['P2'])>3.1 and int(stats['good_hits_1'])+int(stats['good_hits_2'])<=1 and int(stats['good_hits_1'])+int(stats['hits_1'])<=2 and int(stats['good_hits_2'])+int(stats['hits_2'])<=2 and int(stats['corners_1'])+int(stats['corners_2'])<=3 and int(stats['corners_1'])<=2 and int(stats['corners_2'])<=2 and int(stats['good_hits_1'])+int(stats['good_hits_2'])+int(stats['hits_1'])+int(stats['hits_2'])+int(stats['corners_1'])+int(stats['corners_2'])>0):
        return False
    temperature = "Нет данных"
    try:
        temper_data = data["Value"]["MIS"]
        for tmp in temper_data:
            if tmp["K"] == 9:
                temperature = tmp["V"]
    except Exception as e:
        pass
    stats.update({"temperature":temperature})
    return stats
def getStats3(match_id):
    stats = {}
    url = "https://1xstavka.ru/LiveFeed/GetGameZip?id="+str(match_id)+"&lng=ru&cfview=0&isSubGames=true&GroupEvents=true&allEventsGroupSubGames=true&countevents=250&partner=51&grMode=2&marketType=1"
    response = requests.get(url,verify=False, timeout = 30)
    data = json.loads(response.content)
    try:
        P1 = 0
        P2 = 0
        for kf in data["Value"]["GE"]:
            if kf["G"] == 1:
                for E in kf["E"]:
                    for item in E:
                        if item['T'] == 1:
                            P1 = item["C"]
                        if item['T'] == 3:
                            P2 = item["C"]
        if (not P1) or (not P2):
            print("hm3")
            print(P1)
            print(P2)
            return False
    except Exception as e:
        print("kek3")
        print(e)
        return False
    stats.update({"P1":str(P1),"P2":str(P2)})
    match_stats = {}
    match_stats_adv = {}
    for item in data["Value"]["SC"]["S"]:
        match_stats.update({item["Key"]:item["Value"]})
    for item in data["Value"]["SC"]["ST"][0]["Value"]:
        match_stats_adv.update({item["ID"]:{"S1":item["S1"],"S2":item["S2"]}})
    try:
        stats.update({"corners_1":match_stats["ICorner1"],"yellows_1":match_stats["IYellowCard1"],"reds_1":match_stats["IRedCard1"],"penalty_1":match_stats["IPenalty1"]})
        stats.update({"corners_2":match_stats["ICorner2"],"yellows_2":match_stats["IYellowCard2"],"reds_2":match_stats["IRedCard2"],"penalty_2":match_stats["IPenalty2"]})
        # first,second = map(lambda x: x.split(";"),match_stats["Stat"].split("-"))
        # stats.update({"attacks_1":first[0],"dang_attacks_1":first[1],"control_1":first[2],"good_hits_1":first[3],"hits_1":first[4]})
        # stats.update({"attacks_2":second[0],"dang_attacks_2":second[1],"control_2":second[2],"good_hits_2":second[3],"hits_2":second[4]})
        stats.update({"attacks_1":match_stats["Attacks1"],"dang_attacks_1":match_stats["DanAttacks1"],"control_1":match_stats_adv[29]["S1"],"good_hits_1":match_stats["ShotsOn1"],"hits_1":match_stats["ShotsOff1"]})
        stats.update({"attacks_2":match_stats["Attacks2"],"dang_attacks_2":match_stats["DanAttacks2"],"control_2":match_stats_adv[29]["S2"],"good_hits_2":match_stats["ShotsOn2"],"hits_2":match_stats["ShotsOff2"]})
    except Exception as e:
        return False
    if not(float(stats['P1'])>2.6 and float(stats['P2'])>2.6 and int(stats['good_hits_1']) < 4 and int(stats['good_hits_2']) < 4 and int(stats['hits_1'])<6 and int(stats['hits_2'])<6 and int(stats['corners_1'])<7 and int(stats['corners_2'])<7 and int(stats['good_hits_1'])+int(stats['good_hits_2'])+int(stats['hits_1'])+int(stats['hits_2'])+int(stats['corners_1'])+int(stats['corners_2'])>0):
        return False
    temperature = "Нет данных"
    try:
        temper_data = data["Value"]["MIS"]
        for tmp in temper_data:
            if tmp["K"] == 9:
                temperature = tmp["V"]
    except Exception as e:
        pass
    stats.update({"temperature":temperature})
    return stats

def getGoodStats():
    try:
        allStats = []
        # Проверка типа 0
        url = "https://1xstavka.ru/LiveFeed/Get1x2_VZip?sports=1&count=500&mode=4&country=1&partner=51&getEmpty=true"
        response = requests.get(url,verify=False, timeout = 30)
        data = json.loads(response.content)
        for item in data['Value']:
            stats = {}
            #print(item["O1"]+" "+item["O2"])
            #print(item["SC"]["PS"])
            try:
                time_s = item["SC"]["TS"]
            except:
                time_s = 0

            score_stats = {}
            for itm in item["SC"]["PS"]:
                score_stats.update({itm["Key"]:itm["Value"]})
            score_1 = 0
            score_2 = 0
            try:
                score_1 += score_stats[1]["S1"]
            except:
                pass
            try:
                score_1 += score_stats[2]["S1"]
            except:
                pass
            try:
                score_2 += score_stats[1]["S2"]
            except:
                pass
            try:
                score_2 += score_stats[2]["S2"]
            except:
                pass
            stats.update({"score_1":str(score_1),"score_2":str(score_2)})
            if time_s > 20*60-10 and time_s < 20*60+60 and score_1 == 0 and score_2 == 0:
                try:
                    matchStats = getStats(item["I"])
                except Exception as e:
                    print("looooooool")
                
                if matchStats:
                    stats.update(matchStats)
                    stats.update({"type":0,"name_1":item["O1"],"name_2":item["O2"],"league":item["L"],"time":str(time_s),"match_id":str(item["I"])})
                    allStats.append(stats)
        # Проверка типа 1 и 2      
        url = "https://1xstavka.ru/LiveFeed/Get1x2_VZip?sports=1&count=500&mode=4&country=1&partner=51&getEmpty=true"
        response = requests.get(url,verify=False, timeout = 30)
        data = json.loads(response.content)
        # print()
        for item in data['Value']:
            stats = {}
            #print(item["O1"]+" "+item["O2"])
            #print(item["SC"]["PS"])
            try:
                match_type = item["MIO"]['MaF']
            except:
                continue
            if match_type == "2х15":
                type_id = 1
            elif match_type == "2х12":
                type_id = 2
            else:
                continue

            try:
                time_s = item["SC"]["TS"]
            except:
                continue

            score_stats = {}
            for itm in item["SC"]["PS"]:
                score_stats.update({itm["Key"]:itm["Value"]})
            score_1 = 0
            score_2 = 0
            try:
                score_1 += score_stats[1]["S1"]
            except:
                pass
            try:
                score_1 += score_stats[2]["S1"]
            except:
                pass
            try:
                score_2 += score_stats[1]["S2"]
            except:
                pass
            try:
                score_2 += score_stats[2]["S2"]
            except:
                pass
            # print(item["O1"]+" "+item["O2"])
            # print(time_s)
            # print(score_1)
            # print(score_2)
            stats.update({"score_1":str(score_1),"score_2":str(score_2)})
            #  and score_1 == score_2
            if type_id == 1:
                if time_s > 26*60-10 and time_s < 26*60+60 and score_1 == score_2:
                    stats.update({"type":type_id,"name_1":item["O1"],"name_2":item["O2"],"league":item["L"],"time":str(time_s),"match_id":str(item["I"])})
                    allStats.append(stats)
            elif type_id == 2:
                if time_s > 20*60-10 and time_s < 20*60+60 and score_1 == score_2:
                    stats.update({"type":type_id,"name_1":item["O1"],"name_2":item["O2"],"league":item["L"],"time":str(time_s),"match_id":str(item["I"])})
                    allStats.append(stats)

        # Проверка типа 3
        url = "https://1xstavka.ru/LiveFeed/Get1x2_VZip?sports=1&count=500&mode=4&country=1&partner=51&getEmpty=true"
        response = requests.get(url,verify=False, timeout = 30)
        data = json.loads(response.content)
        for item in data['Value']:
            stats = {}
            score_stats = {}
            try:
                time_s = item["SC"]["TS"]
            except:
                continue
            for itm in item["SC"]["PS"]:
                score_stats.update({itm["Key"]:itm["Value"]})
            score_1 = 0
            score_2 = 0
            try:
                score_1 += score_stats[1]["S1"]
            except:
                pass
            try:
                score_1 += score_stats[2]["S1"]
            except:
                pass
            try:
                score_2 += score_stats[1]["S2"]
            except:
                pass
            try:
                score_2 += score_stats[2]["S2"]
            except:
                pass
            stats.update({"score_1":str(score_1),"score_2":str(score_2)})
            # and score_1 == 1 and score_2 == 1
            if time_s > 68*60 and time_s < 73*60 and score_1 == 1 and score_2 == 1:
                try:
                    matchStats = getStats3(item["I"])
                except Exception as e:
                    print("looooooool3")
                
                if matchStats:
                    stats.update(matchStats)
                    stats.update({"type":3,"name_1":item["O1"],"name_2":item["O2"],"league":item["L"],"time":str(time_s),"match_id":str(item["I"])})
                    allStats.append(stats)
        return(allStats)
    except:
        return[]
    
