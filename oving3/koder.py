#Cipher, Person, Sender, og Receiver
#nå skriver jeg en random ting som skal endres
import random as rd
import crypto_utils
from math import gcd, pow

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

    def decode(self, data, key = None):
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

class Unbreakable(Cipher):

    #this class takes a string as argument for the constructor
    def __init__(self, key = None):
        """

        :param key: takes a string and sets the Cipher's encode_key and decode_key
        """
        self.english_Words = []
        try:
            f = open("english_Words.txt", "r")
            for line in f:
                self.english_Words.append(str(line.strip()))

            f.close()
        except:
            print("something went wrong when opening the file")
        self.generate_keys(key)

    def encode(self, data: str) -> str:
        encode_string = ""
        encoded_string = ""
        while len(encode_string) < len(data):
            encode_string += self.encode_key
        for i in range(len(data)):
            encoded_string += self.chars[(self.chars.index(data[i])+self.chars.index(encode_string[i]))%95]
        return encoded_string
    def decode(self, data, key = None):
        if key == None:
            key = self.decode_key
        decode_string = ""
        decoded_string = ""
        while len(decode_string) < len(data):
            decode_string += key
        for i in range(len(data)):
            decoded_string += self.chars[(self.chars.index(data[i]) + self.chars.index(decode_string[i])) % 95]
        return decoded_string

    def generate_keys(self, key = None):
        if key == None:
            key = self.english_Words[rd.randint(0,len(self.english_Words))-1]
        print("the key of unbreakable is: %s"%key)
        self.encode_key = key
        self.decode_key = ""
        for n in key:
            self.decode_key += self.chars[(95 - self.chars.index(n)) % 95]

    def get_key(self):
        return self.decode_key
    def set_key(self, key):
        self.generate_keys(key)
    def verify(self):
        test_string = "".join([chr(rd.randint(32, 126)) for x in range(0, 10)])
        print("Test string is:%s" % test_string)
        encoded = self.encode(test_string)
        print("Encoded string is%s" % encoded)
        decoded = self.decode(encoded)
        print("Decoded string is:%s" % decoded)
        if decoded == test_string:
            print("text was transfered sucsessfully")

class RSA(Cipher):
    def __init__(self):
        self.generate_keys()

    def encode(self, data):
        blocks = crypto_utils.blocks_from_text(data,1)
        print("string values before encoded", end= "")
        print(blocks)
        encrypted_blocks = []
        for n in blocks:
            encrypted_blocks.append((n**self.encode_key[1])%self.encode_key[0])
        return encrypted_blocks

    def decode(self, data, key = None):
        if key == None:
            key = self.decode_key
        encrypted_blocks = data
        decoded_blocks = []
        for n in encrypted_blocks:
            decoded_blocks.append((n**key[1]) % key[0])

        return crypto_utils.text_from_blocks(decoded_blocks, 1)

    def verify(self):
        test_string = "".join([chr(rd.randint(32, 126)) for x in range(0, 10)])
        print("Test string is:%s" % test_string)
        encoded = self.encode(test_string)
        print("Encoded string is%s" % encoded)
        decoded = self.decode(encoded)
        print("Decoded string is:%s" % decoded)
        if (decoded == test_string):
            print("text was transfered sucsessfully")

    def generate_keys(self):
        gcd_value = 0
        while gcd_value != 1:
            p = crypto_utils.generate_random_prime(8)
            q = crypto_utils.generate_random_prime(8)
            while q==p:
                q = crypto_utils.generate_random_prime(8)
            n = p*q
            phi = (p-1)*(q-1)
            e = rd.randint(3, phi-1)
            gcd_value  = gcd(e, phi)
        print("The primes that is chosen is %d and %d "%(p,q))
        d = crypto_utils.modular_inverse(e, phi)
        self.encode_key = (n, e)
        self.decode_key = (n, d)


    def get_key(self):
        return self.decode_key
    def set_key(self, key):
        self.decode_key = key

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

class Hacker(Person):
    chars = [chr(x) for x in range(32, 127)]
    def __init__(self, cipher):
        self.cipher = cipher
        self.english_Words = []
        try:
            f = open("english_Words.txt", "r")
            for line in f:
                self.english_Words.append(str(line.strip()))

            f.close()
        except:
            print("something went wrong when opening the file")

    def hack(self, data):
        is_hacked = False
        if isinstance(self.cipher, Caesar_Cipher):
            key = 0
            while not is_hacked:
                if self.is_English_Words(self.cipher.decode(data, key)):
                    is_hacked = True
                    print("Cipher was hacked. The text was: %s"%(self.cipher.decode(data, key)))
                key +=1
                print("Key: %d"%key)
                if key > 95:
                    print("Cipher was unhackable")
                    break
        elif isinstance(self.cipher, Multiplicative):
            key = 0
            while not is_hacked:
                key += 1
                print("Key: %d" % key)
                if self.is_English_Words(self.cipher.decode(data, key)):
                    is_hacked = True
                    print("Cipher was hacked. The text was: %s" % (self.cipher.decode(data, key)))
                if key > 501:
                    print("Cipher was unhackable")
                    break

        elif isinstance(self.cipher, Affine):
            key = [0,0]
            while not is_hacked:
                key[1] += 1
                print("Key mult: %d, key caecar: %d"%(key[0], key[1]))
                if self.is_English_Words(self.cipher.decode(data, key)):
                    is_hacked = True
                    print("Cipher was hacked. The text was: %s" % (self.cipher.decode(data, key)))
                if key[1] > 100:
                    key[1] = 0
                    key[0]+=1
                if key[0] > 501 and key[1] > 100:
                    print("Cipher was unhackable")
                    break

        elif isinstance(self.cipher, Unbreakable):
            key = 0
            while not is_hacked:
                key += 1
                print("Key: %s" % self.english_Words[key])
                if key > len(self.english_Words)-1:
                    print("Cipher was unhackable")
                    break
                decode_key = ""
                for n in self.english_Words[key]:
                    decode_key += self.chars[(95 - self.chars.index(n)) % 95]
                if self.is_English_Words(self.cipher.decode(data, decode_key)):
                    is_hacked = True
                    print("Cipher was hacked. The text was: %s" % (self.cipher.decode(data, decode_key)))
        else:
            print("Cipher was neither of hackable ciphers")

    def is_English_Words(self, data):
        """
        Checks if the insput string only contains words from the english language
        :param data: str of words
        :return: boolean (all words are english)
        """

        words = data.split()
        is_English_Words = True
        if len(words)==0:
            is_English_Words = False
        for word in words:
            if word not in self.english_Words:
                is_English_Words = False
                break
        return is_English_Words

def main():

    sender = Sender(Unbreakable())
    hacker = Hacker(Unbreakable())
    reciever = Reciever(Unbreakable(), sender.get_key())

    input_text = input("write your message \n>>>")

    while input_text != "exit":
        encoded_text = sender.operate_cipher(input_text)
        print("The encoded text is: %s"%encoded_text)
        hacker.hack(encoded_text)
        decoded_text = reciever.operate_cipher(encoded_text)
        print("The decoded text is: %s"%decoded_text)
        input_text = input("write your message \n>>>")
    print("Goodbye, your secrets has been kept safe!")

def test():
    hacker = Hacker(Caesar_Cipher())
    print(hacker.english_Words)
    print(hacker.is_English_Words("boat"))

if __name__ == '__main__':
    main()
