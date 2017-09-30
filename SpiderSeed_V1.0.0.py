import cx_Oracle
import os
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
import threading
import time
import math

pzsd = "http://202.127.42.47:6010/SDSite/Home/Index"       #品种审定
pzbh = "http://202.127.42.47:6009/Home/BigDataIndex"       #品种保护
zxkz = "http://202.127.42.47:6010/XKSite/Home/Index"       #种子生产经营许可
pzdj = "http://202.127.42.47:6010/index.aspx"              #品种登记
pztg = "http://202.127.42.47:6006/Home/BigDataIndex"       #品种推广
zzjk = "http://202.127.42.47:6010/jcksite/home/SeedImport" #种子进口
zzck = "http://202.127.42.47:6010/jcksite/home/SeedExport" #种子出口
zzcb = "http://202.127.42.47:6010/zzcb/home/bigdataindex"  #种子储备
global databases #数据库连接常量
sleepTime = 1 #网页加载等待时间

percent1 = ""
percent2 = ""
percent3 = ""
percent4 = ""
percent5 = ""
percent6 = ""
percent7 = ""
percent8 = ""
percent9 = ""
percent10 = ""
overtime1 = ""
overtime2 = ""
overtime3 = ""
overtime4 = ""
overtime5 = ""
overtime6 = ""
overtime7 = ""
overtime8 = ""
overtime9 = ""
overtime10 = ""

def changeTime(allTime): #秒转换成时间
    day = 24*60*60
    hour = 60*60
    min = 60
    if allTime <60:        
        return  "%d sec"%math.ceil(allTime)
    elif  allTime > day:
        days = divmod(allTime,day) 
        return "%d days, %s"%(int(days[0]),changeTime(days[1]))
    elif allTime > hour:
        hours = divmod(allTime,hour)
        return '%d hours, %s'%(int(hours[0]),changeTime(hours[1]))
    else:
        mins = divmod(allTime,min)
        return "%d mins, %d sec"%(int(mins[0]),math.ceil(mins[1]))

def getSubjectBasicData():     #获取产品审定基本数据
    global approval_number     #(审定编号)
    global cultivar_name       #(品种名称)
    global year                #(年份)
    global crop_name           #(作物名称)
    global authorized_unit     #(审定单位)
    global transgene           #(是否转基因)
    global applicant_unit      #(申请单位)
    global count
    driver = webdriver.PhantomJS()
    driver.get(pzsd) 
    time.sleep(sleepTime)
    try:
        count = int(driver.find_element_by_id('sp_1_gridPager').text.replace(' ',''))
    except:
        print('审定基本数据 -> 与网站建立连接失败.请重启程序.')
        exit()
    num = 0
    second = 0
    while num<count:
        start = datetime.now()
        num = num + 1
        #print('审定基本数据 -> 目前进度: ',num,'页.  共:',count,'页.  百分比:',((num/count)*100),'%')
        #if second!= 0 : print('审定基本数据 -> 预计',changeTime(second),'后完成.')
        global percent1
        global overtime1
        percent1 = str((num/count)*100)+"%"
        overtime1 = "剩余"+changeTime(second)
        dirver1 = driver.find_element_by_id('gridList').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')#定位
        for it in dirver1:  
            try:
                approval_number = ""
                cultivar_name = ""   
                year = "" 
                crop_name = ""    
                authorized_unit = ""  
                transgene = "" 
                applicant_unit = ""   
                dirver2 = it.find_elements_by_tag_name('td')
                approval_number = dirver2[0].text
                if len(approval_number) == 0 : continue
                cultivar_name = dirver2[1].text
                year = dirver2[2].text
                crop_name = dirver2[3].text
                authorized_unit = dirver2[4].text
                transgene = dirver2[5].text
                applicant_unit = dirver2[6].text
                try:
                    cursor = databases.cursor()
                    sql_select = "select approval_number from SUBJECT_BASIC_DATA where approval_number like '"+approval_number+"'"
                    sql_insert = "insert into SUBJECT_BASIC_DATA(approval_number,cultivar_name,year,crop_name,authorized_unit,transgene,applicant_unit) values('"+approval_number+"','"+cultivar_name+"','"+year+"','"+crop_name+"','"+authorized_unit+"','"+transgene+"','"+applicant_unit+"')"
                    sql_updata = "update SUBJECT_BASIC_DATA set approval_number='"+approval_number+"',cultivar_name='"+cultivar_name+"',year='"+year+"',crop_name='"+crop_name+"',authorized_unit='"+authorized_unit+"',transgene='"+transgene+"',applicant_unit='"+applicant_unit+"' where approval_number like '"+approval_number+"'"
                    cursor.execute(sql_select)
                    result=cursor.fetchall()
                    if len(result)>0: 
                        cursor.execute(sql_updata)
                        cursor.close()
                        databases.commit()
                    else:
                        cursor.execute(sql_insert)
                        cursor.close()
                        databases.commit()
                except:
                    print("审定基本数据 -> 数据添加错误,这可能是字段中存在<''>等字符导致的.")
            except:
                print('审定基本数据 -> 一条数据错误,这可能是网络原因导致的.')
        driver.find_element_by_id('next_gridPager').click()
        time.sleep(sleepTime*2)
        end = datetime.now()
        second = ((end-start).seconds)*(count-num)

