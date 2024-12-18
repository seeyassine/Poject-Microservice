import os
import requests
import json
import socket
from flask import Flask
import strawberry
from strawberry.flask.views import GraphQLView
from models.projet_model import ProjetModel
from py_eureka_client import eureka_client


app = Flask(__name__)

# ======================
# Fetching Configuration for the Service (Dynamic)
# ======================
def fetch_config(service_name):
    config_service_url = os.getenv('CONFIG_SERVICE_URL', 'http://localhost:9999')
    config_url = f'{config_service_url}/{service_name}/default'
    try:
        response = requests.get(config_url)
        response.raise_for_status()  # Raise error for non-2xx responses
        print(f" fetching config: ", response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching config: {e}")
        return {}


# ======================
# Eureka Service Registration
# ======================

# Read Eureka server URL from the environment or fallback to localhost
eureka_server_url = os.getenv('DISCOVERY_SERVICE_URL', 'http://localhost:8761/eureka')

# Initialize Eureka client
eureka_client.init(
    app_name="project-service",           # Register with Eureka using service name
    eureka_server=eureka_server_url,  # Use the Eureka server URL from the configuration
    instance_port=5000,
    instance_host=socket.gethostbyname(socket.gethostname()),
)

# ======================
# GraphQL API Implementation
# ======================
@strawberry.type
class Projet:
    id: int
    titre: str
    date: str
    hum_max: float
    temp_max: float
    pompe_st: int
    biologist_id: int  # Add the biologistId field
    material_id: int   # Add the materialId field

@strawberry.type
class CreateProjetResponse:
    message: str
    projet_id: int

@strawberry.type
class Query:
    @strawberry.field
    def lister_projets(self) -> list[Projet]:
        projets = ProjetModel.lister_projets()
        return [Projet(**projet) for projet in projets]

    @strawberry.field
    def get_by_id(self, id: int) -> Projet:
        projet = ProjetModel.get_by_id(id)
        if projet:
            return Projet(**projet)
        raise ValueError("Projet introuvable")

    @strawberry.field
    def get_by_titre(self, titre: str) -> list[Projet]:
        projets = ProjetModel.get_by_titre(titre)
        return [Projet(**projet) for projet in projets]

    @strawberry.field
    def get_by_date(self, date: str) -> list[Projet]:
        projets = ProjetModel.get_by_date(date)
        return [Projet(**projet) for projet in projets]
   
    @strawberry.field
    def get_by_biologist(self, biologist_id: int) -> list[Projet]:
        projets = ProjetModel.get_by_biologist_id(biologist_id)
        return [Projet(**projet) for projet in projets]

    @strawberry.field
    def get_by_material(self, material_id: int) -> list[Projet]:
        projets = ProjetModel.get_by_material_id(material_id)
        return [Projet(**projet) for projet in projets]

@strawberry.type
class Mutation:
    @strawberry.mutation
    def creer_projet(self, titre: str, date: str, hum_max: float, temp_max: float, pompe_st: int, biologist_id: int, material_id: int) -> CreateProjetResponse:
        projet_id = ProjetModel.creer_projet(titre, date, hum_max, temp_max, pompe_st, biologist_id, material_id)
        return CreateProjetResponse(message="Projet créé avec succès", projet_id=projet_id)

    @strawberry.mutation
    def update_projet(self, id: int, titre: str, date: str, hum_max: float, temp_max: float, pompe_st: int, biologist_id: int, material_id: int) -> str:
        updated = ProjetModel.update_projet(id, titre, date, hum_max, temp_max, pompe_st, biologist_id, material_id)
        if updated:
            return "Projet mis à jour avec succès"
        return "Projet introuvable"

    @strawberry.mutation
    def delete_projet(self, id: int) -> str:
        deleted = ProjetModel.delete_projet(id)
        if deleted:
            return "Projet supprimé avec succès"
        return "Projet introuvable"

# ======================
# Health Check Endpoint
# ======================
@app.route('/health', methods=['GET'])
def health_check():
    return json.dumps({"status": "OK"}), 200

# ======================
# Flask Initialization and Dynamic Registration
# ======================
if __name__ == '__main__':
    # Fetch config for dynamic settings
    config = fetch_config('project-service')  # Fetch the service-specific configuration
    
    port = 5000  # Make sure this port is consistent with your application

    # Set up GraphQL API schema and start Flask application
    schema = strawberry.Schema(query=Query, mutation=Mutation)
    app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql_view', schema=schema))

    app.run(host='0.0.0.0',port=port, debug=True)
