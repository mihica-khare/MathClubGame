from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import re

app = Flask(__name__)
CORS(app)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="innovation"
)

@app.route('/questions/<int:set_id>', methods=['GET'])
def get_questions(set_id):
    cursor = db.cursor(dictionary=True)
    query = """
    SELECT q.question_id, q.question_text, q.ans
    FROM Questions q
    JOIN QuestionSet qs ON q.question_id = qs.question_id
    WHERE qs.set_id = %s
    """
    cursor.execute(query, (set_id,))
    questions = cursor.fetchall()
    cursor.close()
    return jsonify(questions)

@app.route('/validate', methods=['POST'])
def validate_answer():
    data = request.json
    question_id = data['question_id']
    user_answer = data['answer']

    cursor = db.cursor(dictionary=True)
    query = "SELECT ans FROM Questions WHERE question_id = %s"
    cursor.execute(query, (question_id,))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return jsonify({"error": "Question not found"}), 404

    # Normalize both answers for comparison
    normalized_user_answer = user_answer
    normalized_correct_answer = result['ans']

    return jsonify({
        "correct": normalized_user_answer == normalized_correct_answer,
        "correct_answer": result['ans']  # Return original correct answer for display
    })

if __name__ == "__main__":
    app.run(debug=True)