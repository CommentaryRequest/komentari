from tests.automode.util import detect_tags_simple
from booru.commentary import Commentary
import automode
import parser
import settings

def test_automode_simple():
    # No commentary
    assert detect_tags_simple(Commentary(None, None, None, None)) == None

    # Untitled
    for title in automode.UNTITLED_TITLES:
        assert detect_tags_simple(Commentary(title, None, None, None)) == settings.AUTOTAG_UN


    # Invisible only
    assert detect_tags_simple(Commentary("\u3164\u1160\uffa0\u115f", None, None, None)) == parser.NONPERMANENT_SKIP

    # URLs only
    assert detect_tags_simple(Commentary("<https://x.com/rokugou>", None, None, None)) == settings.AUTOTAG_UR

    # Symbol-only (only symbols)
    assert detect_tags_simple(Commentary("🔥🔥🔥^%$^%$(*&(*&！・＠＃☎", None, None, None)) == settings.AUTOTAG_SY

    # Symbol-only (hashtags + URLs + symbols)
    assert detect_tags_simple(Commentary('⇨🐥 "#鳴潮":[https://twitter.com/hashtag/鳴潮] "#鳴潮コレクション":[https://twitter.com/hashtag/鳴潮コレクション] "#WutheringWaves":[https://twitter.com/hashtag/WutheringWaves] <https://example.com>', None, None, None)) == settings.AUTOTAG_SY

    # Bloat-only
    assert detect_tags_simple(Commentary("Skeb Pixiv FANBOX CM", None, None, None)) == settings.AUTOTAG_BL

    # Fullwidth-only
    assert detect_tags_simple(Commentary("ｈｄｋ５　ｉｓ　ｇａｙ", None, None, None)) == settings.AUTOTAG_FW

    # Simple Korean
    assert detect_tags_simple(Commentary("카사네 테스토123", "테스트 해설입니다.", None, None)) == settings.AUTOTAG_KK

    # Simple Japanese
    assert detect_tags_simple(Commentary("重音テスト123", "テストの解説です", None, None)) == settings.AUTOTAG_JP

    # Simple Thai
    assert detect_tags_simple(Commentary("บางอย่างในภาษาไทย", None, None, None)) == settings.AUTOTAG_TH

    # Numbers only
    assert detect_tags_simple(Commentary("1234", "43987345987", None, None)) == settings.AUTOTAG_NM

    # Numbers + symbols
    assert detect_tags_simple(Commentary("1234!", "12345🌈🌈🌈", None, None)) == settings.AUTOTAG_NS

    # English
    assert detect_tags_simple(Commentary("Testing commentary 123", "Example text", None, None)) == settings.AUTOTAG_EN

    # This is not English. This is Spanish.
    # (warning: rating:E self boob sucking) https://danbooru.donmai.us/posts/10711153
    assert detect_tags_simple(Commentary('El Stream se puso rico 🗿🔥 "#DigitalArtist":[https://twitter.com/hashtag/DigitalArtist] "#digitalart":[https://twitter.com/hashtag/digitalart] "#originalcharacter":[https://twitter.com/hashtag/originalcharacter] "#originalcharacterart":[https://twitter.com/hashtag/originalcharacterart] "#nsfw":[https://twitter.com/hashtag/nsfw] "#art":[https://twitter.com/hashtag/art] "#draw":[https://twitter.com/hashtag/draw] "#ArtistOnX":[https://twitter.com/hashtag/ArtistOnX] "#ArtistOnTwitter":[https://twitter.com/hashtag/ArtistOnTwitter] "#skalerart":[https://twitter.com/hashtag/skalerart]', None, None, None)) is None

    # Random gibberish
    assert detect_tags_simple(Commentary("weoifjw39irijwifjweofi jw3", None, None, None)) is None
