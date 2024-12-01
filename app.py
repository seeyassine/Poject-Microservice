# app.py
from flask import Flask
from flask_jsonrpc import JSONRPC
from models.projet_model import ProjetModel

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

@jsonrpc.method('projet.creer_projet')
def creer_projet(titre: str, date: str, hum_max: float, temp_max: float, pompe_st: int):
    projet_id = ProjetModel.creer_projet(titre, date, hum_max, temp_max, pompe_st)
    return {"message": "Projet créé avec succès", "projet_id": projet_id}

@jsonrpc.method('projet.lister_projets')
def lister_projets() -> dict:
    projets = ProjetModel.lister_projets()
    return projets

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
