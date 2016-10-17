import re, os, operator

class Text_Reader():
    def read_Text(self, file):
        return_list = []
        with open(file,mode="r") as f:
            for line in f:
                string = re.sub("[^A-Za-z0-9 ]","",line).lower()
                return_list+=string.split()
        return list(set(return_list))

class prune_reader(Text_Reader):
    def read_Text(self, file):
        words = super().read_Text(file)
        with open("data/stop_words.txt") as f:
            for line in f:
                if line.strip() in words:
                    words.remove(line.strip())
        return words
class Text_Analyzer:
    def __init__(self, folder, reader = Text_Reader() ):
        """
        Mother class for all analyser classes. This class only cares about the popularityof the words
        :param folder: the folder where the negative and poisitive text's are located
        """
        self.reader = reader
        self.folder = folder
        self.positive_word_count = {}
        self.negative_word_count = {}
        self.positive_popularity = {}
        self.negative_popularity = {}
        self.negative_reviews = 0
        self.positive_reviews = 0

    def analyze_Text(self):
        """
        Analyzes the texts in the positive and the negative folders and makes two dictionarys that stores the
        words and their popularity
        :return: dict positive_word_count, dict negative_word_count
        """
        #first we iterate through every positive review and count all words
        for filename in os.listdir(self.folder + "pos"):
            self.positive_reviews += 1
            for word in self.reader.read_Text(self.folder + "pos/" + filename):
                try:
                    self.positive_word_count[word]+=1
                except:
                    self.positive_word_count[word] = 1

        #we iterate throug every negative review and count the words
        for filename in os.listdir(self.folder + "neg"):
            self.negative_reviews += 1
            for word in self.reader.read_Text(self.folder + "neg/" + filename):
                try:
                    self.negative_word_count[word] += 1
                except:
                    self.negative_word_count[word] = 1

        #iterates through positive words and find their popularity
        for key,value in self.positive_word_count.items():
            self.positive_popularity[key] = value/self.positive_reviews

        #iterates through negative words and find their popularity
        for key, value in self.negative_word_count.items():
            self.negative_popularity[key] = value/self.negative_reviews



class Text_Classifier():
    def __init__(self, analyzer, folder):
        self.analyzer = analyzer(folder)

    def classify(self, folder):
        pass

    def get_result(self):
        pass

def test(file):
    analyzer_1 = Text_Analyzer("data/subset/train/", prune_reader())
    analyzer_2 = Text_Analyzer("data/subset/train/")
    analyzer_1.analyze_Text()
    analyzer_2.analyze_Text()
    sort_1 = sorted(analyzer_1.positive_popularity.items(), key = operator.itemgetter(1), reverse = True)
    sort_2 = sorted(analyzer_2.positive_popularity.items(), key = operator.itemgetter(1), reverse = True)
    print(sort_1[:25])
    print(sort_2[:25])




def main():
    pass

if __name__ == '__main__':
    test("data/alle/test/neg/0_2.txt")