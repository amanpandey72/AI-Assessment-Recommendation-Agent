from pathlib import Path
from typing import List, Dict
import json
import logging

logger = logging.getLogger(__name__)


class CatalogLoader:
    """
    Loads the SHL assessment catalog from JSON.
    """

    def __init__(self, catalog_path: str):
        self.catalog_path = Path(catalog_path)

    def load_catalog(self) -> List[Dict]:
        """
        Load catalog into memory.
        """

        if not self.catalog_path.exists():
            raise FileNotFoundError(
                f"Catalog not found: {self.catalog_path}"
            )

        with open(
            self.catalog_path,
            "r",
            encoding="utf-8"
        ) as f:

            catalog = json.load(f)

        logger.info(
            "Loaded %d assessments",
            len(catalog)
        )

        return catalog