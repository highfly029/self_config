#!/usr/bin/env python
#-*- coding: utf-8 -*-

configfile = '/Users/hedley/.lost/fab/lost_constant'
import os
import sys

sys.path.append(os.path.dirname(os.path.expanduser(configfile)))


from fabric.api import *
from fabric.contrib import files
from fabric.contrib.console import confirm
from fabric.colors import red, green
import time
import json
import random
import string
import lost_constant


from datetime import date
import pytz, datetime

reload(sys)
sys.setdefaultencoding('utf8')


# 2020-01-01
d1 = datetime.datetime.utcnow().strftime("%Y-%m-%d")


@roles('game_1', 'ob')
def hotVersion(version):
	run('egrep "\\s+<clientResVersionCode" /home/lost/serverConfig/setting.xml')
	run('sudo sed -i \'/clientResVersionCode/ {s#".*"#"%s"#}\' /home/lost/serverConfig/setting.xml' % (version))

@roles('game_ptr')
def hotVersionPtr(version):
	run('egrep "\\s+<clientResVersionCode" /home/lost/serverConfig/setting.xml')
	run('sed -i \'/clientResVersionCode/ {s#".*"#"%s"#}\' /home/lost/serverConfig/setting.xml' % (version))

@roles('game_1')
def jfr(duration):
	run('sudo jcmd `ps aux | grep \'game.jar game\' |grep -v grep|awk \'{print $2}\'` JFR.start name=online settings=profile filename=/tmp/online.jfr duration=%ss' % (duration))	




SQL = '''
	select now()
'''

@roles('mysql')
def mysql(sql=SQL):
	run("database=`sudo /home/elex/mysql/bin/mysql -e 'show databases\\G' | grep ' lost_game' | cut -d ':' -f 2` && sudo /home/elex/mysql/bin/mysql $database -e '%s\\G'" % (sql))

@roles('mysql')
def player(playerID):
	mysql('select * from player where playerID = %s' % (playerID))
	mysql('select * from rolesocial where playerID = %s' % (playerID))

@roles('mysql')
def roleGroup(groupID):
	mysql('select * from rolegroup where groupID = %s' % (groupID))

@roles('mysql')
def statUser(deviceID):
	mysql('select user_id,pay_total,country,channel,model,reg_cv,last_cv,from_unixtime(reg_time/1000) as reg_time,from_unixtime(last_login/1000) as last_login from stat_user where device_id = "%s" or user_id = "%s" ' % (deviceID, deviceID))


SQL_CH = '''
	select now()
'''

@roles('clickhouse')
def clickhouse(sql=SQL_CH):
	run('sudo clickhouse-client --host=172.31.74.5 --database=stat_allserver --query="%s"' % (sql))

@roles('clickhouse')
def actionSQL(playerID, date1, date2):
	clickhouse("select toDateTime(timestamp/1000),action,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15 from lognew_all where logdate between '%s' and '%s' and f1='%s'" % (date1, date2, playerID))

@roles('clickhouse')
def inoutSQL(playerID, date1, date2):
	clickhouse("select toDateTime(timestamp/1000),action,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15 from lognew_all where logdate between '%s' and '%s' and f1='%s' and (action='loginWay' or action='disconnect') order by timestamp" % (date1, date2, playerID))

@roles('clickhouse')	
def switchSQL(playerID, date1, date2):
	clickhouse("select toDateTime(timestamp/1000),action,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15 from lognew_all where logdate between '%s' and '%s' and f1='%s' and action in ('playerStartSwitchGame', 'playerSwitchGame', 'playerSwitchBackGame') order by timestamp" % (date1, date2, playerID))

@roles('clickhouse')
def actionSQL2(playerID, date1, date2, key):
	clickhouse("select toDateTime(timestamp/1000),action,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15 from lognew_all where logdate between '%s' and '%s' and f1='%s' and action in (%s) order by timestamp" % (date1, date2, playerID, key))



