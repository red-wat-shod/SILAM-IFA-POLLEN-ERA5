#!/bin/bash
. ./environment
set -u
set -e
set -o pipefail
#cd $scriptdir
#START_TIME=`date -u -d $fcdate +"%Y %m %d 00 00 0."`
#export START_TIME


#runFailed=false

mkdir -p $LOGDIR/${fcdate}
outdump=$LOGDIR/${fcdate}/outlog_`date -u +"%Y%m%d%H%M%S"`.log

/usr/bin/time -v $silam_binary PollenDebug.ctrl 2>&1 | tee $outdump || runFailed=true








