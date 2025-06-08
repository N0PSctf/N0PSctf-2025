## Meago

### Description

In Meago precision is key. Sharpen your calculations, find innovative ways to solve the oracle's riddle.

**Author : factoreal**

Challenge designed by **[ASIS](https://asisctf.com/) team**  

### Solution

The challenge presents a Meago oracle that transforms hidden values `(x0, y0)` through iterative applications of a function: 
$ x, y = ((x \cdot y^2)^{1/3}, (x \cdot y^2)^{1/3}) $. 

The initial `x0` encodes the flag as a scaled real number, and only `y0` is revealed. After 5 iterations, the oracle leaks the updated `y` values. 

The solve script inverts the final leaked relation $ l = ((x^3 \cdot y^4)^{1/7}) $ using Halley's root-finding method with high-precision arithmetic to recover `x0`, from which the flag is extracted using `long_to_bytes`.


The full solution script can be found in the [`sol.sage`](sol.sage).


### Flag

The flag is `N0PS{RSA_P3lL_cRyp70_5YSTeM!}`