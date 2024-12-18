# models/projet_model.py
from database import get_db_connection

class ProjetModel:
    @staticmethod
    def creer_projet(titre, date, hum_max, temp_max, pompe_st, biologist_id, material_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO Projet (titre, date, hum_max, temp_max, pompe_st, biologist_id, material_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (titre, date, hum_max, temp_max, pompe_st, biologist_id, material_id))
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
            return projets
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_by_id(id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM Projet WHERE id = %s"
            cursor.execute(query, (id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_projet(id, titre, date, hum_max, temp_max, pompe_st, biologist_id, material_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            query = """
                UPDATE Projet
                SET titre = %s, date = %s, hum_max = %s, temp_max = %s, pompe_st = %s, biologist_id = %s, material_id = %s
                WHERE id = %s
            """
            cursor.execute(query, (titre, date, hum_max, temp_max, pompe_st, biologist_id, material_id, id))
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_projet(id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            query = "DELETE FROM Projet WHERE id = %s"
            cursor.execute(query, (id,))
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_by_biologist_id(biologist_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM Projet WHERE biologist_id = %s"
            cursor.execute(query, (biologist_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_by_material_id(material_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM Projet WHERE material_id = %s"
            cursor.execute(query, (material_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_by_titre(titre):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM Projet WHERE titre LIKE %s"
            cursor.execute(query, ('%' + titre + '%',))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_by_date(date):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM Projet WHERE date = %s"
            cursor.execute(query, (date,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
