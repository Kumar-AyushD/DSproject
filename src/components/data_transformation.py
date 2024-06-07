import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging

@dataclass
class DataTransformationConfig:
  preprocessor_ob_filepath = os.path.join('artifact', "preprocessor.pkl")

class DataTransformation:
  def __init__(self):
    self.data_transformation_config = DataTransformationConfig()
  
  def get_data_transformation_object(self):
    try:
      numerical_columns = ["writing score", "reading score"]
      categorical_columns = [
        "gender",
        "race/ethnicity",
        "parental level of education",
        "lunch",
        "test preparation course",
      ]

      num_pipeline= Pipeline(
        steps=[
          ("imputer", SimpleImputer(strategy="median")),
          ("scalar", StandardScaler())
        ]
      )

      cat_pipeline = Pipeline(

        steps=[
          ("imputer", SimpleImputer(strategy="most_frequent")),
          ("one_hot_encoder", OneHotEncoder()),
          ("scaler", StandardScaler())
        ]
      )

      logging.info(f"categorical columns : {categorical_columns}")
      logging.info(f"numerical columns : {numerical_columns}")

      preprocesor = ColumnTransformer(
        [
          ("num_pipeline", num_pipeline, numerical_columns)
          ("cat_pipeline", cat_pipeline, categorical_columns)
        ]
      )
      return preprocesor
    except Exception as e:
      raise CustomException(e, sys)
    
  def initiate_data_transformation(self, train_path, test_path):
    try:
      train_df = pd.read_csv(train_path)
      test_df = pd.read_csv(test_path)

      logging.info("Read train and test data completed")
      logging.info("Obtaining preprocessing object")

      preprocessor_obj = self.get_data_transformation_object

      target_column_name = "math score"
      numerical_columns = ["writing score", "reading score"]

      input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
      target_feature_train_df = train_df[target_column_name]

      input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
      target_feature_test_df = test_df[target_column_name]

      logging.info("Applying preprocessing object on training and testing dataframe")

      input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)
      input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)

      train_arr = np.c_[
        input_feature_train_arr, np.array(target_feature_train_df)
      ]

      test_arr = np.c_[
        input_feature_test_arr, np.array(target_feature_test_df)
      ]

      logging.info("Saving preprocessing object")

      save_object(
        file_path = self.data_transformation_config.preprocessor_ob_filepath,
        obj = preprocessor_obj
      )

      return(
        train_arr,
        test_arr,
        self.data_transformation_config.preprocessor_ob_filepath
      )
    except:
      pass