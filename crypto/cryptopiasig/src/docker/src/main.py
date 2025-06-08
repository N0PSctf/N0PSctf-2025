import os
from base64 import b64decode

class CrypTopiaShell():

    P = 0xd04159f73a2bcc1d72b112b596e28d80edd1650fba53b3af1d445168759b4b04e201ab081b5be0af75cf3179db10cb039106e1ceba4415549577681ae323cb35c73bc67d17fc2d49931c9fd3a6d92060ead29962a2ac7c8f8d2fba1bfcef2281b9654abcd4a39024fcffa8d1909190f19bcebc548c96a340e9ace60f759760158708e6065198f131f0de9ad5b5fa7feca826d3c2016e6d4323cac711e7643da47ac8d950e5040042f82426f91ca77cf092cc266cad2bf43694c4ba5a758c989e4e16d8f90af2f6bf344ac7abd93b1f209b2a1c9bf88653214c0d14cf8e95c79b5a12f50b31eeeebbb3393969d87fbd4e72c421876f0a28ec3604701f1376759f
    K = 0x94f8c6b2452775bfa8693aed92e7abd8c2f9af34789f5b4b236e0c7ce926c927
    G = 0x8b6eec60fae5681c
    MAGIC = b"\x01\x02CrypTopiaSig\x03\x04"

    def __sign(self, gen, key, mod):
        bl = gen.bit_length()
        for i in range(len(self.data)):
            gen = (gen ^ (self.data[i] << (i % bl))) & 2**bl-1
        s = 1
        while key:
            if key & 1:
                s = s * gen % mod
            key = key >> 1
            gen = gen * gen % mod
        return s

    def create(self, data):
        self.data = data
        self.signature = self.__sign(self.G, self.K, self.P).to_bytes(self.P.bit_length()//8, 'big')
        self.header = self.MAGIC + len(self.data).to_bytes(6, 'big') + len(self.signature).to_bytes(6, 'big')

    def parse(self, data):
        if data[:len(self.MAGIC)]!= self.MAGIC:
            print("Missing magic bytes")
            return False
        length = int.from_bytes(data[len(self.MAGIC):len(self.MAGIC)+6], 'big')
        signature_length = int.from_bytes(data[len(self.MAGIC)+6:len(self.MAGIC)+12], 'big')
        if len(data) > len(self.MAGIC)+12+length+signature_length:
            print("Invalid data size")
            return False
        self.data = data[len(self.MAGIC)+12:len(self.MAGIC)+12+length]
        self.signature = data[len(self.MAGIC)+12+length:len(self.MAGIC)+12+length+signature_length]
        if self.__sign(self.G, self.K, self.P).to_bytes(self.P.bit_length()//8, 'big') != self.signature:
            print("Invalid signature")
            return False
        return True

    def run(self):
        try:
            os.system(self.data)
        except Exception as e:
            print(f"Woops! Something went wrong")

    def dump(self):
        return self.header + self.data + self.signature

ctc = CrypTopiaShell()

print("Welcome to CrypTopiaShell!\nProvide base64 encoded shell commands in the CrypTopiaSig format in order to get them executed.")

while True:
    try:
        data = input("$ ")
        try:
            data = b64decode(data)
        except:
            print("Invalid base64 data")
            continue
        try:
            if not ctc.parse(data):
                continue
            ctc.run()
        except:
            print(f"Invalid CrypTopiaSig file")
    except:
        break