def getApprovalNumberDetails():   #获取审定编号详情
    global subject_number         #(所属审定编号)
    global applicant              #(申请者)
    global breeders               #(育种者)
    global breed_origin           #(品种来源)
    global characteristic         #(特征特性)
    global yield_performance      #(产量表现)
    global cultivation_techniques #(栽培技术要点)
    global approval_opinion       #(审定意见)
    global count
    driver = webdriver.PhantomJS()
    driver.get(pzsd) 
    time.sleep(sleepTime)
    try:
        count = int(driver.find_element_by_id('sp_1_gridPager').text.replace(' ',''))
    except:
        print('品种推广详情 -> 与网站建立连接失败.请重启程序.')
        exit()
    num = 0
    second = 0
    while num<count:
        start = datetime.now()
        num = num + 1
        #print('审定编号详情 -> 目前进度: ',num,'页.  共:',count,'页.  百分比:',((num/count)*100),'%')
        #if second!= 0 : print('审定编号详情 -> 预计',changeTime(second),'后完成.')
        global percent2
        global overtime2
        percent2 = str((num/count)*100)+"%"
        overtime2 = "剩余"+changeTime(second)
        dirver1 = driver.find_element_by_id('gridList').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')#定位
        for it in dirver1:  
            try:
                dirver2 = it.find_elements_by_tag_name('a')
                for it1 in dirver2:                         
                    it1.click()                             
                    time.sleep(sleepTime)
                    if it1.get_attribute('onclick')[0] == 'G' :
                        subject_number = ""
                        applicant = ""
                        breeders = ""
                        breed_origin = ""
                        characteristic = ""
                        yield_performance = ""
                        cultivation_techniques = ""
                        approval_opinion = ""
                        child = driver.find_element_by_id('Announcementlist').find_elements_by_tag_name('tr')
                        child1 = child[0].find_elements_by_tag_name('td')
                        subject_number = child1[1].text
                        if len(subject_number) == 0: continue
                        child2 = child[3].find_elements_by_tag_name('td')
                        applicant = child2[1].text
                        child3 = child[4].find_elements_by_tag_name('td')
                        breeders = child3[1].text
                        child4 = child[5].find_elements_by_tag_name('td')
                        breed_origin = child4[1].text
                        child5 = child[6].find_elements_by_tag_name('td')
                        characteristic = child5[1].text
                        child6 = child[7].find_elements_by_tag_name('td')
                        yield_performance = child6[1].text
                        child7 = child[8].find_elements_by_tag_name('td')
                        cultivation_techniques = child7[1].text
                        child8 = child[9].find_elements_by_tag_name('td')
                        approval_opinion = child8[1].text
                        try:
                            cursor = databases.cursor()
                            sql_select = "select subject_number from APPROVAL_NUMBER_DETAILS where subject_number like '"+subject_number+"'"
                            sql_insert = "insert into APPROVAL_NUMBER_DETAILS(subject_number,applicant,breeders,breed_origin,characteristic,yield_performance,cultivation_techniques,approval_opinion) values('"+subject_number+"','"+applicant+"','"+breeders+"','"+breed_origin+"','"+characteristic+"','"+yield_performance+"','"+cultivation_techniques+"','"+approval_opinion+"')"
                            sql_updata = "update APPROVAL_NUMBER_DETAILS set subject_number='"+subject_number+"',applicant='"+applicant+"',breeders='"+breeders+"',breed_origin='"+breed_origin+"',characteristic='"+characteristic+"',yield_performance='"+yield_performance+"',cultivation_techniques='"+cultivation_techniques+"',approval_opinion='"+approval_opinion+"' where subject_number like '"+subject_number+"'"
                            cursor.execute(sql_select)
                            result=cursor.fetchall()
                            if len(result)>0: 
                                cursor.execute(sql_updata)
                                cursor.close()
                                databases.commit()
                            else:
                                cursor.execute(sql_insert)
                                cursor.close()
                                databases.commit()
                        except:
                            print("审定编号详情 -> 数据添加错误,这可能是字段中存在<''>等字符导致的.")
            except:
                print('审定编号详情 -> 一条数据错误,这可能是网络原因导致的.')
        driver.find_element_by_id('next_gridPager').click()
        time.sleep(sleepTime*2)
        end = datetime.now()
        second = ((end-start).seconds)*(count-num)

def getVarietyLicensingDetails(): #获取品种授权详情
    global variety                #(品种名称)
    global application_number     #(申请号)
    global filing_day             #(申请日)
    global applicant              #(申请人)
    global application_status     #(申请状态)
    global application_notice_date#(申请公告日)
    global authorization_number   #(授权号)
    global authorization_day      #(授权日)
    global announcement_number    #(公告号)
    global variety_rights_holder  #(品种权人)
    global variety_rights_address #(品种权地址)
    global count
    driver = webdriver.PhantomJS()
    driver.get(pzsd) 
    time.sleep(sleepTime)
    try:
        count = int(driver.find_element_by_id('sp_1_gridPager').text.replace(' ',''))
    except:
        print('品种推广详情 -> 与网站建立连接失败.请重启程序.')
        exit()
    num = 0
    second = 0
    while num<count:
        start = datetime.now()
        num = num + 1
        #print('品种授权详情 -> 目前进度: ',num,'页.  共:',count,'页.  百分比:',((num/count)*100),'%')
        #if second!= 0 : print('品种授权详情 -> 预计',changeTime(second),'后完成.')
        global percent3
        global overtime3
        percent3 = str((num/count)*100)+"%"
        overtime3 = "剩余"+changeTime(second)
        dirver1 = driver.find_element_by_id('gridList').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')#定位
        for it in dirver1:  
            try:
                dirver2 = it.find_elements_by_tag_name('a')
                for it1 in dirver2:                         
                    it1.click()                             
                    time.sleep(sleepTime)
                    if it1.get_attribute('onclick')[13] == 'a' :
                        child = driver.find_element_by_id('grantlist').find_elements_by_tag_name('tr')
                        variety = ""
                        application_number = ""
                        filing_day = ""
                        applicant = "" 
                        application_status = "" 
                        application_notice_date = "" 
                        authorization_number = ""
                        authorization_day = "" 
                        announcement_number = "" 
                        variety_rights_holder = "" 
                        variety_rights_address = ""
                        child1 = child[1].find_elements_by_tag_name('td')
                        variety = child1[1].text
                        if len(variety) == 0: continue
                        child2 = child[2].find_elements_by_tag_name('td')
                        application_number = child2[1].text
                        child3 = child[3].find_elements_by_tag_name('td')
                        filing_day = child3[1].text
                        child4 = child[4].find_elements_by_tag_name('td')
                        applicant = child4[1].text
                        child5 = child[5].find_elements_by_tag_name('td')
                        application_status = child5[1].text
                        child6 = child[6].find_elements_by_tag_name('td')
                        application_notice_date = child6[1].text
                        child7 = child[7].find_elements_by_tag_name('td')
                        authorization_number = child7[1].text
                        child8 = child[8].find_elements_by_tag_name('td')
                        authorization_day = child8[1].text
                        child9 = child[9].find_elements_by_tag_name('td')
                        announcement_number = child9[1].text
                        child10 = child[10].find_elements_by_tag_name('td')
                        variety_rights_holder = child10[1].text
                        child11 = child[11].find_elements_by_tag_name('td')
                        variety_rights_address = child11[1].text
                        try:
                            cursor = databases.cursor()
                            sql_select = "select variety from VARIETY_LICENSING_DETAILS where variety like '"+variety+"'"
                            sql_insert = "insert into VARIETY_LICENSING_DETAILS(variety,application_number,filing_day,applicant,application_status,application_notice_date,authorization_number,authorization_day,announcement_number,variety_rights_holder,variety_rights_address) values('"+variety+"','"+application_number+"','"+filing_day+"','"+applicant+"','"+application_status+"','"+application_notice_date+"','"+authorization_number+"','"+authorization_day+"','"+announcement_number+"','"+variety_rights_holder+"','"+variety_rights_address+"')"
                            sql_updata = "update VARIETY_LICENSING_DETAILS set variety='"+variety+"',application_number='"+application_number+"',filing_day='"+filing_day+"',applicant='"+applicant+"',application_status='"+application_status+"',application_notice_date='"+application_notice_date+"',authorization_number='"+authorization_number+"',authorization_day='"+authorization_day+"',announcement_number='"+announcement_number+"',variety_rights_holder='"+variety_rights_holder+"',variety_rights_address='"+variety_rights_address+"' where variety like '"+variety+"'"
                            cursor.execute(sql_select)
                            result=cursor.fetchall()
                            if len(result)>0: 
                                cursor.execute(sql_updata)
                                cursor.close()
                                databases.commit()
                            else:
                                cursor.execute(sql_insert)
                                cursor.close()
                                databases.commit()
                        except:
                            print("品种授权详情 -> 数据添加错误,这可能是字段中存在<''>等字符导致的.")
            except:
                print('品种授权详情 -> 一条数据错误,这可能是网络原因导致的.')
        driver.find_element_by_id('next_gridPager').click()
        time.sleep(sleepTime*2)
        end = datetime.now()
        second = ((end-start).seconds)*(count-num)