@roles('clickhouse')
def unicornLog(playerID, date, beginTime, endTime):
	filename=date + "_" + playerID + ".csv"

	#全LOG单小时
	# clickhouseBi1(filename, "select toDateTime(timestamp/1000) time, concat('_', toString(timestamp_recv-timestamp), '_', toString(timestamp_recv-if(ep_ClientTimeStamp>0,ep_ClientTimeStamp,toInt64(timestamp_recv))), '_') _cg_cs_, up_nowServerid serverID, * from ods_event_all where logdate='%s' and (uid='%s' or device_id='%s') and timestamp between %d and %d order by timestamp/1000, session_id, session_seq" % (date, playerID, playerID, long(beginTime)*1000, long(endTime)*1000))

	#全LOG全天
	# clickhouseBi1(filename, "select toDateTime(timestamp/1000) time, concat('_', toString(timestamp_recv-timestamp), '_', toString(timestamp_recv-if(ep_ClientTimeStamp>0,ep_ClientTimeStamp,toInt64(timestamp_recv))), '_') _cg_cs_, up_nowServerid serverID, * from ods_event_all where logdate='%s' and (uid='%s' or device_id='%s') order by timestamp/1000, session_id, session_seq" % (date, playerID, playerID))

	#客户端LOG单小时
	# clickhouseBi1(filename, "select toDateTime(timestamp/1000) time, concat('_', toString(timestamp_recv-timestamp), '_', toString(timestamp_recv-if(ep_ClientTimeStamp>0,ep_ClientTimeStamp,toInt64(timestamp_recv))), '_') _cg_cs_, up_nowServerid serverID, * from ods_event_all where logdate='%s' and  device_id='%s' and source_id='2' and timestamp between %d and %d order by timestamp, session_id, session_seq" % (date, playerID, long(beginTime)*1000, long(endTime)*1000))

	#客户端LOG全天
	clickhouseBi1(filename, "select toDateTime(timestamp/1000) time, concat('_', toString(timestamp_recv-timestamp), '_', toString(timestamp_recv-if(ep_ClientTimeStamp>0,ep_ClientTimeStamp,toInt64(timestamp_recv))), '_') _cg_cs_, up_nowServerid serverID, * from ods_event_all where logdate='%s' and  device_id='%s' and source_id='2' order by timestamp, session_id, session_seq" % (date, playerID))


def clickhouseBi1(filename, sql=SQL_CH):
	run('sudo clickhouse-client --host=172.34.6.84 --database=bi_1 --query="%s" --format CSVWithNames > /tmp/%s ' % (sql, filename))
	get('/tmp/%s' % (filename), '~/.lost/.log/%s' % (filename))





@roles('gm')
def exceptionStack(playerID, date):
	with cd('/data/scribe_log/errorLog'):
		run('sudo awk \'BEGIN{RS="-------------------------------------------";ORS="\\\\n"} /%s/\' ./errorLog-%s* ' % (playerID, date))

@roles('gm')
def actionNative(playerID, date):	
	with cd('/data/scribe_log/actionLog'):
		run('awk \'/%s/ { if($1=="action") {$1=""; $2=""; $3=strftime("%%Y-%%m-%%d %%H:%%M:%%S", $3/1000);} else { $1="--  "$1 } print $0}\' ./actionLog-%s* ' % (playerID, date))

@roles('gm')
def actionClient(deviceID, date):
	with cd('/data/scribe_log/client_log/'):
		run('awk -F, \'/%s/ { t=strftime("%%Y-%%m-%%d %%H:%%M:%%S", $5); if($NF>0) {t2="_"$5-int($NF/1000)"_"} else {t2="_N_"} print t,t2,$0 }\' ./client_log-%s*' % (deviceID, date))



@parallel(pool_size=100)
@roles('production')
# @roles('login')
# @roles('ob_production')
# @roles('mysql_slave')
# @roles('mysql')
def xx():
	# put('./clean_log.sh', '/tmp/')
	put('./xx.sh', '/tmp/')
	# put('./xx.sql', '/tmp/')
	# put('/Users/hedley/.lost/py/boot/userparameter_jvm.conf', '/tmp/')
	# put('/Users/hedley/.lost/py/boot/parsePush.properties', '/tmp/')
	run('chmod 777 /tmp/xx.sh && sudo /tmp/xx.sh')



