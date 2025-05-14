from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
from datetime import datetime

from jwt_utils import build_token
from jwt_utils import decode_token

from models import (
    question_to_dict,
    reorder_questions_from_ids,
    Participation,
    participation_to_dict
)
from question_manager import insert_question
from db_interface import (
    get_question_by_id,
    get_question_by_position,
    update_question_by_id,
    delete_question_by_id,
    get_question_count,
    delete_all_questions,
    reorder_questions,
    rebuild_database,
    save_participation,
    get_answers_for_question_id,
    get_all_participations
    
)

app = Flask(__name__)
CORS(app)

expected_hash = b'\xd2x\x07{\xbf\xe7(Z\x14MK[\x11\xad\xb9\xcf'

@app.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    tried_password = payload.get('password', '').encode('utf-8')
    hashed = hashlib.md5(tried_password).digest()

    print(f"Reçu : {payload}")
    print(f"Hash généré : {hashed}")

    if hashed == expected_hash:
        token = build_token()
        return {'token': token}, 200
    else:
        return jsonify({"error": "Unauthorized"}), 401

@app.route('/questions', methods=['POST'])
def post_question():
    token = request.headers.get('Authorization')
    if token and token.startswith("Bearer "):
        token = token[7:]

    try:
        decode_token(token)
    except:
        return 'Unauthorized', 401

    data = request.get_json()

    if "possibleAnswers" not in data:
        return {"error": "Missing possibleAnswers"}, 400

    question_id = insert_question(
        position=data["position"],
        title=data["title"],
        text=data["text"],
        image=data["image"],
        possibleAnswers=data["possibleAnswers"]
    )
    return {"id": question_id}, 200

@app.route('/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
    question = get_question_by_id(question_id)
    if question:
        return question_to_dict(question), 200
    else:
        return {"error": "Question not found"}, 404

@app.route("/questions", methods=["GET"])
def get_question_by_position_endpoint():
    position = request.args.get("position", type=int)

    if position is None:
        return {"error": "Missing position parameter"}, 400

    question = get_question_by_position(position)
    if question:
        return question_to_dict(question), 200
    else:
        return {"error": "Question not found"}, 404

@app.route("/questions/<int:question_id>", methods=["PUT"])
def update_question(question_id):
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        token = token[7:]
    try:
        decode_token(token)
    except:
        return {"error": "Unauthorized"}, 401

    data = request.get_json()
    success = update_question_by_id(
        question_id,
        new_position=data["position"],
        title=data["title"],
        text=data["text"],
        image=data["image"]
    )

    if not success:
        return {"error": "Not found"}, 404

    return "", 204

@app.route("/questions/<int:question_id>", methods=["DELETE"])
def delete_question(question_id):
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        token = token[7:]
    try:
        decode_token(token)
    except:
        return {"error": "Unauthorized"}, 401

    success = delete_question_by_id(question_id)
    if not success:
        return {"error": "Not found"}, 404

    return "", 204

@app.route("/quiz-info", methods=["GET"])
def get_quiz_info():
    count = get_question_count()
    participations = get_all_participations()

    scores = [participation_to_dict(p) for p in participations]

    return {
        "size": count,
        "scores": scores
    }, 200

@app.route("/questions/all", methods=["DELETE"])
def delete_all_questions_route():
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        token = token[7:]
    try:
        decode_token(token)
    except:
        return {"error": "Unauthorized"}, 401

    delete_all_questions()
    return "", 204

@app.route("/participations/all", methods=["DELETE"])
def delete_all_participations_route():
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        token = token[7:]
    try:
        decode_token(token)
    except:
        return {"error": "Unauthorized"}, 401

    from db_interface import delete_all_participations
    delete_all_participations()
    return "", 204


@app.route("/questions/order", methods=["POST"])
def reorder_questions_endpoint():
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        token = token[7:]
    try:
        decode_token(token)
    except:
        return {"error": "Unauthorized"}, 401

    data = request.get_json()
    if not isinstance(data, list):
        return {"error": "Invalid payload"}, 400

    id_position_pairs = reorder_questions_from_ids(data)
    reorder_questions(id_position_pairs)
    return "", 204

# 🔧 Optionnel : endpoint rebuild-db à compléter plus tard
@app.route("/rebuild-db", methods=["POST"])
def rebuild_db_route():
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        token = token[7:]
    try:
        decode_token(token)
    except:
        return {"error": "Unauthorized"}, 401

    rebuild_database()
    return "Ok", 200

@app.route("/participations", methods=["POST"])
def post_participation():
    data = request.get_json()

    player_name = data.get("playerName", "")
    answers = data.get("answers", [])

    if not player_name or not isinstance(answers, list):
        return {"error": "Invalid payload"}, 400

    if len(answers) != 10:
        return {"error": "Exactly 10 answers required"}, 400

    # Si on reçoit une liste d'entiers : [id1, id2, ...]
    if all(isinstance(a, int) for a in answers):
        answers = [
            {"questionId": i + 1, "answerId": aid}
            for i, aid in enumerate(answers)
        ]

    score = 0
    for entry in answers:
        if not isinstance(entry, dict):
            return {"error": "Each answer must be an object with questionId and answerId"}, 400

        question_id = entry.get("questionId")
        answer_id = entry.get("answerId")

        if not question_id or not answer_id:
            return {"error": "Missing questionId or answerId"}, 400

        possible_answers = get_answers_for_question_id(question_id)

        if 1 <= answer_id <= len(possible_answers):
            valid_answer = possible_answers[answer_id - 1]  # Interprétation indexée
        else:
            return {"error": "Answer does not match question"}, 400

        if valid_answer["isCorrect"]:
            score += 1

    participation = Participation(
        playerName=player_name,
        score=score,
        date=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    )
    save_participation(participation)

    return participation_to_dict(participation), 200


if __name__ == "__main__":
    app.run()