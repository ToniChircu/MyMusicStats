# MyMusicStats
Un sistem inteligent de monitorizare și analiză a istoricului Spotify, construit cu Python și Streamlit. Include logică anti-duplicate, validare prin timp de ascultare activă și dashboard interactiv pentru statistici muzicale.

Acesta este un proiect personal dezvoltat din dorința de a avea un control total și o analiză detaliată asupra propriului istoric muzical. Nu este doar un simplu colector de date, ci un sistem inteligent care validează ascultările reale și oferă statistici vizuale în timp real.

---

##  Ce face acest proiect special?

Spre deosebire de istoricul standard oferit de Spotify, acest instrument aduce câteva inovații critice la care am lucrat pentru a asigura acuratețea datelor:

* Smart Listening Logic: Sistemul nu se lasă păcălit de "skip-uri". O piesă este înregistrată în baza de date doar dacă a fost ascultată activ cel puțin 50% din durata sa reală.
* Anti-Duplicate Engine: Am implementat o logică de deduplicare bazată pe ferestre de timp (time-windowing). Aceasta rezolvă conflictele dintre sursele de date UTC (API-ul Spotify) și ora locală, prevenind dublarea pieselor la repornirea aplicației.
* State Persistence: Scriptul își „amintește” ultima piesă salvată înainte de închidere, recuperându-și starea automat la restart pentru o monitorizare continuă fără erori.
* Live Dashboard: O interfață grafică interactivă care transformă baza de date SQLite în grafice intuitive și topuri de artiști.

---

## Stack Tehnic

* Python 3.x - Core logic.
* SQLite - Stocare locală persistentă și eficientă.
* Spotipy - Integrare cu Spotify Web API.
* Pandas - Procesarea și curățarea datelor (normalizare UTC & Timezones).
* Streamlit & Plotly - Crearea dashboard-ului și a vizualizărilor interactive.

---

## Cum îl folosești?

### 1. Configurare Spotify
Creează o aplicație în Spotify Developer Dashboard și obține CLIENT_ID și CLIENT_SECRET. Adaugă http://127.0.0.1:8888/callback la Redirect URIs.

### 2. Instalare
Clonează repository-ul și instalează dependențele:
pip install spotipy pandas streamlit plotly

### 3. Pornire
1. Introdu cheile tale API în scrobbler.py.
2. Pornește colectorul: python scrobbler.py
3. Deschide dashboard-ul: streamlit run app.py

---

## Provocări depășite
* Sincronizarea Timezone-urilor: Am rezolvat decalajul de 3 ore dintre serverele Spotify (UTC) și ora locală prin normalizarea întregului flux de date la standardul UTC.
* Validarea Ascultărilor: Am construit un cronometru intern care măsoară timpul efectiv de redare, oferind date mult mai precise decât simpla interogare a poziției piesei.

---
Creat cu pasiune pentru date și muzică.
