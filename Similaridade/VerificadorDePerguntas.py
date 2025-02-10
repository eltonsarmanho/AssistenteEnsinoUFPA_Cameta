import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Classe para verificar perguntas similares no dataset
class VerificadorDePerguntas:
    def __init__(self, df: pd.DataFrame, threshold=0.75):
        self.df = df
        self.threshold = threshold
        self.vectorizer = TfidfVectorizer()

    def verificar_similaridade(self, pergunta):
        # Verificar se o DataFrame está vazio
        if self.df.empty:
            return None, None

        # Vetorizar as perguntas no dataset e a nova pergunta
        tfidf = self.vectorizer.fit_transform(self.df['Pergunta'].tolist() + [pergunta])
        # Calcular a similaridade de cosseno
        cosine_similarities = cosine_similarity(tfidf[-1], tfidf[:-1]).flatten()

        # Encontre o índice da pergunta mais similar, se a similaridade for maior que o threshold
        idx_similar = cosine_similarities.argmax()
        similaridade_max = cosine_similarities[idx_similar]

        # Se a similaridade for maior que o threshold, retornar a pergunta e a resposta associada
        if similaridade_max > self.threshold:
            pergunta_similar = self.df.iloc[idx_similar]['Pergunta']
            resposta_similar = self.df.iloc[idx_similar]['Resposta']
            return pergunta_similar, resposta_similar

        return None, None


