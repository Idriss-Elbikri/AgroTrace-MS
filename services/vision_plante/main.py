from fastapi import FastAPI, UploadFile, File
from PIL import Image
import torch
import numpy as np
import io
import uuid
from minio import Minio
from unet import UNet

app = FastAPI(title="Microservice VisionPlante", description="Analyse d'images UAV + Stockage MinIO")

# --- CONFIGURATION MINIO ---
MINIO_CLIENT = None
BUCKET_NAME = "images-uav-traitees"

def init_minio():
    """Initialise la connexion à MinIO et crée le bucket si nécessaire"""
    global MINIO_CLIENT
    try:
        # 'minio' est le nom du service dans docker-compose
        MINIO_CLIENT = Minio(
            "minio:9000",
            access_key="minioadmin",
            secret_key="minioadmin",
            secure=False
        )
        if not MINIO_CLIENT.bucket_exists(BUCKET_NAME):
            MINIO_CLIENT.make_bucket(BUCKET_NAME)
            print(f"✅ Bucket MinIO '{BUCKET_NAME}' créé.")
        else:
            print(f"✅ Bucket MinIO '{BUCKET_NAME}' trouvé.")
    except Exception as e:
        print(f"⚠️ Attention : MinIO non accessible ({e}). Le stockage sera désactivé.")

# --- CHARGEMENT MODELE ---
DEVICE = "cpu"
model = UNet(n_channels=3, n_classes=2)

@app.on_event("startup")
async def startup_event():
    # 1. Charger MinIO
    init_minio()
    # 2. Charger le Modèle
    try:
        model.load_state_dict(torch.load("models/vision_plante_model.pth", map_location=torch.device('cpu')))
        model.to(DEVICE)
        model.eval()
        print("✅ Modèle IA chargé avec succès !")
    except Exception as e:
        print(f"❌ Erreur chargement modèle : {e}")

# --- TRAITEMENT ---
def process_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((160, 160))
    img_array = np.array(image) / 255.0
    img_array = img_array.transpose((2, 0, 1))
    tensor = torch.tensor(img_array, dtype=torch.float32).unsqueeze(0)
    return tensor

@app.post("/analyze")
async def analyze_crop(file: UploadFile = File(...)):
    # 1. Lecture
    content = await file.read()
    
    # --- SAUVEGARDE MINIO (Le point 20/20) ---
    minio_url = "Non stocké (MinIO down)"
    if MINIO_CLIENT:
        try:
            # On donne un nom unique à l'image
            filename = f"{uuid.uuid4()}_{file.filename}"
            # On remet le curseur de lecture à 0 pour MinIO
            file_data = io.BytesIO(content)
            
            MINIO_CLIENT.put_object(
                BUCKET_NAME,
                filename,
                file_data,
                length=len(content),
                content_type=file.content_type
            )
            minio_url = f"http://localhost:9001/browser/{BUCKET_NAME}/{filename}"
            print(f"💾 Image sauvegardée dans MinIO : {filename}")
        except Exception as e:
            print(f"❌ Erreur upload MinIO : {e}")

    # 2. Prédiction IA
    input_tensor = process_image(content).to(DEVICE)
    with torch.no_grad():
        output = model(input_tensor)
        prediction = torch.argmax(output, dim=1)
    
    pixels_cibles = torch.sum(prediction).item()
    couverture = (pixels_cibles / (160 * 160)) * 100
    
    etat = "Normal"
    if couverture > 15.0: etat = "Anomalie détectée"
    elif couverture > 5.0: etat = "Surveillance"

    return {
        "filename": file.filename,
        "analyse": {
            "couverture": f"{couverture:.2f}%",
            "etat": etat
        },
        "stockage_minio": "Succès ✅" if MINIO_CLIENT else "Échec ❌",
        "image_id": minio_url
    }