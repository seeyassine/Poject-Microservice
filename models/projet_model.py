# models/projet_model.py
from database import get_db_connection

class ProjetModel:
    @staticmethod
    def creer_projet(titre, date, hum_max, temp_max, pompe_st):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO Projet (titre, date, hum_max, temp_max, pompe_st)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (titre, date, hum_max, temp_max, pompe_st))
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def lister_projets():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM Projet"
            cursor.execute(query)
            projets = cursor.fetchall()
            return {"projets": projets}  # Ensure that a dictionary is returned
        finally:
            cursor.close()
            conn.close()
