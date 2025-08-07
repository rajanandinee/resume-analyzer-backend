# recommender.py

from sentence_transformers import SentenceTransformer, util

# Define job descriptions
JOB_ROLE_MAP = {
    "SDE-I": "Developers with strong DSA, problem-solving, and Python/Java skills.",
    "SDE-II": "Experienced in systems design, backend, and architecture decisions.",
    "Data Scientist": "Skilled in machine learning, statistics, and Python libraries like pandas and scikit-learn.",
    "ML Engineer": "Experience with ML model deployment, TensorFlow/PyTorch, and pipelines.",
    "Backend Developer": "Strong in Node.js, databases, API development and optimization.",
    "Frontend Developer": "Fluent in HTML, CSS, JavaScript, React.js or similar frameworks.",
    "Full Stack Developer": "Combination of frontend and backend experience using MERN/MEAN stack.",
    "DevOps Engineer": "Hands-on with CI/CD, Docker, Kubernetes, and infrastructure tools.",
    "DSA Specialist": "Strong knowledge of data structures and algorithms with competitive coding background.",
    "AI/ML Researcher": "Research-focused ML/AI experience with publications or novel models."
}

model = SentenceTransformer('all-MiniLM-L6-v2')  # Load once globally

def recommend_role_semantically(resume_text: str, top_n: int = 3):
    """Returns top N job roles based on semantic similarity to resume"""
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)

    similarities = []
    for role, description in JOB_ROLE_MAP.items():
        role_embedding = model.encode(description, convert_to_tensor=True)
        score = util.cos_sim(resume_embedding, role_embedding).item()
        similarities.append((role, score))

    # Sort descending and return top N
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_n]
