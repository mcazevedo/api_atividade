from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades, Usuarios
from flask_httpauth import HTTPBasicAuth
import json

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

@auth.verify_password
def verificao(login, senha):
    if not (login, senha):
        return False
    return Usuarios.query.filter_by(login=login,senha=senha).first()

class Pessoa(Resource):
    @auth.login_required
    def get(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            response = {
                "nome": pessoa.nome,
                "idade": pessoa.idade,
                "id": pessoa.id
            }
        except AttributeError:
            response = {"status":"Erro", "mensagem":"Pessoa nao encontrada!"}

        return response

    def put(self,nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            dados = request.json
            if "nome" in dados:
                pessoa.nome = dados["nome"]
            if "idade" in dados:
                pessoa.idade = dados["idade"]

            pessoa.save()

            response = {
                "id":pessoa.id,
                "nome":pessoa.nome,
                "idade":pessoa.idade
            }
        except AttributeError:
            response = {
                "status":"Erro",
                "mensagem":"Pessoa nao encontrada!"
            }

        return response

    def delete(self,nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            pessoa.delete()
            return {"status":"Sucesso!", "mensagem":f"pessoa {nome} excluida com sucesso."}
        except AttributeError:
            return {"status":"Erro", "mensagem":f"pessoa {nome} não encontrada"}


class ListaPessoa(Resource):
    @auth.login_required
    def get(self):
        pessoas = Pessoas.query.all()
        response = [{"id":i.id, "nome": i.nome, "idade": i.idade} for i in pessoas]
        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas(nome=dados["nome"], idade=dados["idade"])
        pessoa.save()
        response = {
            "id":pessoa.id,
            "nome":pessoa.nome,
            "idade":pessoa.idade
        }
        return response

class ListaAtividades(Resource):
    def get(self):
        atividades = Atividades.query.all()
        response = [{"id":i.id, "nome":i.nome, "pessoa":i.pessoa.nome} for i in atividades]
        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome=dados["pessoa"]).first()
        atividade = Atividades(nome=dados["nome"], pessoa=pessoa)
        atividade.save()
        response = {
            "pessoa":atividade.pessoa.nome,
            "atividade":atividade.nome,
            "id":atividade.id
        }
        return response


api.add_resource(Pessoa, "/pessoa/<string:nome>/")
api.add_resource(ListaPessoa, "/pessoa/")
api.add_resource(ListaAtividades, "/atividade/")


if __name__ == '__main__':
    app.run(debug=True)