def getVarietyPromotionDetails(): #获取品种推广详情
    global variety                #(品种名称)
    global cultivar_name          #(作物名称)
    global region                 #(地区)
    global year                   #(年份)
    global area                   #(面积)
    global count
    driver = webdriver.PhantomJS()
    driver.get(pztg) 
    time.sleep(sleepTime)
    try:
        count = int(driver.find_element_by_id('mainlist').find_element_by_class_name('page-last').text.replace(' ',''))
    except:
        print('品种推广详情 -> 与网站建立连接失败.请重启程序.')
        exit()
    num = 0
    second = 0
    while num<count:
        start = datetime.now()
        num = num + 1
        #print('品种推广详情 -> 目前进度: ',num,'页.  共:',count,'页.  百分比:',((num/count)*100),'%')
        #if second!= 0 : print('品种推广详情 -> 预计',changeTime(second),'后完成.')
        global percent4
        global overtime4
        percent4 = str((num/count)*100)+"%"
        overtime4 = "剩余"+changeTime(second)
        dirver1 = driver.find_element_by_id('gridList').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')#定位
        for it in dirver1:  
            try:
                variety = ""
                cultivar_name = ""
                region = ""
                year = ""
                area = ""
                dirver2 = it.find_elements_by_tag_name('td')
                variety = dirver2[3].text
                if len(variety) == 0 : continue
                cultivar_name = dirver2[2].text
                region = dirver2[1].text
                year = dirver2[0].text
                area = dirver2[4].text
                try:
                    cursor = databases.cursor()
                    sql_select = "select variety from VARIETY_PROMOTION_DETAILS where variety like '"+variety+"'"
                    sql_insert = "insert into VARIETY_PROMOTION_DETAILS(variety,cultivar_name,region,year,area) values('"+variety+"','"+cultivar_name+"','"+region+"','"+year+"','"+area+"')"
                    sql_updata = "update VARIETY_PROMOTION_DETAILS set variety='"+variety+"',cultivar_name='"+cultivar_name+"',region='"+region+"',year='"+year+"',area='"+area+"' where variety like '"+variety+"'"
                    cursor.execute(sql_select)
                    result=cursor.fetchall()
                    if len(result)>0: 
                        cursor.execute(sql_updata)
                        cursor.close()
                        databases.commit()
                    else:
                        cursor.execute(sql_insert)
                        cursor.close()
                        databases.commit()
                except:
                    print("品种推广详情 -> 数据添加错误,这可能是字段中存在<''>等字符导致的.")
            except:
                print('品种推广详情 -> 一条数据错误,这可能是网络原因导致的.')
        driver.find_element_by_id('mainlist').find_element_by_class_name('page-next').click()
        time.sleep(sleepTime*2)
        end = datetime.now()
        second = ((end-start).seconds)*(count-num)

