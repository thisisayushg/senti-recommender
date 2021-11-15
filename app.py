from flask import Flask, jsonify, request, render_template
from model import LRRecommenderSystem

recommender = LRRecommenderSystem()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/users', methods=['GET'])
def load_users():
    return jsonify({'users': list(recommender.get_all_users())})

@app.route('/predict/<username>', methods=['GET'])
def predictions_for_user(username):
    if recommender.recommend_for(username) is None:
        return jsonify({'recommended_items': []})
    
    user_recommendations = recommender.filter_prediction_with_sentiments(username)

    return jsonify({'recommended_items': user_recommendations.to_dict('records')})
    
if __name__ == '__main__':
    app.run()