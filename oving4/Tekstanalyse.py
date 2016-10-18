import re, os, operator, math
from matplotlib import pyplot as plt
class Text_Reader():
    def read_Text(self, file):
        return_list = []
        with open(file,mode="r") as f:
            for line in f:
                string = re.sub("[^A-Za-z0-9 \']","",line).lower()
                return_list+=string.split()
        return list(set(return_list))

class Filter_Reader(Text_Reader):
    def read_Text(self, file):
        words = super().read_Text(file)
        with open("data/stop_words.txt") as f:
            for line in f:
                if line.strip() in words:
                    words.remove(line.strip())
        return words

class n_grams_reader(Text_Reader):
    def __init__(self, n = 0):
        self.n = n

    def read_Text(self, file):
        text = super(n_grams_reader, self).read_Text(file)
        new_text = [x for x in text]
        if self.n > 0:
            for index in range(len(text)):
                n_gram = "-".join(text[index:(index+self.n)])
                new_text.append(n_gram)

        with open("data/stop_words.txt") as f:
            for line in f:
                if line.strip() in new_text:
                    new_text.remove(line.strip())

        return new_text



class Text_Analyzer():

    def __init__(self, folder, reader = Text_Reader() ):
        """
        Mother class for all analyzer classes. This class only cares about the popularityof the words
        :param folder: the folder where the negative and poisitive text's are located
        """
        self.folder = folder
        self.reader = reader
        self.positive_word_count = {}
        self.negative_word_count = {}

        self.negative_reviews = 0
        self.positive_reviews = 0

    def analyze_Text(self):
        """
        Analyzes the texts in the positive and the negative folders and makes two dictionarys that stores the
        words and their popularity
        :return: dict positive_word_count, dict negative_word_count
        """
        #first we iterate through every positive review and count all words
        for filename in os.listdir(self.folder + "/pos/"):
            self.positive_reviews += 1
            print("positive analyzed: %d"%self.positive_reviews)
            for word in self.reader.read_Text(self.folder + "/pos/" + filename):
                try:
                    self.positive_word_count[word]+=1
                except:
                    self.positive_word_count[word] = 1

        #we iterate throug every negative review and count the words
        for filename in os.listdir(self.folder + "/neg/"):
            print("negative analyzed: %d" % self.negative_reviews)
            self.negative_reviews += 1
            for word in self.reader.read_Text(self.folder + "/neg/" + filename):
                try:
                    self.negative_word_count[word] += 1
                except:
                    self.negative_word_count[word] = 1

    @property
    def positive(self):
        return self.positive_word_count

    @property
    def negative(self):
        return self.negative_word_count


class Popularity_analyzer(Text_Analyzer):
    def __init__(self, folder, reader = Text_Reader()):
        super(Popularity_analyzer, self).__init__(folder, reader)
        self.positive_popularity = {}
        self.negative_popularity = {}

    def analyze_Text(self):
        super().analyze_Text()
        # iterates through positive words and find their popularity
        for key, value in self.positive_word_count.items():
            self.positive_popularity[key] = value / self.positive_reviews

        # iterates through negative words and find their popularity
        for key, value in self.negative_word_count.items():
            self.negative_popularity[key] = value / self.negative_reviews

    @property
    def positive(self):
        return self.positive_popularity

    @property
    def negative(self):
        return self.negative_popularity




