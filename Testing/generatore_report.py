# GENERATO CON L'AI


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# 1. Caricamento e pulizia dati
try:
    df = pd.read_csv("emissions.csv")
    df.columns = df.columns.str.strip()
except Exception as e:
    print(f"Errore nel caricamento del file: {e}")
    exit()

# 2. Funzione per mappare i nomi dei modelli alle categorie
def map_model(name):
    if '3.2' in str(name).lower():
        return 'Leggero (3B)'
    elif '3.1' in str(name).lower():
        return 'Medio (8B)'
    elif '27b' in str(name).lower():
        return 'Pesante (27B)'
    return 'Altro'

df['Categoria'] = df['project_name'].map(map_model)

# 3. Calcolo delle MEDIE per modello
df_avg = df.groupby('Categoria').agg({
    'energy_consumed': 'mean',
    'duration': 'mean',
    'emissions': 'mean',
    'cpu_energy': 'mean',
    'gpu_energy': 'mean',
    'ram_energy': 'mean'
}).reindex(['Leggero (3B)', 'Medio (8B)', 'Pesante (27B)'])

# --- NUOVO CALCOLO: Potenza Media in Watt ---
# Formula: Energia (kWh) * 1000 (per avere Wh) * 3600 (per avere i Joule/secondo -> Watt) diviso il tempo
df_avg['power_watts'] = (df_avg['energy_consumed'] * 1000 * 3600) / df_avg['duration']

# Lista colori per le barre
colors_list = ['#f1c40f', '#3498db', '#e74c3c'] 

# Configurazione stile e layout
plt.style.use('seaborn-v0_8-whitegrid')
fig = plt.figure(figsize=(16, 18))
fig.patch.set_facecolor('#f8f9fa')
gs = gridspec.GridSpec(3, 2, figure=fig, height_ratios=[1, 1, 1.2])

# Assegnazione degli spazi nella griglia (3 righe x 2 colonne)
ax_energy = fig.add_subplot(gs[0, 0])
ax_time = fig.add_subplot(gs[0, 1])
ax_emissions = fig.add_subplot(gs[1, 0])
ax_power = fig.add_subplot(gs[1, 1])     # <--- Il nuovo grafico a linee
ax_pie_medio = fig.add_subplot(gs[2, 0])
ax_pie_pesante = fig.add_subplot(gs[2, 1])

# --- 1. ENERGIA MEDIA CONSUMATA (Barre Verticali) ---
ax_energy.bar(df_avg.index, df_avg['energy_consumed'], color=colors_list, edgecolor='black', alpha=0.85)
ax_energy.set_title('Energia Media Consumata (kWh)', fontweight='bold', fontsize=15)
ax_energy.set_ylabel('kWh', fontsize=12)
ax_energy.grid(axis='y', linestyle='--', alpha=0.5)

# --- 2. TEMPO MEDIO DI RISPOSTA (Barre Verticali) ---
ax_time.bar(df_avg.index, df_avg['duration'], color=colors_list, edgecolor='black', alpha=0.85)
ax_time.set_title('Tempo Medio di Risposta (Secondi)', fontweight='bold', fontsize=15)
ax_time.set_ylabel('Secondi', fontsize=12)
for i, v in enumerate(df_avg['duration']):
    ax_time.text(i, v + (v*0.02), f"{v:.2f} s", ha='center', fontweight='bold', fontsize=11)

# --- 3. EMISSIONI MEDIE (Barre Orizzontali) ---
ax_emissions.barh(df_avg.index, df_avg['emissions'] * 1000, color=colors_list, edgecolor='black', alpha=0.85)
ax_emissions.set_title('Emissioni Medie (g CO2eq)', fontweight='bold', fontsize=15)
ax_emissions.set_xlabel('Grammi di CO2', fontsize=12)
ax_emissions.invert_yaxis()
ax_emissions.grid(axis='x', linestyle='--', alpha=0.5)

# --- 4. POTENZA MEDIA (Grafico a Linee) ---
ax_power.plot(df_avg.index, df_avg['power_watts'], color='#8e44ad', marker='o', markersize=10, linewidth=3)
ax_power.set_title('Potenza Media Assorbita (Watt)', fontweight='bold', fontsize=15)
ax_power.set_ylabel('Watt (W)', fontsize=12)
ax_power.grid(axis='both', linestyle='--', alpha=0.5)

# --- SETUP COMUNE PER LE TORTE ---
labels_hw = ['CPU', 'GPU', 'RAM']
colors_hw = ['#3498db', '#e74c3c', '#2ecc71'] 
wedge_dict = {'edgecolor': 'white', 'linewidth': 2}
text_dict = {'fontweight': 'bold'}

# --- 5. UTILIZZO HARDWARE (Torta - Modello Medio 8B) ---
medio_data = df_avg.loc['Medio (8B)']
sizes_hw_medio = [medio_data['cpu_energy'], medio_data['gpu_energy'], medio_data['ram_energy']]
ax_pie_medio.pie(sizes_hw_medio, labels=labels_hw, autopct='%1.1f%%', startangle=140, 
                 colors=colors_hw, wedgeprops=wedge_dict, textprops=text_dict)
ax_pie_medio.set_title("Dettaglio Consumo Hardware\n(Modello Medio 8B)", fontweight='bold', fontsize=14)

# --- 6. UTILIZZO HARDWARE (Torta - Modello Pesante 27B) ---
pesante_data = df_avg.loc['Pesante (27B)']
sizes_hw_pesante = [pesante_data['cpu_energy'], pesante_data['gpu_energy'], pesante_data['ram_energy']]
ax_pie_pesante.pie(sizes_hw_pesante, labels=labels_hw, autopct='%1.1f%%', startangle=140, 
                   colors=colors_hw, wedgeprops=wedge_dict, textprops=text_dict)
ax_pie_pesante.set_title("Dettaglio Consumo Hardware\n(Modello Pesante 27B)", fontweight='bold', fontsize=14)

# Ottimizzazione e salvataggio
plt.tight_layout(pad=4.0)
plt.savefig('Report_Comparativo_Finale.png', dpi=300)
print("Report salvato correttamente come 'Report_Comparativo_Finale.png'.")
