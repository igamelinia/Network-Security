import os
import sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
from networksecurity.constant.training_pipeline import (TARGET_NAME, DATA_TRANSFORMATION_IMPUTER_PARAMS)
from networksecurity.entity.artifact_entity import (
    DataValidationArtifact, 
    DataTransformationArtifact
)
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_object

# Create Class for initiate Data Transformation Process
class DataTransformation:
    def __init__(self, data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise CustomException(e, sys)
        
    @staticmethod
    def read_data_csv(file_path:str)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e, sys)
        
    def get_data_transformation_object(cls) -> Pipeline:
        try:
            logging.info( "Entered get_data_trnasformer_object method of Trnasformation class")
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"Initiate KNNimputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}")

            prepocessor: Pipeline = Pipeline([("imputer", imputer)])
            return prepocessor
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Entered initiate_data_transformation method of DataTransformation class")
        try:
            logging.info("Starting data transformastion")
            # Read dataset from Data Validation Artifact
            train_df = DataTransformation.read_data_csv(self.data_validation_artifact.valid_train_file_path)
            test_df= DataTransformation.read_data_csv(self.data_validation_artifact.valid_test_file_path)

            # Part of Training dataset
            input_feature_train_df = train_df.drop(columns=[TARGET_NAME], axis=1)
            target_feature_train_df = train_df[TARGET_NAME]
            target_feature_train_df = target_feature_train_df.replace(-1, 0)

            # Part od Test dataset
            input_feature_test_df = test_df.drop(columns=[TARGET_NAME], axis=1)
            target_feature_test_df = test_df[TARGET_NAME]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)

            # get preprocessor 
            preprocessor = self.get_data_transformation_object()

            preprocessor_obj= preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature=preprocessor_obj.transform(input_feature_train_df)
            transformed_input_test_feature=preprocessor_obj.transform(input_feature_test_df)

            # Concat input feature has transformed with target
            train_array = np.c_[transformed_input_train_feature, np.array(target_feature_train_df) ]
            test_array = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]

            # Save numpy array 
            save_numpy_array_data(file_path=self.data_transformation_config.data_transformation_train_file_path,
                                  array=train_array)
            save_numpy_array_data(file_path=self.data_transformation_config.data_transformation_test_file_path,
                                  array=test_array)
            # save preprocessor
            save_object(file_path=self.data_transformation_config.transformed_object_file_path, 
                        obj=preprocessor_obj)
            
            save_object("final_model/prepocessor.pkl", preprocessor_obj)

            # Preparing artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.data_transformation_train_file_path,
                transformed_test_file_path=self.data_transformation_config.data_transformation_test_file_path
            )

            return data_transformation_artifact

        except Exception as e:
            raise CustomException(e, sys)