import pandas as pd
import os

def split_csv_by_mmsi(input_file):
    # Charger le fichier CSV dans un DataFrame
    df = pd.read_csv(input_file)

    # Grouper les données par numéro MMSI
    grouped = df.groupby('sourcemmsi')

    # Créer un dossier pour les fichiers CSV séparés
    output_folder = 'csv_by_mmsi'
    os.makedirs(output_folder, exist_ok=True)

    # Enregistrer les données groupées dans des fichiers CSV séparés
    for mmsi, data in grouped:
        output_file = os.path.join(output_folder, f'{mmsi}.csv')
        data.to_csv(output_file, index=False)

    print("Les fichiers CSV séparés ont été créés avec succès !")

# Appel de la fonction en spécifiant le chemin vers votre fichier CSV
# input_file_path = 'chemin/vers/votre/fichier.csv'
input_file_path = 'nari_dynamic.csv'
split_csv_by_mmsi(input_file_path)