class Information_analyzer(Text_Analyzer):
    def __init__(self, folder, reader = n_grams_reader(0)):
        """

        :param folder: path to the folder where the trainingdata is
        :param reader: the reader that is used to read and format the text in the files
        """
        super(Information_analyzer, self).__init__(folder, reader)
        self.positive_information = {}
        self.negative_information = {}

    def analyze_Text(self):
        #Function iterates through words ini positive_word_count and calculate its positive information rating
        super().analyze_Text()
        counter = 0
        for key, item in self.positive_word_count.items():
            counter+=1
            if key in self.negative_word_count:
                self.positive_information[key] = item/(item+self.negative_word_count[key])
            else:
                self.positive_information[key] = 1

        counter = 0
        # Function iterates through words ini negative_word_count and calculate its negative information rating
        for key, item in self.negative_word_count.items():
            counter+=1
            if key in self.positive_word_count:
                self.negative_information[key] = item / (item + self.positive_word_count[key])
            else:
                self.negative_information[key] = 1

    def prune(self,percentage):
        """
        Removes the words from positive- and negative information that isn't used more that the percentage
        :param percentage: percentage limit
        :return:alters objects list
        """
        #we prune the positive words from positive_interest
        for key in list(self.positive):
            value =  self.positive_word_count[key]/(self.positive_reviews+self.negative_reviews)
            if value < percentage/100:
                del self.positive_information[key]

        #we prune the negative words from negative_interest
        for key in list(self.negative):
            value =  self.negative_word_count[key]/(self.positive_reviews+self.negative_reviews)
            if value < percentage/100:
                del self.negative_information[key]

    @property
    def positive(self):
        return self.positive_information

    @property
    def negative(self):
        return self.negative_information

class Text_Classifier():

    def __init__(self, positive_inf, negative_inf , reader = n_grams_reader(3)):
        self.negative_inf = negative_inf
        self.positive_inf = positive_inf
        self.reader = reader

    def classify(self, folder):
        """

        :param folder: the folder where the positive or negative text's are
        :return: list pos: list of positive text's, list neg: list of negative words
        """
        positive = []
        negative = []
        punishment = 0.02

        for file in os.listdir(folder):
            words = self.reader.read_Text(folder+"/"+file)
            pos_value = 0
            neg_value = 0
            for word in words:
                if word in self.positive_inf:
                    pos_value += math.log(self.positive_inf[word],2)
                else:
                    pos_value += math.log(punishment,2)


                if word in self.negative_inf:
                    neg_value += math.log(self.negative_inf[word],2)
                else:
                    neg_value += math.log(punishment, 2)


            if pos_value > neg_value:
                positive.append(file)
            else:
                negative.append(file)
        return positive, negative

    def classify_folder(self,folder):
        """

        :param folder: the folder which holds the folders neg and pos
        :return: list: pos_correct, list: pos_false, list: neg_correct, list: neg_false
        """
        pos_correct, pos_false = self.classify(folder + "/pos")
        neg_false, neg_correct = self.classify(folder + "/neg")

        return pos_correct, pos_false, neg_correct, neg_false

    def get_result(self):
        pass


def test(file):
    analyzer_1 = Information_analyzer(file, n_grams_reader(3))

    analyzer_1.analyze_Text()


    analyzer_1.prune(2)


    sort_1 = sorted(analyzer_1.positive.items(), key=operator.itemgetter(1), reverse=True)
    sort_2 = sorted(analyzer_1.negative.items(), key=operator.itemgetter(1), reverse=True)

    print(sort_1[:-25])
    print(sort_2[:-25])




def main():
    analyzer = Information_analyzer("data/alle/train",n_grams_reader(3))
    analyzer.analyze_Text()
    analyzer.prune(1)

    sort_1 = sorted(analyzer.positive.items(), key=operator.itemgetter(1), reverse=True)
    sort_2 = sorted(analyzer.negative.items(), key=operator.itemgetter(1), reverse=True)

    print("length of pos %d"%(len(analyzer.positive)))
    print("length of neg %d"%(len(analyzer.negative)))

    print(sort_1)
    print(sort_2)

    classifier = Text_Classifier(analyzer.positive, analyzer.negative,n_grams_reader(3))
    pos_correct, pos_false, neg_correct, neg_false = classifier.classify_folder("data/alle/test")


    print("correct percentage:%d"%(100*(len(pos_correct)+len(neg_correct))/(len(pos_correct)+len(pos_false)+len(neg_correct)+len(neg_false))))


    print(len(pos_correct))
    print(len(pos_false))
    print(len(neg_correct))
    print(len(neg_false))



if __name__ == '__main__':
    main()