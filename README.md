(TESTING È IL PROGRAMMA UTILIZZATO)

# Tesi
Se si dovesse far runnare il programma da zero, usare prima questi comandi:

1.
Creazione ambiente virtuale -> python -m venv venv

2.
Attivazione -> .\venv\Scripts\activate (Windows)

3.
Installazione di massa -> python -m pip install -r requirements.txt


Oltre alle librerie Python, va installato Ollama in tutti e tre i modelli utilizzati per i test:

Ollama -> irm https://ollama.com/install.ps1 | iex

I Modelli: ->   

	Light: ollama pull llama3.2

  	Medium: ollama pull llama3.1
								
    Heavy: ollama pull gemma2:27b

Per usare la dashboard di CodeCarbon andare sul sito https://codecarbon.io/ 

Fare l'accesso, andare su project e creare un nuovo progetto e copiare il codice che viene fornito (andrà inserito nel main.py -> api_key="***" )

A questo punto creare un nuovo esperimento e copiare il codice che verrà fornito ( andrà inserito sempre nel main.py -> experiment_id="***" )

Altrimenti è possibile utilizzarlo come faccio io, salvando i file in maniera locale

