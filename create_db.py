import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    try:
        # Connexion au système postgres par défaut
        conn = psycopg2.connect(host="127.0.0.1", port="5435", user="postgres", password="adminpassword")
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        # Création de la base de données
        cur.execute("CREATE DATABASE agro_business")
        print("✅ Base 'agro_business' créée !")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Info: {e} (La base existe peut-être déjà)")

if __name__ == "__main__":
    create_database()