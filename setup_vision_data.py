import psycopg2
import time

def setup_vision():
    # On attend 5 secondes pour être sûr que Postgres a fini d'initialiser les fichiers
    print("⏳ Attente de l'initialisation de la base de données...")
    time.sleep(5)
    
    try:
        # ON REVIENT SUR 'admin' car c'est ce qui est écrit dans votre docker-compose.yml
        # Modifiez uniquement ces lignes dans setup_vision_data.py
        conn = psycopg2.connect(
            host="127.0.0.1", 
            port="5435", # <--- LE NOUVEAU PORT
            database="agro_business",
            user="postgres", 
            password="adminpassword"
        )
        cur = conn.cursor()
        print("🔗 Connexion réussie !")

        cur.execute("""
            CREATE TABLE IF NOT EXISTS vision_results (
                id SERIAL PRIMARY KEY,
                parcelle_id INTEGER UNIQUE,
                sante_vegetale INTEGER,
                ndvi FLOAT,
                derniere_analyse TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        data = [(1, 88, 0.75), (2, 65, 0.42)]

        for p_id, sante, ndvi in data:
            cur.execute("""
                INSERT INTO vision_results (parcelle_id, sante_vegetale, ndvi)
                VALUES (%s, %s, %s)
                ON CONFLICT (parcelle_id) DO UPDATE 
                SET sante_vegetale = EXCLUDED.sante_vegetale, ndvi = EXCLUDED.ndvi
            """, (p_id, sante, ndvi))

        conn.commit()
        print("✅ Données de Vision UAV injectées avec succès !")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    setup_vision()