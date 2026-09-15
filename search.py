# loads persisted index and returns top-k semantically relevant recency papers

from vector_store import load_index
from retriever import search
import config


class results(list):
    """A concrete result container for retrieved papers.

    This keeps the original list-like behavior while adding a few convenience
    helpers for working with ranked paper results.
    """

    def __init__(self, items=None):
        super().__init__(items or [])

    def add(self, paper):
        """Append a single paper to the result set and return itself."""
        self.append(paper)
        return self

    def extend(self, papers):
        """Append multiple papers while preserving list semantics."""
        super().extend(papers)
        return self

    def top(self, k=None):
        """Return the first k papers or the full result list."""
        if k is None:
            return list(self)
        return list(self[:k])

    def summary(self):
        """Return a simple serializable summary of the ranked results."""
        return [
            {
                "title": paper.get("title", ""),
                "year": paper.get("year", ""),
                "abstract": paper.get("abstract", ""),
            }
            for paper in self
        ]


def main():
    index, papers=load_index(config.INDEX_PATH, config.METADATA_PATH)
    query=input("Enter research query: ")
    k=int(input("How many papers should be retrieved (k)? "))
    
    results_list=search(query, index, papers, k)
    ranked_results=results(results_list)
    print(f"\nTop {k} papers for: '{query}'\n" + "=" *60)
    for rank, paper in enumerate(ranked_results, start=1):
        print(f"{rank}, [{paper['year']}] {paper['title']}")
        print(f" {paper['abstract'][:150]}...\n")

if __name__=="__main__":
    main()












