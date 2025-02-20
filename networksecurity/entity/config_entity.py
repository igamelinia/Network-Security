from datetime import datetime
import os
from networksecurity.constant import training_pipeline

# Print project pipeline name
print(training_pipeline.PIPELINE_NAME)
# print folder name for artifact 
print(training_pipeline.ARTIFACT_DIR)

# Save configuration dinamis in class format
# Config for Training Pipeline 
class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        timestamp=timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        #pipeline nama
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        #artifact folder name
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        #path to artifact folder
        self.artifact_dir = os.path.join(self.artifact_name, timestamp)
        self.timestamp: str = timestamp

# Config for Data Ingestion process
class DataIngestionConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        #path to data ingestion folder 
        self.data_ingestion_dir:str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_DIR_NAME)
        #path for save feature store (raw data)
        self.feature_store_file_path: str = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR, training_pipeline.FILE_NAME)
        #path for save train dataset
        self.training_file_path: str = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TRAIN_FILE_NAME)
        #path for save test dataset
        self.test_file_path:str = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TEST_FILE_NAME)
        #ratio train test split 
        self.train_test_split: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT
        #collection name 
        self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        #database name 
        self.database_name: str = training_pipeline.DATA_INGESTION_DATABASE_NAME