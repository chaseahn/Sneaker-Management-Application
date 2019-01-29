import sqlite3

def run(dbname='shoebox.db'):

    CON = sqlite3.connect(dbname)
    CUR = CON.cursor()

    CUR.execute("""DROP TABLE IF EXISTS user;""")
    # create USER table FOR LOGIN AND SESSION
    CUR.execute("""CREATE TABLE user(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR,
        password VARCHAR,
        age INTEGER,
        gender VARCHAR,
        CONSTRAINT unique_username UNIQUE(username)
    );""")

    CUR.execute("""DROP TABLE IF EXISTS shoes_viewed;""")
    #Everytime a shoe is clicked, count increases by 1
    #FOR whats trending
    CUR.execute("""CREATE TABLE shoes_viewed(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        shoename VARCHAR,
        click_count INTEGER
    );""")

    CUR.execute("""DROP TABLE IF EXISTS shoes_recommended;""")
    #Everytime a shoe is clicked, count increases by 1
    #FOR whats trending
    CUR.execute("""CREATE TABLE shoes_recommended(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        shoename VARCHAR,
        result VARCHAR,
        user_pk INTEGER,
        FOREIGN KEY(user_pk) REFERENCES user(pk)
    );""")

    CUR.execute("""DROP TABLE IF EXISTS user_preferences;""")
    #stores information about what the user likes
    #UPDATES IF USER CHANGES PREFERENCES
    CUR.execute("""CREATE TABLE user_preferences(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        brand VARCHAR,
        color VARCHAR,
        user_pk INTEGER,
        FOREIGN KEY(user_pk) REFERENCES user(pk)
    );""")

    CUR.execute("""DROP TABLE IF EXISTS user_favorites;""")
    #user wish list of favorited shoes
    #when you like it, the shoe name is saved to your pk
    CUR.execute("""CREATE TABLE user_favorites(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        shoename VARCHAR,
        user_pk INTEGER,
        FOREIGN KEY(user_pk) REFERENCES user(pk)
    );""")

    CUR.execute("""DROP TABLE IF EXISTS search_terms;""")
    #search term history
    CUR.execute("""CREATE TABLE search_terms(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        search_terms VARCHAR,
        time INTEGER,
        user_pk INTEGER,
        FOREIGN KEY(user_pk) REFERENCES user(pk)
    );""")

    CUR.execute("""DROP TABLE IF EXISTS shoebox;""")
    #search term history
    CUR.execute("""CREATE TABLE shoebox(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        shoename VARCHAR,
        type VARCHAR,
        date INTEGER,
        price_bought VARCHAR,
        price_sold VARCHAR,
        user_pk INTEGER,
        FOREIGN KEY(user_pk) REFERENCES user(pk)
    );""")

    CON.commit()
    CUR.close()
    CON.close()

if __name__ == '__main__':
    run()