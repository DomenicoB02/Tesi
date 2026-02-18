# Tesi
Se si dovesse far runnare il programma da zero, usare prima questi comandi:
1.
Creazione ambiente virtuale:
python -m venv venv
2.
Attivazione:
.\venv\Scripts\activate (Windows)
3.
Installazione di massa:
pip install -r requirements.txt


Oltre alle librerie Python, va installato Ollama in tutti e tre i modelli utilizzati per i test:
Ollama -> irm https://ollama.com/install.ps1 | iex
I Modelli: ->   Light: ollama pull llama3.2
                Medium: ollama pull llama3.1
                Heavy: ollama pull gemma2:27b
