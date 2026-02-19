import pandas as pd
import matplotlib.pyplot as plt

# 1. Caricamento e pulizia dati
try:
    df = pd.read_csv("emissions.csv")
    df.columns = df.columns.str.strip()
except Exception as e:
    print(f"Errore nel caricamento del file: {e}")
    exit()

# 2. Funzione per mappare i nomi dei modelli alle categorie e colori richiesti
def map_model(name):
    if '3.2' in name.lower():
        return 'Leggero (3B)', 'yellow'
    elif '3.1' in name.lower():
        return 'Medio (8B)', 'blue'
    elif '27b' in name.lower():
        return 'Pesante (27B)', 'red'
    return 'Altro', 'gray'

# Creiamo le colonne di supporto per mappare categorie e colori
df['Categoria'], df['Colore'] = zip(*df['project_name'].map(map_model))

# 3. Calcolo delle MEDIE per modello su tutti gli esperimenti
df_avg = df.groupby('Categoria').agg({
    'energy_consumed': 'mean',
    'duration': 'mean',
    'emissions': 'mean',
    'cpu_energy': 'mean',
    'gpu_energy': 'mean',
    'ram_energy': 'mean'
}).reindex(['Leggero (3B)', 'Medio (8B)', 'Pesante (27B)']) # Ordine fisso delle barre

# Lista colori per le barre (Giallo, Blu, Rosso)
colors_list = ['#f1c40f', '#3498db', '#e74c3c'] 

# Configurazione stile e layout
plt.style.use('seaborn-v0_8-whitegrid')
fig, axs = plt.subplots(2, 2, figsize=(16, 14))
fig.patch.set_facecolor('#f8f9fa')

# --- 1. ENERGIA MEDIA CONSUMATA (Barre Verticali) ---
axs[0, 0].bar(df_avg.index, df_avg['energy_consumed'], color=colors_list, edgecolor='black', alpha=0.85)
axs[0, 0].set_title('Energia Media Consumata (kWh)', fontweight='bold', fontsize=15)
axs[0, 0].set_ylabel('kWh', fontsize=12)
axs[0, 0].grid(axis='y', linestyle='--', alpha=0.5)

# --- 2. TEMPO MEDIO DI RISPOSTA (Barre Verticali) ---
axs[0, 1].bar(df_avg.index, df_avg['duration'], color=colors_list, edgecolor='black', alpha=0.85)
axs[0, 1].set_title('Tempo Medio di Risposta (Secondi)', fontweight='bold', fontsize=15)
axs[0, 1].set_ylabel('Secondi', fontsize=12)
for i, v in enumerate(df_avg['duration']):
    axs[0, 1].text(i, v + (v*0.02), f"{v:.2f} s", ha='center', fontweight='bold', fontsize=11)

# --- 3. EMISSIONI MEDIE (Barre Orizzontali) ---
# Moltiplichiamo per 1000 per visualizzare in grammi
axs[1, 0].barh(df_avg.index, df_avg['emissions'] * 1000, color=colors_list, edgecolor='black', alpha=0.85)
axs[1, 0].set_title('Emissioni Medie (g CO2eq)', fontweight='bold', fontsize=15)
axs[1, 0].set_xlabel('Grammi di CO2', fontsize=12)
axs[1, 0].invert_yaxis() # Inverte l'ordine per avere il Leggero in alto
axs[1, 0].grid(axis='x', linestyle='--', alpha=0.5)

# --- 4. UTILIZZO HARDWARE (Torta - Media Modello Pesante 27B) ---
pesante_data = df_avg.loc['Pesante (27B)']
labels_hw = ['CPU', 'GPU', 'RAM']
sizes_hw = [pesante_data['cpu_energy'], pesante_data['gpu_energy'], pesante_data['ram_energy']]
colors_hw = ['#3498db', '#e74c3c', '#2ecc71'] # Blu CPU, Rosso GPU, Verde RAM

axs[1, 1].pie(sizes_hw, labels=labels_hw, autopct='%1.1f%%', startangle=140, 
              colors=colors_hw, wedgeprops={'edgecolor': 'white', 'linewidth': 2},
              textprops={'fontweight': 'bold'})
axs[1, 1].set_title("Dettaglio Consumo Energetico Hardware\n(Media Modello Pesante)", fontweight='bold', fontsize=15)

# Ottimizzazione e salvataggio
plt.tight_layout(pad=7.0)
plt.savefig('Report_Comparativo_Finale.png', dpi=300)
print("Report salvato correttamente come 'Report_Comparativo_Finale.png'.")