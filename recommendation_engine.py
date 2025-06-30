# agent_recommender/recommendation_engine.py

import json

# Load agent data from JSON
def load_agents():
    with open("agents_db.json", "r") as f:
        return json.load(f)

# Simple task parser to extract keywords
def parse_task(task_description):
    task_keywords = {
        'languages': [],
        'skills': [],
        'env': []
    }

    text = task_description.lower()

    # Look for known languages
    for lang in ["python", "javascript", "java", "typescript"]:
        if lang in text:
            task_keywords['languages'].append(lang)

    # Look for known skills
    for skill in ["frontend", "backend", "api", "autocomplete", "bug", "refactor", "aws", "flask"]:
        if skill in text:
            task_keywords['skills'].append(skill)

    # Check environment keywords
    if "vscode" in text:
        task_keywords['env'].append("requires VSCode")

    return task_keywords

# Give a score to each agent
def score_agent(agent, task_keywords):
    score = 0

    for lang in task_keywords['languages']:
        if lang in agent['languages']:
            score += 2

    for skill in task_keywords['skills']:
        if skill in agent['strengths']:
            score += 3

    for limit in agent.get('limitations', []):
        if limit in task_keywords['env']:
            score -= 2

    return score

# Final recommender
def recommend_agents(task_description):
    agents = load_agents()
    task_keywords = parse_task(task_description)

    scored = []
    for agent in agents:
        score = score_agent(agent, task_keywords)
        scored.append({
            'agent': agent['name'],
            'score': score,
            'justification': f"Strengths: {', '.join(agent['strengths'])}"
        })

    # Sort and pick top 3
    sorted_agents = sorted(scored, key=lambda x: x['score'], reverse=True)
    return sorted_agents[:3]
