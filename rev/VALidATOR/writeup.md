## VALidATOR 

### Description

Jojo has finally triangulated n00psy’s SOS signal... and it’s emanating from a very cranky pink flip-phone running an equally cranky Android app.

Inside the handset lurks VALidATOR, a gatekeeper who refuses to let anyone decipher Noopsy’s voicemail unless you whisper the one valid integer into its single, lonely text box. 
Legend says the number untangles a knot of modular riddles that the three evil Lords have etched.

**Author : packmad**  

**Challenge designed by [ThreatNemesis](https://tnemesis.com/)**


### Writeup

`VALidATOR` is an Android application with native components written in C++, which interface with Java code through the Java Native Interface (JNI).

The app features a single text input field. It reads an integer from this field and passes it to the native method:

```java
public native long validateNumber(long n);
```

This method checks whether the input satisfies a series of modular equations. These equations can be efficiently solved using the **Chinese Remainder Theorem (CRT)**.


If the input number is valid (specifically, `3869593450890186764`) the method returns that number. 
This value also acts as the key for the AES encryption used to protect the flag:

```
N0PS{7h3d4mndr01d15m3553dup}
```

If the number is incorrect, the function simply returns `0`.

Interestingly, the `validateNumber` function always returns `0` when the application is run on an **x86 architecture** (the typical architecture of emulators), regardless of the input. 

The challenge also includes a distraction in the form of a second native method:

```java
private static native long ConfusionAndDiffusion(long value);
```

This method is mapped at runtime to the native function `FUN_00102b90` via `JNI_OnLoad`. However, it is merely a red herring: it simply wraps a one-second sleep operation and has no effect on the logic of the challenge.

### Flag
`N0PS{7h3d4mndr01d15m3553dup}`

