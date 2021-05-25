#!/usr/bin/env python3
'''
LOBSTER v1.0 (Local OBServation-based Tracking of Emission that are misReported) 
ECMWF Jerome Barre 2020-2021

ODB functions

https://acp.copernicus.org/articles/21/5117/2021/
'''

import sys
import os
import numpy as np
import metview as mv
import pandas as pd

#db retrieve from mars
class odb(object):
 def get_odb(self,list_date,list_file,exp,stype,stream,repor,redo):

  for date,ofile in zip(list_date,list_file):
     if not os.path.isfile(ofile):
       request=("retrieve,\n"+
       "class=rd,\n"+
       "date="+date+",\n"+
       "expver="+exp+",\n"+
       "reportype="+repor+",\n"+
       "stream="+stream+",\n"+
       "type="+stype+",\n"+
       "time=00:00:00/12:00:00,\n"+
       "format=odb,\n"+
       "target='"+ofile+"'")
       os.system("rm -f request")
       f= open("request","w")
       f.write(request)
       f.close()
       os.system('mars request')
     elif redo==True or os.path.getsize(ofile)==0:
       request=("retrieve,\n"+
       "class=rd,\n"+
       "date="+date+",\n"+
       "expver="+exp+",\n"+
       "reportype="+repor+",\n"+
       "stream="+stream+",\n"+
       "type="+stype+",\n"+
       "time=00:00:00/12:00:00,\n"+
       "format=odb,\n"+
       "target='"+ofile+"'")
       os.system("rm -f request")
       f= open("request","w")
       f.write(request)
       f.close()
       os.system('mars request')

 #clean odb
 def clean_odb(self,list_file):
  for ofile in list_file:
    os.system('rm -f '+ofile) 

 #db read
 def get_db(self,file_odb,satid,varno):

  db = mv.read(file_odb)

  try:
    db = mv.odb_filter( odb_query    =    "select  "+
                    "varno@body, satellite_instrument@sat, satellite_identifier@sat, "+
                    "lat@hdr, lon@hdr, time@hdr, date@hdr, "+ 
                    "obs_error@errstat, "+
                    "obsvalue@body, fg_depar@body, "+
                    " where varno@body == "+str(varno)+" and satellite_identifier@sat == "+str(satid),
                    odb_data    = db )

    tim = mv.values(db,"time@hdr")
    dat = mv.values(db,"date@hdr")
    lat = mv.values(db,"lat@hdr")
    lon = mv.values(db,"lon@hdr")
    obs = mv.values(db,"obsvalue@body")
    err = mv.values(db,"obs_error@errstat")
    fgd  = mv.values(db,"fg_depar@body")


  except:
    tim = []
    dat = []
    lat = []
    lon = []
    obs = []
    err = []
    fgd = []

  df = pd.DataFrame({'latitude':lat,'longitude':lon,'date':dat,'time':tim,'obsval':obs,'obserr':err,'departure':fgd})
  return df


 #db concat
 def concat_db(self,list_f,sat,var):
   #concatenate ODB

   cf=0
   #sat=64
   #var=188
  
   for file_odb in list_f:
  
    df=self.get_db(file_odb,sat,var)
    #day = get_lintime(dat,tim)
   
   if cf == 0:
     c_df=df
   else:
     c_df=pd.concat([df,c_df])  
 
   cf+=1 

   return c_df




