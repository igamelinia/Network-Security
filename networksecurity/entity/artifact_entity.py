from dataclasses import dataclass

# Define artifact for Data Ingestion
@dataclass
class DataIngestionArtifact:
    train_file_path: str
    test_file_path: str