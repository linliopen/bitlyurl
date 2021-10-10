# Q1-a.)
- Count the total number of HTTP requests recorded by this access logfile.   [Shell Script with annotation](https://github.com/wingying/bitly/blob/main/Q1/http_count.sh)
- Script Result:
```
******************************
HTTP request counts per HTTP request Type:

"GET": 67193
"POST": 18100
"PUT": 91
"OPTION": 1
"HEAD": 531
"DELETE": 0
"TRACE": 0
"PROPFIND": 1
"CONNECT": 34
******************************
TotalNormalTypeHttpRequests: 85951
TotalBADRequest: 133
TotalRequestCounts(NormarlRequests+BADRequests): 86084
******************************
```

# Q1-b.)
- Find the Top 10 hosts that made the most requests from 2019-06-10 00:00:00 up to and including 2019-06-19 23:59:59 [Shell Script with annotation](https://github.com/wingying/bitly/blob/main/Q1/top_hosts.sh)
- Script Result:
```
730 1.222.44.52
730 118.24.71.239
723 119.29.129.76
486 148.251.244.137
440 95.216.38.186
440 136.243.70.151
437 213.239.216.194
436 5.9.71.213
436 5.189.159.208
406 5.9.108.254
```

# Q1-c.)
- Find the country that made the most requests (hint: use the source IP address as start) [Shell Script with annotation](https://github.com/wingying/bitly/blob/main/Q1/top_country.sh)
```
title: "Germany",
title: "United States",
title: "Helsinki",
title: "Shanghai",
title: "China",
```

# Q2 Designing a bit.ly like services(API only), which includes two web API endpoints
- [Architecture Diagram](https://github.com/wingying/bitly/blob/main/Architect_Diagram.pdf) 
- **`NOTE:`** Two options of architectures are designed, `Option 1` use PostGreSQL auto-creatementid to generate shorturl based unqiueid, `Option 2` leads into Redis to generate shorturl based unqiue sid. And For `Option 2`, and for Option 2, I seperate shortcurl query&redirect requests from database to redis.
- [Database Schema Option1](https://github.com/wingying/bitly/blob/main/Q2/Option1/models.py)
- [Database Schema Option2](https://github.com/wingying/bitly/blob/main/Q2/Option2/models.py)
- [Pseudo codes including urlroute, views and orm models Option 1 with annotation](https://github.com/wingying/bitly/tree/main/Q2/Option1)
- [Pseudo codes including urlroute, views and orm models Option 2 with annotation](https://github.com/wingying/bitly/tree/main/Q2/Option2)
- **CI/CD software and design considerations For each component**
```
Both Option 1 and Option 2 use Django, uswgi, nginx, PostGreSQL, the difference between Option 1 and Option 2 is that Option 1 use PostGreSQL build-in auto-createment id feature as based id of shorturl, instead Option 2 use Redis incr feature to generate based id of shorturl, and I seperate ShortUrl query&redirect requests from database to Redis in order to reduce DB direct Queries.

Currently, all softewares are deployed in linux vms. However, it would be better to deploy softwares including django+uswgi, nginx into K8s for centrely management&scaleup and scaledown. We can also use Jenkins, Github Action and Argocd or application for CICD auto-release.

According Database PostGreSQL, it has big advantage than other databases like MySQL. (For example, much more faster speed of queries, open-source with development extendible)
According middleware and loadbalancer, I use keepalived+nginx+uswgi that possible support ten thousand requests.
According to core development language, I use python3+Django3.2, as a good development backend-api frame, Django has friendly url router(easy to use regex), orm model mapping and easy for database mapping)
```

- **Core algorithm**
```
After generating unique id either using Option 1 or Option 2 mentioned above, transfer the id to base-62 num and append 9 digital num if lack digit capacity. For example, the unique generated id is "bf123", the shorturl id would be "0000bf123". The unique generated id is "1gf1", the shorturl id would be "000001gf1"
```

- **High availability**
```
The Architecture display that loadbalancer, middleware, application and databases, all above support high availability and no single point of failure.
```

- **Scalability**
```
Nginx and App Server are scalable, and this architecture is easily to support 1000+ req/s within mutiple nginx/ugwsi worker and threads, and Redis Cache.
```

- **State any assumptions/limitations of the design**
```
No obvious limitations. Need optimize for potential issue such like cache breakdown.
```



