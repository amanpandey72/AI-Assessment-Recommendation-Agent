from app.catalog_loader import CatalogLoader

loader = CatalogLoader("data/assessments.json")

catalog = loader.load_catalog()

print(catalog)