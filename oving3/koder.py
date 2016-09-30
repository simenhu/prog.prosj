#Cipher, Person, Sender, og Receiver
#nå skriver jeg en random ting som skal endres
import random as rd
import crypto_utils
from math import gcd

class Cipher():
    chars = [chr(x) for x in range(32, 127)]
    char_count = len(chars)

    def encode(self):
        pass

    def decode(self, key):
        pass

    def verify(self):
        pass

    def generate_keys(self):
        pass

    def get_key(self):
        pass

    def set_key(self):
        pass

class Caesar_Cipher(Cipher):
    def __init__(self, offset=None):
        if(offset == None):
            self.generate_keys()
        else:
            self.offset = offset
    def encode(self, data):

        return "".join([self.chars[(self.chars.index(x)+self.offset)%self.char_count] for x in data])

    def decode(self, data, key):
            if key == None:
                key=self.offset
            return "".join([self.chars[(self.chars.index(x)+(self.char_count-key))%self.char_count] for x in data])

    def verify(self):
        test_string = "".join([chr(rd.randint(32, 126)) for x in range(0, 10)])
        print("Test string is:%s"%test_string)
        encoded = self.encode(test_string)
        print("Encoded string is%s"%encoded)
        decoded = self.decode(encoded)
        print("Decoded string is:%s"%decoded)
        if(decoded==test_string):
            print ("text was transfered sucsessfully")

    def generate_keys(self):
        self.offset = rd.randint(0,94)


    def get_key(self):
        return self.offset

    def set_key(self,key):
        self.offset = key

class Multiplicative(Cipher):
    def __init__(self):
        self.generate_keys()

    def encode(self, data):
        encoded_list = []
        for i in data:
            index = self.chars.index(i)
            new_index = (index*(self.encode_key)) % self.char_count
            encoded_list.append(self.chars[new_index])
        return "".join(encoded_list)

    def decode(self, data, key = None):
        if key == None:
            key = self.decode_key
        decoded_list = []
        for i in data:
            index = self.chars.index(i)
            new_index = (index * key) % self.char_count
            decoded_list.append(self.chars[new_index])
        return "".join(decoded_list)

    def generate_keys(self):
        n = 95
        while not gcd(n,95) == 1:
            n = rd.randint(1, 500)
        self.encode_key = n
        m = crypto_utils.modular_inverse(n,95)
        self.decode_key = m

    def get_key(self):
        return self.decode_key

    def set_key(self, encode, decode):
        self.encode_key = encode
        self.decode_key = decode

    def verify(self):
        test_string = "".join([chr(rd.randint(32, 126)) for x in range(0, 10)])
        print("Test string is:%s" % test_string)
        encoded = self.encode(test_string)
        print("Encoded string is%s" % encoded)
        decoded = self.decode(encoded)
        print("Decoded string is:%s" % decoded)
        if decoded == test_string:
            print("text was transfered sucsessfully")

class Affine(Cipher):
    def __init__(self):
        self.mult = Multiplicative()
        self.caecar = Caesar_Cipher()
        self.decode_key = (self.mult.get_key(), self.caecar.get_key())

    def generate_keys(self):
        self.mult.generate_keys()
        self.caecar.generate_keys()
        self.decode_key =(self.mult.get_key(), self.caecar.get_key())

    def set_key(self, key):
        self.decode_key = key

    def encode(self, data):
        mult_crypt = self.mult.encode(data)
        affine_crypt = self.caecar.encode(mult_crypt)
        return affine_crypt


    def decode(self,data, key = None):
        if key == None:
            key = self.decode_key
        caecar_uncrypt = self.caecar.decode(data, key[1])
        affine_uncrypt = self.mult.decode(caecar_uncrypt, key[0])
        return affine_uncrypt

    def get_key(self):
        return self.decode_key

    def verify(self):
        test_string = "".join([chr(rd.randint(32, 126)) for x in range(0, 10)])
        print("Test string is:%s" % test_string)
        encoded = self.encode(test_string)
        print("Encoded string is%s" % encoded)
        decoded = self.decode(encoded)
        print("Decoded string is:%s" % decoded)
        if (decoded == test_string):
            print("text was transfered sucsessfully")

class Ubreakable(Cipher):

    #this class takes a string as argument for the constructor
    def __init__(self, key = None):
        self.generate_keys(key)
    def encode(self):
        pass
    def decode(self, key = None):
        pass
    def generate_keys(self, key = None):
        if key == None:
            key = "".join([chr(rd.randint(32,127)) for x in range(5,10)])
        self.encode_key =
    def get_key(self):
        pass
    def set_key(self):
        pass
    def verify(self):
        pass

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

    def __init__(self, cipher):
        super(Sender, self).__init__(cipher, cipher.get_key())

    def operate_cipher(self, data):
        return self.cipher.encode(data)

class Reciever(Person):

    def __init__(self, cipher, key):
        super(Reciever, self).__init__(cipher, key)

    def operate_cipher(self, data):
        return self.cipher.decode(data ,self.key)

class Hacker():
    pass

def main():

    sender = Sender(Affine())

    reciever = Reciever(Affine(), sender.get_key())
    input_text = input("write your message \n>>>")

    while input_text != "exit":
        encoded_text = sender.operate_cipher(input_text)
        print("The encoded text is: %s"%encoded_text)
        decoded_text = reciever.operate_cipher(encoded_text)
        print("The decoded text is: %s"%decoded_text)
        input_text = input("write your message \n>>>")
    print("Goodbye, your secrets has been kept safe!")

def test():
    affine = Affine()
    affine.verify()

if __name__ == '__main__':
    main()