# Comanda — Roadmap del corso

**Inizio:** 1 ottobre 2026 · **Ritmo:** circa 1 ora a sera · **Punto di partenza:** sviluppatore C#, Python ancora poco familiare.

## Come funziona questo corso

1. **Si parte da C#.** Ogni concetto Python viene confrontato con quello che già conosci. Dove i due linguaggi si somigliano andiamo veloci, dove sono diversi ci fermiamo.
2. **Niente fretta.** Una lezione finisce quando l'hai capita, non quando scade l'ora. Se una scheda richiede tre sere, va bene così: le stime qui sotto sono indicative.
3. **Spiegare prima di usare.** Nessuno strumento o costrutto entra nel codice senza essere stato spiegato: cos'è, perché esiste, cosa succede se non lo usi.
4. **Prima senza magia, poi il framework.** Ogni astrazione la scrivi a mano almeno una volta, poi vedi come la risolve il framework.
5. **Il dominio al centro.** Le regole del ristorante vivono in Python puro. FastAPI e Django sono "prese" che ci attacchiamo sopra.
6. **Il frontend c'è sempre.** Dalla Fase 2 ogni funzionalità ha anche la sua interfaccia: template + HTMX + Alpine.js + CSS moderno.

## Come sono fatte le schede

| Simbolo | Significato |
|---|---|
| 🔁 **In C#** | Il confronto con quello che già conosci |
| 🧪 **Prova tu** | Da fare subito, nel REPL o in un file. Prima prova a prevedere il risultato, poi esegui |
| ⚠️ **Attenzione** | Trappole tipiche, soprattutto per chi viene da C# |
| ✔️ **Verifica** | Domande di autoverifica, con le risposte in fondo alla scheda |

Gli esercizi stanno in `esercizi/lezioneNN/`, separati dal codice di Comanda (`src/`).

---

## Fase 0 — Toolchain ✅
Lezione 00: uv, pyproject, ruff, pytest, pre-commit, Git e GitHub. *(Fatta. La Lezione 01 spiega con calma cosa hai fatto.)*

## Fase 1 — Fondamenta Python, partendo da C# (≈ 6 settimane)

| # | Lezione | Cosa impari |
|---|---|---|
| 01 | **Come gira Python** | Interprete e compilatore, REPL, script e moduli, `__name__`, tipizzazione dinamica ma forte. Cosa sono davvero venv, pyproject e `uv run` |
| 02 | **Nomi e oggetti** | In Python le variabili sono etichette, non scatole. Riferimenti, mutabile e immutabile, `is` e `==`, `None` |
| 03 | **Tipi base** | `int` senza limiti, `float` e i suoi tranelli, `Decimal`, stringhe (f-string, slicing, metodi), `bool` e la "truthiness" |
| 04 | **Collezioni** | `list`, `tuple`, `dict`, `set` confrontati con `List<T>`, `Dictionary`, `HashSet`. Le comprehension come alternativa a LINQ |
| 05 | **Controllo di flusso** | `if`, `for` sugli iterabili (non c'è il `for(i=0;…)`), `enumerate`, `zip`, `while`, `match` |
| 06 | **Funzioni** | Argomenti posizionali e per nome, valori di default (e la trappola dei default mutabili), `*args` e `**kwargs`, funzioni come valori, lambda |
| 07 | **Moduli e package** | `import` rispetto a `using`/namespace, `__init__.py`, import assoluti e relativi, il layout `src/` |
| 08 | **Classi (1)** | `class`, `self` esplicito, `__init__` rispetto al costruttore, attributi, `_privato` per convenzione, `@property` |
| 09 | **Classi (2)** | Metodi "dunder" (`__str__`, `__eq__`, `__hash__`…) come equivalenti di ToString/Equals/operatori, ereditarietà, `super()` |
| 10 | **Type hints** | Perché esistono in un linguaggio dinamico, cosa controllano (e cosa no), PyCharm e i type checker, i generics |
| 11 | **Eccezioni** | `try/except/else/finally`, EAFP e LBYL, gerarchia delle eccezioni, eccezioni custom, `with` rispetto a `using` |
| 12 | **dataclass ed enum** | Comanda, primo pezzo: il modello del **menu** con piatti, categorie e i 14 allergeni UE |
| 13 | **Iteratori e generatori** | `yield` (lo conosci da C#!), iterazione "lazy", generator expression |
| 14 | **File e CSV** | `pathlib`, encoding, modulo `csv`. Comanda: **import del menu da CSV** con report degli errori |
| 15 | **pytest per davvero** | Test, fixture e parametrize confrontati con xUnit/NUnit. Comanda: la suite di test del dominio |

## Fase 2 — Il web senza magia (≈ 3 settimane)
Come funziona HTTP dal punto di vista del server. WSGI scritto a mano, un micro-framework tuo con routing, template e form.
**Comanda:** menu pubblico consultabile dal telefono, con filtro allergeni. Primo HTML/CSS e prima interazione HTMX.

## Fase 3 — FastAPI (≈ 4 settimane)
Flask giusto per un assaggio, poi FastAPI con calma: Pydantic, dependency injection (che conosci da ASP.NET), async/await (che conosci da C#), OpenAPI.
**Comanda:** API di menu e prenotazioni, form di prenotazione HTMX.

## Fase 4 — Database (≈ 4 settimane)
PostgreSQL, SQL quanto basta, SQLAlchemy 2.0 (l'equivalente di Entity Framework), migrazioni con Alembic, transazioni.
**Comanda:** tavoli, turni, prenotazioni, controllo della capienza.

## Fase 5 — Architettura (≈ 3 settimane)
Service layer, repository, unit of work, porte e adattatori. Qui il tuo background C# torna utile, perché sono pattern molto diffusi in .NET.
**Comanda:** dominio indipendente dal framework e dal DB.

## Fase 6 — Django (≈ 5 settimane)
Progetto modulare, ORM, admin, autenticazione e ruoli, form, template + HTMX.
**Comanda:** backoffice staff e comande sala → cucina, riusando il dominio della Fase 5.

## Fase 7 — Testing avanzato (≈ 2 settimane)
Test di integrazione con il DB, test delle view, coverage, mocking.

## Fase 8 — Async e lavori in background (≈ 3 settimane)
asyncio, Redis, code di task, aggiornamenti in tempo reale. Docker Compose.
**Comanda:** email di conferma, report di chiusura giornaliera, schermo cucina in tempo reale.

## Fase 9 — Deploy (≈ 3 settimane)
Docker, GitHub Actions, Railway (confronto con Hetzner + Coolify), log, monitoraggio, backup.
**Comanda:** online, con una pipeline completa.

## Fase 10 — Scalabilità e sicurezza (≈ 2 settimane)
Profiling, cache, rate limiting, autenticazione, OWASP, test di carico.

**Durata complessiva indicativa:** 8–9 mesi a un'ora per sera. La Fase 1 è quella che conta di più: se le fondamenta sono solide, tutto il resto va molto più veloce.

---

## Registro avanzamento

| Lezione | Data | Argomento | Note |
|---|---|---|---|
| 00 | 01/10/2026 | Toolchain | ✅ |
| 01 | | Come gira Python | |
