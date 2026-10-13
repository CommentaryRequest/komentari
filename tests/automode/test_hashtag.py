from tests.automode.util import detect_tags_simple
from booru.commentary import Commentary
import settings

def test_automode_hashtag():
    # Hashtag-only commentary
    # https://danbooru.donmai.us/posts/10841093
    assert detect_tags_simple(Commentary('"#GenshinImpact":[https://x.com/hashtag/GenshinImpact] "#Columbina":[https://x.com/hashtag/Columbina]', None, None, None)) == settings.AUTOTAG_HC

    # Hashtag-only untranslatable
    # othernames file must be present for this test to pass
    # https://danbooru.donmai.us/posts/11004370
    assert detect_tags_simple(Commentary('"#トリッカル":[https://x.com/hashtag/トリッカル]', None, None, None)) == settings.AUTOTAG_HU

    # General tag othername match.
    # https://danbooru.donmai.us/posts/12333240
    assert detect_tags_simple(Commentary('"#家団":[https://x.com/hashtag/家団]', None, None, None)) == settings.AUTOTAG_HU

    # Hashtag-only request
    # https://danbooru.donmai.us/posts/10870472
    assert detect_tags_simple(Commentary('"#みんなの正面顔が見たい":[https://misskey.design/tags/%E3%81%BF%E3%82%93%E3%81%AA%E3%81%AE%E6%AD%A3%E9%9D%A2%E9%A1%94%E3%81%8C%E8%A6%8B%E3%81%9F%E3%81%84]', None, None, None)) == settings.AUTOTAG_HR
