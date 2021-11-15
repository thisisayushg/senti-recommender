import numpy as np
import pickle

class LRRecommenderSystem():
    def __init__(self):
        with open('TFIDFTransformer.pkl','rb') as file:
            vectorizer = pickle.load(file)

        with open('LinearRegressionModel.pkl', 'rb') as file:
            lr_model = pickle.load(file)
        
        with open('item_recommendation.pkl', 'rb') as file:
            item_recommender = pickle.load(file)
        
        with open('products.pkl', 'rb') as file:
            data = pickle.load(file)

        self.model = lr_model
        self.vectorizer = vectorizer
        self.data = data
        self.item_recommender = item_recommender


    def get_all_users(self):
        '''
        Return a list of all registered users
        '''
        return self.item_recommender.index


    def recommend_for(self, user: str):
        '''
        Takes in a username and returns the recommended items for the user
        Returns None in case of invalid user
        '''
        try: 
            top20_items = self.item_recommender.loc[user, :].sort_values(ascending=False).index[:20]
        except KeyError:
            return None

        return list(top20_items)


    def filter_prediction_with_sentiments(self, user: str):
        '''
        given a username, return a list of top 5 recommended items with some details like name, brand, category and associated tags
        '''
        top20_items = self.data[self.data.name.isin(self.recommend_for(user))]
        top20_items.loc[:, 'predicted_sentiments'] = self.sentiment_predictor((top20_items['reviews_text']))
        top20_sentimental_score = top20_items.groupby('name')['predicted_sentiments']\
            .agg(['count', 'sum']).rename(columns={'count': 'total users who reviewed', 'sum': 'users with positive sentiments'})

        top20_sentimental_score['percent'] =  \
            top20_sentimental_score['users with positive sentiments'] /top20_sentimental_score['total users who reviewed']* 100
            
        top5_recommendations = top20_sentimental_score.sort_values(by='percent', ascending=False)[:5]


        # Getting detailed data on the top 5 products
        products_data = self.data[self.data.name.isin(top5_recommendations.index)][['id', 'name','brand','categories','broad_category']]

        products_data = products_data.drop_duplicates()

        return products_data


    def sentiment_predictor(self, text: [str]):
        '''
        Given a list of string, predict sentiment in those set of strings
        1- Positive
        0- Negative
        '''
        input_text = self.vectorizer.transform(text)
        return self.model.predict(input_text)
