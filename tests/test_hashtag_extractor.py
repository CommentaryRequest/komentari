import hashtag_extractor

def test_hashtag_extractor():
    # https://danbooru.donmai.us/posts/10922444
    assert hashtag_extractor.extract_hashtags('"#ミクの日":[https://x.com/hashtag/ミクの日] "#ミクの日2026":[https://x.com/hashtag/ミクの日2026]') == ["ミクの日", "ミクの日2026"]
