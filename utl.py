#!/usr/bin/env python3

'''
LOBSTER v1.0 (Local OBServation-based Tracking of Emission that are misReported) 
ECMWF Jerome Barre 2020-2021

Misc. helper functions

https://acp.copernicus.org/articles/21/5117/2021/
'''

import sys
import os
import numpy as np
import matplotlib.colors as mcolors

class utl(object):
 def get_list(self):

   if len(sys.argv) < 2:
    print >>sys.stderr, 'Usage: ', sys.argv[0], ' bufr_in'
    sys.exit(1)
   else:
    if len(sys.argv)==2:
     if not os.path.isfile(sys.argv[1]):
       list_f = os.listdir(sys.argv[1])
       list_f = [ sys.argv[1]+s for s in list_f ]
     else:
       list_f=[str(sys.argv[1])]
    else:
     list_f=sys.argv[1:len(sys.argv)]

    print(list_f)

    lf=len(list_f)

    return list_f, lf


 def make_file_list(self,prefix,listdate):
   file_list=[]
   for date in listdate:
       file_list.append(prefix+date)

   return file_list


 def load_file(self,file_stats,ct):

  coef=1E9

  db=np.load(file_stats)

  count=db['count']

  lat=db['lat']
  lon=db['lon']

  obs_m=db['obs_m']*coef
  err_m=db['err_m']*coef
  fgd_m=db['fgd_m']*coef
  mod_m=db['mod_m']*coef

  fgd_lp_m=db['fgd_lp_m']*coef
  obs_lp_m=db['obs_lp_m']*coef
  mod_lp_m=db['mod_lp_m']*coef

  ########

  lat=lat[count>=ct]
  lon=lon[count>=ct]

  obs_m=obs_m[count>=ct]
  err_m=err_m[count>=ct]
  fgd_m=fgd_m[count>=ct]
  mod_m=mod_m[count>=ct]

  fgd_lp_m=fgd_lp_m[count>=ct]
  obs_lp_m=obs_lp_m[count>=ct]
  mod_lp_m=mod_lp_m[count>=ct]

  count=count[count>=ct]

  return count,lon,lat,obs_m,err_m,fgd_m,mod_m,fgd_lp_m,obs_lp_m,mod_lp_m


 def gen_rdm(self):
   rdm = open("save/README","w")
   L = "The csv files contain the LObsTER CH4 detection points as described in Barre et al., 2021 (ACP) \n\n The file name contains the date, which is the end of the 30day window used to perform the detection (that includes filtering and classification)\n\n'lon':longitude degrees \n'lat':latitude degrees\n'N_occurences':Number of occurences of satellite observation overpass in the data point\n'magnitude':Magnitude of the detection in part per billion (ppb) of CH4\n'category':Category of the detection\n\n1 = high observations (red in Barre et al.,2021): where filtered observations values are higher than filtered forecast absolute values. This class is representative of high XCH4 values detected by TROPOMI that are not seen as high or at all in the forecasts. These are likely originating from emissions that are not reported or under-estimated in the inventories. However, high observation categorisation may also be caused by poor quality observations due to albedo and scattering issues.\n2 = high forecasts (green in Barre et al.,2021): where filtered forecast values are higher than filtered observations absolute values. This class is representative of high CH4 values in the forecasts but not seen as strong or at all in the TROPOMI XCH4 High forecasts categorized data points are likely originating from emissions that are over-estimated or no longer being produced or even mis-located in the emission inventory.\n3 = low observations (blue in Barre et al.,2021): where filtered observations values are lower than filtered forecast absolute values. This class is representative of locally low XCH4 values detected by TROPOMI but are not seen to be as low or at all in the forecasts. Poor-quality observations influenced by low surface albedo likely fall in that category.\n4 = low forecasts (gold in Barre et al.,2021): where filtered forecast values are lower than filtered observations absolute values. This class is representative of low XCH4 values in the forecasts but not seen as low or at all in the TROPOMI XCH4 retrievals. This category has generally much fewer data points very sparsely distributed. Orography could be a reason for data points to fall in that category, i.e., model surface height value that are higher than the observation value. Further developments of the method will likely use orography to improve the filtering.\n\nReferences:\nBarré, J., Aben, I., Agustí-Panareda, A., Balsamo, G., Bousserez, N., Dueben, P., Engelen, R., Inness, A., Lorente, A., McNorton, J., Peuch, V.-H., Radnoti, G., and Ribas,R.: Systematic detection of local CH4 emissions anomalies combining satellite measurements and high-resolution forecasts, Atmos. Chem. Phys.,https://doi.org/10.5194/acp-2020-550, 2021.\n\ncontact: jerome.barre@ecmwf.int or barre@ucar.edu" 
   rdm.write(L)
   rdm.close()  


class plts(object):
 #truncated colormap
 def truncate_colormap(self,cmap, minval=0.0, maxval=1.0, n=-1):
    if n == -1:
        n = cmap.N
    new_cmap = mcolors.LinearSegmentedColormap.from_list(
         'trunc({name},{a:.2f},{b:.2f})'.format(name=cmap.name, a=minval, b=maxval),
         cmap(np.linspace(minval, maxval, n)))
    return new_cmap

 ##############
 ## e.g. get the gold cmap as in the paper
 #minColor = 0.5
 #maxColor = 1.0
 #gold = plts().truncate_colormap(pl.get_cmap("BrBG_r"), minColor, maxColor)
 ##############

