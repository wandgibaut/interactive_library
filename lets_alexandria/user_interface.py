import datetime
from lets_alexandria.core_entities import Library, Article

class UserInterface:
    def __init__(self, library : Library = None) -> None:
        if library is None:
            library = Library("default")
        self.library = library

    def run(self) -> None:
        self.greetings()
        while True:
            self.menu()
            option = self.get_option(8)
            self.process_option(option)


    def menu(self) -> None:
        print("""
        0 - Carregar biblioteca
        1 - Cadastrar artigo
        2 - Listar artigos
        3 - Buscar artigo (por nome, tema ou data)
        4 - Verificar similaridade
        5 - Buscar por similaridade
        6 - Remover artigo (por nome)
        7 - Salvar e sair
        8 - Sair sem salvar
        """)

    def search_menu(self) -> None:
        print("""
        0 - Nome
        1 - Data
        2 - Tema
        3 - Voltar
        """)
    
    def add_menu(self) -> None:
        print("""
        0 - Adicionar artigo via terminal
        1 - Adicionar artigo via arquivo
        2 - Voltar
        """)
    
    def greetings(self) -> None:
        print("""
        Bem vindo ao Alexandria!
        """)

    def goodbye(self) -> None:
        print("""
        Obrigado por usar Alexandria!
        """)

    def get_option(self, n_options) -> int:
        try:
            option = int(input("Digite a opção desejada: "))
        except ValueError:
            self.error_message("Opção inválida!")
            option = self.get_option(n_options)

        if option < 0 or option > n_options:
            self.error_message("Opção inválida!")
            option = self.get_option(n_options)

        return option

    def load_library(self, filepath) -> None:
        try:
            self.library.load(file_name=filepath)
        except FileNotFoundError:
            self.error_message("Não foi possível carregar a biblioteca! Algum erro ocorreu! :/")
        except Exception as e:
            print(e)
    
    def save_library(self, filepath) -> None:
        try:
            self.library.save(filepath)
        except Exception as e:
            print(e)
    

    def add_article(self, file=False) -> None:
        artigo = {}
        artigo["title"] = input("Digite o titulo do artigo: ")
        artigo["tag"] = input("Digite o tema do artigo: ")
        artigo["date"] = input("Digite a data do artigo (no formato dd/mm/yyyy): ")

        if file:
            filepath = input("Digite o caminho do arquivo (com extensão): ")
            artigo["text"] = self.get_text_from_file(filepath)

        else:
            artigo["text"] = input("Digite o texto do artigo: ")

        try:
            self.library.add_article(Article(**artigo))
        except Exception as e:
            print(e)
    
    def get_text_from_file(self, filepath) -> str:
        try:
            with open(filepath, 'r') as f:
                text = f.read()
        except FileNotFoundError:
            self.error_message("Arquivo não encontrado!")
        except Exception as e:
            print(e)
        return text

    def list_articles(self) -> list:
        try:
            return self.library.get_articles_sorted()
        except Exception as e:
            print(e)
    
    def print_articles(self, articles : list) -> None:
        for article in articles:
            print(article)
            print("\n")

    def get_article_by_name(self, name) -> Article:
        try:
            return self.library.get_article_by_name(name)
        except Exception as e:
            print(e)
    
    def get_article_by_date(self, date) -> list:
        try:
            op = datetime.datetime.strptime(date, "%d/%m/%Y").date()
            return self.library.get_articles_by_date(op)
        except Exception as e:
            print(e)

    def get_article_by_tag(self, tag) -> list:
        try:
            return self.library.get_articles_by_tag(tag)
        except Exception as e:
            print(e)
    
    def remove_article(self, name) -> None:
        try:
            self.library.remove_article_by_name(name)
        except Exception as e:
            print(e)

    def save_and_exit(self, library_name) -> None:
        self.save_library('data/' + library_name + '.txt')
        self.goodbye()
        exit()

    def exit_without_saving(self) -> None:
        self.goodbye()
        exit()

    def process_option(self, option : int) -> None:
        if option == 0:
            lib = input("Digite o nome da biblioteca sem a extensão. Ela deve estar na pasta 'data': ")
            self.load_library('data/' + lib + ".txt")
        elif option == 1:
            self.add_menu()
            param = self.get_option(3)
            self.process_add_option(param)
        elif option == 2:
            self.print_articles(self.list_articles())
        elif option == 3:
            self.search_menu()
            param = self.get_option(4)
            answer = self.process_search_option(param)
            if answer is not None:
                if isinstance(answer, list):
                    self.print_articles(answer)
                else:
                    print(answer)
        elif option == 4:
            param = self.get_parameter("nome do artigo")
            sim = self.library.calculate_similarities(self.library.get_article_by_name(param))
            print('Aqui estão todas as similaridades com o artigo buscado!\n')
            print(sim)
        elif option == 5:
            param = self.get_parameter("nome do artigo")
            sim = self.library.get_article_by_greatest_similarity(self.library.get_article_by_name(param))
            print('Aqui está o artigo mais similar ao buscado!\n')
            print(sim)
        elif option == 6:
            param = self.get_parameter("nome do artigo")
            self.remove_article(param)
        elif option == 7:
            lib = input("Digite o nome da biblioteca sem a extensão. Ela estará na pasta 'data': ")
            self.save_and_exit(lib)
        elif option == 8:
            self.exit_without_saving()

    
    def get_parameter(self, parameter_name : str) -> str:
        try:
            parameter = input("Digite o " + parameter_name + ": ")
        except ValueError:
            self.error_message("Parâmetro inválido!")
            parameter = self.get_parameter(parameter_name)
        return parameter

    def process_search_option(self, option : int) -> object:
        answer = None
        if option == 0:
            answer = self.get_article_by_name(self.get_parameter("nome"))
        elif option == 1:
            answer = self.get_article_by_date(self.get_parameter("data"))
        elif option == 2:
            answer = self.get_article_by_tag(self.get_parameter("tema"))
        elif option == 3:
            pass
        else:
            self.error_message("Opção inválida!")
        return answer

    def process_add_option(self, option : int) -> None:
        if option == 0:
            self.add_article()
        elif option == 1:
            self.add_article(file=True)
        else:
            self.error_message("Opção inválida!")

    def error_message(self, error_message: str) -> None:
        print(error_message)