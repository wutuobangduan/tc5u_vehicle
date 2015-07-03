# -*- coding: utf-8 -*-
#!/usr/bin/env python
# encoding: utf-8

import chardet
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import simplejson as json




def update_vehicle_model():
    try:
        for i in xrange(10000,17000):
            vehicle_level,gearbox_gear,emission_value,emission_code,transmission,transmission_int,vehicle_level_int = None,None,None,None,None,None,None

            conn = MySQLdb.connect(host='192.168.2.231',user='root',passwd='dp',charset='utf8')
            curs = conn.cursor()
            conn.select_db('tc_platform')
            curs.execute("select spec_value from tc_vehicle_model where vehicle_model_id=%s" % i)
            get_spec_value = curs.fetchone()
            if not get_spec_value:
                continue
            else:
                #print type(get_spec_value[0])
                spec_value = str(get_spec_value[0])[1:-1]
                #print chardet.detect(spec_value)
                #print json.loads(str(get_spec_value[0])[1:-1])
            try:
                json_spec_value = json.loads(spec_value)
            except:
                continue
            for j in range(len(json_spec_value['attr'])):
                if json_spec_value['attr'][j]['name'] == '挡位个数':
                    try:
                        gearbox_gear = json_spec_value['attr'][j]['vname']
                    except:
                        print "vname attr is not exist..."
                elif json_spec_value['attr'][j]['name'] == '变速箱类型':
                    try:
                        transmission = json_spec_value['attr'][j]['vname']
                    except:
                        print "vname attr is not exist..."
                elif json_spec_value['attr'][j]['name'] == '排量(L)':
                    try:
                        emission_code = json_spec_value['attr'][j]['vname']
                    except:
                        print "vname attr is not exist..."
                elif json_spec_value['attr'][j]['name'] == '排量(mL)':
                    try:
                        emission_value = json_spec_value['attr'][j]['vname']
                    except:
                        print "vname attr is not exist..."
                elif json_spec_value['attr'][j]['name'] == '级别':
                    try:
                        vehicle_level = json_spec_value['attr'][j]['vname']
                    except:
                        print "vname attr is not exist..."
            if gearbox_gear and transmission and emission_code and emission_value:
                print gearbox_gear,transmission,emission_code,emission_value,vehicle_level,i
                #print type(vehicle_level)
                if vehicle_level == '微型车':
                    vehicle_level_int = 1
                elif vehicle_level == '小型车':
                    vehicle_level_int = 2
                elif vehicle_level == '紧凑型车':
                    vehicle_level_int = 3
                elif vehicle_level == '中型车':
                    vehicle_level_int = 4
                elif vehicle_level == '大型车':
                    vehicle_level_int = 5
                elif vehicle_level == '豪华型车':
                    vehicle_level_int = 6
                elif vehicle_level == '跑车':
                    vehicle_level_int = 7
                elif vehicle_level == 'MPV':
                    vehicle_level_int = 8
                elif vehicle_level == 'SUV':
                    vehicle_level_int = 10
                elif vehicle_level == '小型SUV':
                    vehicle_level_int = 11
                elif vehicle_level == '紧凑型SUV':
                    vehicle_level_int = 12

                elif vehicle_level == '中型SUV':
                    vehicle_level_int = 13
                elif vehicle_level == '中大型SUV':
                    vehicle_level_int = 14
                elif vehicle_level == '大型SUV':
                    vehicle_level_int = 15
                elif vehicle_level == '商用车':
                    vehicle_level_int = 20
                elif vehicle_level == '皮卡':
                    vehicle_level_int = 21
                elif vehicle_level == '微卡':
                    vehicle_level_int = 22
                elif vehicle_level == '微面':
                    vehicle_level_int = 23
                elif vehicle_level == '轻客':
                    vehicle_level_int = 24
                #print vehicle_level_int
                if '手动' in transmission:
                    transmission_int = 1
                elif '自动' in transmission:
                    transmission_int = 2
                elif '手自一体' in transmission:
                    transmission_int = 3
                else:
                    transmission_int = 0
                if gearbox_gear == '-':
                    gearbox_gear = None
                if emission_code == '-':
                    emission_code = None
                if emission_value == '-':
                    emission_value = None
                if gearbox_gear is None or len(gearbox_gear)>2:
                    gearbox_gear = 0
                res = [transmission_int,gearbox_gear,vehicle_level_int,emission_code,emission_value,i]
                curs.execute("update tc_vehicle_model set gearbox_type=%s,gearbox_gear=%s,vehicle_level=%s,emission_code=%s,emission_value=%s where vehicle_model_id=%s",res)
            conn.commit()
            curs.close()
            conn.close()
    except MySQLdb.Error,e:
        print "Error %d %s" % (e.args[0],e.args[1])
        sys.exit(1)

if __name__=="__main__":
    update_vehicle_model()
