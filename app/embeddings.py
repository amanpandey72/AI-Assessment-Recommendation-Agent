from pathlib import Path
import json
import pickle
import logging

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Handles embedding generation and FAISS index management.
    """

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        assessment_file: str = "data/assessments.json",
        index_file: str = "data/faiss.index",
        metadata_file: str = "data/metadata.pkl",
    ):

        self.model = SentenceTransformer(model_name)

        self.assessment_file = Path(assessment_file)
        self.index_file = Path(index_file)
        self.metadata_file = Path(metadata_file)

    # ----------------------------------------------------

    def load_assessments(self):

        with open(
            self.assessment_file,
            "r",
            encoding="utf-8",
        ) as f:

            return json.load(f)

    # ----------------------------------------------------

    def build_embeddings(self, assessments):

        documents = []

        for assessment in assessments:
            documents.append(
                assessment["search_text"]
            )

        embeddings = self.model.encode(

            documents,

            batch_size=32,

            show_progress_bar=True,

            convert_to_numpy=True,

            normalize_embeddings=True,

        )

        return embeddings.astype("float32")

    # ----------------------------------------------------

    def create_index(self):

        assessments = self.load_assessments()

        embeddings = self.build_embeddings(
            assessments
        )

        dimension = embeddings.shape[1]

        index = faiss.IndexFlatIP(
            dimension
        )

        index.add(
            embeddings
        )

        faiss.write_index(
            index,
            str(self.index_file)
        )

        with open(
            self.metadata_file,
            "wb"
        ) as f:

            pickle.dump(
                assessments,
                f
            )

        logger.info(
            "FAISS index created successfully."
        )

        print(
            f"Indexed {len(assessments)} assessments."
        )

    # ----------------------------------------------------

    def load_index(self):

        if not self.index_file.exists():
            raise FileNotFoundError(
                "FAISS index not found."
            )

        if not self.metadata_file.exists():
            raise FileNotFoundError(
                "Metadata file not found."
            )

        index = faiss.read_index(
            str(self.index_file)
        )

        with open(
            self.metadata_file,
            "rb"
        ) as f:

            metadata = pickle.load(
                f
            )

        return index, metadata

    # ----------------------------------------------------

    def encode_query(self, query: str):

        embedding = self.model.encode(

            query,

            normalize_embeddings=True,

            convert_to_numpy=True,

        )

        return embedding.reshape(
            1,
            -1
        ).astype("float32")

    # ----------------------------------------------------

    def search(
        self,
        query: str,
        top_k: int = 10,
    ):

        index, metadata = self.load_index()

        query_embedding = self.encode_query(
            query
        )

        scores, indices = index.search(
            query_embedding,
            top_k
        )

        results = []

        for score, idx in zip(
            scores[0],
            indices[0]
        ):

            if idx == -1:
                continue

            assessment = metadata[idx].copy()

            assessment["score"] = float(score)

            results.append(
                assessment
            )

        return results


if __name__ == "__main__":

    service = EmbeddingService()

    service.create_index()