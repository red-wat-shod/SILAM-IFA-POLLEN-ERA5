DSET /home/vasily/POLLEN/SILAM-IFA-POLLEN_ERA5/out/%y4%m2/pollen_%y4%m2%d2.nc4
DTYPE NETCDF
UNDEF -999998980358144.
OPTIONS TEMPLATE
TDEF time       9 LINEAR      00:00Z01mar2024  6hr     
XDEF lon      67 LINEAR   27.0000    0.5000
YDEF lat      81 LINEAR   35.0000    0.5000
ZDEF height    10 LEVELS     12.5     50.0    125.0    275.0    575.0   1150.0   2125.0   3725.0   5725.0   7725.0
VARS   19
dz=>dz   10  z  Layer thickness [m]
daymean_temp2m=>daymean_temp2m                                 0   t,y,x daily mean temperature 2m [K] 
temp_2m_acc=>temp_2m_acc                                       0   t,y,x 2m temperature accum [K sec] 
heatsum_POLLEN_RAGWEED_m18=>heatsum_pRAG                       0   t,y,x heatsum RAGWEED_m18
heatsum_POLLEN_BIRCH_m22=>heatsum_pBIR                         0   t,y,x heatsum BIRCH_m22
poll_tot_m2_POLLEN_RAGWEED_m18=>poll_tot_m_pRAG                0   t,y,x Pollen total per m2 RAGWEED_m18
poll_tot_m2_POLLEN_BIRCH_m22=>poll_tot_m_pBIR                  0   t,y,x Pollen total per m2 BIRCH_m22
Poll_Rdy2fly_POLLEN_RAGWEED_m18=>Poll_Rdy2f_pRAG               0   t,y,x Ready to fly pollen RAGWEED_m18
Poll_Rdy2fly_POLLEN_BIRCH_m22=>Poll_Rdy2f_pBIR                 0   t,y,x Ready to fly pollen BIRCH_m22
pollen_corr_POLLEN_RAGWEED_m18=>pollen_cor_pRAG                0   t,y,x Climate correction of total pollen RAGWEED_m18
pollen_corr_POLLEN_BIRCH_m22=>pollen_cor_pBIR                  0   t,y,x Climate correction of total pollen BIRCH_m22
poll_left_POLLEN_RAGWEED_m18=>poll_left_pRAG                   0   t,y,x Pollen left fraction RAGWEED_m18
poll_left_POLLEN_BIRCH_m22=>poll_left_pBIR                     0   t,y,x Pollen left fraction BIRCH_m22
cnc_POLLEN_RAGWEED_m18=>cnc_pRAG                              10  t,z,y,x  Concentration in air RAGWEED_m18
cnc_POLLEN_BIRCH_m22=>cnc_pBIR                                10  t,z,y,x  Concentration in air BIRCH_m22
dd_POLLEN_RAGWEED_m18=>dd_pRAG                                 0   t,y,x Cocktail dry deposition RAGWEED_m18
dd_POLLEN_BIRCH_m22=>dd_pBIR                                   0   t,y,x Cocktail dry deposition BIRCH_m22
wd_POLLEN_RAGWEED_m18=>wd_pRAG                                 0   t,y,x Cocktail wet deposition RAGWEED_m18
wd_POLLEN_BIRCH_m22=>wd_pBIR                                   0   t,y,x Cocktail wet deposition BIRCH_m22
ENDVARS
