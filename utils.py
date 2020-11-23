from models import Pessoas, Atividades, db_session


def insere_pessoas():
    pessoa = Pessoas(nome="Azevedo", idade=26)
    print(pessoa)
    db_session.add(pessoa)
    pessoa.save()



def consulta_pessoas():
    pessoa = Pessoas.query.all()
    print(pessoa)
    #pessoa = Pessoas.query.filter_by(nome="Zé").first()
    #print(pessoa.nome)

def altera_pessoa():
    pessoa = Pessoas.query.filter_by(nome="Matheus").first()
    pessoa.nome = "Zé"
    pessoa.save()


def exclui_pessoa():
    pessoa = Pessoas.query.filter_by(nome="Zé").first()
    pessoa.delete()

if __name__ == '__main__':
    #insere_pessoas()
    consulta_pessoas()
    #altera_pessoa()
    #exclui_pessoa()
