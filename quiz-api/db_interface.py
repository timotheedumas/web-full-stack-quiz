import sqlite3
from models import Question, dict_to_question
from models import Participation


DATABASE_PATH = "quiz.db"


def save_question(question: Question):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute("BEGIN")
        cursor.execute(
            "INSERT INTO Question (position, title, text, image) VALUES (?, ?, ?, ?)",
            (question.position, question.title, question.text, question.image)
        )
        question_id = cursor.lastrowid
        cursor.execute("COMMIT")
        return question_id
    except Exception as e:
        cursor.execute("ROLLBACK")
        raise e
    finally:
        connection.close()


def get_question_by_id(question_id: int):
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM Question WHERE id = ?", (question_id,))
        row = cursor.fetchone()
        if row:
            return dict_to_question(dict(row))
        else:
            return None
    finally:
        connection.close()


def get_question_by_position(position: int):
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM Question WHERE position = ?", (position,))
        row = cursor.fetchone()
        if row:
            return dict_to_question(dict(row))
        else:
            return None
    finally:
        connection.close()


def update_question_by_id(question_id, new_position, title, text, image):
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row  # pour accéder à existing["id"]
    cursor = connection.cursor()

    try:
        cursor.execute("BEGIN")

        # Récupère la position actuelle
        cursor.execute("SELECT position FROM Question WHERE id = ?", (question_id,))
        row = cursor.fetchone()
        if not row:
            cursor.execute("ROLLBACK")
            return False
        current_position = row["position"]

        cursor.execute("UPDATE Question SET position = -1 WHERE id = ?", (question_id,))

        if new_position < current_position:
            # On monte la question => on décale vers le bas les autres entre new et current-1
            cursor.execute("""
                UPDATE Question
                SET position = position + 1
                WHERE position >= ? AND position < ?
            """, (new_position, current_position))
        elif new_position > current_position:
            # On descend la question => on décale vers le haut les autres entre current+1 et new
            cursor.execute("""
                UPDATE Question
                SET position = position - 1
                WHERE position <= ? AND position > ?
            """, (new_position, current_position))

        # Met à jour la question cible avec la nouvelle position et son contenu
        cursor.execute("""
            UPDATE Question
            SET position = ?, title = ?, text = ?, image = ?
            WHERE id = ?
        """, (new_position, title, text, image, question_id))

        if cursor.rowcount == 0:
            cursor.execute("ROLLBACK")
            return False

        cursor.execute("COMMIT")
        return True

    except Exception as e:
        cursor.execute("ROLLBACK")
        raise e
    finally:
        connection.close()



def delete_question_by_id(question_id):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute("BEGIN")
        # On récupère la position de la question à supprimer
        cursor.execute("SELECT position FROM Question WHERE id = ?", (question_id,))
        row = cursor.fetchone()
        if not row:
            cursor.execute("ROLLBACK")
            return False
        deleted_position = row[0]

        # On supprime la question
        cursor.execute("DELETE FROM Question WHERE id = ?", (question_id,))
        if cursor.rowcount == 0:
            cursor.execute("ROLLBACK")
            return False

        # On décale les suivantes vers le haut
        cursor.execute("""
            UPDATE Question
            SET position = position - 1
            WHERE position > ?
        """, (deleted_position,))

        cursor.execute("COMMIT")
        return True
    except Exception as e:
        cursor.execute("ROLLBACK")
        raise e
    finally:
        connection.close()


def delete_all_questions():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute("BEGIN")
        cursor.execute("DELETE FROM Question")
        cursor.execute("COMMIT")
    except Exception as e:
        cursor.execute("ROLLBACK")
        raise e
    finally:
        connection.close()


def delete_all_participations():
    connection = sqlite3.connect("quiz.db")
    cursor = connection.cursor()

    try:
        cursor.execute("BEGIN")
        cursor.execute("DELETE FROM Participation")
        cursor.execute("COMMIT")
    except Exception as e:
        cursor.execute("ROLLBACK")
        raise e
    finally:
        connection.close()



def get_question_count():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM Question")
        result = cursor.fetchone()
        return result[0] if result else 0
    finally:
        connection.close()


def reorder_questions(id_position_pairs):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute("BEGIN")
        for qid, new_pos in id_position_pairs:
            cursor.execute("UPDATE Question SET position = ? WHERE id = ?", (new_pos, qid))
        cursor.execute("COMMIT")
    except Exception as e:
        cursor.execute("ROLLBACK")
        raise e
    finally:
        connection.close()


def rebuild_database():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute("BEGIN")

        cursor.execute("DROP TABLE IF EXISTS Question")
        cursor.execute("""
            CREATE TABLE Question (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                position INTEGER NOT NULL UNIQUE,
                title TEXT NOT NULL,
                text TEXT NOT NULL,
                image TEXT
            )
        """)

        cursor.execute("DROP TABLE IF EXISTS Answer")
        cursor.execute("""
            CREATE TABLE Answer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                isCorrect BOOLEAN NOT NULL,
                FOREIGN KEY (question_id) REFERENCES Question(id)
            )
        """)

        cursor.execute("DROP TABLE IF EXISTS Participation")
        cursor.execute("""
            CREATE TABLE Participation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                playerName TEXT NOT NULL,
                score INTEGER NOT NULL,
                date TEXT NOT NULL
            )
        """)

        cursor.execute("COMMIT")
    except Exception as e:
        cursor.execute("ROLLBACK")
        raise e
    finally:
        connection.close()

def get_answers_for_question_id(question_id):
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM Answer WHERE question_id = ?", (question_id,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()

def save_participation(participation: Participation):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute("BEGIN")
        cursor.execute(
            "INSERT INTO Participation (playerName, score, date) VALUES (?, ?, ?)",
            (participation.playerName, participation.score, participation.date)
        )
        cursor.execute("COMMIT")
    except Exception as e:
        cursor.execute("ROLLBACK")
        raise e
    finally:
        connection.close()

def get_all_participations():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM Participation ORDER BY score DESC")
        rows = cursor.fetchall()
        return [Participation(**row) for row in rows]
    finally:
        connection.close()