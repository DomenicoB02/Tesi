import os
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from codecarbon import EmissionsTracker

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    source: list[str]
    tools_used: list[str]

llm = ChatOllama(model="llama3.1", temperature=0)
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "Sei un assistente tecnico. Rispondi SEMPRE in formato JSON.\n"
        "Nel campo 'summary', usa il Markdown per creare una risposta ben strutturata.\n"
        "Esempio di summary: '# Risultato: 210\\n\\n- **Passaggio 1**: ...'\n"
        "Assicurati che tutto il testo sia contenuto in una singola stringa JSON valida.\n"
        "{format_instructions}"
    )),
    ("human", "{query}")
]).partial(format_instructions=parser.get_format_instructions())

chain = prompt | llm | parser

query = input("\nDomanda: ")
tracker = EmissionsTracker(save_to_file=False)

tracker.start()
try:
    response = chain.invoke({"query": query})
    
    print("\n" + "—"*40)
    print(f"Risposta: {response.summary}")
    print("—"*40)

except Exception as e:
    # Se fallisce il JSON, mostriamo cosa ha detto l'IA per debug
    print(f"\nRisposta: Errore di formattazione. L'IA ha detto: {e}")

finally:
    tracker.stop()
    dati = tracker.final_emissions_data
    if dati:
        print(f"IMPATTO: {dati.emissions * 1000:.4f}g CO2 | {dati.duration:.2f}s")