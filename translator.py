
from msilib.schema import Error
import pandas as pd
import random
from googletrans import Translator


class Languages():
    def __init__(self):
        self.lang_list = ["af", "ach", "ak", "am", "ar", "az", "be", "bem", "bg", "bh", "bn", "br", "bs", "ca", "chr", "ckb", "co",
             "crs", "cs", "cy", "da", "de", "ee", "el", "en", "eo", "es", "es-419", "et", "eu", "fa", "fi", "fo", "fr",
             "fy", "ga", "gaa", "gd", "gl", "gn", "gu", "ha", "haw", "hi", "hr", "ht", "hu", "hy", "ia", "id", "ig",
             "is", "it", "iw", "ja", "jw", "ka", "kg", "kk", "km", "kn", "ko", "kri", "ku", "ky", "la", "lg", "ln",
             "lo", "loz", "lt", "lua", "lv", "mfe", "mg", "mi", "mk", "ml", "mn", "mo", "mr", "ms", "mt", "ne", "nl",
             "nn", "no", "nso", "ny", "nyn", "oc", "om", "or", "pa", "pcm", "pl", "ps", "pt-BR", "pt-PT", "qu", "rm",
             "rn", "ro", "ru", "rw", "sd", "sh", "si", "sk", "sl", "sn", "so", "sq", "sr", "sr-ME", "st", "su", "sv",
             "sw", "ta", "te", "tg", "th", "ti", "tk", "tl", "tn", "to", "tr", "tt", "tum", "tw", "ug", "uk", "ur",
             "uz", "vi", "wo", "xh", "xx-bork", "xx-elmer", "xx-hacker", "xx-klingon", "xx-pirate", "yi", "yo", "zh-CN",
             "zh-TW", "zu"]

    def __str__(self):
        for lang in self.lang_list:
            print(lang, end="   ")

    def choose(self):
        while True:
            codes = input("Choose codes separated by \",\":\n")
            codes = codes.split(",")
            codes = [code.strip() for code in codes]
            result =  all(elem in self.lang_list for elem in codes)
            if result:
                self.langs = codes
                break
            else:
                print("Try again\n")

        return self.langs


class Sentence():
    def __init__(self):
        self.df = pd.read_csv("GenericsKB-Best.tsv", sep='\t')
    
    def choose_source(self):
        while True:
            self.source = input("Choose difficulty: 0 - random, 1 - easy, 2 - hard:\n")
            if self.source == "0":
                break
            elif self.source == "1":
                break
            elif self.source == "2":
                break
            else:
                print("Try again\n")

    def draw(self):
        if self.source == "2":
            sentence = random.choice(self.df['GENERIC SENTENCE'])

        return sentence


class MultipleTranslator():
    def __init__(self, sentence):
        self.sentence = sentence
        self.translator = Translator()

    def single_translation(self, dest_lang):
        return self.translator.translate(self.sentence, src='en', dest=dest_lang)

    def multiple_translations(self, dest_lang_list):
        return [self.single_translation(lang) for lang in dest_lang_list]

    def __str__(self, dest_lang_list):
        print("Original sentence: ", self.sentence, "\n")
        for t in self.multiple_translations(dest_lang_list):
            print(t.dest)
            input()
            print("\nText:", t.text, "\nPronunciation: ", t.pronunciation, "\n")


def main():
    Languages().__str__()
    print("\n")
    langs = Languages().choose()
    print("\n")
    sentence = Sentence()
    sentence.choose_source()
    print("\n")
    
    while True:
        MultipleTranslator(sentence.draw()).__str__(langs)

        print("---")
        input()


main()


# licnecja https://huggingface.co/datasets/generics_kb?fbclid=IwAR07Hh1JT16IbRJJjg13wvFYVNWMltU462-bvqp-atzxLRLE-3PNy845q8Q

