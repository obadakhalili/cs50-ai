import sys
import nltk

RULES = """
# Non-terminals
S -> NP VP | NP VP Conj NP VP | NP VP Conj VP
NP -> N | Det N | Det AP N | P NP | NP P NP
VP -> V | Adv VP | V Adv | VP NP | V NP Adv
AP -> Adj | AP Adj

# Terminals
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

grammar = nltk.CFG.fromstring(RULES)
parser = nltk.ChartParser(grammar)


def main():
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as file:
            sentence = file.read()
    else:
        sentence = input("Sentence: ")

    tokens = preprocess(sentence)

    try:
        trees = list(parser.parse(tokens))

        if not trees:
            raise ValueError("Could not parse sentence")

        for tree in trees:
            tree.pretty_print()

            print("Noun phrase chunks:")
            for chunck in get_np_chunks(tree):
                print(" ".join(chunck.flatten()))
    except ValueError as e:
        print(e)
        return


def preprocess(sentence):
    return [
        word
        for word in nltk.tokenize.word_tokenize(sentence.lower())
        if any(char.isalpha() for char in word)
    ]


def get_np_chunks(tree):
    def contain_nested_np(tree_node):
        np_subtrees = tree_node.subtrees(
            lambda tree: tree is not tree_node and tree.label() == "NP"
        )
        return len(list(np_subtrees)) > 0

    def get_chuncks(tree_node, chuncks=[]):
        if tree_node.label() == "NP" and not contain_nested_np(tree_node):
            chuncks.append(tree_node)

        for child in tree_node:
            if isinstance(child, nltk.Tree):
                get_chuncks(child, chuncks)

        return chuncks

    return get_chuncks(tree)


if __name__ == "__main__":
    main()
