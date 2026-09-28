import automode
import settings
from booru.commentary import Commentary

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
