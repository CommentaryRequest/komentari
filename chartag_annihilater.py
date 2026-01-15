import re
import debug
import recog

def parse_chartag(chartag):
    chartag = re.sub(r"\(.*\)", "", chartag)
    words = chartag.split("_")
    words = [w for w in words if w not in recog.fetch_words()]
    debug.dprint(f"Parsed chartag {chartag} -> {words}")
    return words

def chartag_annihilate(commentary, chartags):
    if chartags is None:
        return commentary

    char_name_lists = [parse_chartag(chartag) for chartag in chartags]
    char_names = set()
    for char_name_list in char_name_lists:
        for element in char_name_list:
            char_names.add(element)
    debug.dprint(f"Char names: {char_names}")
    clean_commentary = commentary.lower()
    words = []
    for word in clean_commentary.split():
        fixed_word = recog.strip_emoji(recog.strip_punct(word))
        if len(fixed_word.strip()) == 0:
            words.append(word)
        else:
            words.append(fixed_word)
    clean_commentary = " ".join(words)
    debug.dprint(f"clean commentary = {clean_commentary}")
    pre_clean_commentary = clean_commentary
    for element in char_names:
        clean_commentary = re.sub(f"\\b{re.escape(element)}\\b", "", clean_commentary)
    return clean_commentary
