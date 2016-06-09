```shell
#benchmark.sh

Server Software:        Apache/2.2.15
Server Hostname:        site.com
Server Port:            80

Document Path:          /proof-of-concept/
Document Length:        82544 bytes
Finished 2000 requests


Server Software:        Apache/2.2.15

Concurrency Level:      1020
Server Hostname:        site.com
Server Port:            80
Time taken for tests:   127.259 seconds
Completed 1800 requests

Complete requests:      2000
Document Path:          /project-environments/
Failed requests:        3711
Document Length:        81258 bytes
   (Connect: 0, Receive: 794, Length: 2123, Exceptions: 794)

Non-2xx responses:      1333
Concurrency Level:      1020
Total transferred:      3029756 bytes
HTML transferred:       2578824 bytes
Time taken for tests:   127.260 seconds
Complete requests:      2000
Finished 2000 requests


Server Software:        Apache/2.2.15
Server Hostname:        site.com
Server Port:            80

Document Path:          /website-stress-testing/
Document Length:        85812 bytes

Concurrency Level:      1020
Time taken for tests:   127.263 seconds
Complete requests:      2000
Failed requests:        3717
   (Connect: 0, Receive: 794, Length: 2129, Exceptions: 794)
Non-2xx responses:      1344
Total transferred:      2987760 bytes
HTML transferred:       2535609 bytes
Requests per second:    15.72 [#/sec] (mean)
Time per request:       64903.893 [ms] (mean)
Time per request:       63.631 [ms] (mean, across all concurrent requests)
Transfer rate:          22.93 [Kbytes/sec] received
Requests per second:    15.72 [#/sec] (mean)
Completed 2000 requests
Failed requests:        3493
   (Connect: 0, Receive: 740, Length: 2012, Exceptions: 741)
Time per request:       64902.249 [ms] (mean)
Time per request:       63.630 [ms] (mean, across all concurrent requests)
Non-2xx responses:      1283
Transfer rate:          23.25 [Kbytes/sec] received
Completed 1200 requests
Total transferred:      3332135 bytes
HTML transferred:       2895975 bytes
Requests per second:    15.72 [#/sec] (mean)
Finished 2000 requests
Time per request:       64902.566 [ms] (mean)


Time per request:       63.630 [ms] (mean, across all concurrent requests)
Server Software:        Apache/2.2.15

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0 2965 7768.3    164   63301
Processing:   163 25290 42623.3   5919  127246
Waiting:        0 4051 6214.6   2405   65943
Total:        163 28255 42413.6   8169  127246

Percentage of the requests served within a certain time (ms)
  50%   8169
  66%  14387
  75%  24250
  80%  36754
  90%  127236
  95%  127240
  98%  127243
  99%  127244
 100%  127246 (longest request)
Transfer rate:          25.57 [Kbytes/sec] received
Server Hostname:        site.com
Server Port:            80

Document Path:          /disaster-recovery/
Document Length:        82639 bytes

Concurrency Level:      1020
Time taken for tests:   127.266 seconds
Complete requests:      2000
Failed requests:        3708
   (Connect: 0, Receive: 816, Length: 2076, Exceptions: 816)
Non-2xx responses:      1270
Total transferred:      2637821 bytes
HTML transferred:       2212537 bytes
Requests per second:    15.72 [#/sec] (mean)
Time per request:       64905.541 [ms] (mean)
Time per request:       63.633 [ms] (mean, across all concurrent requests)
Transfer rate:          20.24 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0 3666 9927.5    164   64257
Processing:   163 23811 40970.7   6091  127247
Waiting:        0 3962 5790.1   2395   80475
Total:        163 27476 41122.3   8537  127247

Percentage of the requests served within a certain time (ms)
  50%   8537
  66%  16044
  75%  23084
  80%  33843
  90%  127237
  95%  127240
  98%  127243
  99%  127245
 100%  127247 (longest request)

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0 2693 7177.8    164   63299
Processing:   163 29550 46066.5   6496  127246
Waiting:        0 4074 6870.5   2225   77288
Total:        163 32244 45655.8   8880  127246

Percentage of the requests served within a certain time (ms)
  50%   8880
  66%  17541
  75%  33361
  80%  49522
  90%  127239
  95%  127242
  98%  127244
  99%  127245
 100%  127246 (longest request)

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0 3052 8858.1    164   64253
Processing:   163 25346 42512.9   6055  127249
Waiting:        0 3654 5656.2   2175   80461
Total:        163 28399 42476.6   8163  127249

Percentage of the requests served within a certain time (ms)
  50%   8163
  66%  15193
  75%  23723
  80%  34886
  90%  127221
  95%  127244
  98%  127248
  99%  127249
 100%  127249 (longest request)
Completed 1400 requests
Completed 2000 requests
Completed 1600 requests
Finished 2000 requests


Server Software:        Apache/2.2.15
Server Hostname:        site.com
Server Port:            80

Document Path:          /it-consulting/
Document Length:        251 bytes

Concurrency Level:      1020
Time taken for tests:   127.760 seconds
Complete requests:      2000
Failed requests:        3299
   (Connect: 0, Receive: 1155, Length: 989, Exceptions: 1155)
Non-2xx responses:      1127
Total transferred:      743088 bytes
HTML transferred:       376986 bytes
Requests per second:    15.65 [#/sec] (mean)
Time per request:       65157.642 [ms] (mean)
Time per request:       63.880 [ms] (mean, across all concurrent requests)
Transfer rate:          5.68 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0 4247 13018.9    164   64255
Processing:   164 33428 49413.2   6129  127735
Waiting:        0 3287 6029.0   1637   77305
Total:        164 37674 49055.5   8713  127735

Percentage of the requests served within a certain time (ms)
  50%   8713
  66%  20276
  75%  68294
  80%  127205
  90%  127216
  95%  127701
  98%  127734
  99%  127734
 100%  127735 (longest request)
Completed 1800 requests
Completed 2000 requests
Finished 2000 requests


Server Software:        Apache/2.2.15
Server Hostname:        site.com
Server Port:            80

Document Path:          /
Document Length:        251 bytes

Concurrency Level:      1020
Time taken for tests:   133.401 seconds
Complete requests:      2000
Failed requests:        3300
   (Connect: 0, Receive: 1120, Length: 1060, Exceptions: 1120)
Non-2xx responses:      882
Total transferred:      1040555 bytes
HTML transferred:       747722 bytes
Requests per second:    14.99 [#/sec] (mean)
Time per request:       68034.542 [ms] (mean)
Time per request:       66.701 [ms] (mean, across all concurrent requests)
Transfer rate:          7.62 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0 2715 9160.3    160   64254
Processing:   163 56960 59169.2  12423  128222
Waiting:        0 2326 4821.7      0   63078
Total:        163 59675 57728.9  20604  128222

Percentage of the requests served within a certain time (ms)
  50%  20604
  66%  127220
  75%  127246
  80%  127700
  90%  127733
  95%  128215
  98%  128220
  99%  128221
 100%  128222 (longest request)


 Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   664.58ms  633.95ms   1.97s    73.71%
    Req/Sec     0.67      1.09     3.00     73.57%
  507 requests in 4.74m, 344.04MB read
  Socket errors: connect 0, read 14, write 50, timeout 256
  Non-2xx or 3xx responses: 376
Requests/sec:      1.78
Transfer/sec:      1.21MB
 Form redirects count :0
 Started downloads :0
 total socket connection errors:0
 total socket read errors:14
 total socket write errors:50
  total HTTP status codes > 399 :376
 total request timeouts:256
 
```
