import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from codecarbon import EmissionsTracker

load_dotenv()

modello = "gemma2:27b"
llm = ChatOllama(model=modello, temperature=1, max_tokens=1000)
parser = StrOutputParser() 

prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "Devi rispondere solo a quello che ti viene richiesto"
        "Rispondi alla richiesta dell'utente in modo strutturato, chiaro e professionale in italiano."
    )),
    ("human", "{query}")
])

chain = prompt | llm | parser

query = input("\nDomanda: ")

tracker = EmissionsTracker(
    project_name=f"Test_{modello}", 
    output_dir=".",
    output_file="emissions.csv"
)

tracker.start()
try:
    response = chain.invoke({"query": query})
    
    print("\n" + "—"*40)
    print(f"Risposta:\n{response}")
    print("—"*40)

except Exception as e:
    print(f"\nErrore durante l'esecuzione: {e}")

finally:
    tracker.stop()
    dati = tracker.final_emissions_data
    if dati:
        print(f"IMPATTO: {dati.emissions * 1000:.4f}g CO2 | {dati.duration:.2f}s")