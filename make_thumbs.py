#!/bin/python
import argparse
import os
from pathlib import Path
## A POSIX variable
#OPTIND=1         # Reset in case getopts has been used previously in the shell.

## Initialize our own variables:
#str outdir="."
#str inputfile=""
#str interval_secs=0
#str starttime=0
#endtime=0
#average=0

parser = argparse.ArgumentParser()
parser.add_argument('-f', metavar='inputfile', type=str, action='store',
                    help='inputfile', required=True)
parser.add_argument('-d', metavar='output_directory', type=str, default=".",
                    help='output_directory (. is the default)')
parser.add_argument('-i', metavar='interval_secs', type=float, action='store',
                    help='interval_secs',required=True)
parser.add_argument('-s', metavar='starttime', type=float, action='store',
                    help='starttime_secs',default=0.0)
parser.add_argument('-e', metavar='endtime', type=float, action='store',
                    help='endtime_secs',default=0.0)
args = parser.parse_args()
#args, unknown = parser.parse_known_args()
inputfile = args.f
endtime = args.e
interval_secs = args.i
print(args)

#show_help ()
#{
    #echo "   -h (show help)"
    #echo "   -f inputfile"
    #echo "   -d output_directory ('$outdir' is the default)"
    #echo "   -i interval_secs"
    #echo "   -s starttime_secs"
    #echo "   -e endtime_secs"
    #echo "   -a total_images_averaged_over_the_duration_or_start_stop_time (will override interval_secs)"
#}

#while getopts "h?f:i:s:e:a:d:" opt; do
    #case "$opt" in
    #h|\?)
        #show_help
        #exit 0
        #;;
    #f)  inputfile=$OPTARG
        #;;
    #d)  outdir=$OPTARG
        #;;
    #i)  interval_secs=$OPTARG
        #;;
    #s)  starttime=$OPTARG
        #;;
    #e)  endtime=$OPTARG
        #;;
    #a)  average=$OPTARG
        #;;
    #esac
#done

#shift $((OPTIND-1))

#[ "$1" = "--" ] && shift

#if [ -z $inputfile ]; then
   #echo We need a filename to work on
   #show_help
   #exit 1
#fi

if endtime == 0:
   ## When used to calculate average interverals or end time is not defined...
    endtime=os.system("ffprobe -i "+inputfile+' -show_entries format=duration -v quiet -of csv="p=0" '+"| sed 's/\..*//'")
    print(endtime)
#fi

#if [ $average -gt 0 ]; then
   #let duration=endtime-starttime
   #let interval_secs=duration/average
#fi

#if [ $interval_secs -eq 0 ]; then
   #echo We need interval in seconds to work on
   #show_help
   #exit 1
#fi


## Get the filename sans directory...
#filename=`echo $inputfile | sed 's/.*\///'`

filename=Path(inputfile).stem
print(filename)
## Drop off the filename extesion...
#filename="${filename/.mp4/}"
print("ffmpeg -loglevel panic -i +"+inputfile+" -ss $starttime -t $endtime -f image2 -qscale 2 $filename-%d.jpeg -deinterlace -r "+ str(1/interval_secs))
## Create sequence and use the filename for the jpegs to avoid collision with other jpeg processing...
#ffmpeg -loglevel panic -i $inputfile -ss $starttime -t $endtime -f image2  -r 1/$interval_secs -qscale 2 $filename-%d.jpeg -deinterlace 
##fps=1/$interval_secs 

## Get a listing of the thumbnail filenames...
#arr=( $(ls $filename*.jpeg) )
## Number of filenames
#qnt=${#arr[@]}
## First filename will be #1..
#i=1
#while [ $i -le $qnt ]; do
    #let totalsec=`echo "$i*$interval_secs" | bc`
##    $echo $totalsec
    ##i*interval_secs
    #let timestampsecs=`echo "$totalsec+$starttime" | bc`
    ##totalsec+starttime
    #let sec=`echo "($timestampsecs % 60)" | bc`
    ##(timestampsecs % 60)
    #let min=`echo "($timestampsecs % 3600)/60" | bc`
    ##(timestampsecs % 3600)/60
    #let hour=`echo "($timestampsecs/3600)" | bc`
    ##timestampsecs/3600
    #thumb_filename=$(printf "%s-%02d_%02d_%02d-%d.jpeg" "$filename" "$hour" "$min" "$sec" "$interval_secs")
    #echo $thumb_filename
    #mv $filename-$i.jpeg $outdir/$thumb_filename
    #let i=i+1
#done
