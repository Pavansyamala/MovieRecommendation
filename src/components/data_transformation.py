import sys
from dataclasses import dataclass

import numpy as np 
import ast
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    similarity_file_path= os.path.join('artifacts',"similarity.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def extraction(self,sentence):
        req = []
        for i in ast.literal_eval(sentence):
            req.append(i['name'])
        return req
    def extraction_top_characters(self,sentence):
        req = []
        counter = 1
        for i in ast.literal_eval(sentence ):
            if counter <= 3 :
                req.append(i['name'])
            else :
                break 
            counter += 1 
        return req
    def director_evaluation(self,sentence):
        for i  in ast.literal_eval(sentence) :
            if i['job'] == 'Director' :
                return i['name']
    def combiner(self,sentence):
        arr = []
        for i in sentence :
            arr.append(i.replace(" ",""))
        return arr
    
    def join_crew(sent):
        combined_sent = []
        a = ""
        for i in sent:
            a+=i
        combined_sent.append(a)
        return combined_sent
    
    def get_data_transformer_object(self,movies):
        '''
        This function si responsible for data trnasformation
        
        '''
        try:
            
            movies['genres'] = movies['genres'].apply(self.extraction)
            movies['keywords'] = movies['keywords'].apply(self.extraction)
            movies['cast'] = movies['cast'].apply(self.extraction_top_characters)
            movies['crew'] = movies['crew'].apply(self.director_evaluation)
            
            movies['keywords'] = movies['keywords'].apply(self.combiner)
            movies['cast'] = movies['cast'].apply(self.combiner)
            movies['genres'] = movies['genres'].apply(self.combiner)

            movies['crew'] = movies['crew'].apply(self.combiner)
            movies['crew'] = movies['crew'].apply(self.join_crew)

            movies['text'] = movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
            movies['content'] = movies['text'].apply(lambda x : " ".join(x).lower())

            ## Now selecting only id , title , content column
            movies = movies[['id' , 'title' , 'content']]

            cv = CountVectorizer(max_features=6000 , stop_words='english' )
            transformed_vectors = cv.fit_transform(movies['content']).toarray()
            similarity = cosine_similarity(transformed_vectors)

            return similarity

            # logging.info(f"Categorical columns: {categorical_columns}")
            # logging.info(f"Numerical columns: {numerical_columns}")

        
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,movies_path):

        try:
            movies = pd.read_csv(movies_path)

            logging.info("Read movies data is completed")

            logging.info("Obtaining preprocessing object")

            similarity_obj  =self.get_data_transformer_object(movies)

            logging.info(f"Saved preprocessing object.")

            save_object(

                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = similarity_obj
            )
           
            return (
                movies,
                self.data_transformation_config.similarity_file_path,
            )
        except Exception as e:
            raise CustomException(e,sys)