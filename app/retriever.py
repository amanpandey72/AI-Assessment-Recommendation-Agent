from typing import List, Dict

from app.embeddings import EmbeddingService


class Retriever:

    def __init__(self):
        self.embedding_service = EmbeddingService()

        self.index, self.metadata = self.embedding_service.load_index()

    def search(
        self,
        query: str,
        top_k: int = 10,
    ) -> List[Dict]:

        query_vector = self.embedding_service.encode_query(query)

        scores, indices = self.index.search(
            query_vector,
            top_k,
        )

        results = []

        for score, idx in zip(scores[0], indices[0]):

            if idx == -1:
                continue

            assessment = self.metadata[idx].copy()

            assessment["score"] = float(score)

            results.append(assessment)

        return results


if __name__ == "__main__":

    retriever = Retriever()

    while True:

        query = input("\nSearch : ")

        if query.lower() == "exit":
            break

        results = retriever.search(query)

        print("\n")

        for i, item in enumerate(results, 1):

            print("=" * 80)

            print(f"Rank : {i}")

            print(f"Score : {item['score']:.4f}")

            print(f"Assessment : {item['name']}")

            print(f"Duration : {item['duration']}")

            print(f"Remote : {item['remote']}")

            print(f"Adaptive : {item['adaptive']}")

            print(f"URL : {item['url']}")

            print()