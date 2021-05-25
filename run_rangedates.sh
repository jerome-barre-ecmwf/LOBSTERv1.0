#LOBSTER v1.0 (Local OBServation-based Tracking of Emission that are misReported) 
#ECMWF Jerome Barre 2020-2021 
#scripts to run the monitoring job

module load python3

window_len=30
dir_data=work/
dir_save=save/
expver=hjzx #hblp

[ ! -d ${dir_data} ] && mkdir ${dir_data}
[ ! -d ${dir_save} ] && mkdir ${dir_save}

dstart=$1
dend=$2

dstart=$(date -d $dstart +%Y%m%d)
dend=$(date -d $dend +%Y%m%d)

echo $dstart $dend

while [[ $dstart -le $dend ]] 
do

ddate=$(date -d $dstart +%Y-%m-%d)
echo $ddate
./retrieve_filter.py $ddate $window_len $expver $dir_data
./class_save.py $ddate $window_len $dir_data $dir_save
./class_plot.py $ddate $window_len $dir_data $dir_save

dstart=$(date -d"$dstart + 1 day" +"%Y%m%d")

done