def getVarietyProtectionDetails(): #(品种保护表)
    global application_number     #(申请号)
    global authorization_number   #(授权号)
    global crop_name              #(作物名称)
    global cultivar_name          #(品种名称)
    global authorization_date     #(申请/授权日期)
    global announcement_type      #(公告类型)
    global variety_rights_holder  #(申请/品种权人)
    global announcement_number    #(公告号)
    global application_day        #(申请日)
    global application_peple      #(申请人)
    global application_notice_date#(申请公告日)
    global count
    driver = webdriver.PhantomJS()
    driver.get(pzbh) 
    time.sleep(sleepTime)
    try:
        count = int(driver.find_element_by_id('sp_1_gridPager').text.replace(' ',''))
    except:
        print('品种保护表 -> 与网站建立连接失败.请重启程序.')
        exit()
    num = 0
    second = 0
    while num<count:
        start = datetime.now()
        num = num + 1
        #print('品种保护表 -> 目前进度: ',num,'页.  共:',count,'页.  百分比:',((num/count)*100),'%')
        #if second!= 0 : print('品种保护表 -> 预计',changeTime(second),'后完成.')
        global percent5
        global overtime5
        percent5 = str((num/count)*100)+"%"
        overtime5 = "剩余"+changeTime(second)
        dirver1 = driver.find_element_by_id('gridList').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')#定位
        for it in dirver1:  
            try:
                application_number = ""  
                authorization_number = "" 
                crop_name = ""             
                cultivar_name = ""         
                authorization_date = ""    
                announcement_type = ""     
                variety_rights_holder = ""  
                announcement_number =""   
                application_day = ""       
                application_peple = ""      
                application_notice_date = "" 
                dirver2 = it.find_elements_by_tag_name('td')
                application_number = dirver2[0].text
                if len(application_number) == 0 : continue
                authorization_number = dirver2[1].text
                crop_name = dirver2[2].text
                cultivar_name = dirver2[3].text
                authorization_date = dirver2[4].text
                announcement_type = dirver2[5].text
                variety_rights_holder = dirver2[6].text
                announcement_number = dirver2[7].text
                dirver3 = it.find_elements_by_tag_name('a')                     
                dirver3[0].click()                             
                time.sleep(sleepTime)
                child = driver.find_element_by_id('applylist').find_elements_by_tag_name('tr')
                child1 = child[3].find_elements_by_tag_name('td')
                application_day = child1[1].text
                child2 = child[4].find_elements_by_tag_name('td')
                application_peple = child2[1].text
                child3 = child[5].find_elements_by_tag_name('td')
                application_notice_date = child3[1].text
                try:
                    cursor = databases.cursor()
                    sql_select = "select application_number from VARIETY_PROTECTION_DETAILS where application_number like '"+application_number+"'"
                    sql_insert = "insert into VARIETY_PROTECTION_DETAILS(application_number,authorization_number,crop_name,cultivar_name,authorization_date,announcement_type,variety_rights_holder,announcement_number,application_day,application_peple,application_notice_date) values('"+application_number+"','"+authorization_number+"','"+crop_name+"','"+cultivar_name+"','"+authorization_date+"','"+announcement_type+"','"+variety_rights_holder+"','"+announcement_number+"','"+application_day+"','"+application_peple+"','"+application_notice_date+"')"
                    sql_updata = "update VARIETY_PROTECTION_DETAILS set application_number='"+application_number  +"',authorization_number='"+authorization_number+"',crop_name='"+crop_name+"',cultivar_name='"+cultivar_name+"',authorization_date='"+authorization_date+"',announcement_type='"+announcement_type+"',variety_rights_holder='"+variety_rights_holder+"',announcement_number='"+announcement_number+"',application_day='"+application_day+"',application_peple='"+application_peple+"',application_notice_date='"+application_notice_date+"' where application_number like '"+application_number+"'"
                    cursor.execute(sql_select)
                    result=cursor.fetchall()
                    if len(result)>0: 
                        cursor.execute(sql_updata)
                        cursor.close()
                        databases.commit()
                    else:
                        cursor.execute(sql_insert)
                        cursor.close()
                        databases.commit()
                except:
                    print("品种保护表 -> 数据添加错误,这可能是字段中存在<''>等字符导致的.")
            except:
                print('品种保护表 -> 一条数据错误,这可能是网络原因导致的.')
        driver.find_element_by_id('next_gridPager').click()
        time.sleep(sleepTime*2)
        end = datetime.now()
        second = ((end-start).seconds)*(count-num)

def getRegistrationNumberDetails():  #(登记编号表)
    global registration_number   #(登记编号)
    global crop_name             #(作物名称)
    global cultivar_name         #(品种名称)
    global state                 #(状态)
    global year_of_registration  #(登记年份)
    global applicant             #(申请者)
    global breeders              #(育种者)
    global breed_origin          #(品种来源)
    global characteristic        #(特征特性)
    global cultivation_techniques#(栽培技术要点)
    global suitable_for_planting #(适宜种植区域及季节)
    global matters               #(注意事项)
    global count
    driver = webdriver.PhantomJS()
    driver.get(pzdj) 
    time.sleep(sleepTime)
    try:
        count = int(driver.find_element_by_id('sp_1_gridPager').text.replace(' ',''))
    except:
        print('登记编号表 -> 与网站建立连接失败.请重启程序.')
        exit()
    num = 0
    second = 0
    while num<count:
        start = datetime.now()
        num = num + 1
        #print('登记编号表 -> 目前进度: ',num,'页.  共:',count,'页.  百分比:',((num/count)*100),'%')
        #if second!= 0 : print('登记编号表 -> 预计',changeTime(second),'后完成.')
        global percent6
        global overtime6
        percent6 = str((num/count)*100)+"%"
        overtime6 = "剩余"+changeTime(second)
        dirver1 = driver.find_element_by_id('gridList').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')#定位
        for it in dirver1:  
            try:
                registration_number = ""
                crop_name = ""  
                cultivar_name = ""    
                state = ""   
                year_of_registration = ""
                applicant = ""
                breeders = ""        
                breed_origin = ""    
                characteristic = ""   
                cultivation_techniques = ""
                suitable_for_planting = ""
                matters = "" 
                dirver2 = it.find_elements_by_tag_name('td')
                registration_number = dirver2[1].text
                if len(registration_number) == 0 : continue
                crop_name = dirver2[2].text
                cultivar_name = dirver2[3].text
                state = dirver2[4].text
                year_of_registration = dirver2[5].text
                applicant = dirver2[6].text
                dirver3 = it.find_elements_by_tag_name('a')                     
                dirver3[0].click()                             
                time.sleep(sleepTime)
                child = driver.find_element_by_id('Announcementlist').find_elements_by_tag_name('tr')
                child1 = child[4].find_elements_by_tag_name('td')
                breeders = child1[1].text
                child2 = child[5].find_elements_by_tag_name('td')
                breed_origin = child2[1].text
                child3 = child[6].find_elements_by_tag_name('td')
                characteristic = child3[1].text
                child4 = child[7].find_elements_by_tag_name('td')
                cultivation_techniques = child4[1].text
                child5 = child[8].find_elements_by_tag_name('td')
                suitable_for_planting = child5[1].text
                child6 = child[9].find_elements_by_tag_name('td')
                matters = child6[1].text
                try:
                    cursor = databases.cursor()
                    sql_select = "select registration_number from REGISTRATION_NUMBER_DETAILS where registration_number like '"+registration_number+"'"
                    sql_insert = "insert into REGISTRATION_NUMBER_DETAILS(registration_number,crop_name,cultivar_name,state,year_of_registration,applicant,breeders,breed_origin,characteristic,cultivation_techniques,suitable_for_planting) values('"+application_number+"','"+authorization_number+"','"+crop_name+"','"+cultivar_name+"','"+authorization_date+"','"+announcement_type+"','"+variety_rights_holder+"','"+announcement_number+"','"+application_day+"','"+application_peple+"','"+application_notice_date+"')"
                    sql_updata = "update REGISTRATION_NUMBER_DETAILS set registration_number='"+ registration_number +"',crop_name='"+crop_name+"',cultivar_name='"+cultivar_name+"',state='"+state+"',year_of_registration='"+year_of_registration+"',applicant='"+applicant+"',breeders='"+breeders+"',breed_origin='"+breed_origin+"',characteristic='"+characteristic+"',cultivation_techniques='"+cultivation_techniques+"',suitable_for_planting='"+suitable_for_planting+"' where registration_number like '"+registration_number+"'"
                    cursor.execute(sql_select)                
                    result=cursor.fetchall()
                    if len(result)>0: 
                        cursor.execute(sql_updata)
                        cursor.close()
                        databases.commit()
                    else:
                        cursor.execute(sql_insert)
                        cursor.close()
                        databases.commit()
                except:
                    print("登记编号表 -> 数据添加错误,这可能是字段中存在<''>等字符导致的.")
            except:
                print('登记编号表 -> 一条数据错误,这可能是网络原因导致的.')
        driver.find_element_by_id('next_gridPager').click()
        time.sleep(sleepTime*2)
        end = datetime.now()
        second = ((end-start).seconds)*(count-num)

