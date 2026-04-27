# MyMusicStats
Un sistem ingenios de urmărire și analiză a istoriei Spotify, construit cu Python și Streamlit. Dispune de anti-duplicare, verificare prin timpul de ascultare efectivă și un dashboard interactiv pentru statistici muzicale.
Este un proiect personal, dezvoltat din dorința de a avea un control total și o analiză detaliată a propriului istoric muzical. Nu este doar un colector de date, ci un sistem care validează ascultările reale și oferă statistici vizuale în timp real.
De ce este special acest proiect?
Spre deosebire de istoricul standard oferit de Spotify, acest instrument aduce câteva inovații la care am muncit ca să pot oferii o bază de date corectă:
Smart Listening Logic: Sistemul nu se lasă păcălit de "skip-uri". O piesă este înregistrată în baza de date doar dacă a fost ascultată activ cel puțin 50% din durata sa reală.
Anti-Duplicate Engine: Am scris o logică de deduplicare pe baze de ferestre de timp (time-windowing). Rezolvă conflictele dintre UTC (API-ul Spotify) și ora locală, prevenind dublarea pieselor la o repornire a aplicației.
State Persistence: Scriptul “își amintește” ultima piesă salvată înainte de închidere, își revine “ca prin minune” la restart și continuă monitorizarea fără rate-uri.
Live Dashboard: O interfață grafică interactivă care transformă baza de date SQLite în grafice și topuri de artiști.

Stack Tehnic
Python 3.x Core logic.
SQLite Stocare locală persistentă și eficientă.
Spotipy Integrare cu Spotify Web API.
Pandas Înaintarea și curățarea datelor (normalizare UTC & Timezones).
Streamlit & Plotly Crearea dashboard-ului și a vizualizărilor interactive.

Cum îl folosești?
1. Configurare Spotify
Creează o aplicație în Spotify Developer Dashboard și obține CLIENT_ID și CLIENT_SECRET. Adaugă http://127.0.0.1:8888/callback la Redirect URIs.
2. Instalare
Clonează repository-ul și instalează dependențele: pip install spotipy pandas streamlit plotly
3. Pornire
Introdu cheile tale API în scrobbler.py.
Pornește colectorul: python scrobbler.py
Deschide dashboard-ul: streamlit run app.py



