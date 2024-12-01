from flask import Flask
from strawberry.flask.views import GraphQLView
import strawberry
from models.projet_model import ProjetModel

app = Flask(__name__)

# Define GraphQL types
@strawberry.type
class Projet:
    id: int
    titre: str
    date: str
    hum_max: float
    temp_max: float
    pompe_st: int

@strawberry.type
class CreateProjetResponse:
    message: str
    projet_id: int

@strawberry.type
class Query:
    @strawberry.field
    def lister_projets(self) -> list[Projet]:
        # Get the list of projects
        projets = ProjetModel.lister_projets()

        # Return a list of Projet objects, unpacking the dictionary for each project
        return [Projet(**projet) for projet in projets]

@strawberry.type
class Mutation:
    @strawberry.mutation
    def creer_projet(self, titre: str, date: str, hum_max: float, temp_max: float, pompe_st: int) -> CreateProjetResponse:
        projet_id = ProjetModel.creer_projet(titre, date, hum_max, temp_max, pompe_st)
        return CreateProjetResponse(message="Projet créé avec succès", projet_id=projet_id)

# Create GraphQL schema
schema = strawberry.Schema(query=Query, mutation=Mutation)

# Add the GraphQL view to Flask
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql_view', schema=schema))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
