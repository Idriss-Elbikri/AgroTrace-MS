import psycopg2

def init_sig():
    try:
        # Connexion au nouveau port 5435
        conn = psycopg2.connect(
            host="127.0.0.1", port="5435",
            database="agro_business", user="postgres", password="adminpassword"
        )
        cur = conn.cursor()

        # 1. Activation de l'extension PostGIS (indispensable pour les cartes)
        cur.execute("CREATE EXTENSION IF NOT EXISTS postgis;")

        # 2. Création de la table parcelles
        cur.execute("""
            CREATE TABLE IF NOT EXISTS parcelles (
                id SERIAL PRIMARY KEY,
                nom VARCHAR(100),
                culture VARCHAR(50),
                surface FLOAT,
                geom GEOMETRY(Polygon, 4326)
            );
        """)

        # 3. Insertion des deux parcelles (Casablanca)
        # Note: On utilise ST_GeomFromText pour les coordonnées GPS
        cur.execute("""
            INSERT INTO parcelles (id, nom, culture, surface, geom)
            VALUES 
            (1, 'Parcelle Nord', 'Blé', 5.2, ST_GeomFromText('POLYGON((-7.61 33.58, -7.60 33.58, -7.60 33.57, -7.61 33.57, -7.61 33.58))', 4326)),
            (2, 'Parcelle Sud', 'Maïs', 8.4, ST_GeomFromText('POLYGON((-7.62 33.57, -7.61 33.57, -7.61 33.56, -7.62 33.56, -7.62 33.57))', 4326))
            ON CONFLICT (id) DO NOTHING;
        """)

        conn.commit()
        print("✅ Parcelles SIG créées avec succès !")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Erreur SIG : {e}")

if __name__ == "__main__":
    init_sig()