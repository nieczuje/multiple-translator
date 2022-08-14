
from gettext import translation
from msilib.schema import Error
import pandas as pd
import random
import re
from googletrans import Translator
from flask import Flask, redirect, url_for, render_template, request


class Languages():
    def __init__(self):
        self.lang_list = ["af", "ach", "ak", "am", "ar", "az", "be", "bem", "bg", "bh", "bn", "br", "bs", "ca", "chr", "ckb", "co",
             "cs", "cy", "da", "de", "ee", "el", "en", "eo", "es", "es-419", "et", "eu", "fa", "fi", "fo", "fr",
             "fy", "ga", "gaa", "gd", "gl", "gn", "gu", "ha", "haw", "hi", "hr", "ht", "hu", "hy", "ia", "id", "ig",
             "is", "it", "iw", "ja", "jw", "ka", "kg", "kk", "km", "kn", "ko", "kri", "ku", "ky", "la", "lg", "ln",
             "lo", "loz", "lt", "lua", "lv", "mfe", "mg", "mi", "mk", "ml", "mn", "mo", "mr", "ms", "mt", "ne", "nl",
             "nn", "no", "nso", "ny", "nyn", "oc", "om", "or", "pa", "pcm", "pl", "ps", "pt-BR", "pt-PT", "qu", "rm",
             "rn", "ro", "ru", "rw", "sd", "sh", "si", "sk", "sl", "sn", "so", "sq", "sr", "sr-ME", "st", "su", "sv",
             "sw", "ta", "te", "tg", "th", "ti", "tk", "tl", "tn", "to", "tr", "tt", "tum", "tw", "ug", "uk", "ur",
             "uz", "vi", "wo", "xh", "xx-bork", "xx-elmer", "xx-hacker", "xx-klingon", "xx-pirate", "yi", "yo", "zh-CN",
             "zh-TW", "zu"] # "crs" nie dziala
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
        self.level = ""
    
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
            self.source = random.choice(["1", "2"])

        if self.source == "1":
            sentence = sentence_easy
            self.level = "Easy"
        elif self.source == "2":
            sentence = sentence_hard
            self.level = "Hard"
        
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
    
    def checkbox(self, lang, checked):
        return '<li><div class="form-check"><input class="form-check-input" type="checkbox" name="languages" value="' + lang + '" id="flexCheckDefault_' + lang + '" ' + checked + '/><label class="form-check-label" for="flexCheckDefault_' + lang + '">' + lang + '</label></div></li>'
    
    def checkboxes(self, langs, html_class, checked_list):
        checkboxes = '<ul class="' + html_class + '">'
        for count, lang in enumerate(langs):
            checkboxes += self.checkbox(lang, checked_list[count])
        checkboxes += '</ul>'
        return checkboxes
    
    def form(self, langs):
        form = '<form method="post"><ul>'
        for lang in langs:
            form += self.checkbox(lang, "")
        form += '</ul><div class="modal-footer"><input class="btn btn-primary" type="submit" value="Submit"></div></form>'
        return form
    
    def translations(self, sentences):
        translations = ""
        for s in sentences:
            translations += s.text
        return translations
    
    def num_to_text(self, num):
        if num > 9:
            num == 9
        return ['zero','one','two','three','four','five','six','seven','eight','nine'][num].capitalize()
    
    def accordion_item(self, lang, translation, num, pronunciation):
        return '''<div class="accordion-item">
            <h2 class="accordion-header" id="panelsStayOpen-heading''' + self.num_to_text(num) + '''">
              <button
                class="accordion-button"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#panelsStayOpen-collapse''' + self.num_to_text(num) + '''"
                aria-expanded="false"
                aria-controls="panelsStayOpen-collapse''' + self.num_to_text(num) + '''"
              >
                ''' + lang + '''
              </button>
            </h2>
            <div
              id="panelsStayOpen-collapse''' + self.num_to_text(num) + '''"
              class="accordion-collapse collapse"
              aria-labelledby="panelsStayOpen-heading''' + self.num_to_text(num) + '''"
            >
              <div class="accordion-body">
                <div>''' + translation + '''</div>
                <small class="text-muted">''' + pronunciation + '''</small>
              </div>
            </div>
          </div>'''
        
    def accordion(self, langs, translations, pronunciations):
        accordion = '<div class="accordion" id="accordionPanelsStayOpenExample">'
        for count, lang in enumerate(langs):
            accordion += self.accordion_item(lang, translations[count], count + 1, pronunciations[count])
        accordion += '</div>'
        return accordion


