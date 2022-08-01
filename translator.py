
from googletrans import Translator

lang_list = ["af", "ach", "ak", "am", "ar", "az", "be", "bem", "bg", "bh", "bn", "br", "bs", "ca", "chr", "ckb", "co", "crs", "cs", "cy", "da", "de", "ee", "el", "en", "eo", "es", "es-419", "et", "eu", "fa", "fi", "fo", "fr", "fy", "ga", "gaa", "gd", "gl", "gn", "gu", "ha", "haw", "hi", "hr", "ht", "hu", "hy", "ia", "id", "ig", "is", "it", "iw", "ja", "jw", "ka", "kg", "kk", "km", "kn", "ko", "kri", "ku", "ky", "la", "lg", "ln", "lo", "loz", "lt", "lua", "lv", "mfe", "mg", "mi", "mk", "ml", "mn", "mo", "mr", "ms", "mt", "ne", "nl", "nn", "no", "nso", "ny", "nyn", "oc", "om", "or", "pa", "pcm", "pl", "ps", "pt-BR", "pt-PT", "qu", "rm", "rn", "ro", "ru", "rw", "sd", "sh", "si", "sk", "sl", "sn", "so", "sq", "sr", "sr-ME", "st", "su", "sv", "sw", "ta", "te", "tg", "th", "ti", "tk", "tl", "tn", "to", "tr", "tt", "tum", "tw", "ug", "uk", "ur", "uz", "vi", "wo", "xh", "xx-bork", "xx-elmer", "xx-hacker", "xx-klingon", "xx-pirate", "yi", "yo", "zh-CN", "zh-TW", "zu"]


class MultipleTranslator():
    def __init__(self, sentence):
        self.sentence = sentence
        self.translator = Translator()
    
    def single_translation(self, dest_lang):
        return self.translator.translate(sentence_example, src='en', dest=dest_lang)
    
    def multiple_translations(self, dest_lang_list):
        return [self.single_translation(lang) for lang in dest_lang_list]

    def __str__(self, dest_lang_list):
        for t in self.multiple_translations(dest_lang_list):
            print(t)


sentence_example = "The dog is big."

# x = MultipleTranslator(sentence_example).single_translation("de")
# print(x)

# x = MultipleTranslator(sentence_example).multiple_translations(["de"])
# print(x)

# x = MultipleTranslator(sentence_example).__str__(["de"])
x = MultipleTranslator(sentence_example).__str__(["de", "es"])


