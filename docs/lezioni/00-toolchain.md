# Lezione 00 — Toolchain

**Fase 0 · Durata stimata: 1–2 sessioni**

**Obiettivo:** a fine lezione hai un repo Python moderno, con lint e test automatici, su GitHub, e PyCharm configurato. È il template da cui nasceranno tutti i tuoi progetti futuri.

---

## 1. Concetto: perché uv

Fino a pochi anni fa per fare queste cose servivano strumenti diversi:

| Cosa | Prima | Ora |
|---|---|---|
| Installare Python | python.org / pyenv | `uv python install` |
| Ambiente virtuale | `python -m venv` | `uv venv` (automatico) |
| Dipendenze | pip + requirements.txt | `uv add` → pyproject.toml + uv.lock |
| Eseguire | attivare il venv | `uv run` |
| Tool globali | pipx | `uv tool install` |

uv è un unico binario scritto in Rust, ed è molto più veloce di pip. Il file **uv.lock** fissa le versioni esatte di tutto l'albero delle dipendenze: in locale, in CI e in produzione giri lo stesso codice. Il lockfile va **sempre committato**.

**pyproject.toml** è lo standard (PEP 621) che sostituisce setup.py, requirements.txt, setup.cfg e i file di configurazione sparsi dei vari tool.

---

## 2. Installazione (PowerShell)

```powershell
# uv
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# chiudi e riapri il terminale (il PATH va ricaricato), poi:
uv --version
uv python install 3.14
uv python list
```

> **Gotcha Windows:** se `uv` non viene trovato, il terminale (o PyCharm) è stato aperto prima dell'installazione. Riavvialo; per PyCharm serve proprio chiuderlo e riaprirlo.

---

## 3. Inizializza Comanda

Dentro `C:\Users\Davide\Dev\Python\comanda`:

```powershell
uv init --package --name comanda --python 3.14 .
```

`--package` crea il **layout src/**:

```
comanda/
├── .python-version
├── pyproject.toml
├── README.md
└── src/
    └── comanda/
        └── __init__.py
```

**Perché src/ e non la cartella del pacchetto direttamente nella root?** Perché così i test girano contro il pacchetto *installato*, non contro file che Python trova "per caso" nella cartella corrente. È un'intera classe di bug del tipo "da me funziona" che sparisce.

```powershell
uv run python -c "import comanda; print('ok')"
```

La prima volta uv crea `.venv/` e installa il pacchetto in modalità editable.

---

## 4. Dipendenze di sviluppo

```powershell
uv add --dev ruff pytest pytest-cov pre-commit
```

Apri pyproject.toml: le trovi nel gruppo `[dependency-groups] dev`. Non finiscono in produzione.

### Configura ruff e pytest (in pyproject.toml)

```toml
[tool.ruff]
line-length = 100
target-version = "py314"

[tool.ruff.lint]
select = [
    "E", "F",   # errori base (pycodestyle, pyflakes)
    "I",        # ordinamento import
    "UP",       # sintassi moderna
    "B",        # bug comuni (bugbear)
    "SIM",      # semplificazioni
    "RUF",      # regole ruff
]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra --strict-markers"
```

---

## 5. Primo codice + primo test

`src/comanda/__init__.py`:

```python
__version__ = "0.1.0"
```

`src/comanda/money.py`. È il primo pezzo di dominio vero: i soldi **non** si rappresentano mai come `float`.

```python
from decimal import ROUND_HALF_UP, Decimal


def euro(value: str | int | Decimal) -> Decimal:
    """Converte in Decimal arrotondato al centesimo."""
    return Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
```

`tests/test_money.py`:

```python
from decimal import Decimal

from comanda.money import euro


def test_euro_arrotonda_al_centesimo():
    assert euro("12.345") == Decimal("12.35")


def test_float_e_il_male():
    assert 0.1 + 0.2 != 0.3  # ecco perché
    assert euro("0.1") + euro("0.2") == euro("0.3")
```

```powershell
uv run pytest
uv run ruff check .
uv run ruff format .
```

> **Domanda da annotare:** perché `euro()` accetta `str` ma non `float`? Prova `Decimal(0.1)` nel REPL e guarda cosa esce.

---

## 6. Git e GitHub

Crea `.gitattributes` **prima** del primo commit:

```
* text=auto eol=lf
```

> **Gotcha Windows:** senza questo file Git converte gli a-capo in CRLF, e poi Docker e Linux in produzione si lamentano (gli script shell si rompono con `\r`). Va sistemato una volta per tutte, subito.

Il `.gitignore` deve contenere almeno:

```
.venv/
__pycache__/
*.pyc
.pytest_cache/
.ruff_cache/
.coverage
htmlcov/
.env
.idea/
```

> `.idea/` intero o solo in parte? Per un solo dev ignorarlo tutto va bene. Il `.env` **non** si committa mai: dalla fase 3 ci finiscono i segreti.

Poi:

```powershell
git init -b main
git add .
git commit -m "chore: bootstrap progetto con uv, ruff, pytest"
```

Crea il repo `comanda` su GitHub (privato), poi `git remote add origin ...` e `git push -u origin main`.

---

## 7. pre-commit: il guardiano

`.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.x.x   # metti l'ultima versione (vedi la pagina GitHub del repo)
    hooks:
      - id: ruff-check
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-added-large-files
```

```powershell
uv run pre-commit install
uv run pre-commit autoupdate      # aggiorna le rev all'ultima versione
uv run pre-commit run --all-files
```

**Prova:** scrivi apposta `import os` inutilizzato in `money.py` e tenta un commit. Il commit viene bloccato o corretto. È esattamente quello che vogliamo.

---

## 8. PyCharm

1. **Interprete:** Settings → Project → Python Interpreter → Add → seleziona l'ambiente uv esistente (`.venv\Scripts\python.exe`). Le versioni recenti di PyCharm riconoscono uv direttamente.
2. **Sources root:** tasto destro su `src/` → *Mark Directory as* → *Sources Root*.
3. **Test runner:** Settings → Tools → Python Integrated Tools → Default test runner: **pytest**.
4. **Ruff:** installa il plugin Ruff (o usa il supporto integrato se la tua versione ce l'ha) e attiva il format on save.
5. **Terminale:** verifica che il terminale integrato sia PowerShell e che `uv` venga trovato.

---

## ✅ Checklist di fine lezione

- [ ] `uv run pytest` → verde
- [ ] `uv run ruff check .` → nessun errore
- [ ] pre-commit blocca un commit sporco
- [ ] Repo su GitHub con `uv.lock` e `.gitattributes`
- [ ] PyCharm esegue i test dal pulsante ▶ verde accanto alla funzione
- [ ] Riga aggiornata nel registro della ROADMAP

## 🧠 Gotcha riassunto

- Riavvia terminale e PyCharm dopo aver installato uv
- `.gitattributes` con `eol=lf` prima del primo commit
- `uv.lock` si committa, `.venv/` no
- Mai `float` per i soldi
- Non attivare il venv a mano: `uv run` fa tutto

## ✏️ Appunti

&nbsp;

&nbsp;

&nbsp;
