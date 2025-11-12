import parser
import jpchk
import kkchk
import recog
import emjchk
import numchk
import cleaner
import settings

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

def parse(commentary, semi_auto, en_log, quiet, post_id):
    if commentary.og_title.strip().lower() in UNTITLED_TITLES and len(commentary.og_description.strip()) == 0:
        parsed_input = "commentary"
        manual_input = False
    else:
        clean_commentary = commentary.og_title + " " + commentary.og_description

        clean_commentary = cleaner.remove_invisible_chars(clean_commentary)
        if len(clean_commentary.strip()) == 0:
            print("Only invisible characters")
            parsed_input = parser.NONPERMANENT_SKIP
            manual_input = False
        else:
            clean_commentary = cleaner.remove_hashtags(clean_commentary)
            manual_input = False
            if len(clean_commentary.strip()) == 0:
                # The commentary only contained hashtags
                parsed_input = "hashtag-only_commentary"
            else:
                clean_commentary = cleaner.remove_urls(clean_commentary)
                is_emoji = emjchk.is_emoji(clean_commentary)
                if is_emoji:
                    parsed_input = "symbol-only_commentary"
                else:
                    clean_commentary = cleaner.remove_bloat(clean_commentary)
                    if not quiet:
                        print(f"Clean commentary = {clean_commentary}")

                    # If there's only bloat or bloat with emojis
                    if len(clean_commentary.strip()) == 0 or emjchk.is_emoji(clean_commentary):
                        parsed_input = "commentary"
                        manual_input = False
                    else:
                        is_japan = jpchk.is_japan(clean_commentary)
                        is_korea = kkchk.is_korea(clean_commentary)
                        is_numbers = False #numchk.is_numbers(clean_commentary)
                        if is_korea:
                            parsed_input = "commentary_request korean_commentary"
                        elif is_japan:
                            parsed_input = "commentary_request"
                        elif is_numbers:
                            parsed_input = "commentary"
                        else:
                            confidence = check_en(clean_commentary, post_id, en_log)
                            if confidence >= 0.8:
                                parsed_input = "commentary english_commentary"
                            else:
                                if settings.UNRECOG_FAVGROUP == 0:
                                    parsed_input = parser.NONPERMANENT_SKIP
                                else:
                                    parsed_input = f"favgroup:{settings.UNRECOG_FAVGROUP}"
                                manual_input = semi_auto
    return parsed_input, manual_input
