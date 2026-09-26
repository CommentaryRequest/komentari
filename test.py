import parser
import automode
import settings
import cleaner
import hashtag_extractor
from commentary import Commentary

def test_parser():
    # Simple
    assert parser.parse("r") == "commentary_request"

    # Random spacing
    assert parser.parse(" r ee   c") == "commentary_request english_commentary commentary commentary"

    # Invalid
    assert parser.parse("asdf") == parser.UNKNOWN_TAG

    # Invalid and valid
    assert parser.parse("r asdf") == parser.UNKNOWN_TAG

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

def test_hashtag_extractor():
    # https://danbooru.donmai.us/posts/10922444
    assert hashtag_extractor.extract_hashtags('"#ミクの日":[https://x.com/hashtag/ミクの日] "#ミクの日2026":[https://x.com/hashtag/ミクの日2026]') == ["ミクの日", "ミクの日2026"]

def detect_tags_simple(commentary):
    return automode.detect_tags_all(commentary, 0, [], False, "https://example.com")

def test_automode_simple():
    # No commentary
    assert detect_tags_simple(Commentary(None, None, None, None)) == None

    # Untitled
    for title in automode.UNTITLED_TITLES:
        assert detect_tags_simple(Commentary(title, None, None, None)) == settings.AUTOTAG_UN

    # Hashtag-only commentary
    # https://danbooru.donmai.us/posts/10841093
    assert detect_tags_simple(Commentary('"#GenshinImpact":[https://x.com/hashtag/GenshinImpact] "#Columbina":[https://x.com/hashtag/Columbina]', None, None, None)) == settings.AUTOTAG_HC

    # Hashtag-only untranslatable
    # othernames file must be present for this test to pass
    # https://danbooru.donmai.us/posts/11004370
    assert detect_tags_simple(Commentary('"#トリッカル":[https://x.com/hashtag/トリッカル]', None, None, None)) == settings.AUTOTAG_HU

    # Hashtag-only request
    # https://danbooru.donmai.us/posts/10870472
    assert detect_tags_simple(Commentary('"#みんなの正面顔が見たい":[https://misskey.design/tags/%E3%81%BF%E3%82%93%E3%81%AA%E3%81%AE%E6%AD%A3%E9%9D%A2%E9%A1%94%E3%81%8C%E8%A6%8B%E3%81%9F%E3%81%84]', None, None, None)) == settings.AUTOTAG_HR

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

def test_automode_complex():
    # English commentary with character tags
    # (futa) https://danbooru.donmai.us/posts/11900986
    assert automode.detect_tags_all(Commentary(None, "Yoshizawa Kasumi and Sakura Futaba from Persona 5 (futa)", None, None), 0, "necronomicon_(persona_5) oracle_(persona_5) sakura_futaba violet_(persona_5) yoshizawa_kasumi".split(), False, None) == settings.AUTOTAG_EN

    # Non-English commentary with character tags
    # (nsfw) https://danbooru.donmai.us/posts/11969656
    assert automode.detect_tags_all(Commentary(None, "Kanna e tal part 1 (Comisión)", None, None), 0, ["kanna_kamui"], False, None) is None

    # Chinese
    # https://danbooru.donmai.us/posts/10706960
    assert automode.detect_tags_all(Commentary("惬意之~🏍️✨琳奈美成啥了", '"#鸣潮":[https://www.xiaohongshu.com/search_result?keyword=鸣潮] "#鸣潮创作激励":[https://www.xiaohongshu.com/search_result?keyword=鸣潮创作激励] "#鸣潮琳奈":[https://www.xiaohongshu.com/search_result?keyword=鸣潮琳奈] "#鸣潮我们生而眺望":[https://www.xiaohongshu.com/search_result?keyword=鸣潮我们生而眺望]', None, None), 0, [], False, "https://www.xiaohongshu.com/explore/69523346000000002200b44e?xsec_token=ABvfE_KuJoV2hFNhq7kubXglVejGewcScYEnZ8inmQ_CA=") == settings.AUTOTAG_CN

    # Japanese commentary from Chinese source
    # https://danbooru.donmai.us/posts/10688561
    assert automode.detect_tags_all(Commentary(None, '#さいはて駅#":[https://s.weibo.com/weibo?q=%23さいはて駅%23]"#终焉车站#":[https://s.weibo.com/weibo?q=%23终焉车站%23] 先輩のこと 苦しめた人たちを消せば 良いんだって………")', None, None), 0, [], False, 'https://www.weibo.com/6482130941/5082512617115157') == settings.AUTOTAG_JP

    # Only character tags
    # https://danbooru.donmai.us/posts/10706592
    assert automode.detect_tags_all(Commentary("Laevatain", None, None, None), 0, "laevatain_(arknights) surtr_(arknights)".split(), False, None) == settings.AUTOTAG_CT

def alt_text_commentary(description, alt_text):
    return Commentary(None, f"{description}\n\n[quote]\nh6. Image Description\n\n{alt_text}\n[/quote]", None, None)

