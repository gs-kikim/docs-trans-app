from google.cloud import translate_v2 as translate
from google.cloud.translate_v2 import Client
from html import unescape  # >= Python 3.5


class SingletonInstance:
    _instance = None

    @classmethod
    def _get_instance(cls):
        return cls._instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls._instance = cls(*args, **kargs)
        cls.instance = cls._get_instance
        return cls._instance


class _GoogleV2(object):

    def __init__(self):
        self._translate_client = None

    def _get_translate_client(self) -> Client:
        if not self._translate_client:
            self._translate_client = translate.Client()
        return self._translate_client

    def translate_v2(self, src: str, from_language="ko", to_language="en", model="nmt"):
        return unescape(
            self._get_translate_client().translate(src, target_language=to_language, source_language=from_language,
                                                   model=model)["translatedText"])

    def is_detected(self, src, from_language):
        return True if self._get_translate_client().detect_language(src)['language'] == from_language else False


class GoogleV2(_GoogleV2, SingletonInstance):
    pass


instance = GoogleV2.instance()
google_v2 = instance.translate_v2
is_detected = instance.is_detected
