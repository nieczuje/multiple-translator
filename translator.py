
import pandas as pd
import random
import re
from googletrans import Translator
from flask import Flask, redirect, url_for, render_template, request


class Languages():
    def __init__(self):
        self.lang_list = ["af", "ach", "ak", "am", "ar", "az", "be", "bem", "bg", "bh", "bn", "br", "bs", "ca", "chr", "ckb", "co", "crs", "cs", "cy", "da", "de", "ee", "el", "en", "eo", "es", "es-419", "et", "eu", "fa", "fi", "fo", "fr", "fy", "ga", "gaa", "gd", "gl", "gn", "gu", "ha", "haw", "hi", "hr", "ht", "hu", "hy", "ia", "id", "ig", "is", "it", "iw", "ja", "jw", "ka", "kg", "kk", "km", "kn", "ko", "kri", "ku", "ky", "la", "lg", "ln", "lo", "loz", "lt", "lua", "lv", "mfe", "mg", "mi", "mk", "ml", "mn", "mo", "mr", "ms", "mt", "ne", "nl", "nn", "no", "nso", "ny", "nyn", "oc", "om", "or", "pa", "pcm", "pl", "ps", "pt", "pt-BR", "pt-PT", "qu", "rm", "rn", "ro", "ru", "rw", "sd", "sh", "si", "sk", "sl", "sn", "so", "sq", "sr", "sr-ME", "st", "su", "sv", "sw", "ta", "te", "tg", "th", "ti", "tk", "tl", "tn", "to", "tr", "tt", "tum", "tw", "ug", "uk", "ur", "uz", "vi", "wo", "xh", "xx-bork", "xx-elmer", "xx-hacker", "xx-klingon", "xx-pirate", "yi", "yo", "zh-CN", "zh-TW", "zu"]
        self.lang_list_short = ["ar", "de", "es", "fr", "it", "iw", "ja", "ko", "pl", "pt", "ru", "tr", "uk", "zh-CN"]
        self.lang_list_error = ["pt-PT", "ach", "ak", "bem", "bh", "br", "chr", "ckb", "es-419", "fo", "gaa", "gn", "ia", "kg", "kri", "lg", "ln", "loz", "lua", "mfe", "mo", "nn", "nso", "nyn", "oc", "om", "pcm", "pt-BR", "qu", "rm", "rn", "rw", "sh", "sr-ME", "ti", "tk", "tl", "tn", "to", "tt", "tum", "tw", "ug", "ur", "uz", "vi", "wo", "xh", "xx-bork", "xx-elmer", "xx-hacker", "xx-klingon", "xx-pirate"]

    def lang_diff(self):
        return [lang for lang in self.lang_list if not (lang in self.lang_list_short or lang in self.lang_list_error or lang == "en")]


class Sentence():
    def __init__(self):
        with open('sentences_base.txt') as f:
            self.lines = f.readlines()
        self.df = pd.read_csv("GenericsKB-Best.tsv", sep='\t')
        self.level = ""
    
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

        # ascii apostrophe, possible solution https://stackoverflow.com/questions/55737316/python-selenium-text-returns-%C3%A2%E2%82%AC-instead-of-apostrophe
        sentence = sentence.replace(u"â€™", "'")
        sentence = sentence.replace(u"…", "...")

        return sentence


class MultipleTranslator():
    def __init__(self, sentence):
        self.sentence = sentence
        self.translator = Translator()

    def single_translation(self, dest_lang):
        return self.translator.translate(self.sentence, src='en', dest=dest_lang)

    def multiple_translations(self, dest_lang_list):
        return [self.single_translation(lang) for lang in dest_lang_list]


