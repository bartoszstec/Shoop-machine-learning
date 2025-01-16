import pandas as pd
from sklearn.model_selection import train_test_split
import os
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
import joblib

# Załaduj model językowy dla polskiego
nlp = spacy.load("pl_core_news_sm")

# Funkcja do lematyzacji
def lematyzuj_tekst(tekst):
    dokument = nlp(tekst)
    return " ".join([token.lemma_ for token in dokument if not token.is_punct and not token.is_space])

# Wczytanie danych z pliku CSV
file_path = "Dane_startowe_deduplicated.csv"  # Ścieżka do Twojego pliku CSV
df = pd.read_csv(file_path)


# Weryfikacja kolumn
required_columns = {'id', 'kategoria', 'produkt', 'opinia', 'liczba gwiazdek', 'klasyfikacja opinii'}
if not required_columns.issubset(df.columns):
    raise ValueError(f"Plik CSV musi zawierać kolumny: {required_columns}")

# Cechy wejściowe (X)
X = df[['kategoria', 'produkt', 'opinia',]]

# Cele predykcji (y)
y_class = df['klasyfikacja opinii']

# Ścieżki do plików z podziałem danych
x_train_path = "X_train.csv"
x_test_path = "X_test.csv"
y_train_path = "y_train.csv"
y_test_path = "y_test.csv"

# Sprawdzenie, czy pliki z podziałem istnieją
if os.path.exists(x_train_path) and os.path.exists(x_test_path) and os.path.exists(y_train_path) and os.path.exists(y_test_path):
    # Wczytanie istniejącego podziału
    print("Wczytywanie istniejącego podziału...")
    X_train = pd.read_csv(x_train_path)
    X_test = pd.read_csv(x_test_path)
    y_train = pd.read_csv(y_train_path)
    y_test = pd.read_csv(y_test_path)
else:
    #(pierwsze uruchomienie)
    print("Tworzenie nowego podziału danych...")

    #Podział danych na testowe i treningowe
    X_train, X_test,y_train, y_test = train_test_split(
        X, y_class, test_size=0.2, random_state=42
    )


    # Zapis podziału do plików
    X_train.to_csv(x_train_path, index=False)
    X_test.to_csv(x_test_path, index=False)
    y_train.to_csv(y_train_path, index=False)
    y_test.to_csv(y_test_path, index=False)
    print("Podział został zapisany do plików CSV.")

# Przetwarzanie kolumny 'opinia'
X_train["opinia"] = X_train["opinia"].apply(lematyzuj_tekst)
X_test["opinia"] = X_test["opinia"].apply(lematyzuj_tekst)

# Wektoryzacja
X_train["łączone_cechy"] = X_train["kategoria"] + " " + X_train["produkt"] + " " + X_train["opinia"]
X_test["łączone_cechy"] = X_test["kategoria"] + " " + X_test["produkt"] + " " + X_test["opinia"]

tfidf = TfidfVectorizer(max_features=10000)

X_train_tfidf = tfidf.fit_transform(X_train["łączone_cechy"])
X_test_tfidf = tfidf.transform(X_test["łączone_cechy"])


# Inicjalizacja modelu RandomForestClassifier
model = RandomForestClassifier(random_state=42, n_estimators=200, max_depth=None, min_samples_split=5, min_samples_leaf=1, n_jobs=-1)

# Trenowanie modelu na danych treningowych
model.fit(X_train_tfidf, y_train.values.ravel())  # .ravel() konwertuje na wektor

# Predykcja na danych testowych
rf_predictions = model.predict(X_test_tfidf)

# Ocena modelu
print("Macierz konfuzji:")
print(confusion_matrix(y_test, rf_predictions))

print("\nRaport klasyfikacji:")
print(classification_report(y_test, rf_predictions))

# param_grid = {
#     'n_estimators': [100, 200, 300],
#     'max_depth': [10, 20, None],
#     'min_samples_split': [2, 5, 10],
#     'min_samples_leaf': [1, 2, 4],
# }
# grid_search = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=3, scoring='f1_macro')
# grid_search.fit(X_train_tfidf, y_train.values.ravel())
# print("Najlepsze parametry:", grid_search.best_params_)

# Zapis modelu i wektoryzatora
joblib.dump(model, "rf_classifier.pkl")
joblib.dump(tfidf, "tfidf_vectorizer.pkl")
print("Model i wektoryzator zostały zapisane.")