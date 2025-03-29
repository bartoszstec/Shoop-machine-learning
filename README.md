# Shoop-machine-learning
Online store using text classification to evaluate customer opinions

## Description
Shoop is a web application that simulates an e-commerce platform with all its core functionalities, such as browsing products, adding items to the cart, placing orders, simulating payments, leaving product reviews, creating accounts, and logging in.<br><br>
What makes Shoop different from other e-commerce platforms?<br>It features a custom classification model that analyzes user reviews and assigns one of three sentiment ratings: positive, neutral, or negative making process of adding comment automatized. The classification model is specifically designed for the **Polish language** and achieves **85% accuracy** on the test dataset.

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
### Required Technologies:
- Xampp - server Apache and MySQL
- Visual Studio Code - programming enviroment
- Python 3.12.5 or newer - to run the application and dependencies
  <br><br>
### Steps to Install:
1. Download xampp, then create new database named: `shoopdb`.
2. Clone repository:
   ```bash
   git clone https://github.com/bartoszstec/Shoop-machine-learning/tree/automatic
3. Open Visual Studio Code, then open PowerShell and create a new virtual enviroment:
   ```bash
   python -m venv venv
4. Activate virtual enviroment and install needed packages:
   ```bash
   venv\Scripts\activate  # On Windows  
   source venv/bin/activate  # On macOS/Linux  
   pip install -r requirements.txt
6. Create `.env` file in main directory and add configuration:
   ```env
   FLASK_DEBUG=1
   FLASK_APP=app.py
   DATABASE_URL=mysql+pymysql://root:@localhost/shoopdb?charset=utf8mb4
   SECRET_KEY=your_secret_key
   MAIL_USERNAME=your_gmail
   MAIL_PASSWORD=your_password
⚠️ Important: You need a Gmail SMTP account to use this application.

7. After configurating enviroment you have to create tables in database:
   ```bash
   python create_tables.py
## Run application
To run app activate virtual enviroment and type:
   ```bash
   python app.py
