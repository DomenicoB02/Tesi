import os
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from codecarbon import EmissionsTracker

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    source: list[str]
    tools_used: list[str]

llm = ChatOllama(model="llama3.1", temperature=1, max_tokens=1000)
parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ("system", (
            "Il tuo unico compito è ESEGUIRE la richiesta dell'utente.\n"
            "Rispondi in modo strutturato e professionale in italiano."
    )),
    ("human", "{query}")
])

chain = prompt | llm | parser

modello = "llama3.1"

query = input("\nDomanda: ")
tracker = EmissionsTracker(
    project_name=f"Test_{modello}", 
    output_dir=".",
    output_file="emissions.csv"
)

tracker.start()
try:
    response = chain.invoke({"query": query})
    
    print(f"\nRisposta:\n{response}")

except Exception as e:
    # Se fallisce il JSON, mostriamo cosa ha detto l'IA per debug
    print(f"\nRisposta: Errore di formattazione. L'IA ha detto: {e}")

finally:
    tracker.stop()
    dati = tracker.final_emissions_data
    if dati:
        print(f"IMPATTO: {dati.emissions * 1000:.4f}g CO2 | {dati.duration:.2f}s")
