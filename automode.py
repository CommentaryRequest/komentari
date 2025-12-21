import parser
import jpchk
import kkchk
import recog
import emjchk
import numchk
import cleaner
import settings
import chartag_annihilater

UNTITLED_TITLES = [
    "untitled",
    "no title",
    "no_title"
]

def check_en(commentary, pid, en_log):
    confidence = recog.recog(commentary)

    if en_log:
        thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        for threshold in thresholds:
            if confidence >= threshold:
                write_confidence(str(threshold), pid, commentary, confidence)
    return confidence

def detect_tags(commentary, post_id, en_log, chartags, quiet):
    if commentary.og_title.strip().lower() in UNTITLED_TITLES and len(commentary.og_description.strip()) == 0:
        return settings.AUTOTAG_UN


    clean_commentary = commentary.og_title + " " + commentary.og_description

    # Remove invisible chars
    clean_commentary = cleaner.remove_invisible_chars(clean_commentary)
    if len(clean_commentary.strip()) == 0:
        print("Only invisible characters")
        return parser.NONPERMANENT_SKIP

    # Remove hashtags
    clean_commentary = cleaner.remove_hashtags(clean_commentary)
    manual_input = False
    if len(clean_commentary.strip()) == 0:
        # The commentary only contained hashtags
        return settings.AUTOTAG_HT

    # Remove URLs
    clean_commentary = cleaner.remove_urls(clean_commentary)

    # Check if there's only symbols left
    is_emoji = emjchk.is_emoji(clean_commentary)
    if is_emoji:
        return settings.AUTOTAG_SY

    # Remove bloat
    clean_commentary = cleaner.remove_bloat(clean_commentary)
    if not quiet:
        print(f"Clean commentary = {clean_commentary}")

    # If there's only bloat or bloat with emojis
    if len(clean_commentary.strip()) == 0 or emjchk.is_emoji(clean_commentary):
        return settings.AUTOTAG_BL

    # Annihilate chartags
    clean_commentary = chartag_annihilater.chartag_annihilate(clean_commentary, chartags)
    print(f"Clean commentary (after chartag annihilation) = {clean_commentary}")
    if len(clean_commentary.strip()) == 0 or emjchk.is_emoji(clean_commentary.strip()): # only chartags w emojis
        return settings.AUTOTAG_CT

    # Remove fullwidth characters
    clean_commentary = cleaner.remove_fullwidth(clean_commentary)
    if len(clean_commentary.strip()) == 0 or emjchk.is_emoji(clean_commentary.strip()):
        return settings.AUTOTAG_FW

    if kkchk.is_korea(clean_commentary):
        return settings.AUTOTAG_KK

    if jpchk.is_japan(clean_commentary):
        return settings.AUTOTAG_JP

    if False: # TODO
        return settings.AUTOTAG_NM

    confidence = check_en(clean_commentary, post_id, en_log)
    if confidence >= settings.ENGLISH_CONFIDENCE:
        return settings.AUTOTAG_EN

    return None

def parse(commentary, semi_auto, en_log, quiet, post_id, chartags, dry):
    tags = detect_tags(commentary, post_id, en_log, chartags, quiet)

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
