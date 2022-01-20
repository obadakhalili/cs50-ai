from os import path
from pprint import pprint


def parse_family(data_path):
    if not path.isfile(data_path):
        return

    family = {}

    with open(data_path) as buffer:
        for line in buffer.read().splitlines()[1:]:
            name, mother, father, trait = line.split(",")
            family[name] = {
                "parents": [mother, father] if mother and father else None,
                "trait": int(trait) if trait else None,
            }
        buffer.close()

    return family


def main():
    """# noqa
    probs: Probabilities for the hearing impairment version of the GJB2 gene (mutated gene), and the hearing impairment trait
    probs.mutated_gene[0]: Probability of having 0 copies of the mutated gene
    probs.trait[0]: Probability of having the hearing impairment trait, given that the number of mutated genes is 0
    """
    probs = {
        "muated_gene": [0.96, 0.03, 0.01],
        "trait": [0.01, 0.56, 0.65],
        "mutation": 0.01,
    }

    family = parse_family("./families/0.csv")

    pprint(family)


if __name__ == "__main__":
    main()
