import automode
import settings
from booru.commentary import Commentary

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
