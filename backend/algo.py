from .utils import sample_db, synonym, stop_words
from .kmp import KMP
from .bm import boyerMoore
from .regex import regex_sample
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import string

factory = StemmerFactory()
stemmer = factory.create_stemmer()



def func(e):
    if e in synonym:
        return synonym[e]
    else:
        return e


def preprocess(sentence):
    stemmed_sentence = stemmer.stem(sentence)
    split_sentence = stemmed_sentence.split(' ')
    split_sentence = [x for x in split_sentence if x not in {'itu', 'saja', 'kah', 'yang'}]
    to_base = map(func, split_sentence)
    clean_sentence = ' '.join(to_base)
    return clean_sentence


def answer(question_user):
    question_user = preprocess(question_user)
    for q_db in sample_db:
        question_in_db = str(q_db)
        question_in_db = preprocess(question_in_db)
        kmp = KMP(question_user, question_in_db)
        bm = boyerMoore(question_user, question_in_db)
        match = max(kmp, bm)
        if match > 0.6:
            return sample_db[q_db]
    for q_db in sample_db:
        question_in_db = str(q_db)
        question_in_db = preprocess(question_in_db)
        if regex_sample(question_user, question_in_db):
                return sample_db[q_db]
    # possible = sorted(range(len(sample_db.keys())), key=lambda i: KMP(i, question_user))[-2:]
    return "Aku bingung" + "\n"
