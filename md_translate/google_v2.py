from google.cloud import translate_v2 as translate
from google.cloud.translate_v2 import Client
from html import unescape   # >= Python 3.5


class GoogleV2:

    @staticmethod
    def translate_v2(src: str, from_language="ko", to_language="en", model="nmt"):
        r = src
        translate_client: Client = translate.Client()
        if translate_client.detect_language(src)['language'] == from_language:
            r = unescape(translate_client.translate(src, target_language=to_language, source_language=from_language,
                                                    model=model)["translatedText"])
        return r


_google_v2 = GoogleV2()
google_v2 = _google_v2.translate_v2
