# Comanda 🐟

Web app di gestione semplificata per un piccolo ristorante (ispirata a El Tridente, cevichería peruviana a Vimodrone).

È un **progetto formativo**: serve a padroneggiare Python per il web, dagli strati senza magia (WSGI/ASGI a mano) fino a framework, architettura, test, async e deploy. Non è un prodotto finito, ma è pensato per diventare qualcosa di realmente usabile.

## Cosa farà (in crescita, lezione dopo lezione)

- **Menu**: piatti, categorie, prezzi, **14 allergeni UE** (obbligatori per legge), food cost
- **Menu pubblico**: pagina consultabile dai clienti, anche via QR al tavolo
- **Prenotazioni**: turni, coperti, capienza, conferma via email
- **Sala e tavoli**: mappa tavoli, stato (libero / occupato / da pulire)
- **Comande**: sala → cucina in tempo reale, con stati (in attesa / in preparazione / pronta)
- **Backoffice staff**: login, ruoli (titolare, sala, cucina)
- **Report**: chiusura giornaliera, piatti più venduti, incasso per turno

## Stack (si costruisce per fasi)

| Strato | Scelta |
|---|---|
| Linguaggio | Python 3.14 |
| Tooling | uv, ruff, pytest, pre-commit |
| API / servizi | FastAPI + Pydantic |
| Dati | PostgreSQL, SQLAlchemy 2.0, Alembic |
| Backoffice | Django |
| Frontend | Template server-side + HTMX + Alpine.js + CSS moderno vanilla |
| Background | Redis + coda di task |
| Deploy | Docker, GitHub Actions, Railway (confronto con Hetzner + Coolify) |

## Struttura documentazione

- `docs/ROADMAP.md` — percorso completo per fasi
- `docs/lezioni/` — una scheda per lezione, pensata per essere stampata e annotata
