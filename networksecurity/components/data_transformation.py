import sys,os

import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constants.training_pipeline import TARGET_COLUMN
from networksecurity.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact
from networksecurity.entity.config_entity import DataTransformationConfig

from networksecurity.utils.main_utils.utils import save_object,save_numpy_array_data

from networksecurity.exception.exception_handling import NetworkSecurityException
from networksecurity.logging.logger import logging


class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact: DataValidationArtifact = data_validation_artifact
            self.data_transformation_config: DataTransformationConfig = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def get_data_transformer_object(cls)->Pipeline:
        """
        It initialises a KNNImputer object with the parameters specified in the training_pipeline.py file
        and returns a Pipeline object with the KNNImputer object as the first step.

        Args:
          cls: DataTransformation

        Returns:
          A Pipeline object
        """
        logging.info(
            "Entered get_data_trnasformer_object method of Trnasformation class"
        )
        try:
            imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(
                f"Initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}"
            )
            preprocessor:Pipeline=Pipeline([("imputer",imputer)])
            return preprocessor
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    @staticmethod
    def read_data(file_path:str)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def initiate_data_transformation(self):
        logging.info("Entered the initiate_data_transformation method of DataTransformation class")
        try:
            logging.info("Initiating data transformation")
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            # train data frame
            train_df_input_feature=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            train_df_target_feature=train_df[TARGET_COLUMN]
            train_df_target_feature.replace(-1,0,inplace=True)

            # test data frame
            test_df_input_feature=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            test_df_target_feature=test_df[TARGET_COLUMN]
            test_df_target_feature.replace(-1,0,inplace=True)

            preprocessor=self.get_data_transformer_object()
            logging.info("Fitting and transforming the training data")

            preprocessor_object=preprocessor.fit(train_df_input_feature)
            transformed_train_input_feature=preprocessor_object.transform(train_df_input_feature)
            transformed_test_input_feature=preprocessor_object.transform(test_df_input_feature)

            train_arr=np.c_[transformed_train_input_feature,np.array(train_df_target_feature)]
            test_arr=np.c_[transformed_test_input_feature,np.array(test_df_target_feature)]
            logging.info("Data transformation completed successfully")

            # save numpy array
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,test_arr) 
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_object)
            logging.info("Saved transformed training and testing array")

            # preparing artifact
            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)