
from msilib.schema import Error
import pandas as pd
import random
import re
from googletrans import Translator
from flask import Flask, redirect, url_for, render_template, request


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
        self.lang_list_short = ["ar", "de", "es", "fr", "it", "iw", "ja", "ko", "pl", "pt-PT", "ru", "tr", "uk", "zh-CN"]

    def lang_diff(self):
        return [lang for lang in self.lang_list if not (lang in self.lang_list_short or lang == "en")]

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
        with open('sentences_base.txt') as f:
            self.lines = f.readlines()
        self.df = pd.read_csv("GenericsKB-Best.tsv", sep='\t')
    
    def choose_source(self):
        while True:
            self.source = input("Write your sentence or choose difficulty:\n0 - random, 1 - easy, 2 - hard\n")
            if self.source == "0" or self.source == "1" or self.source == "2":
                break
            elif len(self.source) > 2:
                break
            else:
                print("Try again\n")
    
    def draw(self):
        sentence_easy = random.choice(self.lines)
        sentence_hard = random.choice(self.df['GENERIC SENTENCE'])
        if self.source == "0":
            sentence = random.choice([sentence_easy, sentence_hard])
        elif self.source == "1":
            sentence = sentence_easy
        elif self.source == "2":
            sentence = sentence_hard
        else:
            sentence = self.source
        
        sentence = self.clean(sentence)

        return sentence

    def clean(self, sentence):
        # comment line or empty line
        if len(sentence) < 2 or sentence[0] == "#":
            self.draw()
        # starts with number and dot
        match1 = re.findall(r"(^[0-9]+[.])", sentence)
        if match1:
            sentence = sentence[len(match1[0]):]
        # start with word and colon
        match2 = re.findall(r"([a-zA-Z]+[:]\s)", sentence)
        if match2:
            sentence = sentence[len(match2[0]):]

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
            print("\nText: ", t.text, "\nPronunciation: ", t.pronunciation, "\n")


class Display():
    def __init__(self):
        # self.item = item
        self.hmtl = ""
    
    def checkbox(self, lang):
        return '<li><div class="form-check"><input class="form-check-input" type="checkbox" name="languages" value="' + lang + '" id="flexCheckDefault_' + lang + '" /><label class="form-check-label" for="flexCheckDefault_' + lang + '">' + lang + '</label></div></li>'
    
    def checkboxes(self, langs, html_class):
        checkboxes = '<ul class="' + html_class + '">'
        for lang in langs:
            checkboxes += self.checkbox(lang)
        checkboxes += '</ul>'
        return checkboxes
    
    def form(self, langs):
        form = '<form method="post"><ul>'
        for lang in langs:
            form += self.checkbox(lang)
        form += '</ul><div class="modal-footer"><input class="btn btn-primary" type="submit" value="Submit"></div></form>'
        return form
    
    def translations(self, sentences):
        translations = ""
        for s in sentences:
            translations += s.text
        return translations


# print(Display().checkbox("de"))
# print(Display().form(Languages().lang_list))


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
        if len(sentence.source) == 1:
            sentence_user = input()
            if len(sentence_user) > 2:
                sentence.source = sentence_user
        else:
            sentence.choose_source()


# main()

# form = '<form method="post"> \
#         <input type="checkbox" name="hello" value="world" checked> \
#         <input type="checkbox" name="hello" value="davidism" checked> \
#         <div class="form-check"> \
#         <input \
#           class="form-check-input" \
#           type="checkbox" \
#           value="" \
#           id="flexCheckDefault" \
#         /> \
#         <label class="form-check-label" for="flexCheckDefault"> de </label> \
#       </div> \
#         <input type="submit"> \
#         </form>'

form = Display().form(Languages().lang_list)
checkboxes = Display().checkboxes(Languages().lang_diff(), "diff")
checkboxes_short = Display().checkboxes(Languages().lang_list_short, "short")


app = Flask(__name__)

languages = []
inlineRadioOptions = 2
sentence = Sentence()
english_sentence = ""
translations = ""

@app.route('/', methods=['GET', 'POST'])
def index():
    global languages
    global inlineRadioOptions
    global sentence
    global translations
    global english_sentence
    if request.method == 'POST':
        if len(request.form.getlist('languages')) > 0:
            languages = request.form.getlist('languages')
        if len(request.form.getlist('inlineRadioOptions')) > 0:
            inlineRadioOptions = request.form.getlist('inlineRadioOptions')
            sentence.source = inlineRadioOptions[0]
            print(sentence.source)
            # sen = MultipleTranslator("The cat is white").multiple_translations(languages)
            english_sentence = sentence.draw()
            sen = MultipleTranslator(english_sentence).multiple_translations(languages)
            translations = Display().translations(sen)
    print(languages, inlineRadioOptions)
    return render_template("index.html", content_form=form, content_sentence=english_sentence, content_translations=translations, content_checkboxes=checkboxes, content_checkboxes_short=checkboxes_short)

if __name__ == "__main__":
    app.run(debug=False)


# licnecja https://huggingface.co/datasets/generics_kb?fbclid=IwAR07Hh1JT16IbRJJjg13wvFYVNWMltU462-bvqp-atzxLRLE-3PNy845q8Q

