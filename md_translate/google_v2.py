from google.cloud import translate_v2 as translate
from google.cloud.translate_v2 import Client


class GoogleV2:

    @staticmethod
    def translate_v2(src: str, from_language="ko", to_language="en", model="nmt"):
        translate_client: Client = translate.Client()
        result = translate_client.translate(src, target_language=to_language, source_language=from_language,
                                            model=model)
        return result["translatedText"]


_google_v2 = GoogleV2()
google_v2 = _google_v2.translate_v2
