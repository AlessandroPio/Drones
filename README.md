## Drones Agents

Questo documento descrive un sistema multi-agente progettato per pianificare e monitorare una flotta di droni utilizzati per la consegna di pacchi. Viene fornita una panoramica dei vari agenti coinvolti, le loro responsabilità e le modalità di comunicazione tra di essi.

## File Principali

- **weather_handler.py**: Questo modulo è utilizzato dagli agenti droni per chiamare il modello di linguaggio (LLM moondream) e analizzare le immagini. Restituisce un predicato Prolog che fornisce informazioni sul meteo ai droni.

- **main.py**: Questo script funge da interfaccia principale per il progetto. È utilizzato sia per chiamare l'assistente chatbot (LLM llama2) che fornisce informazioni su missioni avviate o passate, sia per testare l'LLM in relazione alle immagini.

## Configurazione
Il progetto include un file di configurazione (`config.py`) che contiene impostazioni necessarie al funzionamento di esso. Bisogna modificare queste informazioni in base alle proprie necessità, come ad esempio:

- **path immagini da analizzare**: default ./images/
- **LLM per conversare o analizzare immagini**: default llama2, moondream
- **path nel quale verranno salvati gli stati degli agenti**

## DALI
Per eseguire il sistema multi agente bisogna scaricare l'interprete DALI dal seguente link: https://github.com/AAAI-DISIM-UnivAQ/DALI e successivamente caricare i file nella cartella 'agents' all'interno di esso
