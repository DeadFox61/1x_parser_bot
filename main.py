import telebot
from emoji import emojize
import MySQLdb
import time
from threading import Thread
import parser_ft


bot = telebot.TeleBot("1111111111:AAAAAAAAA" , threaded=False)
	


def check_and_send():
	conn = MySQLdb.connect('localhost', 'non-root', '123', 'parser_foot')
	cursor = conn.cursor()
	conn.set_character_set('utf8')
	cursor.execute("SELECT `match_id`, `league`, `name_1`, `name_2`, `time`, `score_1`, `score_2`, `P1`, `P2`, `attacks_1`, `attacks_2`, `dang_attacks_1`, `dang_attacks_2`, `control_1`, `control_2`, `good_hits_1`, `good_hits_2`, `hits_1`, `hits_2`, `corners_1`, `corners_2`, `reds_1`, `reds_2`, `yellows_1`, `yellows_2`, `penalty_1`, `penalty_2`, `total`, `temperature`, `type` FROM stats WHERE `is_sended` = 0")
	allStats = cursor.fetchall()
	for stats in allStats:
		send_stats(stats)
		cursor.execute("UPDATE `stats` Set `is_sended` = 1 WHERE `match_id` = "+str(stats[0]) )
		conn.commit()
	cursor.close()
	conn.close()
