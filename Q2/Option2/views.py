#import redis cache model
from django.core.cache import cache
rom django.shortcuts import HttpResponseRedirect,HttpResponse,JsonResponse
from django.utils import timezone
from .models import ShortUrl
import re
import redis

baseList = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

# core algorithm, make id to base-64 num 
def changeBase(n,b):

    x,y = divmod(n,b)
    print(x,y)
    if x>0:
        return changeBase(x,b) + baseList[y]
    else:
        return baseList[y]

# addShortURL function
def addShortUrl(request):
    createdtime = timezone.now()
    if (request.method == 'POST'):
        #Get Parameter URL - original web site url
        url = request.POST.get('url')
        #Declare response format containg original url and shortenurl
        response = {"url": url, "shortenUrl": None}
        #Regex inspect original web site url
        res=re.search("^(http|https|ftp)\://([a-zA-Z0-9\.\-]+(\:[a-zA-Z0-9\.&%\$\-]+)*@)?"
                      "((25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\."
                      "(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\."
                      "(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\."
                      "(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])|"
                      "([a-zA-Z0-9\-]+\.)*[a-zA-Z0-9\-]+\.[a-zA-Z]{2,4})(\:[0-9]+)?"
                      "(/[^/][a-zA-Z0-9\.\,\?\'\\/\+&%\$#\=~_\-@]*)*$",url)
        #If not pass inspection, response "error website, try again"
        if not res:
            response["shortenUrl"]="error website"
        else:
            try:
                #check whether there is existing original url and mapping shorturl in database by both redis id and original url, if yes, response the existing original url and shorturl.
                 ori_url = ShortUrl.objects.filter(ori_url=url).filter(pool='r1').values('short_url')
                 short_url = ori_url[0]['short_url']
                 response["shortenUrl"] = "http:/hostname:port/" + short_url
            except:
                #Connect to redis DB 0 to generate auto-increased sid
                 con1 = redis.StrictRedis(host='redisserverip', port=6379, db=0,password='password')
                 if con1.exists('r1') != 1:
                    con1.set('r1',1)
                    con1.incr('r1')
                 sid = int(con1.get('r1'))
                #transfer sid to based-62 num
                 tempid=changeBase(sid,62)    
                 #as we need nine-digit for shorturl id, we need combine blank digit within tempid. for example: if we get tempid= "b6", we need combine with blank digit and finally, we get "0000000b6" 
                 tempother=""
                 i = 9 - len(tempid)
                 for i in range(0,i):
                     tempother += str(0)
                 short_url=tempother + tempid
                 # Connect to redis DB 1 to insert new shorturl-original web site url mapping
                 con2 = redis.StrictRedis(host='redisserverip', port=6379, db=1,password='password')
                 con2.set(short_url,url)
                 # Create the same entry into database with redis instance id, shorturl and orginal url as unique constraint
                 ShortUrl.objects.create(pool='r1',short_url=short_url,ori_url=url)
                 # Update response message with new shorturl.
                 response["shortenUrl"] = "http:/hostname:port/" + short_url
        return JsonResponse(response)
    if (request.method == "GET"):
        return HttpResponse("No get method")

#get shorturl from redis and have a 302 redirection.
def url(request,url):
    if request.method=="GET":
        #Connect to redis DB 1 and check whether related shortul in existing key, if yes, 302 redirect to related key value url
        r = redis.StrictRedis(host='redisserverip', port=6379, db=1,password='password')
        if r.exists(url) != 1:
           original_url = int(r.get('url'))
        if not original_url or not original_url:
            return HttpResponse("no shortenURL")
        return HttpResponseRedirect(original_url)
    if request.method=="POST":
        return HttpResponse("Request error")