def test_automode_additional():
    # English with alt text
    # https://danbooru.donmai.us/posts/12251811
    assert detect_tags_simple(alt_text_commentary("mornings", "A digital painting of eevee\n\nIn a bedroom in the morning, sunlight streams through the window. A man getting ready for work is using a lint roller to remove fur from his dress shirt. A toy brought by the eevee is sitting on top of his work bag. He tries to check the time, but the eevee's tail, playfully swishing over his shoulder, is blocking his view. He's about to be late for work")) == settings.AUTOTAG_EN + " " + settings.AUTOTAG_AT

    # Japanese with alt text
    # Deliberate fake example that has more EN than JP characters, in the form of the Image Description heading.
    # It should be ignored by the detector.
    assert detect_tags_simple(alt_text_commentary("あ", "ﾃｽﾃｽ")) == settings.AUTOTAG_JP + " " + settings.AUTOTAG_AT

    # Date matching test
    DATES = [
        "2026-09-09",
        "2026-9-9",
        "2026-9-09",
        "2010/04/13",
        "1984-07-11",
        "20260909",
        "2026年10月10日",
        "2026年9月9日",
        "2014.11",
        "2026.09",
        "2025.6"
    ]
    for date in DATES:
        assert settings.AUTOTAG_DT in detect_tags_simple(Commentary(date, None, None, None))

    # These aren't dates, it should not match them.
    NOT_DATES = [
        "3.14.15",
        "1920-1080-144",
        "1-2-3",
        "100/200/300",
        "12.34.56",
        "200-02/22",
        "2026-67-67", # six sevennn
        "01010101",
        "12121212",
        "2026年10日10月", # In before I find this in an actual post
        "226年00月00日",
        "2026年11月99日",
        "2014.00",
        "2014-13"
    ]
    for not_date in NOT_DATES:
        assert settings.AUTOTAG_DT not in detect_tags_simple(Commentary(not_date, None, None, None))

    # https://danbooru.donmai.us/posts/12262727
    assert detect_tags_simple(Commentary(None, 'コラボキャンペーン開催決定！\r\n\r\nTVアニメ「らんま1/2」× ラウンドワン\r\n\r\n【開催期間】\r\n2026年10月10日(土)～2027年1月11日(月・祝)\r\n\r\n<https://animetoyinfo.com/2026/09/26/ranma-roksaof/>\r\n\r\n"#らんまアニメ":[https://x.com/hashtag/らんまアニメ]', None, None)) == settings.AUTOTAG_JP + " " + settings.AUTOTAG_DT

    # https://danbooru.donmai.us/posts/12253287
    assert detect_tags_simple(Commentary("20140610", "私はもう満足だ！！！私はとても幸せです！！！！", None, None)) == settings.AUTOTAG_JP + " " + settings.AUTOTAG_DT

    # https://danbooru.donmai.us/posts/12248626
    assert detect_tags_simple(Commentary("2023.10.31", "吸血鬼被抓到啦", None, None)) == settings.AUTOTAG_JP + " " + settings.AUTOTAG_DT

    # https://danbooru.donmai.us/posts/12255367
    assert detect_tags_simple(Commentary("願望", "2014.11", None, None)) == settings.AUTOTAG_JP + " " + settings.AUTOTAG_DT

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

    # https://danbooru.donmai.us/posts/12029039
    assert automode.detect_translated(Commentary("尾刃カンナ", "For HD version on patreon/fanbox :\n・<https://www.patreon.com/R0_Ref>\n・<https://ref.fanbox.cc>\nFollow me to on Twitter and Bluesky :\n・<https://x.com/r0_Ref>\n・<https://bsky.app/profile/r0ref.bsky.social>\nCommission :\n・<https://vgen.co/Ref>", "Ogata Kanna", "")) == settings.AUTOTAG_TF

    # https://danbooru.donmai.us/posts/11880266
    assert automode.detect_translated(Commentary("メイちゃん", "skebありがとございました！", "Rosa-chan", "skebありがとございました！")) == settings.AUTOTAG_TP

def test_cleaner():
    assert cleaner.remove_hashtags('"#Skeb":[https://twitter.com/hashtag/Skeb] commission') == " commission"
    assert cleaner.remove_bloat("Skebリクエストです。差分はPixivFANBOXで。") == "リクエストです。差分はで。"
    assert cleaner.remove_urls('<https://x.com/rokugou> [b]"twitter/rokugou":[https://twitter.com/rokugou][/b] twitter/rokugou [b]"user/11974199":[https://www.pixiv.net/users/11974199] "»":[/artists?search%5Burl_matches%5D=https%3A%2F%2Fwww.pixiv.net%2Fusers%2F11974199][/b] [b]pixiv #76512810 "»":[/posts?tags=pixiv%3A76512810][/b] "@jack":[https://twitter.com/jack] https://example.com').strip() == ""
    assert cleaner.remove_fullwidth("ｂｂｂｂｂｂfumo９") == "fumo"
    assert cleaner.remove_invisible_chars("testoᅠtesto") =="testotesto"
    assert cleaner.remove_alt_text("content\n\n[quote]\nh6. Image Description\n\nimage description\n[/quote]") == "content\n\nimage description"
