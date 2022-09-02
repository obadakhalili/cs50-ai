from functools import reduce
from math import log
import itertools
import os
import re
import nltk


def tokenize(text):
    return [
        token for token in nltk.word_tokenize(text.lower()) if re.search(r"[\w]", token)
    ]


def load_corpus(path):
    corpus = {}

    for file in os.listdir(path):
        with open(os.path.join(path, file)) as file_buffer:
            corpus[file] = file_buffer.read()

    return corpus


def tokenize_corpus(corpus):
    return {doc: tokenize(text) for doc, text in corpus.items()}


def compute_tfs(corpus):
    return {
        doc: {token: log(tokens.count(token)) for token in set(tokens)}
        for doc, tokens in corpus.items()
    }


def compute_idfs(corpus):
    docs_tokens = corpus.values()
    voc = set(reduce(lambda voc, tokens: voc + tokens, docs_tokens, []))
    docs_count = len(corpus)

    return {
        token: log(
            docs_count / sum([1 for doc_tokens in docs_tokens if token in doc_tokens])
        )
        for token in voc
    }


def get_top_docs(docs, query, tfs, idfs, n):
    docs_scores = {
        doc: reduce(
            lambda score, query_token: score
            + tfs[doc].get(query_token, 0) * idfs.get(query_token, 0),
            query,
            0,
        )
        for doc in docs
    }

    return sorted(docs_scores, key=lambda key: docs_scores[key], reverse=True)[:n]


def get_top_sentences(sentences, query, idfs, n):
    def compute_sentence_score(sentence):
        sentence_tokens = tokenize(sentence)
        common_tokens = set(sentence_tokens).intersection(set(query))
        matching_word_measure = reduce(
            lambda matching_word_measure, token: matching_word_measure
            + idfs.get(token, 0),
            common_tokens,
            0,
        )
        query_term_density = len(common_tokens) / len(sentence_tokens)

        return (matching_word_measure, query_term_density)

    sentences_scores = {
        sentence: compute_sentence_score(sentence) for sentence in sentences
    }

    return sorted(
        sentences_scores, key=lambda key: sentences_scores[key], reverse=True
    )[:n]


def main():
    corpus = load_corpus(os.path.join(os.path.dirname(__file__), "./corpus"))
    corpus_tokenized = tokenize_corpus(corpus)
    tfs = compute_tfs(corpus_tokenized)
    idfs = compute_idfs(corpus_tokenized)
    query = input("Q: ")
    query_tokens = tokenize(query)
    top_docs = get_top_docs(corpus.keys(), query_tokens, tfs, idfs, 3)
    top_docs_sentences = list(
        itertools.chain.from_iterable(
            [nltk.sent_tokenize(corpus[doc]) for doc in top_docs]
        )
    )
    top_sentences = get_top_sentences(top_docs_sentences, query_tokens, idfs, 3)

    print("A(s):\n  - {0}".format("\n  - ".join(top_sentences)))


if __name__ == "__main__":
    main()
