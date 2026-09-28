import json
import debug

def extract_trigrams(text):
    text = text.lower()
    text = " ".join(text.split())
    return [text[i:i+3] for i in range(len(text) - 4)]

def score_text(text, model):
    unseen_logprob = model["unseen_logprob"]
    trigrams = extract_trigrams(text)
    if not trigrams:
        return float("-inf")

    debug.dprint(f"Trigrams: {trigrams}")

    score = 0
    for tg in trigrams:
        trigram_score = model.get(tg, unseen_logprob)
        debug.dprint(f"{tg} = {trigram_score}")
        score += trigram_score

    return score / len(trigrams)

def load_model(path):
    with open(path, "r") as model:
        return json.load(model)
