import parser
import zhchk
import jpchk
import thchk
import kkchk
import enrecog
import re
import symchk
import numchk
import cleaner
import settings
import chartag_annihilater
import hashtag_extractor
import json
import debug
import os
from urllib.parse import urlparse

UNTITLED_TITLES = [
    "untitled",
    "no title",
    "no_title"
]

def is_chinese_source(url):
    debug.dprint(f"Checking if {url} is a Chinese source")

    if not url:
        return False

    try:
        netloc = urlparse(url).netloc.lower()
    except Exception as exc:
        print(f"Error when parsing URL {url}: {exc}")
        return False
    
    netloc = netloc.split(":")[0]
    for domain in settings.CHINESE_SOURCES:
        if netloc == domain or netloc.endswith("." + domain):
            debug.dprint(f"Found match: {netloc} and {domain}")
            return True
        debug.dprint(f"Did not match {netloc} with {domain}")
    return False

en_model = {}
def get_model():
    global en_model
    if not en_model:
        en_model = enrecog.load_model("./enmodel.json")
    return en_model

def check_en(commentary):
    commentary = re.sub(r"\d", " ", commentary)
    commentary = "".join([ch if not symchk.test_category(ch) else " " for ch in commentary])
    confidence = enrecog.score_text(commentary, get_model())
    debug.dprint(f"Confidence for text = '{commentary}': {confidence}")
    return confidence

othernames = []
def get_othernames():
    global othernames
    if not othernames:
        if not os.path.exists("othernames.json"):
            return []
        with open("othernames.json", "r") as othernames_file:
            othernames = json.load(othernames_file)
    return othernames

def othername_match(h):
    return h in get_othernames()

def empty_or_symbols(s):
    s = s.strip()
    return len(s) == 0 or symchk.is_symbol_only(s)

def is_empty(s):
    return not s or not s.strip()

def is_latin_hashtag(h):
    return not jpchk.detect_jp_chars(h) and not kkchk.detect_kr_chars(h) and not thchk.detect_th_chars(h)

def detect_hashtag_only(s):
    hashtags = hashtag_extractor.extract_hashtags(s)
    debug.dprint(hashtags)
    if all(is_latin_hashtag(h) for h in hashtags):
        return settings.AUTOTAG_HC

    if all(othername_match(h) or is_latin_hashtag(h) for h in hashtags):
        return settings.AUTOTAG_HU

    return settings.AUTOTAG_HR

def has_foreign_chars(text):
    if is_empty(text):
        return False
    text = cleaner.remove_hashtags(text)
    text = cleaner.remove_fullwidth(text)
    text = cleaner.remove_invisible_chars(text)
    return jpchk.detect_jp_chars(text) or kkchk.detect_kr_chars(text) or thchk.detect_th_chars(text) or "ó" in text

def detect_translated(commentary):
    # TODO https://danbooru.donmai.us/posts/11880266

    og_title_empty = is_empty(commentary.og_title)
    tl_title_empty = is_empty(commentary.tl_title)
    og_desc_empty = is_empty(commentary.og_description)
    tl_desc_empty = is_empty(commentary.tl_description)

    # Handle untranslated commentaries and weird abnormalities
    # where the commentary is translated but there's no original
    # commentary.
    if (tl_title_empty and tl_desc_empty) or (og_title_empty and og_desc_empty):
        return None

    # Full translation:
    #  * Each original field has its corresponding translation.
    #  * For simplicity's sake, any translations with non-english
    #    characters are ignored. This may be due to the commentary
    #    being bilingual or the translation being partial and
    #    I'd just go through that stuff manually.
    if has_foreign_chars(commentary.tl_title) or has_foreign_chars(commentary.tl_description):
        return None

    og_title_foreign = has_foreign_chars(commentary.og_title)
    og_desc_foreign = has_foreign_chars(commentary.og_description)

    full_title_translated = ((og_title_empty or not og_title_foreign) and tl_title_empty) or (not og_title_empty and not tl_title_empty)
    full_description_translated = ((og_desc_empty or not og_desc_foreign) and tl_desc_empty) or (not og_desc_empty and not tl_desc_empty)
    debug.dprint(f"ote={og_title_empty} tte={tl_title_empty} ode={og_desc_empty} tde={tl_desc_empty} otf={og_title_foreign} odf={og_desc_foreign}\nftt={full_title_translated} fdt={full_description_translated}")
    if full_title_translated and full_description_translated:
        return settings.AUTOTAG_TF

    if (full_title_translated and not full_description_translated) or (full_description_translated and not full_title_translated):
        return settings.AUTOTAG_TP

    return None

