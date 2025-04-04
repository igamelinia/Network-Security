from networksecurity.entity.artifact_entity import DataTransformationArtifact, ClassificationMetricArtifact, ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.utils.main_utils.utils import load_numpy_array_data, load_object, save_object
from networksecurity.utils.ml_utils.metric.classification import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel, evaluate_models
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging

import os, sys
import json
from sklearn.metrics import f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (
    AdaBoostClassifier, 
    GradientBoostingClassifier,
    RandomForestClassifier
)

import mlflow
from urllib.parse import urlparse

import dagshub
dagshub.init(repo_owner='igamelinia', repo_name='Network-Security', mlflow=True)

# Create class for initiate Model Trainer process
class ModelTrainer:
    def __init__(self, data_transformation_artifact:DataTransformationArtifact,
                 model_trainer_config:ModelTrainerConfig):
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config
        except Exception as e:
            raise CustomException(e, sys)

    def track_mlflow(self, best_model, classification_metric, params):
        mlflow.set_registry_uri("https://dagshub.com/igamelinia/Network-Security.mlflow")
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
        with mlflow.start_run():
            f1_score=classification_metric.f1_score
            precision_score = classification_metric.precision_score
            recall_score = classification_metric.recall_score
            model_name = best_model.__class__.__name__

            if isinstance(params, str):
                params = json.loads(params)

            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("precision_score", precision_score)
            mlflow.log_metric("recall_score", recall_score)

            mlflow.log_params(params)

            #Note : Model registry does not work with file store 
            if tracking_url_type_store != "file":
                mlflow.sklearn.log_model(best_model, "model", registered_model_name=model_name)
            else :
                mlflow.sklearn.log_model(best_model, "model")

    def train_model(self, X_train, y_train, X_test, y_test):
        models = {
            "Logistic Regression" : LogisticRegression(),
            "Random Forest" : RandomForestClassifier(),
            "AdaBoost" : AdaBoostClassifier(),
            "Gradien Boosting" : GradientBoostingClassifier()
        }

        params = {
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            
        }

        model_reports, best_model, params, best_model_name = evaluate_models(X_train, y_train, X_test, y_test, models, params)

        # best_model_score = model_reports[best_model_name]["test_f1_score"]
        logging.info(f"Model Report : \n {model_reports}")
        # # to get best model score from dict
        # best_model_score = max(sorted(model_report.values()))

        # # to get best model name from dict
        # best_model_name = list(model_report.keys())[
        #     list(model_report.values()).index(best_model_score)]
        # best_model = models[best_model_name]

        y_test_pred = best_model.predict(X_test)
        y_train_pred = best_model.predict(X_train)
        classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)
        classification_train_metric = get_classification_score(y_true=y_train, y_pred=y_train_pred)

        # params_best_model = getattr(best_model, "params_", None)

        logging.info(f"Best model : {best_model}")
        logging.info(f"Best name model : {best_model_name}")
        logging.info(f"Params Best Model : {params}")

        # track experiment with mlflow
        self.track_mlflow(best_model=best_model, classification_metric=classification_test_metric, params=params)
        self.track_mlflow(best_model=best_model, classification_metric=classification_train_metric, params=params)

        # Load prepocessor 
        prepocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

        # Create model trained directory
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path, exist_ok=True)

        network_model = NetworkModel(prepocessor=prepocessor, model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path, obj=best_model)

        save_object("final_model/model.pkl", best_model)

        # Model trainer artifact
        model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                                                    train_metric_artifact=classification_train_metric,
                                                    test_metric_artifact=classification_test_metric)
        
        logging.info(f"Model trainer artifact : {model_trainer_artifact}")
        return model_trainer_artifact
    
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            # load data
            train_array = load_numpy_array_data(file_path=train_file_path)
            test_array = load_numpy_array_data(file_path=test_file_path)

            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )

            model_trainer_artifact = self.train_model(X_train, y_train, X_test, y_test)
            return model_trainer_artifact
        except Exception as e :
            raise CustomException(e, sys)
