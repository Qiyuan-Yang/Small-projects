import requests
from bs4 import BeautifulSoup
import bs4
import re
import time as t
import matplotlib.pyplot as plt
import numpy as np 
import random


def getHtmlText(url, code="utf-8"): 
    try:
        r = requests.get(url,headers = {'user-agent':'Mozilla/5.0'})
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ''


def buildT(num):
    ta = [0]*24*60
    for i in range(1,34):
        text = getHtmlText('https://flights.ctrip.com/schedule/departairport-lukou/outmap-{}.html'.format(i))
        timePat = '  \d{2}:\d{2}'
        for time in re.findall(timePat,text)[::2]:
            if time[2] == '0' and time[5] == '0':
                time = eval(time[3])*60+eval(time[6]) - 60
            elif time[2] == '0' and time[5] != '0':
                time = eval(time[3])*60+eval(time[::-1][0:2][::-1]) - 60
            elif time[2] != '0' and time[5] == '0':
                time = eval(time[2:4])*60+eval(time[6]) - 60
            else:
                time = eval(time[2:4])*60+eval(time[::-1][0:2][::-1]) - 60
            #ta[time] += round(570/650*124*0.1/2)
            ta[time] += num
    return ta


def buildP(num):
    pop = [0]*24*60
    for i in range(1,34):
        text = getHtmlText('https://flights.ctrip.com/schedule/departairport-lukou/inmap-{}.html'.format(i))
        timePat = '  \d{2}:\d{2}'
        for time in re.findall(timePat,text)[::2]:
            if time[2] == '0' and time[5] == '0':
                time = eval(time[3])*60+eval(time[6]) + 20
            elif time[2] == '0' and time[5] != '0':
                time = eval(time[3])*60+eval(time[::-1][0:2][::-1]) + 20
            elif time[2] != '0' and time[5] == '0':
                time = eval(time[2:4])*60+eval(time[6]) + 20
            else:
                time = eval(time[2:4])*60+eval(time[::-1][0:2][::-1]) + 20
            if time < 1440:
                #pop[time] += round(570/650*124*0.1/2)
                pop[time] += num
            else:
                continue
    return pop


def buildH():
    hang = [0]*24*60
    for i in range(1,34):
        text = getHtmlText('https://flights.ctrip.com/schedule/departairport-lukou/inmap-{}.html'.format(i))
        timePat = '  \d{2}:\d{2}'
        for time in re.findall(timePat,text)[::2]:
            if time[2] == '0' and time[5] == '0':
                time = eval(time[3])*60+eval(time[6])
            elif time[2] == '0' and time[5] != '0':
                time = eval(time[3])*60+eval(time[::-1][0:2][::-1])
            elif time[2] != '0' and time[5] == '0':
                time = eval(time[2:4])*60+eval(time[6])
            else:
                time = eval(time[2:4])*60+eval(time[::-1][0:2][::-1])
            hang[time] += 570/650
    return hang






class taxi:
    '出租车'


    def __init__(self,duiChang,arrive,name):
        self.duiChang = duiChang
        self.arrive = arrive
        self.name = name


    def judge(self,pop,popAm):
        p = {0:0.06,1:0.043529412,2:0.040560748,3:0.021023622,4:0.019090909,5:0.01729927,6:0.01729927,7:0.027857143,8:0.064155844,9:0.084615385,10:0.135135135,11:0.135135135,12:0.135135135,13:0.135135135,14:0.135135135,15:0.135135135,16:0.135135135,17:0.135135135,18:0.084615385,19:0.06,20:0.064516129,21:0.084615385,22:0.084615385,23:0.074516129}

        q = {0:20,1:30,2:40,3:50,4:50,5:60,6:60,7:60,8:70,9:70,10:70,11:70,12:70,13:70,14:80,15:80,16:80,17:80,18:90,19:90}


        count = 0
        long = 5
        while sum(pop[self.arrive:self.arrive + long + 1]) + popAm < self.duiChang:
            long += 5
            if self.arrive + long + 1 > 1440:
                return 0
        chengBen = round(max(long/10,self.duiChang/10)) + q[random.randint(0,19)]
        shouYi = 0
        i = 30
        tic = round(self.arrive/60+0.5)
        for times in range(5):
            while i < chengBen:
                if random.random() > p[tic]*1.2:
                    i += 1
                else:
                    if i + 25 < chengBen:
                        i += 25
                        shouYi += 25
                    else:
                        shouYi += chengBen - i
                        i = chengBen
            if shouYi > chengBen - round(max(long/10,self.duiChang/10)):
                count += 1
        if count >= 3:
            return 0
        else:
            return 1




