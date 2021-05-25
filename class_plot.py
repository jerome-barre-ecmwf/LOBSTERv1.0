#!/usr/bin/env python3
import sys
import os

#import matplotlib.pyplot as plt

#from mpl_toolkits.basemap import Basemap,cm

import numpy as np
import scipy as sp

#import scipy.ndimage
#import metview as mv
import matplotlib.pyplot as pl
from mpl_toolkits.basemap import Basemap
#basemap is deprecated this needs to be changed to geopandas or cartopy
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
#import matplotlib.colors as mcolors


#from matplotlib import cm
#import scipy.stats as stats
#from datetime import datetime, timedelta
#from scipy.interpolate import RegularGridInterpolator


#local functions (not everything is necessary)
from odb import *
from geo import *
from dat import *
from utl import *
from clc import *

##################################

###input params
date=sys.argv[1]
window_len=sys.argv[2]
dir_data=sys.argv[3]
dir_plot=sys.argv[4]


file_stats=dir_data+"st_bin_"+date+"_w"+str(window_len)+"days.npz"

#############
#make the classification per zone
# fgd_lp, obs_lp, mod_lp and lon,lat are needed


#############
#get the gold cmap as in the paper (Barre et al., 2021 ACP)
minColor = 0.5
maxColor = 1.0
gold = plts().truncate_colormap(pl.get_cmap("BrBG_r"), minColor, maxColor)
#############

#dots size
exp=5
base=10

#areas list
list_region=['global','europe','northam','mideast']

for area in list_region:

    cnt_thrsh=3
    cnt,lon,lat,obs,err,fgd,mod,fgd_lp,obs_lp,mod_lp = utl().load_file(file_stats,cnt_thrsh)


    m,milo,malo,mila,mala = geo().base_region(area)

    cnt,lon,lat,obs,err,mod,fgd_lp,obs_lp,mod_lp = geo().cut_geo_multi_list(cnt,lon,lat,obs,err,mod,fgd_lp,obs_lp,mod_lp,milo,malo,mila,mala)

    bx,by=m(lon,lat)

    ths=err#-0.005*obs
    out_lab = clc().get_filt_ths(fgd_lp,ths)
    #out_lab = get_filt_sig(fgd_lp,3.0)

    fgd_lp=fgd_lp[out_lab==-1]
    obs_lp=obs_lp[out_lab==-1]
    mod_lp=mod_lp[out_lab==-1]
    by=by[out_lab==-1]
    bx=bx[out_lab==-1]
    cnt=cnt[out_lab==-1]

    quad=clc().get_class_quadrants(obs_lp,mod_lp)
    #dist_norm=np.sqrt(obs_lp**2+mod_lp**2)
    dist_norm=abs(fgd_lp)
    #make the classification plot

    fig = pl.figure(0,figsize=(15, 7))


    gs = GridSpec(nrows=6, ncols=2, width_ratios=[1.5,0.25], height_ratios=[1,0.1,0.1,0.1,0.1,1])
    ax11 = fig.add_subplot(gs[:, 0])
    m.drawcoastlines(linewidth=1,color='grey')
    m.drawcountries(linewidth=0.5,color='grey')
    m.drawstates(linewidth=0.25,color='grey')

    ax21, ax22, ax23, ax24, ax25, ax26= [fig.add_subplot(gs[i, 1]) for i in range(6)]
    ax21.set_visible(False)
    ax26.set_visible(False)


    o1 = np.argsort(dist_norm[quad==1])
    o2 = np.argsort(dist_norm[quad==2])
    o3 = np.argsort(dist_norm[quad==3])
    o4 = np.argsort(dist_norm[quad==4])

    k1=ax11.scatter(bx[quad==1][o1],by[quad==1][o1],s=cnt[quad==1][o1]*exp+base,c=dist_norm[quad==1][o1],edgecolor='None',cmap=cm.Reds,vmin=0,vmax=75)
    k2=ax11.scatter(bx[quad==2][o2],by[quad==2][o2],s=cnt[quad==2][o2]*exp+base,c=dist_norm[quad==2][o2],edgecolor='None',cmap=cm.Greens,vmin=0,vmax=75)
    k3=ax11.scatter(bx[quad==3][o3],by[quad==3][o3],s=cnt[quad==3][o3]*exp+base,c=dist_norm[quad==3][o3],edgecolor='None',cmap=cm.Blues,vmin=0,vmax=75)
    k4=ax11.scatter(bx[quad==4][o4],by[quad==4][o4],s=cnt[quad==4][o4]*exp+base,c=dist_norm[quad==4][o4],edgecolor='None',cmap=gold,vmin=0,vmax=75)

    ax11.set_title('End of 30 day window date: '+date)

    cbar1=pl.colorbar(k1,cax=ax22,orientation='horizontal',extend='both')
    cbar1.set_label('High Obs (ppb)')

    cbar2=pl.colorbar(k2,cax=ax23,orientation='horizontal',extend='both')
    cbar2.set_label('High Fcst (ppb)')

    cbar3=pl.colorbar(k3,cax=ax24,orientation='horizontal',extend='both')
    cbar3.set_label('Low Obs (ppb)')

    cbar4=pl.colorbar(k4,cax=ax25,orientation='horizontal',extend='both')
    cbar4.set_label('Low Fcst (ppb)')

    pl.tight_layout()

    #pl.show()
    #exit()
    pl.savefig(dir_plot+date+'_'+area)
    pl.close()

exit()
