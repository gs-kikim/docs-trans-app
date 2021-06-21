import pytest

from docs_translate import const
from docs_translate.exceptions import UnknownServiceError
from docs_translate.translator import get_translator_by_service_name


class TestUtils:
    @pytest.mark.parametrize('service_name, translator', [
        [const.TRANSLATION_SERVICE_YANDEX, const.yandex],
        [const.TRANSLATION_SERVICE_GOOGLE, const.google],
        [const.TRANSLATION_SERVICE_BING, const.bing],
        [const.TRANSLATION_SERVICE_DEEPL, const.deepl],
        [const.TRANSLATION_SERVICE_GOOGLE_V2, const.google_v2],
        ['bad service name', None],
    ])
    def test_get_translator_class(self, service_name, translator):
        if service_name in const.TRANSLATOR_BY_SERVICE_NAME:
            assert get_translator_by_service_name(service_name) == translator
        else:
            with pytest.raises(UnknownServiceError):
                get_translator_by_service_name(service_name)
