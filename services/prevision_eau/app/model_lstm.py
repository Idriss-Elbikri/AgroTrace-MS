import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from app.database import get_sensor_data

# --- 1. LE CERVEAU (Architecture du Réseau de Neurones) ---
class LSTMModel(nn.Module):
    def __init__(self, input_size=1, hidden_layer_size=50, output_size=1):
        super().__init__()
        self.hidden_layer_size = hidden_layer_size
        # La couche LSTM (Mémoire à long terme)
        self.lstm = nn.LSTM(input_size, hidden_layer_size)
        # La couche linéaire (Pour donner la réponse finale)
        self.linear = nn.Linear(hidden_layer_size, output_size)
        self.hidden_cell = (torch.zeros(1,1,self.hidden_layer_size),
                            torch.zeros(1,1,self.hidden_layer_size))

    def forward(self, input_seq):
        lstm_out, self.hidden_cell = self.lstm(input_seq.view(len(input_seq) ,1, -1), self.hidden_cell)
        predictions = self.linear(lstm_out.view(len(input_seq), -1))
        return predictions[-1]

# --- 2. LA FONCTION PRINCIPALE ---
def run_lstm_model(sensor_id, days_to_predict=7):
    print(f"[LSTM] Démarrage du réseau de neurones pour {sensor_id}...")
    
    # A. Récupération des données
    df = get_sensor_data(sensor_id)
    if df.empty:
        return None
    
    # On ne garde que l'humidité (C'est ce qu'on veut prédire)
    data = df['soil_humidity'].values.astype(float)
    
    # B. Normalisation (Mise à l'échelle entre -1 et 1)
    # Les réseaux de neurones détestent les grands nombres comme "55.4"
    scaler = MinMaxScaler(feature_range=(-1, 1))
    data_normalized = scaler.fit_transform(data.reshape(-1, 1))
    data_normalized = torch.FloatTensor(data_normalized).view(-1)
    
    # C. Préparation de l'entraînement
    # On découpe l'historique en petits morceaux de 24h pour apprendre
    train_window = 24
    def create_inout_sequences(input_data, tw):
        inout_seq = []
        L = len(input_data)
        for i in range(L-tw):
            train_seq = input_data[i:i+tw]
            train_label = input_data[i+tw:i+tw+1]
            inout_seq.append((train_seq ,train_label))
        return inout_seq

    train_inout_seq = create_inout_sequences(data_normalized, train_window)

    # D. Initialisation du Modèle
    model = LSTMModel()
    loss_function = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    
    # E. Entraînement (Training)
    epochs = 3 # On met 3 tours pour que ce soit rapide à tester (mets 50 pour le vrai projet)
    print(f"[LSTM] Apprentissage en cours ({epochs} époques)...")
    
    for i in range(epochs):
        for seq, labels in train_inout_seq:
            optimizer.zero_grad()
            model.hidden_cell = (torch.zeros(1, 1, model.hidden_layer_size),
                            torch.zeros(1, 1, model.hidden_layer_size))
            
            y_pred = model(seq)
            single_loss = loss_function(y_pred, labels)
            single_loss.backward()
            optimizer.step()
        
        if i%1 == 0:
            print(f"   - Époque {i+1}/{epochs} terminée.")

    # F. Prédiction (Forecasting)
    print(f"[LSTM] Prédiction des {days_to_predict} prochains jours...")
    fut_pred = 24 * days_to_predict # 7 jours * 24 heures
    
    # On prend les 24 dernières heures connues pour commencer à deviner
    test_inputs = data_normalized[-train_window:].tolist()
    
    model.eval()
    for i in range(fut_pred):
        seq = torch.FloatTensor(test_inputs[-train_window:])
        with torch.no_grad():
            model.hidden_cell = (torch.zeros(1, 1, model.hidden_layer_size),
                            torch.zeros(1, 1, model.hidden_layer_size))
            test_inputs.append(model(seq).item())

    # G. Dénormalisation (Revenir aux vraies valeurs d'humidité)
    actual_predictions = scaler.inverse_transform(np.array(test_inputs[train_window:] ).reshape(-1, 1))
    
    # Création du tableau de résultat avec les dates futures
    last_date = pd.to_datetime(df['time'].iloc[-1])
    future_dates = pd.date_range(start=last_date, periods=fut_pred, freq='h')
    
    result_df = pd.DataFrame({
        'ds': future_dates,
        'yhat': actual_predictions.flatten()
    })
    
    return result_df

# --- BLOC DE TEST ---
if __name__ == "__main__":
    result = run_lstm_model('capteur_parcelle_A', days_to_predict=1) # Juste 1 jour pour tester vite
    print("\n--- RÉSULTAT LSTM (PYTORCH) ---")
    print(result.head())