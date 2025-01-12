import joblib
import spacy


nlp = spacy.load("pl_core_news_sm")

def lematyzuj_tekst(tekst):
    dokument = nlp(tekst)
    return " ".join([token.lemma_ for token in dokument if not token.is_punct and not token.is_space])

# Wczytanie modelu i wektoryzatora
model = joblib.load("rf_classifier.pkl")
tfidf = joblib.load("tfidf_vectorizer.pkl")

# Przetwarzanie nowej opinii
nowa_opinia = "OK, nie powalająca"
nowa_opinia_przetworzona = lematyzuj_tekst(nowa_opinia)
nowa_opinia_cechy = "AGD lodówka " + nowa_opinia_przetworzona
nowa_opinia_tfidf = tfidf.transform([nowa_opinia_cechy])

# Predykcja klasy
predykcja_klasy = model.predict(nowa_opinia_tfidf)
print(f"Przewidywana klasyfikacja: {predykcja_klasy[0]}")

# Głosy z poszczególnych drzew
głosy_drzew = [estimator.predict(nowa_opinia_tfidf)[0] for estimator in model.estimators_]
print("Głosy z poszczególnych drzew decyzyjnych:")
print(głosy_drzew)