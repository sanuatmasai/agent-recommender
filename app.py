# agent_recommender/app.py

from flask import Flask, request, jsonify
from recommendation_engine import recommend_agents

app = Flask(__name__)

# Home route to test server
def home():
    return "Welcome to AI Coding Agent Recommender!"

# Route to get recommendations for a task
@app.route('/recommend', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    task = data.get('task', '')
    if not task:
        return jsonify({'error': 'Task description is required'}), 400

    recommendations = recommend_agents(task)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
