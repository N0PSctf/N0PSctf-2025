## Forensics: Unkown file

### Description

Hello young trainees!
Today, we are studying [digital forensics](https://en.wikipedia.org/wiki/Digital_forensics)!
This may be useful if one day you have to face PwnTopia...

Here is a file, you have to find a way to read its content. Good luck!

**Author: algorab**

### Solution

When opening the file with a text editor, we can see that it start with `%PDF-1.6`. If we rename it `challenge.pdf`, we can then open it with a regular PDF reader!

### Flag

The flag is `B4BY{IJUSTDECODEDACAESARCIPHERWHICHMAKESMEAPROFESSIONALCRYPTOHERO}`