import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sqlite3
import time
from datetime import datetime, timezone

# DATELE TALE DE LA SPOTIFY
ID_CLIENT = "VĂ RUGĂM INTRODUCEȚI ID-UL VOSTRU AICI"
SECRET_CLIENT = "VĂ RUGĂM INTRODUCEȚI SECRET-UL VOSTRU AICI"
URL_REDIRECT = "http://127.0.0.1:8888/callback"
# Inițializăm Spotipy pentru a ne permite citirea istoricului și piesa pe care o ascultăm curent
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=ID_CLIENT,
    client_secret=SECRET_CLIENT,
    redirect_uri=URL_REDIRECT,
    scope="user-read-recently-played user-read-currently-playing"
))

# --- VARIABILE GLOBALE PENTRU LOGICA INTELIGENTĂ ---
timp_ascultat_efectiv = 0
id_piesa_sub_verificare = None

def setup_db():
    """Creează baza de date și tabelul dacă nu există deja."""
    conexiune = sqlite3.connect('muzica_mea.db')
    conexiune.execute('''CREATE TABLE IF NOT EXISTS istoric_muzica
                    (timestamp TEXT UNIQUE, artist TEXT, piesa TEXT, album TEXT, durata_ms INTEGER, spotify_id TEXT)''')
    conexiune.close()

def import_initial():
    """Recuperează istoricul de 50 de piese și evită duplicatele la fiecare pornire."""
    print("Sincronizare istoric (UTC standard)...")
    try:
        recent = sp.current_user_recently_played(limit=50)
        conn = sqlite3.connect('muzica_mea.db')
        cursor = conn.cursor()
        count = 0
        
        for item in recent['items']:
            t = item['track']
            spotify_id = t['id']
            timestamp_spotify = item['played_at']
            
            # Verificăm dacă există ID-ul piesei în ultimele 10 minute (toleranță offset)
            cursor.execute("""
                SELECT 1 FROM istoric_muzica 
                WHERE timestamp = ? 
                OR (spotify_id = ? AND ABS(strftime('%s', timestamp) - strftime('%s', ?)) < 600)
            """, (timestamp_spotify, spotify_id, timestamp_spotify))
            
            if not cursor.fetchone():
                try:
                    conn.execute("INSERT INTO istoric_muzica VALUES (?,?,?,?,?,?)",
                                (timestamp_spotify, t['artists'][0]['name'], t['name'], 
                                 t['album']['name'], t['duration_ms'], spotify_id))
                    count += 1
                except: continue
        
        conn.commit()
        conn.close()
        if count > 0:
            print(f"Import finalizat. Am adăugat {count} piese noi.")
        else:
            print("Totul este la zi. Nicio piesă nouă găsită în istoric.")
    except Exception as e:
        print(f"Eroare la importul inițial: {e}")

def monitorizare_live():
    # Logica principală: verifică timpul ascultat efectiv și salvează în format UTC.
    global timp_ascultat_efectiv, id_piesa_sub_verificare
    
    current = sp.current_user_playing_track()
    
    if current and current['is_playing']:
        track = current['item']
        track_id_curent = track['id']
        durata_ms = track['duration_ms']
        
        # Dacă s-a schimbat piesa, resetăm contorul de timp
        if track_id_curent != id_piesa_sub_verificare:
            id_piesa_sub_verificare = track_id_curent
            timp_ascultat_efectiv = 0
            print(f"Acum asculți: {track['name']} - {track['artists'][0]['name']}")
        else:
            # Adunăm secundele trecute (verificăm la fiecare 5 secunde)
            timp_ascultat_efectiv += 5000 

        # Verificăm dacă 50% din piesă a fost ascultată ACTIV
        prag_jumătate = durata_ms / 2

        if timp_ascultat_efectiv >= prag_jumătate:
            conn = sqlite3.connect('muzica_mea.db')
            cursor = conn.cursor()
            
            # Verificăm dacă piesa e deja ultima salvată în DB pentru a nu creea duplicate
            cursor.execute("SELECT spotify_id FROM istoric_muzica ORDER BY timestamp DESC LIMIT 1")
            rezultat = cursor.fetchone()
            ultima_piesa_id = rezultat[0] if rezultat else None

            if track_id_curent != ultima_piesa_id:
                # Generăm timestamp UTC identic cu formatul Spotify,pentru a evita duplicate la importul inițial
                acum_utc = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                
                conn.execute("INSERT INTO istoric_muzica VALUES (?,?,?,?,?,?)",
                            (acum_utc, track['artists'][0]['name'], track['name'], 
                             track['album']['name'], durata_ms, track_id_curent))
                conn.commit()
                print(f"[Smart Scrobble] Ascultare confirmată și salvată: {track['name']}")
                # Blocăm resalvarea aceleiași piese în această sesiune
                timp_ascultat_efectiv = 9999999 
            
            conn.close()
    else:
        # Dacă muzica e oprită, nu resetăm id_piesa_sub_verificare ca să nu pornim 
        # contorul de la zero când dai Resume
        pass

if __name__ == "__main__":
    setup_db()
    import_initial()
    
    # --- STATE RECOVERY (Recuperare memorie la pornire) ---
    conn = sqlite3.connect('muzica_mea.db')
    last_entry = conn.execute("SELECT spotify_id FROM istoric_muzica ORDER BY timestamp DESC LIMIT 1").fetchone()
    conn.close()
    
    if last_entry:
        id_piesa_sub_verificare = last_entry[0]
        # Presupunem că e deja salvată dacă e ultima în DB, deci setăm timpul la "infinit"
        timp_ascultat_efectiv = 9999999 
        print(f"Memorie recuperată: Ultima piesă salvată a fost ID {id_piesa_sub_verificare}")

    print("Scrobbler pornit. Monitorizez timpul real de ascultare...")
    
    while True:
        try:
            monitorizare_live()
        except Exception as e:
            print(f"Eroare: {e}")
        
        # Verificăm la fiecare 5 secunde pentru precizie
        time.sleep(5)