def getLicenceMain():     #(许可证主证信息)
    global deputy_card         #(许可证编号)
    global enterprise_name     #(企业名称)
    global legal_spokesperson  #(法定代言人)
    global issuing_authority   #(发证机关)
    global notice_number       #(公告文号)
    global date_of_issue       #(发证日期)
    global valid_until         #(有效期至)
    global address             #(住所)
    global scope_production_management#(生产经营范围)
    global mode_production     #(生产经营方式)
    global effective_region    #(有效区域)
    global agreed_social_credit_code#(同意社会信用代码)
    global count
    driver = webdriver.PhantomJS()
    driver.get(zxkz) 
    time.sleep(sleepTime)
    try:
        count = int(driver.find_element_by_id('sp_1_gridPager').text.replace(' ',''))
    except:
        print('许可证主证信息 -> 与网站建立连接失败.请重启程序.')
        exit()
    num = 0
    second = 0
    while num<count:
        start = datetime.now()
        num = num + 1
        #print('许可证主证信息 -> 目前进度: ',num,'页.  共:',count,'页.  百分比:',((num/count)*100),'%')
        #if second!= 0 : print('许可证主证信息 -> 预计',changeTime(second),'后完成.')
        global percent7
        global overtime7
        percent7 = str((num/count)*100)+"%"
        overtime7 = "剩余"+changeTime(second)
        dirver1 = driver.find_element_by_id('gridList').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')#定位
        for it in dirver1:  
            try:
                driver6 = it.find_elements_by_tag_name('a') 
                if len(driver6) != 0:
                    deputy_card = ""         
                    enterprise_name = ""    
                    legal_spokesperson = ""  
                    issuing_authority = ""  
                    notice_number = ""     
                    date_of_issue = ""  
                    valid_until = ""       
                    address = ""      
                    scope_production_management = ""
                    mode_production = ""   
                    effective_region = ""  
                    agreed_social_credit_code = ""
                    child = webdriver.PhantomJS()
                    child.get(driver6[0].get_attribute('href'))
                    time.sleep(sleepTime)
                    itDir1 = child.find_element_by_tag_name('body').find_element_by_class_name('main')
                    itDir_left_data = itDir1.find_element_by_class_name('left').find_elements_by_tag_name('span')
                    itDir_right_data = itDir1.find_element_by_class_name('right').find_elements_by_tag_name('span')
                    deputy_card = itDir_left_data[0].text
                    if len(deputy_card) == 0: continue
                    enterprise_name = itDir_left_data[1].text
                    legal_spokesperson = itDir_left_data[2].text
                    issuing_authority = itDir_left_data[3].text
                    notice_number = itDir_left_data[4].text
                    date_of_issue = itDir_left_data[5].text
                    valid_until = itDir_left_data[6].text + "-" + itDir_left_data[7].text + "-" + itDir_left_data[8].text
                    address = itDir_right_data[5].text
                    scope_production_management = itDir_right_data[7].text
                    mode_production = itDir_right_data[8].text
                    effective_region = itDir_right_data[9].text
                    agreed_social_credit_code = itDir_right_data[11].text
                    try:
                        cursor = databases.cursor()
                        sql_select = "select deputy_card from LICENCE_MAIN where deputy_card like '"+deputy_card+"'"
                        sql_insert = "insert into LICENCE_MAIN(deputy_card,enterprise_name,legal_spokesperson,issuing_authority,notice_number,date_of_issue,valid_until,address,scope_production_management,mode_production,effective_region,agreed_social_credit_code) values('"+deputy_card+"','"+enterprise_name+"','"+legal_spokesperson+"','"+issuing_authority+"','"+notice_number+"','"+date_of_issue+"','"+valid_until+"','"+address+"','"+scope_production_management+"','"+mode_production+"','"+effective_region+"','"+agreed_social_credit_code+"')"
                        sql_updata = "update LICENCE_MAIN set deputy_card='"+ deputy_card +"',enterprise_name='"+enterprise_name+"',legal_spokesperson='"+legal_spokesperson+"',issuing_authority='"+issuing_authority+"',notice_number='"+notice_number+"',date_of_issue='"+date_of_issue+"',valid_until='"+valid_until+"',address='"+address+"',scope_production_management='"+scope_production_management+"',mode_production='"+mode_production+"',effective_region='"+effective_region+"',agreed_social_credit_code='"+agreed_social_credit_code+"' where deputy_card like '"+deputy_card+"'"
                        cursor.execute(sql_select)                
                        result=cursor.fetchall()
                        if len(result)>0: 
                            cursor.execute(sql_updata)
                            cursor.close()
                            databases.commit()
                        else:
                            cursor.execute(sql_insert)
                            cursor.close()
                            databases.commit()
                    except:
                        print("许可证主证信息 -> 数据添加错误,这可能是字段中存在<''>等字符导致的.")
            except:
                print('许可证主证信息 -> 一条数据错误,这可能是网络原因导致的.')
        driver.find_element_by_id('next_gridPager').click()
        time.sleep(sleepTime*2)
        end = datetime.now()
        second = ((end-start).seconds)*(count-num)