def main():
    duiLie = []
    ta = buildT(9)
    pop = buildP(9)
    #hang = buildH()
    #plt.plot(range(len(hang)),hang)
    #plt.show()
    #plt.plot(range(len(ta)),ta)
    #plt.show()
    #plt.plot(range(len(pop)),pop)
    #plt.show()
    count = 0
    #popMax = 5
    popMax = 10
    taxiAm = 0
    popAm = 0
    dengdai = [0]*24*60
    likai = [0]*24*60
    while count < 24*60:
        taxiAm = ta[count]
        popAm += pop[count]
        for i in range(taxiAm):
            exec('t{0}_{1} = taxi({2},{0},"{0}_{1}")'.format(count,i,len(duiLie)))
            if len(duiLie) > 560:
                exec('t{0}_{1}.leave = {0}'.format(count,i))
                exec('t{0}_{1}.judge = 0'.format(count,i))
                likai[count] += 1
                with open('data.txt','a') as f:
                    exec("f.write(str(t{0}_{1}.duiChang)+','+str(t{0}_{1}.arrive)+','+str(t{0}_{1}.leave)+','+str(t{0}_{1}.name)+','+str(t{0}_{1}.judge))".format(count,i))
                    f.write('\n')
            else:
                if eval('t{0}_{1}.judge({2},{3})'.format(count,i,pop,popAm)):
                    exec('duiLie.append(t{0}_{1})'.format(count,i))
                    exec('t{0}_{1}.judge = 1'.format(count,i))
                    dengdai[count] += 1
                else:
                    exec('t{0}_{1}.leave = {0}'.format(count,i))
                    exec('t{0}_{1}.judge = 0'.format(count,i))
                    likai[count] += 1
                    with open('data.txt','a') as f:
                        exec("f.write(str(t{0}_{1}.duiChang)+','+str(t{0}_{1}.arrive)+','+str(t{0}_{1}.leave)+','+str(t{0}_{1}.name)+','+str(t{0}_{1}.judge))".format(count,i))
                        f.write('\n')
        if len(duiLie) <= popMax and popAm > 0:
            popAm -= popMax
            if popAm < 0:
                popAm = 0
            for i in duiLie:
                i.leave = count
                duiLie.remove(i)
                with open('data.txt','a') as f:
                    f.write(str(i.duiChang)+','+str(i.arrive)+','+str(i.leave)+','+str(i.name)+','+str(i.judge)+'\n')
        elif len(duiLie) > popMax and popAm > popMax:
            popAm -= popMax
            for i in duiLie[0:popMax]:
                i.leave = count
                duiLie.remove(i)
                with open('data.txt','a') as f:
                    f.write(str(i.duiChang)+','+str(i.arrive)+','+str(i.leave)+','+str(i.name)+','+str(i.judge)+'\n')
        else:
            popAm = 0
            for i in duiLie[0:popAm]:
                i.leave = count
                duiLie.remove(i)
                with open('data.txt','a') as f:
                    f.write(str(i.duiChang)+','+str(i.arrive)+','+str(i.leave)+','+str(i.name)+','+str(i.judge)+'\n')
        if popAm > 30*popMax:
            popAm -= round((popAm-30*popMax)*random.random())
        #plt.scatter(count,len(duiLie),1,'red')
        #plt.scatter(count,popAm,1,'black')
        count += 1
        print(count)
    #plt.legend(['taxi','passenger'])
    #plt.show()
    #dengdai = np.array(dengdai)
    #likai = np.array(likai)
    #print(dengdai.sum())
    #print(likai.sum())
    #plt.plot(range(1440),dengdai+likai,color = 'red')
    #plt.plot(range(1440),dengdai,color = 'black')
    #plt.legend(['leave','wait'])
    #plt.show()
    #plt.plot(range(1440),dengdai/(dengdai+likai+1))
    #plt.show()


if __name__ == '__main__':
    main()