def send_stats(stats):
	conn = MySQLdb.connect('localhost', 'non-root', '123', 'parser_foot')
	cursor = conn.cursor()
	conn.set_character_set('utf8')
	cursor.execute("SELECT `user_id`, `types` FROM users WHERE `is_active` = 1")
	users = cursor.fetchall()
	for user in users:
		if stats[29] == 0:
			if "0" in user[1].split():
				bot.send_message(user[0], emojize(""":soccer: """+stats[1]+""" 

*"""+stats[2]+"""* :zero:::zero: *"""+stats[3]+"""* | :stopwatch: 20'

*Коэффициенты:*
ТМ 0.5 первого тайма ("""+str(stats[27])+""")
П1 первого тайма ("""+str(stats[7])+""")
П2 первого тайма ("""+str(stats[8])+""")

*Статистика:*
Атаки: """+str(stats[9])+""" - """+str(stats[10])+"""
Опасные атаки: """+str(stats[11])+""" - """+str(stats[12])+"""
Удары в створ: """+str(stats[15])+""" - """+str(stats[16])+"""
Удары мимо: """+str(stats[17])+""" - """+str(stats[18])+"""
Угловые: """+str(stats[19])+""" - """+str(stats[20])+"""
Владение мячом: """+str(stats[13])+"""% - """+str(stats[14])+"""%
Жёлтые карточки: """+str(stats[23])+""" - """+str(stats[24])+"""
Красные карточки: """+str(stats[21])+""" - """+str(stats[22])+"""
Температура: """+stats[28]+""" """, use_aliases=True), parse_mode="Markdown")
		elif stats[29] == 1:
			if "1" in user[1].split():
				bot.send_message(user[0], emojize(""":soccer: """+stats[1]+""" 
2x15
*"""+stats[2]+"""* """+str(stats[5])+""":"""+str(stats[6])+""" *"""+stats[3]+"""* | :stopwatch: 26'
""", use_aliases=True), parse_mode="Markdown")
		elif stats[29] == 2:
			if "2" in user[1].split():
				bot.send_message(user[0], emojize(""":soccer: """+stats[1]+""" 
2x12
*"""+stats[2]+"""* """+str(stats[5])+""":"""+str(stats[6])+""" *"""+stats[3]+"""* | :stopwatch: 20'
""", use_aliases=True), parse_mode="Markdown")
		elif stats[29] == 3:
			if "3" in user[1].split():
				bot.send_message(user[0], emojize(""":soccer: """+stats[1]+""" 

*"""+stats[2]+"""* :one:::one: *"""+stats[3]+"""* | :stopwatch: """+str(stats[4]//60)+"""'

*Коэффициенты:*
П1 ("""+str(stats[7])+""")
П2 ("""+str(stats[8])+""")

*Статистика:*
Атаки: """+str(stats[9])+""" - """+str(stats[10])+"""
Опасные атаки: """+str(stats[11])+""" - """+str(stats[12])+"""
Удары в створ: """+str(stats[15])+""" - """+str(stats[16])+"""
Удары мимо: """+str(stats[17])+""" - """+str(stats[18])+"""
Угловые: """+str(stats[19])+""" - """+str(stats[20])+"""
Владение мячом: """+str(stats[13])+"""% - """+str(stats[14])+"""%
Жёлтые карточки: """+str(stats[23])+""" - """+str(stats[24])+"""
Красные карточки: """+str(stats[21])+""" - """+str(stats[22])+"""
Температура: """+stats[28]+""" """, use_aliases=True), parse_mode="Markdown")
	cursor.close()
	conn.close()
def inf_check_and_send():
	while True:
		try:
			check_and_send()
		except Exception as e:
			print(e)
		time.sleep(2)
def inf_parse():
	while True:
		try:
			goodStats = parser_ft.getGoodStats()
			if goodStats:
				conn = MySQLdb.connect('localhost', 'non-root', '123', 'parser_foot')
				cursor = conn.cursor()
				conn.set_character_set('utf8')
				for stats in goodStats:
					if stats["type"] == 0:
						query = "INSERT IGNORE INTO `stats`(`match_id`, `league`, `name_1`, `name_2`, `time`, `score_1`, `score_2`, `P1`, `P2`, `attacks_1`, `attacks_2`, `dang_attacks_1`, `dang_attacks_2`, `control_1`, `control_2`, `good_hits_1`, `good_hits_2`, `hits_1`, `hits_2`, `corners_1`, `corners_2`, `reds_1`, `reds_2`, `yellows_1`, `yellows_2`, `penalty_1`, `penalty_2`, `total`, `temperature`) VALUES ("+stats['match_id']+", '"+stats['league']+"', '"+stats['name_1']+"', '"+stats['name_2']+"', "+stats['time']+", "+str(stats['score_1'])+", "+str(stats['score_2'])+", "+stats['P1']+", "+stats['P2']+", "+stats['attacks_1']+", "+stats['attacks_2']+", "+stats['dang_attacks_1']+", "+stats['dang_attacks_2']+", "+stats['control_1']+", "+stats['control_2']+", "+stats['good_hits_1']+", "+stats['good_hits_2']+", "+stats['hits_1']+", "+stats['hits_2']+", "+stats['corners_1']+", "+stats['corners_2']+", "+stats['reds_1']+", "+stats['reds_2']+", "+stats['yellows_1']+", "+stats['yellows_2']+", "+stats['penalty_1']+", "+stats['penalty_2']+", "+stats['total']+", '"+stats['temperature']+"')"
						cursor.execute(query) 
						conn.commit()
					elif stats["type"] == 1 or stats["type"] == 2:
						# print(stats)
						query = "INSERT IGNORE INTO `stats`(`match_id`, `league`, `name_1`, `name_2`, `time`, `score_1`, `score_2`, `type`) VALUES ("+stats['match_id']+", '"+stats['league']+"', '"+stats['name_1']+"', '"+stats['name_2']+"', "+stats['time']+", "+stats['score_1']+", "+stats['score_2']+", "+str(stats["type"])+")"
						cursor.execute(query) 
						conn.commit()
					elif stats["type"] == 3:
						query = "INSERT IGNORE INTO `stats`(`match_id`, `league`, `name_1`, `name_2`, `time`, `score_1`, `score_2`, `P1`, `P2`, `attacks_1`, `attacks_2`, `dang_attacks_1`, `dang_attacks_2`, `control_1`, `control_2`, `good_hits_1`, `good_hits_2`, `hits_1`, `hits_2`, `corners_1`, `corners_2`, `reds_1`, `reds_2`, `yellows_1`, `yellows_2`, `penalty_1`, `penalty_2`, `temperature`, `type`) VALUES ("+stats['match_id']+", '"+stats['league']+"', '"+stats['name_1']+"', '"+stats['name_2']+"', "+stats['time']+", "+stats['score_1']+", "+stats['score_2']+", "+stats['P1']+", "+stats['P2']+", "+stats['attacks_1']+", "+stats['attacks_2']+", "+stats['dang_attacks_1']+", "+stats['dang_attacks_2']+", "+stats['control_1']+", "+stats['control_2']+", "+stats['good_hits_1']+", "+stats['good_hits_2']+", "+stats['hits_1']+", "+stats['hits_2']+", "+stats['corners_1']+", "+stats['corners_2']+", "+stats['reds_1']+", "+stats['reds_2']+", "+stats['yellows_1']+", "+stats['yellows_2']+", "+stats['penalty_1']+", "+stats['penalty_2']+", '"+stats['temperature']+"', "+str(stats["type"])+")"
						cursor.execute(query) 
						conn.commit()
				cursor.close()
				conn.close()
		except Exception as e:
			print(e)
		time.sleep(10)
inf_tr_pr = Thread(target=inf_parse) 
inf_tr = Thread(target=inf_check_and_send)
inf_tr_pr.start()
inf_tr.start()
# bot.infinity_polling(True)