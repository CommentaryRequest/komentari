from tests.automode.util import detect_tags_simple, alt_text_commentary
from booru.commentary import Commentary
import settings

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
        "2025.6",
        "2017.7/17",
        "2026 02 14",
        "２００１．６"
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
        "2014-13",
        "2033211"
    ]
    for not_date in NOT_DATES:
        assert settings.AUTOTAG_DT not in detect_tags_simple(Commentary(not_date, None, None, None))

    # Some testing on real commentaries.
    # https://danbooru.donmai.us/posts/12262727
    assert detect_tags_simple(Commentary(None, 'コラボキャンペーン開催決定！\r\n\r\nTVアニメ「らんま1/2」× ラウンドワン\r\n\r\n【開催期間】\r\n2026年10月10日(土)～2027年1月11日(月・祝)\r\n\r\n<https://animetoyinfo.com/2026/09/26/ranma-roksaof/>\r\n\r\n"#らんまアニメ":[https://x.com/hashtag/らんまアニメ]', None, None)) == settings.AUTOTAG_JP + " " + settings.AUTOTAG_DT
    # https://danbooru.donmai.us/posts/12253287
    assert detect_tags_simple(Commentary("20140610", "私はもう満足だ！！！私はとても幸せです！！！！", None, None)) == settings.AUTOTAG_JP + " " + settings.AUTOTAG_DT
    # https://danbooru.donmai.us/posts/12248626
    assert detect_tags_simple(Commentary("2023.10.31", "吸血鬼被抓到啦", None, None)) == settings.AUTOTAG_JP + " " + settings.AUTOTAG_DT
    # https://danbooru.donmai.us/posts/12255367
    assert detect_tags_simple(Commentary("願望", "2014.11", None, None)) == settings.AUTOTAG_JP + " " + settings.AUTOTAG_DT

    # Date inside a link, should be ignored.
    # https://danbooru.donmai.us/posts/1531590
    assert settings.AUTOTAG_DT not in detect_tags_simple(Commentary("Cosmic Star Heroine - Cover art", 'We finally unveiled the Teaser I\'d been working on with Dean Dodrill at the latest PAX, at a Sony indie-focused event. We also unveiled the cover art on the PS Blog along with a slew of sprites I\'d done. Check \'em out here:\r\n\r\n"blog.us.playstation.com/2013/0…":http://blog.us.playstation.com/2013/08/30/retro-sci-fi-rpg-cosmic-star-heroine-revealed-at-pax/\r\n\r\nNow I can post the cover art up on DA! yay!', None, None))

    # Same as above, but the link is in brackets.
    # Not sure if that changes anything but nice to have.
    # https://danbooru.donmai.us/posts/1562316
    assert settings.AUTOTAG_DT not in detect_tags_simple(Commentary("GnRまとめ", '◆ゲームプロジェクト「The Girl and the Robot」のKickstarter支援期間も残り３日！\r\nということで、GnRの一日一枚絵とキャラデザ・プロモ用イラストもろもろまとめました。\r\n◆ハヤニエモズさんがGnRの紹介記事を書いてくださいました！初・日本語記事です〜ありがとうございます！よかったらチェックしてみてください。（"http://nydgamer.blogspot.jp/2013/11/kickstarter-my-heartthe-girl-and-robot.html":[http://nydgamer.blogspot.jp/2013/11/kickstarter-my-heartthe-girl-and-robot.html]）\r\n◆そんなわけで、応援してもらえたらうれしいです。よろしくお願いします。(*_ _)The Girl and the Robot のKickstarterページ（"http://www.kickstarter.com/projects/2039811773/the-girl-and-the-robot?ref=card":[http://www.kickstarter.com/projects/2039811773/the-girl-and-the-robot?ref=card]）\r\n\r\n---\r\n"1/31P":http://www.pixiv.net/member_illust.php?mode=manga_big&illust_id=39940723&page=0'))
