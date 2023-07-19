#!/usr/bin/env python
#-*- coding: utf-8 -*-
from fabric.api import *
from fabric.contrib import files
from fabric.contrib.console import confirm
from fabric.colors import red, green
import time
import os
import json
import random
import sys
import string

from datetime import date
import pytz, datetime

reload(sys)
sys.setdefaultencoding('utf8')

env.user = 'ec2-user'
env.key_filename = '~/.lost/superchameleon.pem'
env.roledefs = {
	'game_1' : ['52.9.26.155'],
	'game_ptr' : ['gateway-lost-pre.super-chameleon.com'],
	'mysql' : ['52.52.191.63'],
	'clickhouse' : ['35.171.15.48'],
	'gm' : ['34.236.42.247'],
	'ob' : ['13.52.168.221']
}

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
	run('sudo jcmd `ps aux | grep \'AllApp game\' |grep -v grep|awk \'{print $2}\'` JFR.start name=online settings=profile filename=/tmp/online.jfr duration=%ss' % (duration))	




SQL = '''
	select now()
'''

@roles('mysql')
def mysql(sql=SQL):
	run("sudo /home/elex/mysql/bin/mysql lost_game_1 -e '%s\\G'" % (sql))

@roles('mysql')
def player(playerID):
	mysql('select * from player where playerID = "%s" or name = "%s" or uid = "%s"' % (playerID, playerID, playerID))
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
def actionSQL2(playerID, date1, date2, key):
	clickhouse("select toDateTime(timestamp/1000),action,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15 from lognew_all where logdate between '%s' and '%s' and f1='%s' and action in (%s) order by timestamp" % (date1, date2, playerID, key))





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
	with cd('/data/htdocs/lostWeb/action_log'):
		run('awk -F, \'/%s/ { t=strftime("%%Y-%%m-%%d %%H:%%M:%%S", $5); print t,$0 }\' ./act_%s*' % (deviceID, date))

