from lets_alexandria.core_entities import Article, Library
from lets_alexandria.user_interface import UserInterface
0
def main():
    ui = UserInterface()

    ui.run()


if __name__ == '__main__':
    main()




'''
Crie um programa em python para cadastrar pequenos artigos contendo: título, assunto, data (ano/mês/dia ex. 2021/09/10) de publicação e o texto. Não se esqueça de persistir os artigos em arquivos.  
  
Os artigos devem estar alocados em uma biblioteca de artigos, que são separados por assuntos: esporte, política e tecnologia.  
  
O usuário pode consultar em ordem de data quais artigos foram publicados (mostrar somente data, título e assunto).  
  
Poderá também ter um relatório de quais artigos são mais parecidos. (utilize como métrica número de palavras únicas coincidentes dividido pela soma de palavras únicas dos artigos).  
  
Não se esqueça de criar um menu para facilitar a vida do nosso usuário.  
  
Pontos considerados na avaliação:  
- Legibilidade do código, pessoas que nunca viram o código devem entender e conseguir dar manutenção (O segredo é modularizar de forma coerente).  
- Orientação a Objetos, aplicar os conceitos principais.  
- O quanto eficiente o programa é para processar os dados.  
- Uso correto das estruturas de dados, decisão e repeticão.  
  '''