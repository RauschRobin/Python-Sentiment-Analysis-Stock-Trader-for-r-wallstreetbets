# Python_Projekt
Das ist unser Python Projekt im 4. Semester (Wahlfach Python A) von Ozan Akcebe, Jonas Stöckermann und Robin Rausch. Es handelt sich um einen Sentiment Analysis Bot welcher periodisch einen Subreddit durchstöbert und die neusten top-posts analysiert. Bei einer Kaufempfehlung einer Aktie wird diese gekauft, bei einer Verkaufsempfehlung wird sie verkauft. Zusätzlich gibt es einen Chart im Frontend. Das Frontend läuft über Streamlit.

## Requirements
```
pip install asyncpraw==7.7.0
pip install twelvedata==1.2.11
pip install nltk==3.8.1
pip install pyyaml==6.0
pip install fastapi==0.95.1
pip install uvicorn==0.22.0
pip install streamlit==1.22.0
pip install matplotlib==3.7.1
```
Bevor das Projekt zum ersten mal gestartet wird, muss einmal ```nltk.download('punkt')``` in einem zusätzlichen Python script ausgeführt werden oder das hierfür angelegte Skript ```SETUP/SETUP_install_nltk_punkt.py``` ausgeführt werden.

## Was macht der Code?
Dieser Code überprüft täglich den Subreddit r/wallstreetbets und liest die Top-Beiträge des Tages. Anschließend erfolgt der Kauf oder Verkauf der in den Beiträgen erwähnten Aktien. Um die Beiträge zu lesen und zu interpretieren, haben wir einen Sentiment-Analysis-Bot implementiert, der maschinelles Lernen nutzt. Um diesen Bot zu trainieren, erstellen wir einen einzigartigen Datensatz, der spezifisch für r/wallstreetbets ist. Um die Aktien zu kaufen, zu halten und zu verkaufen, haben wir einen Handler erstellt, der diese Transaktionen mit den realen Aktienkursen simuliert, die wir genau zu diesem Zeitpunkt von einer Börsen-API erhalten haben.
