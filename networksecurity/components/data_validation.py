from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file
from scipy.stats import ks_2samp
import pandas as pd 
import os
import sys 

# create Class for initiate Data validation process
class DataValidation:
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(e,sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e :
            raise CustomException(e, sys)
        
    def validate_number_of_columns(self, dataframe:pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self.schema_config)
            logging.info(f"Required number of columns : {number_of_columns}")
            logging.info(f"Dataframe has columns : {len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            else : 
                return False
        except Exception as e:
            raise CustomException(e, sys)

    def detect_dataset_drift(self, old_df, new_df, threshold=0.05):
        try:
            status = True 
            report = {}
            for column in old_df.columns:
                d1=old_df[column]
                d2=new_df[column]
                is_same_distribution = ks_2samp(d1,d2)
                if threshold <= is_same_distribution.pvalue:
                    is_found = False
                else :
                    is_found = True
                    status = False
                report.update({column:{"p_value" : float(is_same_distribution.pvalue), 
                                       "drift_status" : is_found}})
            
            # Path data drift file 
            data_drift_file_path = self.data_validation_config.drift_report_file_path
            # Create Directory
            dir_path = os.path.dirname(data_drift_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=data_drift_file_path, content=report)

        except Exception as e:
            raise CustomException(e, sys)
    
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # Read data train and test from data ingestion artifact
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            # Validate number of columns
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = f"Train dataframe does not contain all columns"
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = f"Test dataframe does not contain all columns"

            # Check Data drift
            status=self.detect_dataset_drift(old_df=train_dataframe, new_df=test_dataframe)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            train_dataframe.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
            test_dataframe.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                valid_train_file_path=self.data_ingestion_artifact.train_file_path,
                invalid_test_file_path=None,
                invalid_train_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            return data_validation_artifact

        except Exception as e:
            raise CustomException(e, sys)
                                  
        
    
        
        

