import pandas as pd
from database import engine

def check_db():
    print("🔎 Vérification du contenu de la table 'water_forecasts'...")
    try:
        # On lit les 10 dernières prévisions enregistrées
        df = pd.read_sql("SELECT * FROM water_forecasts ORDER BY created_at DESC LIMIT 10;", engine)
        if df.empty:
            print("❌ La table est vide.")
        else:
            print(f"✅ Il y a {len(df)} nouvelles prévisions trouvées !")
            print(df[['time', 'sensor_id', 'predicted_humidity', 'model_used']])
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    check_db()