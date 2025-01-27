from flask import Flask
from extensions import db
from models import Comment, Person, Product, Order, Category
from werkzeug.security import generate_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/shoopdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    print("Tabele zostały utworzone!")

    # **Dodawanie użytkowników**
    if not Person.query.filter_by(email="user@email.com").first():
        user = Person(
            login="user",
            email="user@email.com",
            password=generate_password_hash("user", method="scrypt"),
            role="user"
        )
        user.activated=True
        db.session.add(user)

    if not Person.query.filter_by(email="admin@email.com").first():
        admin = Person(
            login="admin",
            email="admin@email.com",
            password=generate_password_hash("admin", method="scrypt"),
            role="admin"
        )
        admin.activated=True
        db.session.add(admin)

    # **Dodawanie kategorii**
    categories = [
        (1, "AGD"),
        (2, "RTV"),
        (3, "Telefony"),
        (4, "Odzież"),
        (5, "Sport"),
        (6, "Zegarki i biżuteria")
    ]

    for cat_id, cat_name in categories:
        if not Category.query.filter_by(id=cat_id).first():
            db.session.add(Category(id=cat_id, category_name=cat_name))

    # **Dodawanie produktów**
    products = [
        (7, "Lodówka", 1, "<b>Nazwa marki:</b> IKEA<br><b>Klasa efektywności energetycznej:</b> E<br><b>Roczne zużycie energii:</b> 244 kWh/rocznie<br><b>Suma objętości komory zamrażalnika:</b> 120 L<br><b>Suma objętości komory chłodzących:</b> 223 L<br><b>Liczba gwiazdek dla zamrażarki:</b> 4<br><b>Klasa klimatyczna:</b> -<br><b>Poziom emisji hałasu:</b> 38 dB", 141, 1000, "/static/images/produkty/lodówka.jpg"),
        (9, "Żelazko", 1, "<b>Nazwa marki:</b> Philips<br><b>Rodzaj stopy:</b> SteamGlide Plus<br><b>Moc [W]:</b> 3000<br><b>Wytwarzanie pary [g/min]:</b> 65<br><b>Dodatkowe uderzenie pary [g/min]:</b> 250<br><b>Funkcje:</b> Regulacja strumienia pary, Pionowy wyrzut pary, Blokada kapania, Automatyczne wyłączenie żelazka, System antywapienny, Funkcja samooczyszczenia, Automatyczny dobór temperatury", 91, 449.99, "/static/images/produkty/żelazko.jpg"),
        (10, "Odkurzacz", 1, "<b>Poziom hałasu [dB]:</b> 57<br><b>Moc maksymalna [W]:</b> 500<br><b>Moc nominalna [W]:</b> 500<br><b>Typ filtra:</b> Antyalergiczny<br><b>Zbieranie kurzu:</b> Worek<br><b>Pojemność pojemnika/worka [l]:</b> 3.5<br><b>Zasięg pracy [m]:</b> 12<br><b>Funkcje:</b> Regulacja mocy ssania, Zwijacz przewodu", 138, 999.99, "/static/images/produkty/odkurzacz.jpg"),
        (11, "Telewizor", 2, "<b>Nazwa marki:</b> Samsung<br><b>Przekątna ekranu:</b> 48\"<br><b>Rozdzielczość:</b> UHD 4K 3840 x 2160<br><b>Częstotliwość odświeżania:</b> 144 Hz<br><b>HDR:</b> Tak<br><b>Standard HDR:</b> HDR10<br><b>Ambilight:</b> Nie<br><b>Funkcje smart:</b> Współpraca z asystentem głosowym Alexa, Współpraca z asystentem głosowym Google<br><b>Aplikacje:</b> Amazon Prime Video, Netflix, YouTube, Disney+<br><b>Wbudowany tuner:</b> DVB-S (cyfrowy satelitarny), DVB-S2 (cyfrowy satelitarny), DVB-T (cyfrowy naziemny), DVB-T2 (cyfrowy naziemny), DVB-C (cyfrowy kablowy)<br><b>Łączność bezprzewodowa:</b> Wi-Fi 5 (802.11ac), Bluetooth 5.2<br><b>Liczba złączy HDMI:</b> 4 szt.<br><b>Złącze HDMI 2.1:</b> Tak<br><b>Liczba złączy USB:</b> 2 szt.<br><b>Złącze CI:</b> Tak<br><b>Pozostałe złącza:</b> Wejście antenowe, Wejście Ethernet RJ 45 (LAN)<br><b>Moc głośników:</b> 2 x 20 W<br><b>Kolor obudowy:</b> Czarny<br><b>Klasa energetyczna:</b> G<br><b>Średni pobór mocy:</b> 66 W<br><b>Pobór mocy (tryb czuwania):</b> 0,5 W<br><b>Standard VESA:</b> 300 x 200 mm", 50, 4399.99, "/static/images/produkty/telewizor.jpg"),
        (12, "Słuchawki", 2, "<b>Nazwa marki:</b> Sony<br><b>Typ słuchawek:</b> Nauszne<br><b>Przeznaczenie:</b> Do podróży<br><b>Transmisja bezprzewodowa:</b> Bluetooth<br><b>Pasmo przenoszenia min. [Hz]:</b> 4<br><b>Pasmo przenoszenia max. [Hz]:</b> 40000<br><b>Aktywna redukcja szumów (ANC):</b> Tak<br><b>Funkcje dodatkowe:</b> Google Assistant, Zasięg: 10 m<br><b>Kolor:</b> Czarny", 99, 999.99, "/static/images/produkty/słuchawki.jpg"),
        (14, "Nawigacja samochodowa", 2, "<b>Wyświetlacz [cale]:</b> 7<br><b>Wydawca mapy:</b> Navitel<br><b>Aktualizacja map:</b> Dożywotnia<br><b>Profile tras:</b> Dla samochodów osobowych<br><b>Zainstalowane mapy:</b> Albania, Andora, Austria, Belgia, Białoruś, Bośnia i Hercegowina, Bułgaria, Chorwacja, Cypr, Czarnogóra, Czechy, Dania, Estonia, Finlandia, Francja, Gibraltar, Grecja, Hiszpania, Holandia, Islandia, Kazachstan, Lichtenstein, Litwa, Łotwa, Luksemburg, Macedonia, Malta, Mołdawia, Monako, Niemcy, Norwegia, Polska, Portugalia, Rosja, Rumunia, San Marino, Serbia, Słowacja, Słowenia, Szwajcaria, Szwecja, Ukraina, Watykan, Węgry, Wielka Brytania, Włochy, Wyspa Man <b>Czytnik kart pamięci:</b> Tak<br><b>Wbudowana pamięć [GB]:</b> 8<br><b>Bluetooth:</b> Nie", 89, 399.99, "/static/images/produkty/nawigacja_samochodowa.jpg"),
        (15, "Smartfon MOTOROLA Edge 50 Neo", 3, "<b>Wyświetlacz:</b> 6.4\", 2670 x 1220px, P-OLED<br><b>Pamięć wbudowana [GB]:</b> 512<br><b>Pamięć RAM:</b> 12 GB<br><b>Aparat:</b> Tylny 50 Mpx + 13 Mpx + 10 Mpx, Przedni 32 Mpx<br><b>Model procesora:</b> MediaTek Dimensity 7300<br><b>Liczba rdzeni procesora:</b> Ośmiordzeniowy<br><b>System operacyjny:</b> Android<br><b>Wersja systemu:</b> Android 14<br><b>Pojemność akumulatora [mAh]:</b> 4310<br><b>NFC:</b> Tak<br><b>5G:</b> Tak<br><b>Kolor obudowy:</b> Granatowy", 95, 1899.99, "/static/images/produkty/smartphone_motorola.jpg"),
        (16, "Telefon NOKIA 230", 3, "<b>Wyświetlacz:</b> 2.8\", 320 x 240px, TFT<br><b>Pamięć wbudowana [GB]:</b> 0.16<br><b>Pamięć RAM:</b> 8 MB<br><b>Aparat:</b> Tylny 2 Mpx, Przedni 2 Mpx<br><b>Model procesora:</b> Spreadtrum SC6531F<br><b>Liczba rdzeni procesora:</b> Jednordzeniowy<br><b>System operacyjny:</b> Nokia OS<br><b>Wersja systemu:</b> Producenta<br><b>Pojemność akumulatora [mAh]:</b> 1450<br><b>NFC:</b> Nie<br><b>5G:</b> Nie<br><b>Kolor obudowy:</b> Czarny", 98, 349.99, "/static/images/produkty/nokia230.jpg"),
        (17, "Torebka", 4, "<b>Marka:</b> Kazar<br><b>Materiał:</b> Skóra naturalna<br><b>Kolor:</b> Czarny<br><b>Kolor metali:</b> Srebrny<br><b>Zapięcie:</b> Zawiasowe<br><b>Długość:</b> 26 cm<br><b>Wysokość:</b> 22 cm<br><b>Szerokość:</b> 10 cm<br><b>Wysokość uchwytu:</b> 8 cm<br><b>Minimalna długość paska:</b> 74 cm<br><b>Maksymalna długość paska:</b> 142 cm", 150, 849.99, "/static/images/produkty/torebka.jpg"),
        (18, "Klapki", 4, "<b>Materiał zewnętrzny:</b> Zamsz<br><b>Materiał wewnętrzny:</b> Materiał<br><b>Wyściółka:</b> Skóra<br><b>Podeszwa:</b> Tworzywo sztuczne<br><b>Rodzaj ocieplenia:</b> Bez ocieplenia<br><b>Wskazówki pielęgnacyjne:</b> Przed pierwszym użyciem zalecamy zaimpregnowanie<br><b>Nosek buta:</b> Okrągły<br><b>Kształt obcasa:</b> Płaski<br><b>Zapięcie:</b> Brak<br><b>Wzór:</b> Kolor jednolity<br><b>Wysokość obcasa:</b> Bez obcasa<br><b>materiał zewnętrzny:</b> 100% Skóra zatwierdzona przez Leather Working Group (LWG)", 70, 150, "/static/images/produkty/klapki.jpg"),
        (19, "Bluza", 4, "<b>Producent:</b> QueQuality<br><b>Bawełna:</b><br>- wysokiej jakości, zrobiona na specjalne zamówienie<br>- poddana postprocesom uszlachetniającym i wydłużającym żywotność jak enzymowanie, sylikonowanie, stabilizacja- apretura antypilingowa (zapobiega „kulkowaniu się\")<br>- wysoka gramatura (ponad 350g), jednak odpowiednio wygładzona, aby zapewnić lekkość<br><br><b>Detale:</b><br>- bawełniane sznurki zakończone agletem ze stali chirurgicznej, nierdzewnej, robione na specjalne zamówienie<br>- zakończenia przy kapturze - haftowane<br>- dodatkowo wzmocnione ściągacze<br>", 16, 250, "/static/images/produkty/bluza.jpg"),
        (20, "Białko WPC 80", 5, "<b>KFD Regular WPC 80 Instant</b> to produkt, w którym głównym składnikiem jest w 100% czysty koncentrat białka serwatkowego. Produkt charakteryzuje się dobrą rozpuszczalnością (ale nieco słabszą niż wersja Premium) i delikatnym smakiem.<br>Surowiec został stworzony przy wykorzystaniu procesu ultrafiltracji, co pozwala na otrzymanie produktu wyróżniającego się niską zawartością tłuszczów i cukrów.<br>Produkt powstał z myślą o osobach, dla których nie smak a wysoka zawartość prawdziwego białka - bez zbędnych, w opinii wielu klientów, dodatków (np. zagęstników czy barwników) jest najważniejsza.<br><b>KFD Regular WPC 80</b> nie posiada enzymów trawiennych, które, przyjmowane przede wszystkim w produktach amerykańskich, służą często jako element maskujący niskiej jakości surowiec.", 25, 499.99, "/static/images/produkty/białko.jpg"),
        (21, "Rakieta do squash", 5, "<b>Model:</b> Wilson Hyper Hammer 120<br><b>Waga ramy [g]:</b> 120<br><b>Waga real [g]:</b> 146<br><b>Pokrowiec:</b> główka<br><b>Wyważenie:</b> główka<br><b>Główka [cm2]:</b> 498<br><b>Materiał:</b> grafit", 5, 409.99, "/static/images/produkty/rakieta_squash.jpg"),
        (22, "Rower magnetyczny", 5, "<b>Model:</b> Zipro One S<br><b>Maksymalna waga użytkownika:</b> 110 kg<br><b>Wymiary rowerka:</b>wymiary (dł. x szer. x wys.): 89 x 43,5 x 110 cm<br><b>waga:</b> 16,5 kg<br><b>wymiary transportowe:</b> 59 x 25,5 x 47 cm<br><b>waga brutto:</b> 18,5 kg<br><br><b>System oporu:</b> magnetyczny system oporu<br>waga systemu napędowego: 4,5 kg<br>regulacja: manualna<br>ilość poziomów obciążenia: 8<br><br><b>Komputer</b><br>• Wyświetlacz LCD<br>• Mierzone parametry:<br>• czas<br>• prędkość<br>• dystans<br>• całkowity dystans (ODO)<br>• kalorie<br>• puls<br><br><b>Funkcje:</b><br>• SCAN - cykliczne wyświetlanie parametrów treningu<br>• odliczanie ustawionej wartości (czasu, dystansu, ilość kalorii)<br>• ostrzeżenie o przekroczeniu ustawionej wartości pulsu (z alarmem)<br>• Pulse Rate<br>• oszczędzanie energii - wyłączenie po 4 minutach bezczynności", 8, 359.99, "/static/images/produkty/rower_magnetyczny.jpg"),
        (23, "Zegarek Rolex Datejust", 6, "Zegarek Rolex Datejust 41mm Iced Out, został w całości wysadzony naturalnymi diamentami, które nadają mu niezwykłego blasku i podnoszą jego wartość.<br><br>Ten zegarek jest definicją życiowego sukcesu. Zainwestuj w Swój wizerunek i wybierz zegarek, który sprawi, że każdy Twój ruch będzie pełen luksusu!<br><br>Autentyczność została potwierdzona certyfikatem. Zegarek jest nowy, a data produkcji to 2023 rok.<br><br><b>Mechanizm:</b> automatyczny, cal. Rolex 3235, 31 kamieni łożyskujących, 70h rezerwy chodu<br><b>Obudowa:</b> 1 mm, koperta i bezel w całości wysadzone diamentami, szafirowe szkiełko, tarcza zdobiona diamentami<br><b>Wodoszczelność:</b> 10 ATM<br><b>Wymiary:</b> 2,8 cm x 4,4 cm<br><b>Bransoleta:</b> Jubilee, również wysadzana diamentami<br><b>Rok produkcji:</b> 2023<br><b>Płeć:</b> zegarek męski/unisex<br><b>Zawartość:</b> certyfikat, oryginalne pudełko, komplet dokumentów, zegarek", 6, 26500, "/static/images/produkty/zegarek.jpg"),
        (24, "Naszyjnik", 6, "Długość 42 cm, cztery przedłużki do 47 cm, wymiary el ozdobnego: długość do 2,1 cm, szerokość do 2,2<br>Srebrny naszyjnik z kolekcji Kwiaty Nocy to idealny wybór dla miłośniczek kolorowych dodatków pełnych finezji. Zawieszony na delikatnym łańcuszku element w kształcie serca zdobi ruchoma zawieszka z motywem kwiatu bzu. Białe i fioletowe cyrkonie, wprawione w obręcz serca harmonijnie współgrają z odcieniami fioletowego bzu. Ręcznie nakładana emalia i blask rodowanego srebra tworzą wyjątkową biżuterię, o symbolicznym wymiarze.Inspirowana pięknem kwitnącego krzewu fioletowego bzu, kolekcja Kwiaty Nocy zachwyca świeżością barw i finezją wzorów. Symbolizujące wiosnę fioletowe kwiaty bzu wniosą powiew świeżości do kreacji utrzymanych w różnych stylach.", 24, 139.99, "/static/images/produkty/naszyjnik.jpg"),
        (25, "Bransoletka", 6, "<b>Kategoria:</b> Bransoletki<br><b>Marka:</b> Apart<br><b>Kolekcja:</b> Simple<br><b>Surowiec:</b> Srebro rodowane<br><b>Próba:</b> 925<br><b>Długość elementu dekoracyjnego:</b> 8 mm<br><b>Szerokość elementu dekoracyjnego:</b> 3,5 mm<br><b>Przedłużka:</b> 35 mm", 69, 234, "/static/images/produkty/bransoletka.jpg"),
    ]

    for prod_id, name, cat_id, desc, qty, price, img_url in products:
        if not Product.query.filter_by(id=prod_id).first():
            db.session.add(Product(
                id=prod_id,
                name=name,
                category_id=cat_id,
                description=desc,
                quantity=qty,
                price=price,
                image_url=img_url,
                date_added=datetime.now()
            ))

    # **Zapis zmian w bazie**
    db.session.commit()
    print("Użytkownicy, kategorie i produkty zostały dodane do bazy!")