def detect_tags(commentary, post_id, chartags, quiet, source):
    if not is_empty(commentary.tl_title) != 0 or not is_empty(commentary.tl_description) != 0:
        tags = detect_translated(commentary)
        return tags

    # Empty commentary
    if is_empty(commentary.og_title) and is_empty(commentary.og_description):
        return None

    # Untitled
    if commentary.og_title and commentary.og_title.strip().lower() in UNTITLED_TITLES and is_empty(commentary.og_description):
        return settings.AUTOTAG_UN

    # Flatten the commentary into a single string
    clean_commentary = (commentary.og_title or "") + " " + (commentary.og_description or "")
    debug.dprint(f"clean commentary = {clean_commentary}")

    # Remove invisible chars
    clean_commentary = cleaner.remove_invisible_chars(clean_commentary)
    if len(clean_commentary.strip()) == 0:
        print("Only invisible characters")
        return parser.NONPERMANENT_SKIP

    # Remove hashtags
    hashtags_commentary = clean_commentary
    clean_commentary = cleaner.remove_hashtags(clean_commentary)
    debug.dprint(f"remove hashtags = {clean_commentary}")
    manual_input = False
    if len(clean_commentary.strip()) == 0:
        return detect_hashtag_only(hashtags_commentary)

    # Remove URLs
    clean_commentary = cleaner.remove_urls(clean_commentary)
    debug.dprint(f"remove urls = {clean_commentary}")

    # Check if there's only URLs left
    if is_empty(clean_commentary):
        return settings.AUTOTAG_UR

    # Check if there's only symbols left
    is_symbol_only = symchk.is_symbol_only(clean_commentary)
    if is_symbol_only:
        return settings.AUTOTAG_SY

    # Remove bloat
    clean_commentary = cleaner.remove_bloat(clean_commentary)
    debug.dprint(f"remove bloat = {clean_commentary}")

    # If there's only bloat or bloat with emojis
    if empty_or_symbols(clean_commentary):
        return settings.AUTOTAG_BL

    # Annihilate chartags
    clean_commentary = chartag_annihilater.chartag_annihilate(clean_commentary, chartags)
    debug.dprint(f"remove chartags = {clean_commentary}")
    if len(clean_commentary.strip()) == 0 or symchk.is_symbol_only(clean_commentary.strip()): # only chartags w symbols
        return settings.AUTOTAG_CT

    # Remove fullwidth characters
    clean_commentary = cleaner.remove_fullwidth(clean_commentary)
    debug.dprint(f"remove fullwidth = {clean_commentary}")
    if len(clean_commentary.strip()) == 0 or symchk.is_symbol_only(clean_commentary.strip()):
        return settings.AUTOTAG_FW

    if kkchk.is_korea(clean_commentary):
        return settings.AUTOTAG_KK
    # TODO implement a non-Chinese source Chinese detector
    if is_chinese_source(source) and zhchk.zhongwen_yuyan_jiance_xitong(clean_commentary):
        return settings.AUTOTAG_CN
    if jpchk.is_japan(clean_commentary):
        return settings.AUTOTAG_JP
    if thchk.is_thai(clean_commentary):
        return settings.AUTOTAG_TH
    if numchk.is_numbers(clean_commentary):
        return settings.AUTOTAG_NM
    if numchk.is_numbers(symchk.strip_symbols(clean_commentary)):
        return settings.AUTOTAG_NS

    confidence = check_en(clean_commentary)
    if not has_foreign_chars(clean_commentary) and confidence >= settings.ENGLISH_CONFIDENCE:
        return settings.AUTOTAG_EN

    return None

def parse(commentary, semi_auto, quiet, post_id, chartags, dry, source):
    tags = detect_tags(commentary, post_id, chartags, quiet, source)

    if dry:
        print(f"Detected tags: {tags or 'none'}")
        return "", True

    if tags is None:
        if semi_auto:
            return "", True
    
        if settings.UNRECOG_FAVGROUP == 0:
            return parser.NONPERMANENT_SKIP, False   
        return f"favgroup:{settings.UNRECOG_FAVGROUP}", False

    return tags, False
