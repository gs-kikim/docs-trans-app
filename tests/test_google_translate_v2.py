import unittest
from google.cloud import translate_v2 as translate


class MyTestCase(unittest.TestCase):

    def test_translate_v2(self, model="nmt"):
        """Translates text into the target language.

        Make sure your project is allowlisted.

        Target must be an ISO 639-1 language code.
        See https://g.co/cloud/translate/v2/translate-reference#supported_languages
        """
        translate_client = translate.Client()

        src = str("**Live Response**의 quicksearch 명령어를 이용해 검색하고자 할 경우 **지정 파일 목록 인덱싱** 설정을 사용으로 변경해야 합니다.")
        dst = str("If you want to search using the quicksearch command in **Live Response**, you must change the **Index Specified File List** setting to Enabled.")

        # Text can also be a sequence of strings, in which case this method
        # will return a sequence of results for each text.
        result = translate_client.translate(src, target_language="en")

        print(u"Text: {}".format(result["input"]))
        print(u"Translation: {}".format(result["translatedText"]))
        print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))
        self.assertEqual(dst, result["translatedText"])


if __name__ == '__main__':
    unittest.main()
