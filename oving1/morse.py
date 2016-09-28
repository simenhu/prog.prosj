import serial

class Mocoder:


    __serial_port = None
    current_symbol = ""
    current_word = ""
    __serial1 = None
    __letters= {"01":"a","100":"b","1010":"c","100":"d","0":"e","0010":"f","110":"g","0000":"h","00":"i","0111":"j","101":"k","0100":"l","11":"m","10":"n",
                "111":"o","0110":"p","1101":"q","010":"r","000":"s","1":"t","001":"u","0001":"v","011":"w","1001":"x","1011":"y","1100":"z"}

    def __init__ (self):
        self.__serial_port = "/dev/ttyACM0"
        self.serial1 = serial.Serial(self.__serial_port, 9600, bytesize = serial.EIGHTBITS)
        self.current_symbol = ""



    def read_one_signal(self):
        return  int(self.serial1.read(1))

    def process_signal(self, signal):
        if signal == 0 or signal == 1:
            self.update_current_symbol(signal)

        elif signal == 2:
            self.handle_symbol_end()

        else:
            self.handle_word_end()


    def update_current_symbol(self, signal):
        self.current_symbol += str(signal)

    def handle_symbol_end(self):
        symbol = self.__letters.get(self.current_symbol)
        self.update_current_word(str(symbol))
        self.current_symbol = ""

    def update_current_word(self, symbol):
        self.current_word += symbol
        self.current_word = self.current_word.strip("\n")

    def handle_word_end(self):
        self.handle_symbol_end()
        print(self.current_word)
        self.current_word = ""


if __name__ == '__main__':
        myCoder = Mocoder()
        while 1:
            signal = myCoder.read_one_signal()
            myCoder.process_signal(signal)