# print(Display().checkbox("de"))
# print(Display().form(Languages().lang_list))
# print(Display().accordion_item("de", "Berlin"))
# print(Display().accordion(["de", "it"], ["deeee", "itttt"]))
# print(Display().num_to_text(1))
# input()


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



languages = []
inlineRadioOptions = 2
sentence = ""
english_sentence = ""
translations = ""
btnradio = "1"
checked_easy = ""
checked_hard = ""
checked_random = ""
accordion = ""
small = ""

checked_list_short = ["" for lang in Languages().lang_list_short]
checked_list_diff = ["" for lang in Languages().lang_diff()]
form = Display().form(Languages().lang_list)
checkboxes_diff = Display().checkboxes(Languages().lang_diff(), "diff", checked_list_diff)
checkboxes_short = Display().checkboxes(Languages().lang_list_short, "short", checked_list_short)


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    global languages
    global inlineRadioOptions
    global sentence
    global translations
    global english_sentence
    global btnradio
    global checked_easy
    global checked_hard
    global checked_random
    global accordion
    global small
    global checkboxes_short
    global checkboxes_diff
    if request.method == 'POST':
        if len(request.form.getlist('languages')) > 0:
            languages = request.form.getlist('languages')
        if len(request.form.getlist('btnradio')) > 0:
            btnradio = request.form.getlist('btnradio')
            btnradio = btnradio[0]
            sentence = Sentence()
            sentence.source = btnradio
            print(sentence.source)
            # sen = MultipleTranslator("The cat is white").multiple_translations(languages)
            english_sentence = sentence.draw()
            sen = MultipleTranslator(english_sentence).multiple_translations(languages)
            # translations = Display().translations(sen)
            translations = [translation.text for translation in sen]
            pronunciations = [pronunciation.pronunciation if not (pronunciation.pronunciation in translations or pronunciation.pronunciation == english_sentence) else '&nbsp;' for pronunciation in sen]

            accordion = Display().accordion(languages, translations, pronunciations)
            small = sentence.level
            print(small)

            # langs checked
            checked_list_short = ["checked" if lang in languages else "" for lang in Languages().lang_list_short]
            checkboxes_short = Display().checkboxes(Languages().lang_list_short, "short", checked_list_short)
            checked_list_diff = ["checked" if lang in languages else "" for lang in Languages().lang_diff()]
            checkboxes_diff = Display().checkboxes(Languages().lang_diff(), "diff", checked_list_diff)

            # radio checked
            if btnradio == "1":
                checked_easy = "checked"
                checked_hard = ""
                checked_random = ""
            elif btnradio == "2":
                checked_easy = ""
                checked_hard = "checked"
                checked_random = ""
            else:
                checked_easy = ""
                checked_hard = ""
                checked_random = "checked"

    print(languages, btnradio)
    print(english_sentence)
    return render_template("index.html", content_form=form, content_sentence=english_sentence, content_translations=translations, content_checkboxes_diff=checkboxes_diff, content_checkboxes_short=checkboxes_short, content_checked_easy=checked_easy, content_checked_hard=checked_hard, content_checked_random=checked_random, content_accordion=accordion, content_small=small)

if __name__ == "__main__":
    app.run(debug=False)


# licnecja https://huggingface.co/datasets/generics_kb?fbclid=IwAR07Hh1JT16IbRJJjg13wvFYVNWMltU462-bvqp-atzxLRLE-3PNy845q8Q

