

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
        self.langs = ["es"]

    def __str__(self):
        for lang in self.lang_list:
            print(lang, self.lang_list.index(lang) + 1, end="   ")
        print("\n")
    
    def choose(self):
        while True:
            try:
                numbers = input("Choose numbers separated by \",\":\n")
                numbers = numbers.split(",")
                self.langs = [self.lang_list[int(number) - 1] for number in numbers]
            except ValueError:
                print("Try again\n")
            else:
                break

        print("\n")
        for lang in self.langs:
            print(lang)
        print("\n")

        return self.langs


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
    langs = Languages().choose()
    
    while True:
        df = pd.read_csv("GenericsKB-Best.tsv", sep='\t')
        sentence = random.choice(df['GENERIC SENTENCE'])

        MultipleTranslator(sentence).__str__(langs)

        print("---")
        input()


main()


# licnecja https://huggingface.co/datasets/generics_kb?fbclid=IwAR07Hh1JT16IbRJJjg13wvFYVNWMltU462-bvqp-atzxLRLE-3PNy845q8Q

