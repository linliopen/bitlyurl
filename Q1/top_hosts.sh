#!/bin/sh
#Use sed truncate log between requested date, and then use awk command to filter, sort and obtain top 10 hosts made the requests.
sed -n '/10\/Jun\/2019:00:00:47/,/19\/Jun\/2019:23:46:35/p' ./access.log | awk '{print $1}' |sort -nr | uniq -c | sort -nr | head -n 10