def getLicenceVice():    #(许可证副证信息)
    global deputy_card         #(许可证编号)
    global enterprise_name     #(企业名称)
    global date_of_issue       #(发证日期)
    global valid_until         #(有效期至)
    #(副证详情)
    #licence_number      (所属许可证编号)
    global licence_number
    global crop_species        #(作物种类)
    global seed_type           #(种子类型)
    global cultivar_name       #(品种名称)
    global variety_approval_number#(品种审定（登记）编号)
    global seed_production_site#(种子生产地点)
    global remarks             #(备注)
    global count
    driver = webdriver.PhantomJS()
    driver.get(zxkz) 
    time.sleep(sleepTime)
    try:
        count = int(driver.find_element_by_id('sp_1_gridPager').text.replace(' ',''))
    except:
        print('许可证副证信息 -> 与网站建立连接失败.请重启程序.')
        exit()
    num = 0
    second = 0
    while num<count:
        start = datetime.now()
        num = num + 1
        #print('许可证副证信息 -> 目前进度: ',num,'页.  共:',count,'页.  百分比:',((num/count)*100),'%')
        #if second!= 0 : print('许可证副证信息 -> 预计',changeTime(second),'后完成.')
        global percent8
        global overtime8
        percent8 = str((num/count)*100)+"%"
        overtime8 = "剩余"+changeTime(second)
        dirver1 = driver.find_element_by_id('gridList').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')#定位
        for it in dirver1:  
            try:
                driver6 = it.find_elements_by_tag_name('a') 
                if len(driver6) > 1:
                    deputy_card = ""        
                    enterprise_name = ""      
                    date_of_issue = ""      
                    valid_until = ""    
                    child = webdriver.PhantomJS()
                    child.get(driver6[1].get_attribute('href'))
                    time.sleep(sleepTime)
                    itDirver01 = child.find_element_by_tag_name('body')
                    itDirver01_div = itDirver01.find_elements_by_tag_name('div')
                    itDirver01_div_dieyu = itDirver01_div[0].find_element_by_class_name('dieyu_page_style')
                    itDirver01_div_dieyu_a = itDirver01_div_dieyu.find_elements_by_tag_name('a')
                    itDirver01_div_main = itDirver01.find_element_by_class_name('main') 
                    itDirver01_div_right = itDirver01_div_main.find_element_by_class_name('right')
                    itDirver01_div_right_spanData = itDirver01_div_right.find_elements_by_tag_name('span')
                    deputy_card = itDirver01_div_right_spanData[1].text+"("+itDirver01_div_right_spanData[2].text+")农种许字("+itDirver01_div_right_spanData[3].text+")第"+itDirver01_div_right_spanData[4].text+"号"
                    enterprise_name = itDirver01_div_right_spanData[0].text
                    date_of_issue = itDirver01_div_right_spanData[5].text
                    valid_until = itDirver01_div_right_spanData[6].text
                    try:
                        cursor = databases.cursor()
                        sql_select = "select deputy_card from LICENCE_VICE where deputy_card like '"+deputy_card+"'"
                        sql_insert = "insert into LICENCE_VICE(deputy_card,enterprise_name,date_of_issue,valid_until) values('"+deputy_card+"','"+enterprise_name+"','"+date_of_issue+"','"+valid_until+"')"
                        sql_updata = "update LICENCE_VICE set deputy_card='"+ deputy_card +"',enterprise_name='"+enterprise_name+"',date_of_issue='"+date_of_issue+"',valid_until='"+valid_until+"' where deputy_card like '"+deputy_card+"'"
                        cursor.execute(sql_select)                
                        result=cursor.fetchall()
                        if len(result)>0: 
                            cursor.execute(sql_updata)
                            cursor.close()
                            databases.commit()
                        else:
                            cursor.execute(sql_insert)
                            cursor.close()
                            databases.commit()
                    except:
                        print("许可证副证信息 -> 数据添加错误,这可能是字段中存在<''>等字符导致的.")
                    i = 7 
                    while i < (len(itDirver01_div_right_spanData)-4):
                        licence_number = deputy_card
                        crop_species = ""
                        seed_type = ""  
                        cultivar_name = ""
                        variety_approval_number = ""
                        seed_production_site = ""
                        remarks = ""    
                        crop_species = itDirver01_div_right_spanData[i+1].text
                        seed_type = itDirver01_div_right_spanData[i+2].text
                        cultivar_name = itDirver01_div_right_spanData[i+3].text
                        variety_approval_number = itDirver01_div_right_spanData[i+4].text
                        seed_production_site = itDirver01_div_right_spanData[i+5].text
                        remarks = itDirver01_div_right_spanData[i+6].text
                        try:
                            cursor = databases.cursor()
                            sql_select = "select licence_number from VICE_DETAILS where licence_number like '"+licence_number+"'"
                            sql_insert = "insert into VICE_DETAILS(licence_number,crop_species,seed_type,cultivar_name,variety_approval_number,seed_production_site,remarks) values('"+licence_number+"','"+crop_species+"','"+seed_type+"','"+cultivar_name+"','"+variety_approval_number+"','"+seed_production_site+"','"+remarks+"')"
                            sql_updata = "update VICE_DETAILS set licence_number='"+ licence_number +"',crop_species='"+crop_species+"',seed_type='"+seed_type+"',cultivar_name='"+cultivar_name+"',variety_approval_number='"+variety_approval_number+"',seed_production_site='"+seed_production_site+"',remarks='"+remarks+"' where licence_number like '"+licence_number+"'"
                            cursor.execute(sql_select)                
                            result=cursor.fetchall()
                            if len(result)>0: 
                                cursor.execute(sql_updata)
                                cursor.close()
                                databases.commit()
                            else:
                                cursor.execute(sql_insert)
                                cursor.close()
                                databases.commit()
                        except:
                            print("许可证副证信息 -> 数据添加错误,这可能是字段中存在<''>等字符导致的.")
                        i += 7 
                    for it in itDirver01_div_dieyu_a:
                        driver_temp = webdriver.PhantomJS()
                        driver_temp.get(it.get_attribute('href')) 
                        time.sleep(sleepTime)
                        itDirver_temp = driver_temp.find_element_by_tag_name('body')
                        itDirver_temp_div_main = itDirver_temp.find_element_by_class_name('main')
                        itDirver_temp_div_right = itDirver_temp_div_main.find_element_by_class_name('right')
                        itDirver_temp_div_right_spanData = itDirver_temp_div_right.find_elements_by_tag_name('span')
                        i = 7 
                        while i < (len(itDirver_temp_div_right_spanData)-4):
                            licence_number = deputy_card
                            crop_species = ""
                            seed_type = ""  
                            cultivar_name = ""
                            variety_approval_number = ""
                            seed_production_site = ""
                            remarks = ""    
                            crop_species = itDirver_temp_div_right_spanData[i+1].text
                            seed_type = itDirver_temp_div_right_spanData[i+2].text
                            cultivar_name = itDirver_temp_div_right_spanData[i+3].text
                            variety_approval_number = itDirver_temp_div_right_spanData[i+4].text
                            seed_production_site = itDirver_temp_div_right_spanData[i+5].text
                            remarks = itDirver_temp_div_right_spanData[i+6].text
                            try:
                                cursor = databases.cursor()
                                sql_select = "select licence_number from VICE_DETAILS where licence_number like '"+licence_number+"'"
                                sql_insert = "insert into VICE_DETAILS(licence_number,crop_species,seed_type,cultivar_name,variety_approval_number,seed_production_site,remarks) values('"+licence_number+"','"+crop_species+"','"+seed_type+"','"+cultivar_name+"','"+variety_approval_number+"','"+seed_production_site+"','"+remarks+"')"
                                sql_updata = "update VICE_DETAILS set licence_number='"+ licence_number +"',crop_species='"+crop_species+"',seed_type='"+seed_type+"',cultivar_name='"+cultivar_name+"',variety_approval_number='"+variety_approval_number+"',seed_production_site='"+seed_production_site+"',remarks='"+remarks+"' where licence_number like '"+licence_number+"'"
                                cursor.execute(sql_select)                
                                result=cursor.fetchall()
                                if len(result)>0: 
                                    cursor.execute(sql_updata)
                                    cursor.close()
                                    databases.commit()
                                else:
                                    cursor.execute(sql_insert)
                                    cursor.close()
                                    databases.commit()
                                i += 7 
                            except:
                                print("许可证副证信息 -> 数据添加错误,这可能是字段中存在<''>等字符导致的.")   
            except:
                print('许可证副证信息 -> 一条数据错误,这可能是网络原因导致的.')
        driver.find_element_by_id('next_gridPager').click()
        time.sleep(sleepTime*2)
        end = datetime.now()
        second = ((end-start).seconds)*(count-num)

