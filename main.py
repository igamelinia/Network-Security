from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.entity.config_entity import ( 
    DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig,
    DataTransformationConfig, ModelTrainerConfig)
import sys


if __name__=="__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info("initiate the data ingestion")
        dataingestionartifact= data_ingestion.initiate_data_ingestion()
        print(dataingestionartifact)
        logging.info("Process Data ingestion Success")

        datavalidationconfig = DataValidationConfig(trainingpipelineconfig)
        data_vallidation = DataValidation(data_ingestion_artifact=dataingestionartifact, data_validation_config=datavalidationconfig)
        logging.info("initiate data validation process")
        datavalidationartifact = data_vallidation.initiate_data_validation()
        print(datavalidationartifact)
        logging.info("Process Data validation Success")

        datatransformationconfig = DataTransformationConfig(trainingpipelineconfig)
        data_transformation = DataTransformation(data_validation_artifact=datavalidationartifact, data_transformation_config=datatransformationconfig)
        logging.info("initiate data transformation process")
        datatransformationartifact = data_transformation.initiate_data_transformation()
        print(datatransformationartifact)
        logging.info("Process Data transformation Success")

        modeltrainerconfig = ModelTrainerConfig(trainingpipelineconfig)
        model_trainer = ModelTrainer(data_transformation_artifact=datatransformationartifact, model_trainer_config=modeltrainerconfig)
        logging.info("initiate Model Trainer process")
        modeltraineraartifact = model_trainer.initiate_model_trainer()
        print(modeltraineraartifact)
        logging.info("Process Model Trainer Success")

    except Exception as e:
        raise CustomException(e, sys)