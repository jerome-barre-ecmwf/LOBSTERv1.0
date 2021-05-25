#!/usr/bin/env python3
'''
LOBSTER v1.0 (Local OBServation-based Tracking of Emission that are misReported) 
ECMWF Jerome Barre 2020-2021

Time and date helper functions

https://acp.copernicus.org/articles/21/5117/2021/
'''

import sys
import os
import numpy as np
from datetime import datetime, timedelta

class dat(object):

 def get_date_list(self,end_date,ndays):

   date_generated = [(end_date - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(0, ndays)]

   return date_generated
    
 def roll_dates(self,start,end,ndays):

   start_date = datetime.strptime(start, "%Y-%m-%d")
   end_date = datetime.strptime(end, "%Y-%m-%d")

   delta = end_date - start_date
   list_dates=[]
   for i in range(delta.days + 1):
      day = start_date + timedelta(days=i)
      list_dates.append(get_date_list(day,ndays))

   return list_dates

 def single_date_window(self,date,ndays):
   date_time = datetime.strptime(date, "%Y-%m-%d")
   list_dates=self.get_date_list(date_time,ndays)
   return list_dates

 def get_lintime(self,date,time):
  lintime=[]
  for i in range(len(date)):
   year=str(date[i])[0:4]
   month=str(date[i])[4:6]
   day=str(date[i])[6:8]
 
   if len(str(time[i]))==5:
      hour="00"
      minu=str(time[i])[0:1]
      secs=str(time[i])[1:3]
   if len(str(time[i]))==6:
      hour="00"
      minu=str(time[i])[0:2]
      secs=str(time[i])[2:4]
   if len(str(time[i]))==8:
      hour=str(time[i])[0:2]
      minu=str(time[i])[2:4]
      secs=str(time[i])[4:6]
   elif len(str(time[i]))==7:
      hour=str(time[i])[0:1]
      minu=str(time[i])[1:3]
      secs=str(time[i])[3:5]
 
   sdate=datetime(2019,1,1,1,1,1)
   cdate=datetime(int(year),int(month),int(day),int(hour),int(minu),int(secs))
 
   ddate = cdate - sdate

   lintime.append(ddate.days+ddate.seconds/86400.)
 
  lintime=np.array(lintime)

  return lintime

 def sort_list(self, par, time):

    time,sort_par = zip(*sorted(zip(time, par)))

    return sort_par
