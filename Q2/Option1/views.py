from django.shortcuts import HttpResponseRedirect,HttpResponse,JsonResponse
from django.utils import timezone
from .models import ShortUrl
import re

baseList = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

# core algorithm, make id to base-62 num 
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
            response["shortenUrl"]="error website, try again"
        else:
            #!!check whether there is existing original url and mapping shorturl in database by orginal url, if yes, response the existing original url and shorturl.
            try:
                 ori_url = ShortUrl.objects.filter(ori_url=url).values('short_url')
                 short_url = ori_url[0]['short_url']
                 response["shortenUrl"] = "http:/hostname:port/" + short_url
            except:
                 #if no found url, create the empty entry in shorturl table.
                 res = ShortUrl.objects.create(createdtime=createdtime)
                 #use PostGreSQL auto-crement id build-in feature to get unique id.
                 n=res.id
                 #transfer id to based-62 num
                 tempid=changeBase(n,62)
                 #as we need nine-digit for shorturl id, we need combine blank digit within tempid. for example: if we get tempid= "b6", we need combine with blank digit and finally, we get "0000000b6"
                 tempother=""
                 i = 9 - len(tempid)
                 for i in range(0,i):
                     tempother += str(0)
                 short_url=tempother + tempid
                 #Update short_url and ori_url based on above information.
                 ShortUrl.objects.filter(id=n).update(short_url=short_url,ori_url=url)
                 #Update response message with new shorturl.
                 response["shortenUrl"] = "http:/hostname:port/" + short_url
        return JsonResponse(response)

    if (request.method == "GET"):
        return HttpResponse("No get method")

#get shorturl and have a 302 redirection.
def url(request,url):
    if request.method=="GET":
        #check whether url in existing table, if not response )"no shortenUrl", if existing, have a 302 redirection to original web site url.
        res = ShortUrl.objects.filter(short_url=url).first()
        if not res or not res.ori_url:
            return HttpResponse("no shortenURL")
        return HttpResponseRedirect(res.ori_url)
    if request.method=="POST":
        return HttpResponse("Request error")