def getSeedImport():      #(种子进口)
    global approval_number     #(审批单编号)
    global applicant_unit      #(申请单位)
    global crop_name           #(作物名称)
    global cultivar_name       #(品种名称)
    global suppliers           #(供种单位)
    global import_country      #(进口国家)
    global purpose             #(用途)
    global date_of_application #(申请日期)
    global count
    driver = webdriver.PhantomJS()
    driver.get(zzjk)  
    time.sleep(sleepTime)
    try:
        count = int(driver.find_element_by_id('sp_1_gridPager').text.replace(' ',''))
    except:
        print('种子进口 -> 与网站建立连接失败.请重启程序.')
        exit()
    num = 0
    second = 0
    while num<count:
        start = datetime.now()
        num = num + 1
        #print('种子进口 -> 目前进度: ',num,'页.  共:',count,'页.  百分比:',((num/count)*100),'%')
        #if second!= 0 : print('种子进口 -> 预计',changeTime(second),'后完成.')
        global percent9
        global overtime9
        percent9 = str((num/count)*100)+"%"
        overtime9 = "剩余"+changeTime(second)
        dirver1 = driver.find_element_by_id('gridList').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')#定位
        for it in dirver1:  
            try:
                approval_number = ""
                applicant_unit = ""
                crop_name = ""
                cultivar_name = ""
                suppliers = "" 
                import_country = ""
                purpose = "" 
                date_of_application = "" 
                dirver2 = it.find_elements_by_tag_name('td')
                approval_number = dirver2[0].text
                if len(approval_number) == 0: continue
                applicant_unit = dirver2[1].text
                crop_name = dirver2[2].text
                cultivar_name = dirver2[3].text
                suppliers = dirver2[4].text
                import_country = dirver2[5].text
                purpose = dirver2[6].text
                date_of_application = dirver2[7].text
                try:
                    cursor = databases.cursor()
                    sql_select = "select approval_number from SEED_IMPORT where approval_number like '"+approval_number+"'"
                    sql_insert = "insert into SEED_IMPORT(approval_number,applicant_unit,crop_name,cultivar_name,suppliers,import_country,purpose,date_of_application) values('"+approval_number+"','"+applicant_unit+"','"+crop_name+"','"+cultivar_name+"','"+exporter+"','"+exporting_countries+"','"+purpose+"','"+date_of_application+"')"
                    sql_updata = "update SEED_IMPORT set approval_number='"+approval_number+"',applicant_unit='"+applicant_unit+"',crop_name='"+crop_name+"',cultivar_name='"+cultivar_name+"',suppliers='"+suppliers+"',import_country='"+import_country+"',purpose='"+purpose+"',date_of_application='"+date_of_application+"' where approval_number like '"+approval_number+"'"
                    cursor.execute(sql_select)
                    result=cursor.fetchall()
                    if len(result)>0: 
                        cursor.execute(sql_updata)
                        cursor.close()
                        databases.commit()
                    else:
                        cursor.execute(sql_insert)
                        cursor.close()
                        databases.commit()
                except:
                    print("种子进口 -> 数据添加错误,这可能是字段中存在<''>等字符导致的.")
            except:
                print('种子进口 -> 一条数据错误,这可能是网络原因导致的.')
        driver.find_element_by_id('next_gridPager').click()
        time.sleep(sleepTime*2)
        end = datetime.now()
        second = ((end-start).seconds)*(count-num)

