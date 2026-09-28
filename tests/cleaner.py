import cleaner

def test_cleaner():
    assert cleaner.remove_hashtags('"#Skeb":[https://twitter.com/hashtag/Skeb] commission') == " commission"
    assert cleaner.remove_bloat("Skebリクエストです。差分はPixivFANBOXで。") == "リクエストです。差分はで。"
    assert cleaner.remove_urls('<https://x.com/rokugou> [b]"twitter/rokugou":[https://twitter.com/rokugou][/b] twitter/rokugou [b]"user/11974199":[https://www.pixiv.net/users/11974199] "»":[/artists?search%5Burl_matches%5D=https%3A%2F%2Fwww.pixiv.net%2Fusers%2F11974199][/b] [b]pixiv #76512810 "»":[/posts?tags=pixiv%3A76512810][/b] "@jack":[https://twitter.com/jack] https://example.com').strip() == ""
    assert cleaner.remove_fullwidth("ｂｂｂｂｂｂfumo９") == "fumo"
    assert cleaner.remove_invisible_chars("testoᅠtesto") =="testotesto"
    assert cleaner.remove_alt_text("content\n\n[quote]\nh6. Image Description\n\nimage description\n[/quote]") == "content\n\nimage description"
