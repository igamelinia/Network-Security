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
        self.model_dir:str = os.path.join("final_model")

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

# Config for Data Validation
class DataValidationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        # path for data validation folder
        self.data_validation_dir:str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_VALIDATION_DIR_NAME)
        # path for data validation valid folder
        self.data_validation_valid : str = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_VALID_DIR)
        # path for data validation invalid folder
        self.data_validation_invalid :str = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_INVALID_DIR)
        # path for valid train and test data file
        self.valid_train_file_path : str = os.path.join(self.data_validation_valid, training_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path :str = os.path.join(self.data_validation_valid, training_pipeline.TEST_FILE_NAME)
        # path for invalid train and test data file
        self.invalid_train_file_path: str = os.path.join(self.data_validation_invalid, training_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path : str = os.path.join(self.data_validation_invalid, training_pipeline.TEST_FILE_NAME)
        # path for drift report file
        self.drift_report_file_path : str = os.path.join(self.data_validation_dir, 
                                                        training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
                                                        training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)
        
# config for data transformation
class DataTransformationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir : str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_TRANSFORMATION_DIR_NAME)
        self.data_transformation_train_file_path :str = os.path.join(self.data_transformation_dir, 
                                                                     training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, 
                                                                     training_pipeline.DATA_TRANSFORMATION_TRAIN_FILE_NAME)
        self.data_transformation_test_file_path : str = os.path.join(self.data_transformation_dir,
                                                                     training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                                     training_pipeline.DATA_TRANSFORMATION_TEST_FILE_NAME)
        self.transformed_object_file_path: str = os.path.join(self.data_transformation_dir,
                                                              training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
                                                              training_pipeline.PREPROCESSING_OBJECT_FILE_NAME)

# config for model trainer
class ModelTrainerConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_dir : str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.MODEL_TRAINER_DIR_NAME)
        self.trained_model_file_path :str = os.path.join(self.model_trainer_dir, 
                                                         training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR,
                                                         training_pipeline.MODEL_TRAINER_TRAINED_MODEL_FILE_NAME)
        self.expected_accuracy: float = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.overfitting_underfitting_thershold : float = training_pipeline.MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD
        
        