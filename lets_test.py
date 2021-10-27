import datetime
import unittest
import os
import io
import sys
from lets_alexandria.core_entities import Article, Library
from lets_alexandria.user_interface import UserInterface

class AlexandriaTest(unittest.TestCase):
    # Testes da classe Article
    def test_simple_article_creation(self):
        article = Article(title="title", tag="tema", text="texto")
        self.assertEqual(article.title, "title")
        self.assertEqual(article.tag, "tema")
        self.assertEqual(article.get_text(), "texto")

    def test_article_from_file(self):
        article = Article(title="title", tag="tema", filepath="data/teste_file_artigo.txt")
        
        expected_text = "Três Anéis para os Reis-Elfos sob este céu;\n" + \
        "Sete para os Senhores-Anões em seus rochosos corredores;\n" + \
        "Nove para os Homens Mortais fadados a morrer;\n" + \
        "Um para o Senhor do Escuro em seu Escuro Trono,\n" + \
        "Na terra de Mordor, onde as Sombras se deitam.\n" + \
        "Um Anel para a todos governar, Um Anel para encontrá-los,\n" + \
        "Um Anel para a todos trazer e na Escuridão aprisioná-los,\n" + \
        "Na terra de Mordor, onde as Sombras se deitam." 
        
        
        self.assertEqual(article.title, "title")
        self.assertEqual(article.tag, "tema")
        self.assertEqual(article.get_text(), expected_text)
    
    def test_repr(self):
        article = Article(title="title", tag="tema", text="texto")
        answer ={
            'Title': article.get_title(), 
            'Tag': article.get_tag(), 
            'Date': article.get_date().strftime("%d/%m/%Y"), 
            'Text': article.get_text()}
        #answer = ''
        #answer += 'Title: ' + article.get_title() + '\n'
        #answer += 'Tag: ' + article.get_tag() + '\n'
        #answer += 'Date: ' + str(article.get_date()) + '\n'
        #answer += 'Text: ' + article.get_text() + '\n'

        self.assertEqual(article.__repr__(), str(answer))

    def test_article_creation_with_date(self):
        article = Article(title="title", tag="tema", text="texto", date="21/10/2021")
        self.assertEqual(article.title, "title")
        self.assertEqual(article.tag, "tema")
        self.assertEqual(article.get_text(), "texto")
        self.assertEqual(article.get_date(), datetime.date(2021, 10, 21))
    

    def test_similarity_with_same_article(self):
        article = Article(title="title", tag="tema", text="texto")
        self.assertEqual(article.calculate_similarity(article), 1)

    def test_similarity_with_different_article(self):
        article1 = Article(title="title", tag="tema", filepath="data/teste_file_artigo.txt")
        article2 = Article(title="title", tag="tema", filepath="data/teste_file_artigo_2.txt")
        self.assertEqual(article1.calculate_similarity(article2), 0.3864)


    # Testes da classe Library
    def test_simple_library_creation(self):
        library = Library("BAE")
        self.assertEqual(library.articles, [])

    def test_library_creation_with_articles(self):
        article1 = Article(title="title", tag="tema", filepath="data/teste_file_artigo.txt")
        article2 = Article(title="title", tag="tema", filepath="data/teste_file_artigo_2.txt")
        
        library = Library("BAE", [article1, article2])
        articles = [article1, article2]
        self.assertEqual(library.articles, articles)

    def test_add_article(self):
        article1 = Article(title="title", tag="tema", filepath="data/teste_file_artigo.txt")
        article2 = Article(title="title", tag="tema", filepath="data/teste_file_artigo_2.txt")
        
        library = Library("BAE", [article1])
        library.add_article(article2)
        articles = [article1, article2]
        self.assertEqual(library.articles, articles)
    
    def test_remove_article_by_name(self):
        article1 = Article(title="title", tag="tema", filepath="data/teste_file_artigo.txt")
        article2 = Article(title="title_2", tag="tema", filepath="data/teste_file_artigo_2.txt")
        
        library = Library("BAE", [article1, article2])
        library.remove_article_by_name("title")
        articles = [article2]
        self.assertEqual(library.articles, articles)

    def test_remove_article_by_name_not_found(self):
        article1 = Article(title="title", tag="tema", filepath="data/teste_file_artigo.txt")
        article2 = Article(title="title_2", tag="tema", filepath="data/teste_file_artigo_2.txt")
        
        library = Library("BAE", [article1, article2])
        library.remove_article_by_name("title_3")
        articles = [article1, article2]
        self.assertEqual(library.articles, articles)

    def test_remove_article(self):
        article1 = Article(title="title", tag="tema", filepath="data/teste_file_artigo.txt")
        article2 = Article(title="title_2", tag="tema", filepath="data/teste_file_artigo_2.txt")
        
        library = Library("BAE", [article1, article2])
        library.remove_article(article2)
        articles = [article1]
        self.assertEqual(library.articles, articles)
    
    def test_representation(self):
        article1 = Article(title="title", tag="tema", text="text")
        article2 = Article(title="title_2", tag="tema", text="text_2")
        
        library = Library("BAE", [article1, article2])
        answer =str({'Library': library.name, 'Articles': library.articles})
        #answer = ''
        #answer += 'Library: BAE\n'
        #answer += 'Articles:\n'
        #answer += 'Title: title\n'
        #answer += 'Tag: tema\n'
        #answer += 'Date: ' + str(article1.get_date()) + '\n'
        #answer += 'Text: text\n\n\n'
        #answer += 'Title: title_2\n'
        #answer += 'Tag: tema\n'
        #answer += 'Date: ' + str(article2.get_date()) + '\n'
        #answer += 'Text: text_2\n\n\n'
        self.assertEqual(library.__repr__(), answer)

    def test_get_article_by_name(self):
        article1 = Article(title="title", tag="tema", filepath="data/teste_file_artigo.txt")
        article2 = Article(title="title_2", tag="tema", filepath="data/teste_file_artigo_2.txt")
        
        library = Library("BAE", [article1, article2])
        self.assertEqual(library.get_article_by_name("title"), article1)

    def test_get_article_by_name_not_found(self):
        article1 = Article(title="title", tag="tema", filepath="data/teste_file_artigo.txt")
        article2 = Article(title="title_2", tag="tema", filepath="data/teste_file_artigo_2.txt")
        
        library = Library("BAE", [article1, article2])
        self.assertEqual(library.get_article_by_name("title_3"), None)
    
    def test_get_articles_by_tag(self):
        article1 = Article(title="title", tag="tema", filepath="data/teste_file_artigo.txt")
        article2 = Article(title="title_2", tag="tema", filepath="data/teste_file_artigo_2.txt")
        
        library = Library("BAE", [article1, article2])
        self.assertEqual(library.get_articles_by_tag("tema"), [article1, article2])

    def test_get_articles_by_tag_not_found(self):
        article1 = Article(title="title", tag="tema", filepath="data/teste_file_artigo.txt")
        article2 = Article(title="title_2", tag="tema", filepath="data/teste_file_artigo_2.txt")
        
        library = Library("BAE", [article1, article2])
        self.assertEqual(library.get_articles_by_tag("tema_2"), []) 
    
    def test_get_articles_by_date(self):
        article1 = Article(title="title", tag="tema", filepath="data/teste_file_artigo.txt")
        article2 = Article(title="title_2", tag="tema", filepath="data/teste_file_artigo_2.txt", date="21/10/2021")
        
        library = Library("BAE", [article1, article2])
        self.assertEqual(library.get_articles_by_date(datetime.date(2021, 10, 25)), [article1])
    
    def test_get_articles_sorted_by_date(self):
        article1 = Article(title="title", tag="tema", filepath="data/teste_file_artigo.txt")
        article2 = Article(title="title_2", tag="tema", filepath="data/teste_file_artigo_2.txt", date="21/10/2021")
        
        library = Library("BAE", [article1, article2])
        self.assertEqual(library.get_articles_sorted()[::-1], [article2, article1])

    def test_calculate_similarity(self):
        article1 = Article(title="title", tag="tema", filepath="data/teste_file_artigo.txt")
        article2 = Article(title="title_2", tag="tema", filepath="data/teste_file_artigo_2.txt")
        
        library = Library("BAE", [article1, article2])
        self.assertEqual(library.calculate_similarities(article1), [1.0, 0.3864])

    def test_calculate_all_similarities(self):
        article1 = Article(title="title", tag="tema", filepath="data/teste_file_artigo.txt")
        article2 = Article(title="title_2", tag="tema", filepath="data/teste_file_artigo_2.txt")
        
        library = Library("BAE", [article1, article2])
        self.assertEqual(library.calculate_all_similarities(), [[1.0, 0.3864],[0.3864, 1.0]])

    def test_get_greatest_similarity(self):
        article1 = Article(title="title", tag="tema", filepath="data/teste_file_artigo.txt")
        article2 = Article(title="title_2", tag="tema", filepath="data/teste_file_artigo_2.txt")
        
        library = Library("BAE", [article1, article2])
        self.assertEqual(library.get_greatest_similarity(article1)[1], 0.3864)
    
    def test_get_article_by_greatest_similarity(self):
        article1 = Article(title="title", tag="tema", filepath="data/teste_file_artigo.txt")
        article2 = Article(title="title_2", tag="tema", filepath="data/teste_file_artigo_2.txt")
        
        library = Library("BAE", [article1, article2])
        self.assertEqual(library.get_article_by_greatest_similarity(article1), article2)


    def test_save_library(self):
        article1 = Article(title="title", tag="tema", filepath="data/teste_file_artigo.txt")
        article2 = Article(title="title_2", tag="tema", filepath="data/teste_file_artigo_2.txt", date="21/10/2021")
        
        library = Library("BAE", [article1, article2])
        library.save("data/teste_file_biblioteca.txt")
        self.assertTrue(os.path.isfile("data/teste_file_biblioteca.txt"))
        #os.remove("data/teste_file_biblioteca.txt")

    def test_load_library(self):
        article1 = Article(title="title", tag="tema", filepath="data/teste_file_artigo.txt")
        article2 = Article(title="title_2", tag="tema", filepath="data/teste_file_artigo_2.txt", date="21/10/2021")
        
        library = Library("BAE", [article1, article2])
        library2 = Library("IMECC")
        library.save("data/teste_file_biblioteca.txt")
        library2.load("data/teste_file_biblioteca.txt")
        self.assertEqual(library, library2)
        self.assertEqual(library2.get_articles(), [article1, article2])
        #os.remove("data/teste_file_biblioteca.txt")

    # Testes para a classe userInterface
    def test_menu_user_interface(self):
        ui = UserInterface()
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        expected_messsage = """
        0 - Carregar biblioteca
        1 - Cadastrar artigo
        2 - Listar artigos
        3 - Buscar artigo (por nome, tema ou data)
        4 - Verificar similaridade
        5 - Buscar por similaridade
        6 - Remover artigo (por nome)
        7 - Salvar e sair
        8 - Sair sem salvar
        """
        ui.menu()
        sys.stdout = sys.__stdout__
        self.assertTrue(expected_messsage in capturedOutput.getvalue())

    def test_greetings(self):
        ui = UserInterface()
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        expected_messsage = """
        Bem vindo ao Alexandria!
        """
        ui.greetings()
        sys.stdout = sys.__stdout__
        self.assertTrue(expected_messsage in capturedOutput.getvalue())
    
    def test_goodbye(self):
        ui = UserInterface()
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        expected_messsage = """
        Obrigado por usar Alexandria!
        """
        ui.goodbye()
        sys.stdout = sys.__stdout__
        self.assertTrue(expected_messsage in capturedOutput.getvalue())

if __name__ == '__main__':
    unittest.main()