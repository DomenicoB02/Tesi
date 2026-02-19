import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from codecarbon import EmissionsTracker
import time

load_dotenv()

modelli_da_testare = ["llama3.2", "llama3.1", "gemma2:27b"]

query_benchmark = (
    "Scrivi una guida dettagliata su come costruire una serra idroponica in casa, includendo materiali necessari, fasi di assemblaggio e consigli per la manutenzione delle piante"
)

parser = StrOutputParser()

# Loop
for nome_modello in modelli_da_testare:
    print(f"\n" + "="*50)
    print(f"AVVIO TEST MODELLO: {nome_modello}")
    print("="*50)
    
    # Inizializzazione modello specifico
    llm = ChatOllama(model=nome_modello, temperature=0.8, max_tokens=500)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system",  "Devi rispondere solo a quello che ti viene richiesto. Rispondi in modo strutturato, chiaro e professionale in italiano."),
        ("human", "{query}")
    ])
    
    chain = prompt | llm | parser

    # Tracker configurato per distinguere i progetti nel CSV
    tracker = EmissionsTracker(
        project_name=f"Benchmark_{nome_modello.replace(':', '-')}", 
        output_dir=".",
        output_file="emissions.csv"
    )

    tracker.start()
    try:
        start_time = time.time()
        response = chain.invoke({"query": query_benchmark})
        end_time = time.time()
        
        print(f"\nRisposta di {nome_modello}:\n{response}")
        
    except Exception as e:
        print(f"Errore con {nome_modello}: {e}")
    finally:
        tracker.stop()
        dati = tracker.final_emissions_data
        if dati:
            print(f"\nRISULTATI {nome_modello}:")
            print(f"CO2: {dati.emissions * 1000:.4f}g | Tempo: {dati.duration:.2f}s | Watt GPU: {dati.gpu_power:.2f}W")
    
    # Una piccola pausa per far raffreddare la GPU tra un test e l'altro
    print("\nFase di raffreddamento (5s)...")
    time.sleep(10)

print("\nCOMPLIMENTI! Tutti i test sono stati completati e i dati sono nel file emissions.csv")