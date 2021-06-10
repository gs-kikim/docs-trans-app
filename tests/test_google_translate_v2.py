import unittest


class MyTestCase(unittest.TestCase):

    def test_translate_v2(self, model="nmt"):
        """Translates text into the target language.

        Make sure your project is allowlisted.

        Target must be an ISO 639-1 language code.
        See https://g.co/cloud/translate/v2/translate-reference#supported_languages
        """
        from google.cloud import translate_v2 as translate

        translate_client = translate.Client()

        text = str("**Live Response**의 quicksearch 명령어를 이용해 검색하고자 할 경우 **지정 파일 목록 인덱싱** 설정을 '사용'으로 변경해야 합니다.")

        # Text can also be a sequence of strings, in which case this method
        # will return a sequence of results for each text.
        result = translate_client.translate(text, target_language="en", model=model)

        print(u"Text: {}".format(result["input"]))
        print(u"Translation: {}".format(result["translatedText"]))
        print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
    test = MyTestCase()
    test.test_translate_v2()
