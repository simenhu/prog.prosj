#Cipher, Person, Sender, og Receiver
import random as rd

class Cipher():
    def __init__(self):
        self.chars = [chr(x) for x in range(32,127)]
        self.char_count = len(self.chars)


    def encode(self):
        pass

    def decode(self):
        pass

    def verify(self):
        pass

    def generate_keys(self):
        pass

class Caesar_Cipher(Cipher):
    def __init__(self, offset):
        self.offset = offset

    def encode(self, data):
        data = "dette er en test"
        return [self.chars[(self.chars.index(x)+self.offset)%self.char_count] for x in data]

    def decode(self, data):
        return [self.chars[self.chars.index(x)+(self.char_count-self.offset)]%self.char_count for x in data]

    def verify(self):
        test_string = "dette er en teststreng som er kul"
            #"".join([chr(rd.randint(32, 127)) for x in range(0, 10)])
        print("Test string is:%s"%test_string)
        encoded = self.encode(test_string)
        print("Encoded string is%s"%encoded)
        decoded = self.decode(encoded)
        print("Decoded string is:%s"%decoded)

class Person():

    def __init__(self, cipher, key):
        self.key = key
        self.cipher = cipher

    def get_key(self):
        return self.key

    def set_key(self,key):
        self.key = key

    def operate_cipher(self):
        pass

class Sender(Person):

    def __init__(self, cipher, key):
        super(Sender, self).__init__(self, cipher, key)
        pass

    def operate_cipher(self, data):
        return self.cipher.encode(data)

class Reciever(Person):

    def __init__(self, cipher, key):
        super(Reciever, self).__init__(self, cipher, key)

    def operate_cipher(self, data):
        return self.cipher.decode(data)


class Hacker():
    pass

def main():
    cipher = None
    sender = Sender(cipher,)
    reciecer = Reciever(cipher)

