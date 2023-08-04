import os
import sys
from src.exception import CustomException
from src.components.data_transformation import DataTransformation , DataTransformationConfig
from src.logger import logging
import pandas as pd

# from src.components.model_trainer import ModelTrainer

from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    movies_data_path: str=os.path.join('artifacts',"movies.csv")
    credits_data_path: str=os.path.join('artifacts',"credits.csv")
    movies_combined_data_path = os.path.join('artifacts','combined_movies.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered Data Ingestion Config")
        try:
            movies_df=pd.read_csv('D:\\Movie Recomendation System\\Notebook\\tmdb_5000_credits.csv')
            credits_df = pd.read_csv('D:\\Movie Recomendation System\\Notebook\\tmdb_5000_movies.csv')
            logging.info('Read the movies and credits dataset as dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.movies_data_path),exist_ok=True)

            movies_df.to_csv(self.ingestion_config.movies_data_path,index=False,header=True)
            credits_df.to_csv(self.ingestion_config.credits_data_path , index=False,header=True )

            
            logging.info('Merging of Movies Dataset and Credit Dataset on title')
            movies = pd.merge(movies_df,credits_df,on = 'title')

            logging.info("Column Selection Initiated")
            '''
            [ 'id' : Id of the Movie which is the one of the useful to identify the movie ,
              'title' : Represents name of the movie ,
               'genres' : Genere of th the movie like action , scify , romantic , thriller  ,
                 'keywords' : Words that describes the movie , 
                 'cast' : Star Characters acted in the movie , 
                 'crew' : Non acting characters in the movie]
            Only These are the columns which helps us to recommend the movie sincs budjet and runtime of the movie are not matter as much
            '''
            req_columns = ['id' , 'title','genres' , 'keywords','cast','crew']
            movies = movies[req_columns]
            movies.dropna(inplace = True)
            movies.to_csv(self.ingestion_config.movies_combined_data_path , index=False , header= True)
            logging.info("Ingestion of the data is completed")
            # print(movies.shape)
            return(
                self.ingestion_config.movies_combined_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":
    obj=DataIngestion()
    movies_path = obj.initiate_data_ingestion() 

    obj2 = DataTransformation()
    movies_data , _ = obj2.initiate_data_transformation(movies_path)
    print(movies_data.shape)

    # obj3 = ModelTrainer()
    # print(obj3.initiate_model_trainer(train_arr,test_arr))