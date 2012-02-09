#!/bin/sh
hostname=$1
name=$2
local_rrd=$3
if [ -n "$hostname" -a -n "$name" -a -n "$local_rrd" ]; then
  mkdir -p $(dirname $local_rrd)
  name=${name/\.rrd/}
  echo "rrd get $name" | nc $hostname 43698 >"$local_rrd"
  exit 0
elif [ -n "$hostname" ]; then
  echo "rrd list" | nc $hostname 43698
  exit 0
fi
exit 111
