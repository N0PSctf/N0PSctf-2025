## Game Boy

### Description

Hey!! We have a small problem...
We deployed a blog application for N0PStopians, and we got hacked by WebTopia!
Can you find how they did this?

**Authors : algorab & Sto**

### Solution

After playing tetris and writing some posts, we can see that the git repository of the API is available at `/.git`. We can then access the entire source code!

Especially, we find a `config.py` file that contains a JWT secret key.

```python
JWT_SECRET_KEY = '6e29664d48f684ce84a...aaa5ca542cdc79'
```

This would allow an attacker to sign their own JWT, and therefore impersonate the administrator of the platform! Only thing we need now is admin's public id, as identification is based on public id, as we can see in `app.py`:

```python
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.public_id
```

There is also a [Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/) that allows any user to access users information through `/api/users`. We can then get the admin's public id, and therefore impersonate them! Once we are the administrator, we can review every user's private posts, and we can find the flag in n00psy's private posts.

### Flag

`N0PS{d0t_G17_1n_Pr0DuC710n?!!}`