def getSeedExport():    #(种子出口)
    global approval_number     #(审批单编号)
    global applicant_unit      #(申请单位)
    global crop_name           #(作物名称)
    global cultivar_name       #(品种名称)
    global exporter            #(出口单位)
    global exporting_countries #(出口国家)
    global purpose             #(用途)
    global date_of_application #(申请日期)
    global count
    driver = webdriver.PhantomJS()
    driver.get(zzck) 
    time.sleep(sleepTime)
    try:
        count = int(driver.find_element_by_id('sp_1_gridPager').text.replace(' ',''))
    except:
        print('种子出口 -> 与网站建立连接失败.请重启程序.')
        exit()
    num = 0
    second = 0
    while num<count:
        start = datetime.now()
        num = num + 1
        #print('种子出口 -> 目前进度: ',num,'页.  共:',count,'页.  百分比:',((num/count)*100),'%')
        #if second!= 0 : print('种子出口 -> 预计',changeTime(second),'后完成.')
        global percent10
        global overtime10
        percent10 = str((num/count)*100)+"%"
        overtime10 = "剩余"+changeTime(second)
        dirver1 = driver.find_element_by_id('gridList').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')#定位
        for it in dirver1:  
            try:
                approval_number = ""
                applicant_unit = ""
                crop_name = ""
                cultivar_name = ""
                exporter = "" 
                exporting_countries = ""
                purpose = "" 
                date_of_application = "" 
                dirver2 = it.find_elements_by_tag_name('td')
                approval_number = dirver2[0].text
                if len(approval_number) == 0: continue
                applicant_unit = dirver2[1].text
                crop_name = dirver2[2].text
                cultivar_name = dirver2[3].text
                exporter = dirver2[4].text
                exporting_countries = dirver2[5].text
                purpose = dirver2[6].text
                date_of_application = dirver2[7].text
                try:
                    cursor = databases.cursor()
                    sql_select = "select approval_number from SEED_EXPORT where approval_number like '"+approval_number+"'"
                    sql_insert = "insert into SEED_EXPORT(approval_number,applicant_unit,crop_name,cultivar_name,exporter,exporting_countries,purpose,date_of_application) values('"+approval_number+"','"+applicant_unit+"','"+crop_name+"','"+cultivar_name+"','"+exporter+"','"+exporting_countries+"','"+purpose+"','"+date_of_application+"')"
                    sql_updata = "update SEED_EXPORT set approval_number='"+approval_number+"',applicant_unit='"+applicant_unit+"',crop_name='"+crop_name+"',cultivar_name='"+cultivar_name+"',exporter='"+exporter+"',exporting_countries='"+exporting_countries+"',purpose='"+purpose+"',date_of_application='"+date_of_application+"' where approval_number like '"+approval_number+"'"
                    cursor.execute(sql_select)
                    result=cursor.fetchall()
                    if len(result)>0: 
                        cursor.execute(sql_updata)
                        cursor.close()
                        databases.commit()
                    else:
                        cursor.execute(sql_insert)
                        cursor.close()
                        databases.commit()
                except:
                    print("种子出口 -> 数据添加错误,这可能是字段中存在<''>等字符导致的.")
            except:
                print('种子出口 -> 一条数据错误,这可能是网络原因导致的.')
        driver.find_element_by_id('next_gridPager').click()
        time.sleep(sleepTime*2)
        end = datetime.now()
        second = ((end-start).seconds)*(count-num)

def showMessage():
    while 1:
        global percent1
        global percent2
        global percent3
        global percent4
        global percent5
        global percent6
        global percent7
        global percent8
        global percent9
        global percent10
        global overtime1
        global overtime2
        global overtime3
        global overtime4
        global overtime5
        global overtime6
        global overtime7
        global overtime8
        global overtime9
        global overtime10
        if len(percent1) == 0: percent1 = "0%"
        if len(overtime1) == 0: overtime1 = "正在计算"
        if len(percent2) == 0: percent2 = "0%"
        if len(overtime2) == 0: overtime2 = "正在计算"
        if len(percent3) == 0: percent3 = "0%"
        if len(overtime3) == 0: overtime3 = "正在计算"
        if len(percent4) == 0: percent4 = "0%"
        if len(overtime4) == 0: overtime4 = "正在计算"
        if len(percent5) == 0: percent5 = "0%"
        if len(overtime5) == 0: overtime5 = "正在计算"
        if len(percent6) == 0: percent6 = "0%"
        if len(overtime6) == 0: overtime6 = "正在计算"
        if len(percent7) == 0: percent7 = "0%"
        if len(overtime7) == 0: overtime7 = "正在计算"
        if len(percent8) == 0: percent8 = "0%"
        if len(overtime8) == 0: overtime8 = "正在计算"
        if len(percent9) == 0: percent9 = "0%"
        if len(overtime9) == 0: overtime9 = "正在计算"
        if len(percent10) == 0: percent10 = "0%"
        if len(overtime10) == 0: overtime10 = "正在计算"
        print("      表名            进度              剩余时间")
        print()
        print("产品审定基本数据表  "+percent1+overtime1)
        print("审定编号详情表      "+percent2+overtime2)
        print("品种授权详情表      "+percent3+overtime3)
        print("品种推广详情表      "+percent4+overtime4)
        print("品种保护表          "+percent5+overtime5)
        print("产登记编号表        "+percent6+overtime6)
        print("许可证主证信息表    "+percent7+overtime7)
        print("许可证副证信息表    "+percent8+overtime8)
        print("种子进口表         "+percent9+overtime9)
        print("种子出口表         "+percent10+overtime10)
        time.sleep(10)
        i = os.system('cls')

print('为了安全起见,请先备份数据库.')
print("开始连接数据库.")
try:
    databases = cx_Oracle.connect('seed/seed@192.168.1.108:1521/orcl');
    print("连接数据库成功.")
except: 
    print('连接数据库失败.请检查网络连接或主机是否开启.')  
    print('程序中断.')  
    exit()

print('开始构造线程池...')
threads = []
t1 = threading.Thread(target=getSubjectBasicData)
threads.append(t1)
t2 = threading.Thread(target=getApprovalNumberDetails)
threads.append(t2)
t3 = threading.Thread(target=getVarietyLicensingDetails)
threads.append(t3)
t4 = threading.Thread(target=getVarietyPromotionDetails)
threads.append(t4)
t5 = threading.Thread(target=getVarietyProtectionDetails)
threads.append(t5)
t6 = threading.Thread(target=getRegistrationNumberDetails)
threads.append(t6)
t7 = threading.Thread(target=getLicenceMain)
threads.append(t7)
t8 = threading.Thread(target=getLicenceVice)
threads.append(t8)
t9 = threading.Thread(target=getSeedImport)
threads.append(t9)
t10 = threading.Thread(target=getSeedExport)
threads.append(t10)
t11 = threading.Thread(target=showMessage)
threads.append(t11)
if __name__ == '__main__':
    print('构造完成, 正在启动线程')
    for t in threads:
        t.setDaemon(True)
        t.start()
    print('程序开始运行,请保持网络通畅. 如网络情况较差,请手动更改sleepTime.')
    for t in threads:
        t.join()

#E:\PythonSpace\ToOracle.py