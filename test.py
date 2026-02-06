import parser
import automode
import settings
import cleaner
from commentary import Commentary

def test_parser():
    # Simple
    assert parser.parse("r") == "commentary_request"

    # Random spacing
    assert parser.parse(" r ee   c") == "commentary_request english_commentary commentary commentary"

    # Invalid
    assert parser.parse("asdf") == parser.ERROR

    # Invalid and valid
    assert parser.parse("r asdf") == f"commentary_request {parser.ERROR}"

    # Literal tags
    assert parser.parse("~1girl") == "1girl"

    # Negative tags
    assert parser.parse("-r") == "-commentary_request"
    assert parser.parse("-ee") == "-english_commentary -commentary"

    # Special commands
    assert parser.parse("h") == parser.HELP
    assert parser.parse("sk") == parser.SKIP
    assert parser.parse("q") == parser.QUIT
    assert parser.parse("b") == parser.BROWSER
    assert parser.parse("skk") == parser.NONPERMANENT_SKIP

def detect_tags_simple(commentary):
    return automode.detect_tags(commentary, 0, False, [], False, "https://example.com")

def test_automode_simple():
    # No commentary
    assert detect_tags_simple(Commentary(None, None, None, None)) == None

    # Untitled
    for title in automode.UNTITLED_TITLES:
        assert detect_tags_simple(Commentary(title, None, None, None)) == settings.AUTOTAG_UN

    # Hashtag-only
    assert detect_tags_simple(Commentary(None, "\"#ALNST\":[https://twitter.com/hashtag/ALNST] \"#에이스테\":[https://twitter.com/hashtag/에이스테] \"#SUA\":[https://twitter.com/hashtag/SUA]", None, None)) == settings.AUTOTAG_HT

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

def test_automode_complex():
    # English commentary with character tags
    # https://danbooru.donmai.us/posts/10707268
    assert automode.detect_tags(Commentary(None, "Mega Gardevoir, Midnight Lycanroc and Froslass Fusion 🤍🌙 (Commission)", None, None), 0, False, "froslass gardevoir lycanroc lycanroc_(midnight) mega_gardevoir".split(), False, None) == settings.AUTOTAG_EN

    # Chinese
    # https://danbooru.donmai.us/posts/10706960
    assert automode.detect_tags(Commentary("惬意之~🏍️✨琳奈美成啥了", '"#鸣潮":[https://www.xiaohongshu.com/search_result?keyword=鸣潮] "#鸣潮创作激励":[https://www.xiaohongshu.com/search_result?keyword=鸣潮创作激励] "#鸣潮琳奈":[https://www.xiaohongshu.com/search_result?keyword=鸣潮琳奈] "#鸣潮我们生而眺望":[https://www.xiaohongshu.com/search_result?keyword=鸣潮我们生而眺望]', None, None), 0, False, [], False, "https://www.xiaohongshu.com/explore/69523346000000002200b44e?xsec_token=ABvfE_KuJoV2hFNhq7kubXglVejGewcScYEnZ8inmQ_CA=") == settings.AUTOTAG_CN

    # Japanese commentary from Chinese source
    # https://danbooru.donmai.us/posts/10688561
    assert automode.detect_tags(Commentary(None, '#さいはて駅#":[https://s.weibo.com/weibo?q=%23さいはて駅%23]"#终焉车站#":[https://s.weibo.com/weibo?q=%23终焉车站%23] 先輩のこと 苦しめた人たちを消せば 良いんだって………")', None, None), 0, False, [], False, 'https://www.weibo.com/6482130941/5082512617115157') == settings.AUTOTAG_JP

    # Only character tags
    # https://danbooru.donmai.us/posts/10706592
    assert automode.detect_tags(Commentary("Laevatain", None, None, None), 0, False, "laevatain_(arknights) surtr_(arknights)".split(), False, None) == settings.AUTOTAG_CT

def test_automode_translated():
    # Full commentary, full translation
    assert automode.detect_translated(Commentary("解説", "リクエスト", "Commentary", "Request")) == settings.AUTOTAG_TF

    # Only translated title
    assert automode.detect_translated(Commentary("解説", None, "Commentary", None)) == settings.AUTOTAG_TF

    # Only translated description
    assert automode.detect_translated(Commentary(None, "リクエスト", None, "Request")) == settings.AUTOTAG_TF

    # Full commentary, only title/description translated
    assert automode.detect_translated(Commentary("解説リクエスト", "ミクミクビーム　ゆっくりしていってね", "Commentary Request", None)) == settings.AUTOTAG_TP
    assert automode.detect_translated(Commentary("解説リクエスト", "ミクミクビーム　ゆっくりしていってね", None, "Miku Miku Beam Take it easy")) == settings.AUTOTAG_TP

    # Full commentary, full title translation, partial description translation
    assert automode.detect_translated(Commentary("解説リクエスト", "ミクミクビーム　ゆっくりしていってね", "Commentary Request", "Miku Miku Beam ゆっくりしていってね")) == None

    # Abnormality
    assert automode.detect_translated(Commentary(None, None, "Commentary", "Request")) == None

def test_cleaner():
    assert cleaner.remove_hashtags('"#Skeb":[https://twitter.com/hashtag/Skeb] commission') == " commission"
    assert cleaner.remove_bloat("Skebリクエストです。差分はPixivFANBOXで。") == "リクエストです。差分はで。"
    assert cleaner.remove_urls('<https://x.com/rokugou> [b]"twitter/rokugou":[https://twitter.com/rokugou][/b] twitter/rokugou [b]"user/11974199":[https://www.pixiv.net/users/11974199] "»":[/artists?search%5Burl_matches%5D=https%3A%2F%2Fwww.pixiv.net%2Fusers%2F11974199][/b] [b]pixiv #76512810 "»":[/posts?tags=pixiv%3A76512810][/b] "@jack":[https://twitter.com/jack] https://example.com').strip() == ""
    assert cleaner.remove_fullwidth("ｂｂｂｂｂｂfumo９") == "fumo"
    assert cleaner.remove_invisible_chars("testoᅠtesto") == "testotesto"
