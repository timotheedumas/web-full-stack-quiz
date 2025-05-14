import sqlite3

DATABASE_PATH = "quiz.db"

def insert_question(position, title, text, image, possibleAnswers):
    connection = sqlite3.connect("quiz.db")
    cursor = connection.cursor()

    try:
        cursor.execute("BEGIN")

        # Décale les questions suivantes
        cursor.execute(
            "UPDATE Question SET position = position + 1 WHERE position >= ?",
            (position,)
        )

        # Insère la question
        cursor.execute(
            "INSERT INTO Question (position, title, text, image) VALUES (?, ?, ?, ?)",
            (position, title, text, image)
        )

        question_id = cursor.lastrowid

        # 🔽 Insère les réponses
        for answer in possibleAnswers:
            cursor.execute(
                "INSERT INTO Answer (question_id, text, isCorrect) VALUES (?, ?, ?)",
                (question_id, answer["text"], int(answer["isCorrect"]))
            )

        cursor.execute("COMMIT")
        return question_id

    except Exception as e:
        cursor.execute("ROLLBACK")
        raise e
    finally:
        connection.close()
