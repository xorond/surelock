# surelock

Ein Passwort-Manager, der mit Python programmiert ist.

Das hier ist unser Projekt für das Programmierpraktikum der Universität Wien Bachelor Mathematik.

## Verwendung:

Siehe [USAGE.md](https://github.com/xorond/surelock/blob/master/docs/USAGE.md)

## Features: 
- [x] Mittels Kommandozeile,
- [x] oder Benutzeroberfläche (Tkinter) verwendbar.
- [x] Verschiedene Kryptographie-Libraries werden verwendet.
- [x] Eine SQL-Library (voraussichtlich sqlite3) wird benutzt. 
- [x] Lokale verschlüsselte SQL Datenbank, die mit einem Master-Passwort geschützt wird, um die anderen Passwörter zu sichern.
- [x] Die lokale Datenbank wird mit RSA oder AES verschlüsselt
- [ ] eventuell implementieren wir ein File-Key Feature, um eine Art von Zwei-Faktor-Authentifizierung zu realisieren.
- [x] Mit einer simplen Pass Phrase (oder auch ohne) kann ein komplizierteres Passwort (Länge und vorkommende Sonderzeichen wählbar) mit einem unumkehrbaren Algorithmus (Hashing-Algorithmen kombiniert mit Base64-Transformationen) generiert und in der lokalen Datenbank gespeichert werden.
 - [ ] Möglicherweise: Cloud-Synchronisation per Dropbox (damit man seine Passwörter unkompliziert auf verschiedenen Geräten verwenden kann).

## Entwicklungs-Workflow: 
Wir machen ein privates Git-Repository, um den Code zusammen ohne Versions- oder Codekonflikte bearbeiten zu können. Wir planen das Projekt nach dem Semesterende zu veröffentlichen (Open Source!).

### Gruppenmitglieder:
  * Oguz Bektas           [@xorond](https://github.com/xorond)
  * Alexander Panzenböck  [@Alex6312](https://github.com/Alex6312)

### Tutor: 
  * Clemens Karner

