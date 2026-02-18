from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from codecarbon import EmissionsTracker
import configparser
import os

load_dotenv()
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    source: list[str]
    tools_used: list[str]
# Inizializzo CodeCarbon
tracker = EmissionsTracker(
    project_name="Test_Impatto_IA",
    save_to_api=True,
    api_key="***",
    experiment_id="0c10affb-6f8a-4fee-a808-dee1a6c62ce8"
)
tracker.start()
#Implemento un LLM
llm = ChatOllama(model="llama3.2", temperature = 0)
parser = PydanticOutputParser(pydantic_object=ResearchResponse)
#Prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Sei un assistente alla ricerca esperto. 
            Tutte le tue risposte devono essere scritte rigorosamente in LINGUA ITALIANA.
            La tua risposta FINALE deve essere un oggetto JSON che rispetti ESATTAMENTE questo schema.
            Non usare nomi di campo diversi. Usa solo questi:
            - topic: (l'argomento della ricerca)
            - summary: (una breve spiegazione in italiano)
            - source: (lista di URL o nomi delle fonti)
            - tools_used: (lista degli strumenti utilizzati)
            Istruzioni di formattazione:
            {format_instructions}
            """
        ),
        ("placeholder","{chat_history}"),
        ("human","{query}"),
        ("placeholder","{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

# Creo una catena semplice
chain = prompt | llm | parser
query = input("In cosa posso aiutarti? ")
try:
    print(f"--- Ricerca su {query} in corso... ---")
    response = chain.invoke({
        "query": query,
        "chat_history": [],
        "agent_scratchpad": []
    })
    print("\n--- RISULTATO ---")
    print("\n" + "="*30)
    print("      REPORT DI RICERCA")
    print("="*30)
    print(f"TOPIC:   {response.topic}")
    print(f"SUMMARY: {response.summary}")
    print(f"SOURCES: {', '.join(response.source)}")
    print(f"TOOLS:   {', '.join(response.tools_used)}")
    print("="*30)
except Exception as e:
    print(f"Errore: {e}")
finally:
    emissions_data = tracker.stop()
    dati = tracker.final_emissions_data
    print("\n" +  " - "*15 )
    print("      ANALISI IMPATTO AMBIENTALE")
    print("  -"*15)
    print(f"Durata:           {dati.duration:.2f} secondi")
    print(f"Consumo Energetico: {dati.energy_consumed:.6f} kWh")
    emissions_gr = dati.emissions * 1000
    print(f"Emissioni CO2:      {emissions_gr:.4f} grammi")
    potenza_watt = (dati.energy_consumed / (dati.duration / 3600)) * 1000
    print(f"Potenza Media:     {potenza_watt:.2f} Watt")
    print("  -"*15)