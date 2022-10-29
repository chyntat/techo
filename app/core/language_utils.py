import hashlib


def get_hash(content):
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def get_urls(content):
    return "no urls as of now"


def get_mentions(content):
    return "no mentions as of now"


def get_nsfw_score(content):
    return {'score': 0.0}  # TODO: implement this


def get_profanity_words(content):
    return "no profanity words as of now"
