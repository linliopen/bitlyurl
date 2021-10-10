#!/bin/sh
# sort top 5 source ips made the requests, save them into array
IP=$(cat ./access.log|awk '{print $1}' |sort -nr|uniq -c |sort -nr|head -5|awk '{print $2}')
# request to third party findip website to query and print source ip location
for i in $IP
do
   curl https://www.find-ip.net/ip-locator?ip=$i -s |  grep -m 1 "title\:" | head -1
done
