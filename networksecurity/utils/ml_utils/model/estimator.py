from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
import os, sys
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV

# Class for prepocess data until train model
class NetworkModel:
    def __init__(self, prepocessor, model):
        try:
            self.prepocessor = prepocessor
            self.model = model
        except Exception as e:
            raise CustomException(e,sys)
        
    def predict(self, input_feature):
        try:
            x_transformed = self.prepocessor.transform(input_feature)
            y_hat = self.model.predict(x_transformed)
            return y_hat
        except Exception as e:
            raise CustomException(e, sys)
        
# function for evaluate and do cross validation for model

def evaluate_models(X_train, y_train, X_test, y_test, models, params=None):
    try:
        reports = {}
        best_model = None
        best_score = 0
        best_params = {}
        best_model_name = None  

        for model_name, model in models.items():
            param_grid = params.get(model_name, {})  # Ambil parameter model, jika tidak ada gunakan {}

            gs = GridSearchCV(model, param_grid, cv=3, scoring="f1", n_jobs=-1)
            gs.fit(X_train, y_train)

            # Set model dengan best params
            best_model_params = gs.best_params_
            model.set_params(**best_model_params)
            model.fit(X_train, y_train)

            # Prediksi dan hitung skor
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)
            train_f1 = f1_score(y_train, y_train_pred)
            test_f1 = f1_score(y_test, y_test_pred)

            # Simpan hasil evaluasi
            reports[model_name] = {
                "test_f1_score": test_f1,
                "train_f1_score": train_f1,
                "best_params": best_model_params
            }

            # Cek apakah model ini yang terbaik
            if test_f1 > best_score:
                best_score = test_f1
                best_model = model
                best_model_name = model_name  # Simpan nama model terbaik
                best_params = best_model_params
 

        return reports, best_model, best_params, best_model_name

    except Exception as e:
        raise CustomException(e, sys)




# def evaluate_models(X_train, y_train, X_test, y_test, models, params=None):
#     try:
#         reports = {}
        
#         for i in range(len(list(models))):
#             model = list(models.value())[i]
#             param = params[list(models.keys())[i]]

#             gs = GridSearchCV(model, param, cv=3, scoring=[f1_score])
#             gs.fit(X_train, y_train)

#             model.set_params(**gs.best_params_)
#             model.fit(X_train, y_train)

#             y_train_pred = model.predict(X_train)
#             y_test_pred = model.predict(X_test)
#             train_model_f1_score = f1_score(y_true=y_train, y_pred=y_train_pred)
#             test_model_f1_score = f1_score(y_true=y_test, y_pred=y_test_pred)

#             reports[list(models.keys())[i]] = test_model_f1_score


#         return reports

#     except Exception as e:
#         raise CustomException(e, sys)
                                  
    