class Display():
    def __init__(self):
        pass
    
    def checkbox(self, lang, checked):
        return '<li><div class="form-check"><input class="form-check-input" type="checkbox" name="languages" value="' + lang + '" id="flexCheckDefault_' + lang + '" ' + checked + '/><label class="form-check-label" for="flexCheckDefault_' + lang + '">' + lang + '</label></div></li>'
    
    def checkboxes(self, langs, html_class, checked_list):
        checkboxes = '<ul class="' + html_class + '">'
        for count, lang in enumerate(langs):
            checkboxes += self.checkbox(lang, checked_list[count])
        checkboxes += '</ul>'
        return checkboxes
    
    def digit_to_text(self, digit):
        return ['zero','one','two','three','four','five','six','seven','eight','nine'][digit].capitalize()
    
    def accordion_item(self, lang, translation, num, pronunciation):
        return '''<div class="accordion-item">
            <h2 class="accordion-header" id="panelsStayOpen-heading''' + self.digit_to_text(num) + '''">
              <button
                class="accordion-button"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#panelsStayOpen-collapse''' + self.digit_to_text(num) + '''"
                aria-expanded="false"
                aria-controls="panelsStayOpen-collapse''' + self.digit_to_text(num) + '''"
              >
                ''' + lang + '''
              </button>
            </h2>
            <div
              id="panelsStayOpen-collapse''' + self.digit_to_text(num) + '''"
              class="accordion-collapse collapse"
              aria-labelledby="panelsStayOpen-heading''' + self.digit_to_text(num) + '''"
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
            if count == 9:
                break
            accordion += self.accordion_item(lang, translations[count], count + 1, pronunciations[count])
        accordion += '</div>'
        return accordion


languages = []
inlineRadioOptions = 2
sentence = ""
english_sentence = "aaa"
translations = ""
btnradio = "1"
checked_easy = ""
checked_hard = ""
checked_random = ""
accordion = ""
small = ""
input_text = ""
english_sentence_old = "bbb"

checked_list_short = ["" for lang in Languages().lang_list_short]
checked_list_diff = ["" for lang in Languages().lang_diff()]

checkboxes_short = Display().checkboxes(Languages().lang_list_short, "short", checked_list_short)
checkboxes_diff = Display().checkboxes(Languages().lang_diff(), "diff", checked_list_diff)


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
    global input_text
    global english_sentence_old
    if request.method == 'POST':
        if len(request.form.getlist('languages')) > 0:
            languages = request.form.getlist('languages')
        if len(request.form.getlist('btnradio')) > 0 and len(request.form.get('input_text')) > 0:
            btnradio = request.form.getlist('btnradio')
            btnradio = btnradio[0]

            print("aaaaall", sentence)
            if sentence != "":
                small = sentence.level
            print(small)

            print("input_text", request.form.get('input_text'), english_sentence_old, english_sentence)
            print("c", english_sentence_old)
            print("d", request.form.get('input_text'))
            if english_sentence_old == request.form.get('input_text'):
                print("wygneerowane", english_sentence_old, english_sentence)
            else:
                print("user input sentence!!", request.form.get('input_text'))
                english_sentence = request.form.get('input_text')
                small = "Your sentence"

            sentence = Sentence()
            sentence.source = btnradio
            print(sentence.source)

            sen = MultipleTranslator(english_sentence).multiple_translations(languages)
            translations = [translation.text for translation in sen]
            pronunciations = [pronunciation.pronunciation if not (pronunciation.pronunciation in translations or pronunciation.pronunciation == english_sentence or pronunciation.pronunciation == None) else '&nbsp;' for pronunciation in sen]

            accordion = Display().accordion(languages, translations, pronunciations)

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
            
            english_sentence_old = english_sentence.rstrip()
            english_sentence = sentence.draw()


    print(languages, btnradio)
    print(english_sentence)
    return render_template("index.html", content_sentence=english_sentence_old, content_translations=translations, content_checkboxes_diff=checkboxes_diff, content_checkboxes_short=checkboxes_short, content_checked_easy=checked_easy, content_checked_hard=checked_hard, content_checked_random=checked_random, content_accordion=accordion, content_small=small)

if __name__ == "__main__":
    app.run(debug=False)


# licnecja https://huggingface.co/datasets/generics_kb?fbclid=IwAR07Hh1JT16IbRJJjg13wvFYVNWMltU462-bvqp-atzxLRLE-3PNy845q8Q

