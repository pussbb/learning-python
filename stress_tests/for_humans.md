```shell
$ loads-runner for_humans.TestWebSite.test_es -u 1
[====================================================================================================================================================================] 100%
Duration: 10.17 seconds
Hits: 10
Started: 2016-06-09 07:36:01.676036
Approximate Average RPS: 0
Average request time: 0.62s
Opened web sockets: 0
Bytes received via web sockets : 0

Success: 1
Errors: 0
Failures: 0


Slowest URL: http://site.com/thank-you-so-much/      Average Request Time: 0.936171

Stats by URLs:
- http://site.com/thank-you-so-much/                         Average request time: 0.936171  Hits success rate: 1.0
- http://site.com:80/                                             Average request time: 0.760891  Hits success rate: 1.0
- http://site.com:80/website-stress-testing/                      Average request time: 0.619245  Hits success rate: 1.0
- http://site.com:80/project-environments/                        Average request time: 0.576191  Hits success rate: 1.0
- http://site.com:80/it-consulting/                               Average request time: 0.573726  Hits success rate: 1.0
- http://site.com:80/proof-of-concept/                            Average request time: 0.57362   Hits success rate: 1.0
- http://site.com:80/disaster-recovery/                           Average request time: 0.565783  Hits success rate: 1.0
- http://site.com:80/thank-you-so-much                            Average request time: 0.429524  Hits success rate: 1.0
- http://site.com:80/wp-content/uploads/2016/05/JavaScript.pdf    Average request time: 0.189188  Hits success rate: 1.0


$ loads-runner for_humans.TestWebSite.test_es -u 50
[====================================================================================================================================================================] 100%
Duration: 121.07 seconds
Hits: 460
Started: 2016-06-09 07:49:52.412960
Approximate Average RPS: 3
Average request time: 5.18s
Opened web sockets: 0
Bytes received via web sockets : 0

Success: 39
Errors: 11
Failures: 0

1 occurrences of: 
    ConnectionError: HTTPConnectionPool(host='site.com', port=80): Max retries exceeded with url: /thank-you-so-much/ (Caused by NewConnectionError(': Failed to establish a new connection: [Errno 113] No route to host',))    Traceback: 
  File "/usr/lib/python2.7/unittest/case.py", line 329, in run
    testMethod()
  File "for_humans.py", line 84, in test_es
    allow_redirects=True, verify=VERIFY_SSL)
  File "/usr/lib/python2.7/dist-packages/requests/sessions.py", line 511, in post
    return self.request('POST', url, data=data, json=json, **kwargs)
  File "/usr/local/lib/python2.7/dist-packages/loads/measure.py", line 79, in request
    method, url, headers=headers, **kwargs)
  File "/usr/lib/python2.7/dist-packages/requests/sessions.py", line 468, in request
    resp = self.send(prep, **send_kwargs)
  File "/usr/local/lib/python2.7/dist-packages/loads/measure.py", line 87, in send
    res = _Session.send(self, request, **kwargs)
  File "/usr/lib/python2.7/dist-packages/requests/sessions.py", line 597, in send
    history = [resp for resp in gen] if allow_redirects else []
  File "/usr/lib/python2.7/dist-packages/requests/sessions.py", line 195, in resolve_redirects
    **adapter_kwargs
  File "/usr/local/lib/python2.7/dist-packages/loads/measure.py", line 87, in send
    res = _Session.send(self, request, **kwargs)
  File "/usr/lib/python2.7/dist-packages/requests/sessions.py", line 576, in send
    r = adapter.send(request, **kwargs)
  File "/usr/lib/python2.7/dist-packages/requests/adapters.py", line 437, in send
    raise ConnectionError(e, request=request)
1 occurrences of: 
    ConnectionError: HTTPConnectionPool(host='site.com', port=80): Max retries exceeded with url: /thank-you-so-much/ (Caused by NewConnectionError(': Failed to establish a new connection: [Errno 113] No route to host',))    Traceback: 
  File "/usr/lib/python2.7/unittest/case.py", line 329, in run
    testMethod()
  File "for_humans.py", line 84, in test_es
    allow_redirects=True, verify=VERIFY_SSL)
  File "/usr/lib/python2.7/dist-packages/requests/sessions.py", line 511, in post
    return self.request('POST', url, data=data, json=json, **kwargs)
  File "/usr/local/lib/python2.7/dist-packages/loads/measure.py", line 79, in request
    method, url, headers=headers, **kwargs)
  File "/usr/lib/python2.7/dist-packages/requests/sessions.py", line 468, in request
    resp = self.send(prep, **send_kwargs)
  File "/usr/local/lib/python2.7/dist-packages/loads/measure.py", line 87, in send
    res = _Session.send(self, request, **kwargs)
  File "/usr/lib/python2.7/dist-packages/requests/sessions.py", line 597, in send
    history = [resp for resp in gen] if allow_redirects else []
  File "/usr/lib/python2.7/dist-packages/requests/sessions.py", line 195, in resolve_redirects
    **adapter_kwargs
  File "/usr/local/lib/python2.7/dist-packages/loads/measure.py", line 87, in send
    res = _Session.send(self, request, **kwargs)
  File "/usr/lib/python2.7/dist-packages/requests/sessions.py", line 576, in send
    r = adapter.send(request, **kwargs)
  File "/usr/lib/python2.7/dist-packages/requests/adapters.py", line 437, in send
    raise ConnectionError(e, request=request)
1 occurrences of: 
    ConnectionError: HTTPConnectionPool(host='site.com', port=80): Max retries exceeded with url: /thank-you-so-much/ (Caused by NewConnectionError(': Failed to establish a new connection: [Errno 113] No route to host',))    Traceback: 
  File "/usr/lib/python2.7/unittest/case.py", line 329, in run
    testMethod()
  File "for_humans.py", line 84, in test_es
    allow_redirects=True, verify=VERIFY_SSL)
  File "/usr/lib/python2.7/dist-packages/requests/sessions.py", line 511, in post
    return self.request('POST', url, data=data, json=json, **kwargs)
  File "/usr/local/lib/python2.7/dist-packages/loads/measure.py", line 79, in request
    method, url, headers=headers, **kwargs)
  File "/usr/lib/python2.7/dist-packages/requests/sessions.py", line 468, in request
    resp = self.send(prep, **send_kwargs)
  File "/usr/local/lib/python2.7/dist-packages/loads/measure.py", line 87, in send
    res = _Session.send(self, request, **kwargs)
  File "/usr/lib/python2.7/dist-packages/requests/sessions.py", line 597, in send
    history = [resp for resp in gen] if allow_redirects else []
  File "/usr/lib/python2.7/dist-packages/requests/sessions.py", line 195, in resolve_redirects
    **adapter_kwargs
  File "/usr/local/lib/python2.7/dist-packages/loads/measure.py", line 87, in send
    res = _Session.send(self, request, **kwargs)
  File "/usr/lib/python2.7/dist-packages/requests/sessions.py", line 576, in send
    r = adapter.send(request, **kwargs)
  File "/usr/lib/python2.7/dist-packages/requests/adapters.py", line 437, in send
    raise ConnectionError(e, request=request)


Slowest URL: http://site.com:80/  Average Request Time: 8.51882161224

Stats by URLs:
- http://site.com:80/                                             Average request time: 8.51882161224     Hits success rate: 1.0
- http://site.com:80/proof-of-concept/                            Average request time: 6.87364155102     Hits success rate: 1.0
- http://site.com:80/it-consulting/                               Average request time: 6.84250677551     Hits success rate: 1.0
- http://site.com:80/disaster-recovery/                           Average request time: 6.60765157143     Hits success rate: 1.0
- http://site.com:80/project-environments/                        Average request time: 6.54705822449     Hits success rate: 1.0
- http://site.com:80/website-stress-testing/                      Average request time: 6.21323295918     Hits success rate: 1.0
- http://site.com/thank-you-so-much/                         Average request time: 2.94018753846     Hits success rate: 1.0
- http://site.com:80/thank-you-so-much                            Average request time: 2.16664277551     Hits success rate: 1.0
- http://site.com:80/wp-content/uploads/2016/05/JavaScript.pdf    Average request time: 0.177483179487    Hits success rate: 1.0

```