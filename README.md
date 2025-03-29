# Shoop-machine-learning
Online store using text classification to evaluate customer opinions

## Description
Shoop is a web application that simulates an e-commerce platform with all its core functionalities, such as browsing products, adding items to the cart, placing orders, simulating payments, leaving product reviews, creating accounts, and logging in.<br><br>
What makes Shoop different from other e-commerce platforms?<br>It features a custom classification model that analyzes user reviews and assigns one of three sentiment ratings: positive, neutral, or negative making process of adding comment automatized. The classification model is specifically designed for the Polish language and achieves 85% accuracy on the test dataset.

## Features
- User account registration
- Account activation via email confirmation
- User login system
- Product search
- Placing orders
- Viewing user orders
- Posting comments
- Admin functionalities: changing user roles, adding products to the store, viewing existing orders

## Technologies
- Python 3.12.5 – main programming language
- Flask - web framework for backend development
- MySQL, ORM SQLAlchemy - database management and ORM for handling data models
- spacy, scikit-learn - machine learning libraries for text classification and sentiment analysis

## Instalation
You need technologies listed below:
- Xampp - server Apache and MySQL
- Visual Studio Code - programing enviroment
- Python 3.12.5 or newer - to launch application and dependies
  <br><br>
1. Download xampp and create new database called: shoopdb
2. Clone repo: https://github.com/bartoszstec/Shoop-machine-learning/tree/automatic
3. Open VSC then open powershell and create new virtual enviroment by typing: python -m venv venv
4. Activate virtual enviroment (\venv\Scripts\activate) and install needed packages (pip install -r requirements.txt)
   ```bash
6. Create .env file in main directory and add configuration:
FLASK_DEBUG=1
FLASK_APP=app.py
DATABASE_URL=mysql+pymysql://root:@localhost/shoopdb?charset=utf8mb4
SECRET_KEY=sekretnyklucz0192409218
MAIL_USERNAME=your_gmail
MAIL_PASSWORD=your_password
ATTENTION: You have to have created account on gmail SMTP to use this application

## Użycie
1. Zarejestruj nowe konto
2. Dodaj zadanie
...
