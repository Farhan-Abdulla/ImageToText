import sys
import cv2
import requests
import io
from googletrans import Translator

"""
Class Description:
Represents the reader that uses OCR to pull text off of a photo, and translate it to the desired langauge
onto another .txt file called 'extracted_text_from_image.txt'

@author Farhan Abdulla
@version 2022.05.29
"""
class ImageReader:
    def __init__(self, path, key, fromLang, toLang='en'):
        """
        Initializes all ImageReader objects.
        @param path String containing the path to the image
        @param key String containing the api key
        @param fromLang String containing the language code of language in the image
        @param toLang String containing the language code of language to translate to.
            By default, it will translate to english.
        """
        self.fromLang = fromLang
        self.toLang = toLang
        self.translate(self.parse_text(path, key))

    def translate(self, text):
        """
        Translates the extracted text and writes the translation onto a .txt file
        @param text String containing the extracted text from image.
        """
        translator = Translator()
        translation = translator.translate(text, src=self.fromLang, dest=self.toLang)
        with open('extracted_text_from_image.txt', 'w') as f:
            f.write(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
            print('Text extraction successful')

    def parse_text(self, path, key):
        """
        Extracts text from image.
        @param path String containing the path to the image
        @param key String containing the api key
        @return String representing the text extracted.
        """
        file_bytes = self.__convert_image(path)
        result = requests.post('https://api.ocr.space/parse/image', 
            files = {path : file_bytes},
            data = {'apikey' : key,
                'language' : self.__swapcode()[self.fromLang]})
        result = result.json()
        text_detected = result.get('ParsedResults')[0].get('ParsedText')
        return text_detected
        
    def __convert_image(self, path):
        """
        Helper function to convert image into bytes.
        @param path String containing the path to the image
        @return bytes of the image
        """
        img = cv2.imread(path)
        _, compressed_img = cv2.imencode(path, img, [1, 90])
        file_bytes = io.BytesIO(compressed_img)
        if (sys.getsizeof(compressed_img) > 1000000):
            sys.exit('File is too large: +' + str(sys.getsizeof(compressed_img) - 1000000))
        return file_bytes

    def __swapcode(self):
        """
        Helper function to bridge the language codes from googletrans api to ocr.space api
        @return dictionary containing the language codes. Codes of googletrans api are mapped to
            codes of ocr.space api
        """
        dict = {'ar' : 'ara',
                'zh-cn' : 'chs',
                'hr' : 'hrv',
                'cs' : 'cze',
                'da' : 'dan',
                'nl' : 'dut',
                'en' : 'eng',
                'fi' : 'fin',
                'fr' : 'fre',
                'de' : 'ger',
                'el' : 'gre',
                'hu' : 'hun',
                'ko' : 'kor',
                'it' : 'ita',
                'ja' : 'jpn',
                'pl' : 'pol',
                'pt' : 'por',
                'ru' : 'rus',
                'sl' : 'slv',
                'es' : 'spa',
                'sv' : 'swe',
                'tr' : 'tur'}
        return dict