import re
import random
from os import path, walk


def crawl(corpus_dir):
    if not path.isdir(corpus_dir):
        return

    _, _, filenames = next(walk(corpus_dir))

    pages = {}

    for filename in filenames:
        with open(path.join(corpus_dir, filename)) as buffer:
            pages[filename] = re.findall(r'<a href="(.+?)"', buffer.read())
        buffer.close()

    return pages


def remove_recursive_outgoing_links(pages):
    return {
        page: [
            outgoing_link for outgoing_link in outgoing_links if outgoing_link != page
        ]
        for page, outgoing_links in pages.items()
    }


def sampling_pagerank(pages, samples_count, teleport_factor=0.15):
    pages = remove_recursive_outgoing_links(pages)
    starting_page, *rest_pages = pages.keys()
    pages_visits_count = {starting_page: 1, **{page: 0 for page in rest_pages}}
    current_page = starting_page

    for _ in range(samples_count - 1):
        current_page = (
            random.choice(list(pages.keys()))
            if random.random() < teleport_factor or not pages[current_page]
            else random.choice(pages[current_page])
        )
        pages_visits_count[current_page] += 1

    return {
        page: visits_count / samples_count
        for page, visits_count in pages_visits_count.items()
    }


def iterative_pagerank(pages, teleport_factor=0.15):
    pages = remove_recursive_outgoing_links(pages)
    pageranks = {page: 1 / len(pages) for page in pages}
    inverted_pages = {
        page_i: [
            page_j
            for page_j, outgoing_links in pages.items()
            if page_i in outgoing_links
        ]
        for page_i in pages
    }

    while True:
        new_pageranks = {
            page: teleport_factor / len(pages)
            + (1 - teleport_factor)
            * sum(
                pageranks[incoming_link] / len(pages[incoming_link] or pages)
                for incoming_link in inverted_pages[page]
            )
            for page in pages
        }

        if all(abs(pageranks[page] - new_pageranks[page]) < 0.001 for page in pages):
            pageranks_sum = sum(prob for prob in new_pageranks.values())
            return {
                page: pagerank / pageranks_sum
                for page, pagerank in new_pageranks.items()
            }

        pageranks = new_pageranks


def main():
    pages = crawl("corpuses/0")
    samples_count = 10000

    print(f"PageRank results from sampling (n = {samples_count}):")

    for page, PageRank in sampling_pagerank(pages, samples_count).items():
        print(f"\t{page}: {PageRank}")

    print("PageRank results from iteration:")

    for page, PageRank in iterative_pagerank(pages).items():
        print(f"\t{page}: {PageRank:.4f}")


if __name__ == "__main__":
    main()
