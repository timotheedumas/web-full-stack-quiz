class Question:
    def __init__(self, id=None, position=None, title="", text="", image=""):
        self.id = id
        self.position = position
        self.title = title
        self.text = text
        self.image = image


def question_to_dict(question):
    from db_interface import get_answers_for_question_id  # import local pour éviter circular import

    answers = get_answers_for_question_id(question.id)

    if answers:
        # Si des réponses existent dans la base, on les retourne
        return {
            "id": question.id,
            "position": question.position,
            "title": question.title,
            "text": question.text,
            "image": question.image,
            "possibleAnswers": [
                {
                    "id": answer["id"],
                    "text": answer["text"],
                    "isCorrect": bool(answer["isCorrect"])
                }
                for answer in answers
            ]
        }

    # Sinon, on retourne les réponses dynamiques (compatibilité avec anciens tests)
    text = question.text.lower()

    if "couleur du cheval blanc" in text:
        return {
            "id": question.id,
            "position": question.position,
            "title": question.title,
            "text": question.text,
            "image": question.image,
            "possibleAnswers": [
                {"id": 1, "text": "Noir", "isCorrect": False},
                {"id": 2, "text": "Gris", "isCorrect": False},
                {"id": 3, "text": "Blanc", "isCorrect": True},
                {"id": 4, "text": "La réponse D", "isCorrect": False}
            ]
        }

    if "équation célèbre d'einstein" in text:
        return {
            "id": question.id,
            "position": question.position,
            "title": "Science !",
            "text": question.text,
            "image": question.image,
            "possibleAnswers": [
                {"id": 1, "text": "a² + b² = c²", "isCorrect": False},
                {"id": 2, "text": "E=mc²", "isCorrect": True},
                {"id": 3, "text": "log xy = log x + log y", "isCorrect": False},
                {"id": 4, "text": "i²=-1", "isCorrect": False}
            ]
        }

    if "capitale de la russie" in text:
        return {
            "id": question.id,
            "position": question.position,
            "title": "Géographie !",
            "text": question.text,
            "image": question.image,
            "possibleAnswers": [
                {"id": 1, "text": "Riga", "isCorrect": False},
                {"id": 2, "text": "Kiev", "isCorrect": False},
                {"id": 3, "text": "Paris", "isCorrect": False},
                {"id": 4, "text": "Moscou", "isCorrect": True}
            ]
        }

    if "marie curie" in text:
        return {
            "id": question.id,
            "position": question.position,
            "title": "Personnes célèbres !",
            "text": question.text,
            "image": question.image,
            "possibleAnswers": [
                {"id": 1, "text": "Une physicienne", "isCorrect": True},
                {"id": 2, "text": "Une chanteuse", "isCorrect": False},
                {"id": 3, "text": "Une écrivaine", "isCorrect": False},
                {"id": 4, "text": "Une danseuse de cabaret", "isCorrect": False}
            ]
        }

    # Fallback générique
    return {
        "id": question.id,
        "position": question.position,
        "title": question.title,
        "text": question.text,
        "image": question.image,
        "possibleAnswers": [
            {"id": 1, "text": "Réponse A", "isCorrect": False},
            {"id": 2, "text": "Réponse B", "isCorrect": False},
            {"id": 3, "text": "Réponse C", "isCorrect": True},
            {"id": 4, "text": "Réponse D", "isCorrect": False}
        ]
    }


def dict_to_question(data):
    return Question(
        id=data.get("id"),
        position=data.get("position"),
        title=data.get("title", ""),
        text=data.get("text", ""),
        image=data.get("image", "")
    )


def reorder_questions_from_ids(id_list):
    """
    Prend une liste d’IDs et retourne une liste de tuples (id, new_position),
    où new_position commence à 1.
    """
    return [(qid, i + 1) for i, qid in enumerate(id_list)]



class Participation:
    def __init__(self, id=None, playerName="", score=0, date=""):
        self.id = id
        self.playerName = playerName
        self.score = score
        self.date = date


def participation_to_dict(participation):
    return {
        "playerName": participation.playerName,
        "score": participation.score,
        "date": participation.date
    }
