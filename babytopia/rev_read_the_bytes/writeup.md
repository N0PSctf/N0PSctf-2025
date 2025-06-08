## Reverse Engineering: Read the bytes 

### Description

Look who's there! New students!
Fine, this time we will focus on [reverse engineering](https://en.wikipedia.org/wiki/Reverse_engineering). This could help you against PwnTopia one day!

I give you now a Python program and its output. Try to understand how it works!

**Author: algorab**

### Solution

The python script takes the flag, a bytes object, and print the code of each of its character.
Therefore, in order to get the flag back, we can convert each of these number back to its original character!

```python
chars = [66, 52, 66, 89, 123, 52, 95, 67, 104, 52, 114, 97, 67, 55, 51, 114, 95, 49, 115, 95, 74, 117, 53, 116, 95, 52, 95, 110, 85, 109, 56, 51, 114, 33, 125]
flag = ""

for char in chars:
    flag += chr(char)

print(flag)
```

### Flag

The flag is `B4BY{4_Ch4raC73r_1s_Ju5t_4_nUm83r!}`