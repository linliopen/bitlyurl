#!/bin/sh
# declare TotalNormalTypeHttpRequests counter "sum"
declare -i sum=0
# declare array containing mainly HTTP methods
var=("\"GET" "\"POST" "\"PUT" "\"OPTION" "\"HEAD" "\"DELETE" "\"TRACE" "\"PROPFIND" "\"CONNECT")
echo "******************************"
echo -e "HTTP request counts per HTTP request Type:\n"
# circulate the array, and calucate and print count of each HTTP methods
for str in ${var[@]}; do

 temp=`grep -c $str ./access.log`
 echo -e "$str\": \c"
 echo $temp
 let sum+=$temp
done
echo "******************************"
echo -e "TotalNormalTypeHttpRequests: \c"
### print TotalNormalTypeHttpRequests within all HTTP methods
echo $sum
# declare TotalRequestCounts counter "totalreq", and calucate counts of all requests.
totalreq=`awk '{print NR}' access.log|tail -n1`
# declare TotalBADRequest, and let TotalRequestCounts"totalreq" - TotalNormalTypeHttpRequests"sum" to get left requests, all left lines are 400 error related badrequests.
badreq=`expr $totalreq - $sum`
### print counts of TotalBADRequests.
echo -e "TotalBADRequest: \c"
echo $badreq
### print counts of TotalRequestCounts.
echo -e "TotalRequestCounts(NormarlRequests+BADRequests): \c"
echo $totalreq
echo "******************************"
