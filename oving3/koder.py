#Cipher, Person, Sender, og Receiver
#nå skriver jeg en random ting som skal endres
import random as rd

class Cipher():
    chars = [chr(x) for x in range(32, 127)]
    char_count = len(chars)

    def encode(self):
        pass

    def decode(self):
        pass

    def verify(self):
        pass

    def generate_keys(self):
        pass

    def set_key(self, key):
        pass

class Caesar_Cipher(Cipher):
    def __init__(self, offset=None):
        if(offset == None):
            self.offset = self.generate_keys()
        else:
            self.offset = offset
    def encode(self, data):

        return "".join([self.chars[(self.chars.index(x)+self.offset)%self.char_count] for x in data])

    def decode(self, data):


        return "".join([self.chars[(self.chars.index(x)+(self.char_count-self.offset))%self.char_count] for x in data])

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
        return rd.randint(0,94)

    def set_key(self,key):
        self.offset = key

class Multiplicative(Cipher):
    def __init__(self):
        self.encode_key = None

    def encode(self, data):
        pass
    def decode(self, data):
        pass
    def generate_keys(self):
        pass
    def set_key(self, key):
        pass

class Person():

    def __init__(self, cipher, key):
        self.key = key
        self.cipher = cipher

    def get_key(self):
        return self.key

    def set_key(self,key):
        self.key = key
        self.cipher.set_key(key)

    def operate_cipher(self):
        pass

class Sender(Person):

    def __init__(self, cipher):
        super(Sender, self).__init__(cipher, cipher.generate_keys())

    def operate_cipher(self, data):
        return self.cipher.encode(data)

class Reciever(Person):

    def __init__(self, cipher, key):
        super(Reciever, self).__init__(cipher, key)

    def operate_cipher(self, data):
        return self.cipher.decode(data)



class Hacker():
    pass

def main():
    cipher = Caesar_Cipher()
    sender = Sender(cipher)
    reciecer = Reciever(cipher, sender.get_key())
    input_text = input("write your message \n>>>")

    while input_text != "exit":
        encoded_text = sender.operate_cipher(input_text)
        print("The encoded text is: %s"%encoded_text)
        decoded_text = reciecer.operate_cipher(encoded_text)
        print("The decoded text is: %s"%decoded_text)
        reciecer.set_key(sender.get_key())
        input_text = input("write your message \n>>>")
    print("Goodbye, your secrets has been kept safe!")

if __name__ == '__main__':
    main()