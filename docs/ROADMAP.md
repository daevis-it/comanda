# Comanda — Roadmap

**Inizio:** 1 ottobre 2026 · **Ritmo:** almeno 1 ora a sera · **Stima:** circa 55 sessioni, quindi fine dicembre / inizio gennaio con un po' di margine.

## Principi

1. **Prima senza magia, poi il framework.** Ogni astrazione la scrivi a mano almeno una volta.
2. **Il dominio sta al centro.** Le regole del ristorante (capienza, allergeni, stati della comanda) vivono in Python puro, senza dipendere da FastAPI o Django. I framework sono adattatori intercambiabili.
3. **Test fin dal giorno 1.** La fase 7 approfondisce, ma pytest c'è sempre.
4. **Il frontend è sempre presente.** Dalla fase 2 ogni funzionalità ha anche la sua interfaccia.
5. **Ogni lezione finisce con un commit.** Messaggio chiaro, repo sempre verde.

## Formato di ogni lezione

1. **Concetto**: teoria breve e codice minimo
2. **Esercizio**: lo scrivi tu, poi code review
3. **Comanda**: il pezzo che entra nel progetto
4. **Gotcha**: gli errori tipici in produzione
5. **Appunti**: spazio per le note a mano sulla scheda stampata

---

## Fasi

### Fase 0 — Toolchain (≈2 sessioni)
uv, Python 3.14, struttura `src/`, pyproject.toml, ruff, pytest, pre-commit, Git e GitHub, PyCharm configurato.
**Comanda:** repo inizializzato, primo test verde, primo push.

### Fase 1 — Python moderno (≈5)
Type hints, `dataclass` e `enum`, `Protocol`, gestione errori ed eccezioni custom, context manager, generatori, `pathlib`, `decimal` per i soldi.
**Comanda:** modello di dominio del **menu** (Piatto, Categoria, Allergene) e import del menu da CSV con validazione e report errori. Calcolo del food cost.

### Fase 2 — HTTP a mano (≈4)
Cos'è davvero una richiesta HTTP. WSGI puro, poi ASGI. Routing, middleware, cookie e form scritti da te.
**Comanda:** **menu pubblico** servito dal tuo micro-framework, con template HTML e CSS mobile-first. Filtro per allergeni.
**Frontend:** HTML semantico, CSS moderno (custom properties, nesting, grid), prima interazione con HTMX.

### Fase 3 — Microframework (≈6)
Flask di passaggio (per vedere WSGI "vestito"), poi FastAPI in profondità: Pydantic, dependency injection, async/await, OpenAPI, gestione errori.
**Comanda:** API di **menu e prenotazioni**, con un form di prenotazione HTMX servito da FastAPI e Jinja2.

### Fase 4 — Dati (≈6)
PostgreSQL in locale, SQLAlchemy 2.0 (Core e ORM), Alembic, transazioni, vincoli, indici, problema N+1, query per i report.
**Comanda:** persistenza di menu, **tavoli, turni e prenotazioni**. Gestione della capienza a livello DB, con la concorrenza su due prenotazioni simultanee.

### Fase 5 — Architettura (≈5)
Service layer, repository, unit of work, porte e adattatori, configurazione 12-factor, moduli disaccoppiati, eventi di dominio.
**Comanda:** refactor completo. Il dominio diventa indipendente da FastAPI e SQLAlchemy, e il servizio prenotazioni si testa senza DB.

### Fase 6 — Django fatto bene (≈8)
Progetto modulare, custom user, ORM avanzato, admin personalizzato, permessi e ruoli, form, Django Ninja per le API, template e HTMX.
**Comanda:** **backoffice staff** (titolare, sala, cucina) e **comande** sala → cucina, riusando il dominio della fase 5. Confronto onesto FastAPI vs Django sullo stesso dominio.

### Fase 7 — Testing serio (≈4)
Fixture, factory, test di integrazione con Postgres vero, test delle view HTMX, coverage, mocking fatto bene (e quando non farlo).
**Comanda:** suite completa, che girerà in CI.

### Fase 8 — Async e background (≈5)
asyncio in profondità, Redis, coda di task, cache, Server-Sent Events / WebSocket. Su Windows qui si passa a **Docker Compose**.
**Comanda:** **email di conferma prenotazione**, **report di chiusura giornaliera**, schermo cucina con **comande in tempo reale**.

### Fase 9 — Deploy e ops (≈5)
Docker multi-stage, GitHub Actions (lint → test → build → deploy), Railway, confronto con Hetzner + Coolify, logging strutturato, Sentry, backup del DB.
**Comanda:** online con pipeline completa e ambiente di staging.

### Fase 10 — Scalabilità e sicurezza (≈4)
Profiling, caching avanzato, rate limiting, autenticazione (sessioni vs JWT), OWASP top 10, load test con Locust.
**Comanda:** hardening e test di carico simulando il sabato sera.

---

## Registro avanzamento

| Lezione | Data | Argomento | Fatto |
|---|---|---|---|
| 00 | | Toolchain | ☐ |
