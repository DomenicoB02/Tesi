import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from codecarbon import EmissionsTracker
import time

load_dotenv()

NOME_FILE_RISPOSTE = "risposte.txt"

with open(NOME_FILE_RISPOSTE, "w", encoding="utf-8") as f:
    f.write(f"### BENCHMARK AI ###\n")
    f.write("="*80 + "\n\n")

#Domande generate con L'IA
domande = [
    "Spiega brevemente (massimo 150 parole) il paradosso del gatto di Schrödinger e dimmi perché è considerato un esperimento mentale enon un esperimento fisico reale"
    "Risolvi questo problema: in una stanza ci sono 3 interruttori fuori dalla porta (tutti attualmente su OFF). Solo uno di essi accende la lampadina all'interno della stanza. Puoi entrare nella stanza solo una volta. Come fai a capire quale interruttore è quello corretto?",
    "Scrivi una funzione Python che trovi la sottostringa più lunga senza caratteri ripetuti in una data stringa. Ottimizza il codice per la velocità e spiega la sua complessità computazionale O(n).",
    "Riassumi i principi fondamentali della termodinamica in 5 punti chiave, spiegando come il concetto di entropia si applica alla vita di tutti i giorni.",
    "Scrivi un prologo per un romanzo noir ambientato in una Milano futuristica e piovosa nell'anno 2077. Usa uno stile asciutto e descrittivo (circa 400 parole).",
    "Traduci il seguente testo in un linguaggio formale e burocratico: 'Ehi, scusa il ritardo, ma c'era un sacco di traffico e non riuscivo a trovare parcheggio. Sarò lì in dieci minuti!'",
    "Spiega le principali differenze tra l'etica aristotelica e l'imperativo categorico di Kant, usando un esempio pratico come il problema del carrello ferroviario.",
    "Crea una lista JSON di 5 pianeti del sistema solare, includendo: nome, distanza media dal sole, diametro equatoriale e composizione atmosferica prevalente.",
    "Sviluppa un piano editoriale di una settimana per un blog che tratta di sostenibilità ambientale e intelligenza artificiale, includendo i titoli dei post e le parole chiave.",
    "Identifica l'errore logico in questo frammento di codice (anche se sintatticamente corretto): for i in range(len(lista)): if lista[i] == target: return i; return -1 quando usato all'interno di un ciclo annidato.",
    "Scrivi una guida dettagliata su come costruire una serra idroponica in casa, includendo i materiali necessari, le fasi di assemblaggio e i consigli per la manutenzione delle piante.",
    "Risolvi questo enigma logico: hai due brocche, una con una capienza di 5 litri e un'altra di 3 litri. Non ci sono scale graduate sulle brocche. Come puoi misurare esattamente 4 litri d'acqua usando solo questi due contenitori?",
    "Progetta un'architettura di sistema per un'applicazione di chat in tempo reale. Spiega come gestiresti la scalabilità per 1 milione di utenti simultanei e quale tecnologia di database (SQL vs NoSQL) sceglieresti per la memorizzazione dei messaggi.",
    "Confronta le teorie economiche di Adam Smith e John Maynard Keynes. Spiega come le loro diverse visioni sull'intervento del governo si applicherebbero a una recessione globale dei giorni nostri.",
    "Scrivi uno studio dettagliato del personaggio di un antagonista (villain) che crede sinceramente di essere l'eroe della propria storia. Descrivi le sue motivazioni, un dilemma morale specifico che ha affrontato e la sua giustificazione psicologica per un'azione controversa.",
    "Analizza l'impatto dell'invenzione della stampa sulla Riforma Protestante. Discuti come la democratizzazione dell'informazione nel XVI secolo sia parallela all'attuale impatto dei social media sui movimenti politici.",
    "Spiega il processo biologico dell'editing genetico CRISPR-Cas9 a un non scienziato. Discuti una delle principali preoccupazioni etiche riguardo ai 'bambini su misura' (designer babies) e una potenziale svolta nel trattamento delle malattie ereditarie.",
    "Crea una query SQL che trovi il secondo stipendio più alto da una tabella Employee, assicurandoti che la soluzione gestisca i casi in cui ci sono stipendi duplicati o meno di due voci distinte.",
    "Redigi una proposta di progetto formale per un consiglio comunale per implementare un bosco verticale su un edificio pubblico. Includi i benefici ambientali, le stime delle sfide di manutenzione e il potenziale impatto sulla biodiversità urbana.",
    "Valuta il concetto di 'Uncanny Valley' (Valle dell'Indisponenza) nella robotica e nella CGI. Spiega perché robot dall'aspetto umano 'quasi' perfetti possano innescare un senso di repulsione e come gli sviluppatori cerchino di superare questo effetto.",
    "Scrivi una serie di cinque protocolli di sicurezza complessi e non ovvi per una stazione di ricerca situata su Europa, la luna di Giove, considerando le radiazioni estreme, le temperature sotto lo zero e la potenziale scoperta di vita microbica extraterrestre."
]

modelli_da_testare = ["llama3.2", "llama3.1", "gemma2:27b"]

parser = StrOutputParser()

for i, domanda in enumerate(domande, 1):
    print(f"\n" + "#"*70)
    print(f"### ESECUZIONE DOMANDA {i}/20")
    print(f"### TEST: {domanda}...")
    print("#"*70)  

    # Loop
    for nome_modello in modelli_da_testare:
        print(f"\n" + "="*50)
        print(f"AVVIO TEST MODELLO: {nome_modello}")
        print("="*50)
        
        # Inizializzazione modello specifico
        llm = ChatOllama(
            model=nome_modello, 
            temperature=0.6, 
            num_predict=3000,
            repeat_penalty=1.2, 
            top_p=0.95,
            top_k=20,
            thinking_effort="auto",
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system",  "Devi rispondere solo a quello che ti viene richiesto. Rispondi in modo strutturato, chiaro e professionale in italiano."),
            ("human", "{query}")
        ])
        
        chain = prompt | llm | parser

        # Tracker configurato per distinguere i progetti nel CSV
        tracker = EmissionsTracker(
            project_name=f"Q{i}_{nome_modello}", 
            output_dir=".",
            output_file="emissions.csv",
            log_level="error"
        )

        tracker.start()
        try:
            response = chain.invoke({"query": domanda})

            print(f"\nRisposta da {nome_modello}:")
            print("—"*40)
            print(response)
            print("—"*40)

            with open(NOME_FILE_RISPOSTE, "a", encoding="utf-8") as f:
                f.write(f"--- DOMANDA {i} | MODELLO: {nome_modello} ---\n")
                f.write(f"QUERY: {domanda}\n\n")
                f.write(f"RISPOSTA:\n{response}\n")
                f.write("-" * 50 + "\n\n")
            
        except Exception as e:
            print(f"Errore con {nome_modello}: {e}")
        finally:
            tracker.stop()
            dati = tracker.final_emissions_data
            if dati:
                print(f"\n[METRICHE {nome_modello}]")
                print(f"CO2: {dati.emissions * 1000:.4f}g | Tempo: {dati.duration:.2f}s | Energia: {dati.energy_consumed * 1000:.4f}Wh")
        
        # Pausa per far raffreddare la GPU tra un test e l'altro
        print("\nFase di raffreddamento (5s)...")
        time.sleep(10)

    time.sleep(15)

print("\nCOMPLIMENTI! Tutti i test sono stati completati e i dati sono nel file emissions.csv")

