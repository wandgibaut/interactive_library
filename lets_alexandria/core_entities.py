import datetime
from ast import literal_eval

class Article:
    def __init__(self, title='', tag='', date : datetime = None, text='', filepath=None):
        
        #self.id = uuid.uuid4()
        self.title = title
        self.tag = tag
        
        if filepath is not None:
            with open(filepath, 'r') as file:
                self.text = file.read()       
        else:
            self.text = text 
                
        
        if date is None:
            self.date = datetime.datetime.now().date()
        else:
            try:
                self.date = datetime.datetime.strptime(date, '%d/%m/%Y').date()
            except:
                self.date = datetime.datetime.now().date()
        
    def __str__(self):
        answer ={
            'Title': self.title, 
            'Tag': self.tag, 
            'Date': self.date.strftime("%d/%m/%Y"), 
            'Text': self.text}
        return str(answer)


    def __repr__(self):
        answer ={
            'Title': self.title, 
            'Tag': self.tag, 
            'Date': self.date.strftime("%d/%m/%Y"), 
            'Text': self.text}
        return str(answer)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Article):
            if self.title == o.title and self.tag == o.tag and self.date == o.date and self.text == o.text:
                return True
        return False

    def set_text(self, text):
        self.text = text
    
    def set_title(self, title):
        self.title = title
    
    def set_tag(self, tag):
        self.tag = tag
    
    def set_date(self, date):
        self.date = datetime.strptime(date, '%d/%m/%y').date()
    
    def get_title(self):
        return self.title

    def get_tag(self):
        return self.tag
    
    def get_date(self):
        return self.date
    
    def get_text(self):
        return self.text

    def get_all(self):
        return self.title, self.tag, self.date, self.text
    
    def calculate_similarity(self, article):
        answer = 0
        f_set = set(self.text.split(' '))
        s_set = set(article.text.split(' '))

        for word in f_set:
            if word in s_set:
                answer += 1
        return float("{:.4f}". format(answer/len(f_set.union(s_set))))


class Library:
    def __init__(self, name, articles=None):
        self.name = name
        self.articles = articles or []

    def add_article(self, article):
        self.articles.append(article)

    def remove_article_by_name(self, name):
        for article in self.articles:
            if article.get_title() == name:
                self.articles.remove(article)
                return True
        return False
    
    def remove_article(self, article):
        self.articles.remove(article)
    
    def __str__(self):
        answer = {'Library': self.name, 'Articles': self.articles}
        return str(answer)
    
    def __repr__(self):
        answer = {'Library': self.name, 'Articles': self.articles}
        return str(answer)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Library):
            if self.name == o.name and self.articles == o.articles:
                return True
        return False

    def get_articles(self):
        return self.articles
    
    def get_name(self):
        return self.name
    
    def get_article_by_name(self, name):
        for article in self.articles:
            if article.get_title() == name:
                return article
        return None

    def get_articles_by_tag(self, tag):
        answer = []
        for article in self.articles:
            if tag == article.get_tag():
                answer.append(article)
        return answer

    def get_articles_by_date(self, date):
        answer = []
        for article in self.articles:
            if article.get_date() >= date:
                answer.append(article)
        return answer

    # gives the most recent articles first
    def get_articles_sorted(self):
        self.articles.sort(key=lambda x: x.get_date())
        return self.articles[::-1]
        
    def load(self, file_name):
        with open(file_name, 'r') as file:
            proto_library = literal_eval(file.read())
            try:
                self.name = proto_library['Library']
                self.articles = []
                for article in proto_library['Articles']:
                    self.articles.append(Article(article['Title'], article['Tag'], article['Date'], article['Text']))
            except:
                print('Error loading Library!')
            
    def set_name(self, name):
        self.name = name

    def save(self, filepath):
        with open(filepath, 'w') as file:
            file.write(self.__repr__())
    
    def calculate_similarities(self, article):
        answer = []
        for a in self.articles:
            answer.append(a.calculate_similarity(article))
        return answer

    def calculate_all_similarities (self):
        answer = []
        for a in self.articles:
            answer.append(self.calculate_similarities(a))
        return answer

    
    def get_greatest_similarity(self, article):
        answer = []
        temp_articles = self.articles.copy()
        temp_articles.sort(key=lambda x: x.calculate_similarity(article))
        return self.articles.index(temp_articles[-2]), temp_articles[-2].calculate_similarity(article)


    def get_article_by_greatest_similarity(self, article):
        return self.articles[self.get_greatest_similarity(article)[0]]
