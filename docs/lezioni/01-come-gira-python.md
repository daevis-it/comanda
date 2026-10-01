# Lezione 01 — Come gira Python

**Fase 1 · Fondamenta · Tempo: 1–2 sere, senza fretta**

### Obiettivi

Alla fine di questa lezione saprai:

1. cosa succede davvero quando lanci un programma Python, e perché è diverso da C#
2. usare il **REPL**, la console interattiva, come campo di prova
3. leggere la sintassi base: indentazione, blocchi, commenti
4. cosa significa che Python è **dinamico ma forte**, e quali conseguenze ha
5. a cosa serve `if __name__ == "__main__":`
6. cosa hai fatto *davvero* nella Lezione 00: venv, pyproject, uv, src layout, ruff, pytest

Questa lezione non contiene codice di Comanda. Servono fondamenta solide prima di costruire.

---

## 1. Dal sorgente all'esecuzione: C# e Python a confronto

### 🔁 In C#

Quando fai `dotnet build` e poi `dotnet run`:

```
Program.cs ──(compilatore Roslyn)──► Program.dll (codice IL) ──(CLR + JIT)──► codice macchina
```

Il punto chiave è che il **compilatore legge tutto il codice prima di eseguire qualsiasi cosa**. Se scrivi il nome sbagliato di una variabile, oppure passi una `string` dove serve un `int`, la build fallisce e il programma non parte nemmeno. Il compilatore è il tuo primo controllore.

### In Python

```
programma.py ──(compilazione in bytecode, automatica e nascosta)──► bytecode ──(interprete CPython)──► esecuzione
```

Anche Python compila, ma in un modo molto diverso:

- **Non c'è un passaggio di build separato.** Lanci `python programma.py` e lui compila al volo e poi esegue.
- Il bytecode viene salvato nelle cartelle `__pycache__/` (i file `.pyc`). Le hai viste comparire nella Lezione 00: sono una cache, servono solo a non ricompilare ogni volta. Si possono cancellare senza problemi, e infatti stanno nel `.gitignore`.
- **La compilazione controlla solo la sintassi**, cioè parentesi, due punti, indentazione. **Non controlla** se una variabile esiste o se i tipi sono giusti. Quelle cose si scoprono **solo quando la riga viene eseguita**.

Questa è la differenza più importante di tutta la lezione. La vedrai con i tuoi occhi nell'esercizio 2.

> **"Interprete" = CPython.** Il programma `python.exe` che hai installato con uv si chiama *CPython*, perché è scritto in C. È l'implementazione standard: quando si dice "Python" si intende questa. Ne esistono altre (PyPy, ad esempio), ma noi useremo sempre CPython.

### ⚠️ La conseguenza pratica

In C# il compilatore trova tantissimi errori per te. In Python quel controllo automatico non c'è, quindi lo rimpiazziamo con tre strumenti:

| Chi | Cosa trova | Quando |
|---|---|---|
| **ruff** (linter) | variabili non definite, import inutilizzati, codice sospetto | mentre scrivi / prima del commit |
| **type checker** (lo vedremo in Lezione 10) | tipi sbagliati, se usi i type hints | mentre scrivi in PyCharm |
| **test** (pytest) | logica sbagliata, *e qualsiasi riga che i test eseguono* | quando lanci i test |

È per questo che nella Lezione 00 li abbiamo configurati *subito*, prima di scrivere codice vero. In Python sono la rete di sicurezza che in C# ti dà il compilatore.

---

## 2. Il REPL: la tua console di prova

**REPL** sta per *Read–Eval–Print Loop*: legge una riga, la esegue, stampa il risultato e ricomincia. È lo strumento più utile per imparare Python, perché puoi provare ogni cosa in un secondo senza creare file.

> 🔁 **In C#** l'equivalente esiste (C# Interactive in Visual Studio, `dotnet-script`), ma quasi nessuno lo usa. In Python invece il REPL si usa tutti i giorni, anche da esperti.

### Aprirlo

Dal terminale di PyCharm, nella cartella `comanda`:

```powershell
uv run python
```

Vedrai qualcosa come:

```
Python 3.14.5 (...) on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

`>>>` è il prompt: Python aspetta un'istruzione. Per uscire scrivi `exit()` oppure premi `Ctrl+Z` e poi `Invio`.

> PyCharm ha anche una **Python Console** integrata (menu *Tools → Python or Debug Console*). Fa la stessa cosa, con in più l'autocompletamento e la vista delle variabili. Usa quella che preferisci.

### 🧪 Prova tu

Scrivi una riga alla volta. **Prima di premere Invio prova a indovinare il risultato.**

```python
>>> 2 + 3
>>> 7 / 2
>>> 7 // 2
>>> 2 ** 100
>>> "ciao" * 3
>>> len("Comanda")
>>> type(42)
>>> type("42")
>>> type(3.5)
```

Cose da notare:

- **Nel REPL non serve `print()`.** Se scrivi un'espressione, il REPL ne mostra il valore. In un file `.py` invece serve `print()`, altrimenti non vedi niente.
- `7 / 2` dà `3.5`, **non** `3` come in C# con due `int`. In Python `/` è *sempre* una divisione con virgola. La divisione intera è `//`.
- `2 ** 100` è l'elevamento a potenza, e restituisce un numero enorme senza andare in overflow. In Python gli `int` **non hanno limite di dimensione**. In C# un `long` si sarebbe fermato a circa 9×10¹⁸.

### Due funzioni da ricordare: `help()` e `dir()`

```python
>>> help(len)          # documentazione di una funzione (esci con q)
>>> dir("ciao")        # tutti i metodi disponibili su una stringa
>>> "ciao".upper()
```

`dir()` è un po' il tuo IntelliSense nel REPL. Ignora per ora i nomi con i doppi underscore (`__add__` e simili): li vedremo nella Lezione 09.

---

## 3. La sintassi base: indentazione al posto delle graffe

La stessa funzione nei due linguaggi:

```csharp
// C#
public static decimal PrezzoConCoperto(decimal prezzo, int persone)
{
    // il coperto è 2 euro a persona
    if (persone <= 0)
    {
        throw new ArgumentException("Almeno una persona");
    }
    return prezzo + 2m * persone;
}
```

```python
# Python
def prezzo_con_coperto(prezzo, persone):
    # il coperto è 2 euro a persona
    if persone <= 0:
        raise ValueError("Almeno una persona")
    return prezzo + 2 * persone
```

Le differenze, una per una:

| C# | Python | Note |
|---|---|---|
| `{ }` delimitano i blocchi | **l'indentazione** delimita i blocchi | Non è stile, è sintassi: se sbagli l'indentazione il programma è sbagliato o non parte |
| `if (...)` | `if ...:` | Niente parentesi obbligatorie, ma **i due punti `:` aprono il blocco** |
| `;` a fine riga | niente | Una riga = un'istruzione |
| `// commento` | `# commento` | |
| `throw new ...` | `raise ...` | Le eccezioni le vediamo nella Lezione 11 |
| `PascalCase` per i metodi | `snake_case` per funzioni e variabili | `PascalCase` solo per le classi. È la convenzione **PEP 8**, la guida di stile ufficiale, e ruff la fa rispettare |
| tipi dichiarati (`decimal prezzo`) | nessun tipo obbligatorio | Si possono aggiungere *type hints* facoltativi (Lezione 10) |
| `public static` | niente | In Python non ci sono modificatori di accesso (Lezione 08) |

**Indentazione: 4 spazi, mai tab.** PyCharm lo fa da solo. Se mescoli tab e spazi, Python dà errore.

---

## 4. Dinamico ma forte: cosa significa

Sono due proprietà diverse, e spesso vengono confuse.

**Statico o dinamico** dice *quando* si controllano i tipi:
- C# è **statico**: ogni variabile ha un tipo fisso, deciso quando scrivi il codice e controllato dal compilatore.
- Python è **dinamico**: le variabili *non hanno* un tipo. Il tipo ce l'hanno **i valori**, e viene controllato durante l'esecuzione.

**Forte o debole** dice *quanto* il linguaggio converte i tipi da solo:
- Python è **forte**: non mescola tipi diversi senza che glielo chiedi.
- JavaScript è **debole**: converte tutto in silenzio (`"3" + 4` dà `"34"`).

### 🧪 Prova tu (nel REPL)

```python
>>> x = 5
>>> type(x)
>>> x = "cinque"
>>> type(x)
```

È tutto lecito: `x` è solo un **nome**. Prima indicava un intero, poi una stringa. In C# `var x = 5; x = "cinque";` non compila.

```python
>>> "3" + 4
```

Otterrai:

```
TypeError: can only concatenate str (not "int") to str
```

Python si rifiuta di indovinare cosa intendevi. Per farlo funzionare devi convertire in modo esplicito:

```python
>>> "3" + str(4)      # '34'  → concatenazione tra stringhe
>>> int("3") + 4      # 7     → somma tra numeri
```

> 🔁 **Curiosità:** in C# `"3" + 4` *compila* e dà `"34"`, perché l'operatore `+` con una stringa converte l'altro operando. Su questo punto Python è più rigido di C#.

### ⚠️ Cosa ti porti via

- Un nome può essere riassegnato a un valore di qualsiasi tipo. Si *può* fare, ma nel codice serio **non si fa**: confonde chi legge. I type hints (Lezione 10) servono proprio a dichiarare le intenzioni.
- Gli errori di tipo esistono anche in Python, ma arrivano **durante l'esecuzione**, non alla build.

Il concetto di "nome che indica un valore" è più profondo di quanto sembri, e ha conseguenze importanti (ad esempio quando passi una lista a una funzione). Ci dedichiamo **tutta la Lezione 02**.

---

## 5. Script, moduli e `if __name__ == "__main__":`

### Ogni file `.py` è un modulo

In Python **ogni file `.py` è un modulo**, cioè un'unità di codice che può essere:

1. **eseguita direttamente**: `uv run python file.py`
2. **importata** da un altro file: `import file`

> 🔁 **In C#** c'è una separazione netta: c'è *un solo* punto d'ingresso (`static void Main` o i top-level statements in `Program.cs`), e tutte le altre classi sono librerie. In Python qualsiasi file può fare l'una e l'altra cosa.

### Il problema

Quando importi un modulo, **Python esegue tutto il suo codice dall'alto verso il basso**. Le definizioni (`def`) creano funzioni, ma le istruzioni "sciolte" come `print(...)` vengono eseguite davvero, anche durante un import. Spesso questo non è quello che vuoi.

### La soluzione: `__name__`

Ogni modulo ha una variabile speciale, `__name__`, che Python imposta in automatico:

- se il file viene **eseguito direttamente** → `__name__` vale `"__main__"`
- se il file viene **importato** → `__name__` vale il nome del modulo (es. `"modulo_b"`)

Per questo il codice "da eseguire solo se lancio questo file" si mette sotto:

```python
if __name__ == "__main__":
    # eseguito solo se lanci questo file, NON quando qualcuno lo importa
    ...
```

È l'equivalente pratico del tuo `Main`. Lo vedrai funzionare nell'esercizio 3.

---

## 6. Cosa hai fatto davvero nella Lezione 00

Nella Lezione 00 hai eseguito i comandi senza che ti spiegassi cosa facevano. Rimediamo adesso, partendo da quello che conosci in .NET.

### Tabella di traduzione

| Python (uv) | .NET | Cos'è |
|---|---|---|
| `uv python install 3.14` | installare il .NET SDK | L'interprete, cioè il "runtime" |
| `.python-version` | `global.json` | Fissa la versione dell'interprete per il progetto |
| `pyproject.toml` | file `.csproj` | Nome, versione, dipendenze, configurazione dei tool |
| `uv add pacchetto` | `dotnet add package` | Aggiunge una dipendenza |
| `uv.lock` | `packages.lock.json` | Le versioni *esatte* di tutte le dipendenze, comprese quelle indirette |
| PyPI (pypi.org) | NuGet.org | Il registro pubblico dei pacchetti |
| `.venv/` | *(non c'è un equivalente diretto, vedi sotto)* | L'ambiente isolato del progetto |
| `uv run ...` | `dotnet run` | Esegue un comando dentro l'ambiente del progetto |
| ruff | analyzer Roslyn + `dotnet format` | Linter e formattatore |
| pytest | xUnit / NUnit | Framework di test |
| pre-commit | Husky.NET | Comandi lanciati in automatico prima di ogni commit |

### Il virtual environment (`.venv`): perché esiste

In .NET ogni progetto dichiara le sue dipendenze nel `.csproj`. NuGet le scarica in una cache globale e ogni progetto usa le sue versioni. L'isolamento c'è di default, e non ci hai mai dovuto pensare.

In Python, storicamente, i pacchetti venivano installati **dentro l'interprete stesso**: un'unica cartella condivisa da tutti i progetti del PC. Se il progetto A voleva Django 4 e il progetto B Django 5, avevi un conflitto senza soluzione.

Il **virtual environment** risolve il problema. È una cartella (`.venv`) che contiene:

```
.venv/
├── Scripts/
│   └── python.exe        ← un interprete "privato" del progetto (su Windows)
└── Lib/
    └── site-packages/    ← i pacchetti installati SOLO per questo progetto
```

Ogni progetto ha il suo `.venv` con i suoi pacchetti. Non si committa su Git: si ricrea in qualsiasi momento da `pyproject.toml` + `uv.lock`, proprio come le cartelle `bin/` e `obj/` in .NET.

### Cosa fa `uv run`

Quando scrivi `uv run pytest`, uv:

1. controlla che `.venv` esista, altrimenti lo crea
2. controlla che i pacchetti installati corrispondano a `uv.lock`, altrimenti li sincronizza
3. esegue `pytest` **usando l'interprete e i pacchetti di `.venv`**

Per questo non devi mai "attivare" il venv a mano. Nelle guide vecchie troverai `.venv\Scripts\activate`: con uv non serve.

> 🧪 **Prova tu:** guarda dentro `.venv\Lib\site-packages`. Troverai le cartelle di `pytest`, `ruff` e degli altri pacchetti. Sono "le DLL" del tuo progetto.

### Il layout `src/` e il package `comanda`

```
comanda/                    ← la cartella del progetto (la "solution", diciamo)
├── pyproject.toml
├── src/
│   └── comanda/            ← il PACKAGE: questo è il codice che si distribuisce
│       ├── __init__.py
│       └── money.py
└── tests/                  ← i test: NON fanno parte del package
```

- Un **package** è una cartella che contiene un file `__init__.py`. Dall'esterno si importa con `import comanda`. È più o meno l'equivalente di un namespace contenuto in un assembly.
- `__init__.py` viene eseguito la prima volta che importi il package. Può anche essere vuoto: serve a dire "questa cartella è un package". Ne parliamo nella Lezione 07.
- Come fa `import comanda` a funzionare da qualsiasi punto? Durante la prima `uv run`, uv ha **installato il tuo progetto dentro `.venv`** in modalità *editable*: invece di copiare i file, crea un collegamento a `src/comanda`. Se modifichi un file, la modifica è subito visibile. È come una *project reference* in Visual Studio.

**Perché i test non vanno dentro `src/comanda/`:** tutto quello che sta lì dentro *è* il prodotto. Se un giorno pubblichi il pacchetto o lo metti in un'immagine Docker, i test finirebbero in produzione. È come mettere le classi di xUnit dentro il progetto principale invece che in un progetto `.Tests` separato.

---

## 7. Sistemiamo la Lezione 00 (passo per passo)

Adesso che sai cosa sono i vari pezzi, le correzioni hanno senso.

### 7.1 Spostare il test

1. In PyCharm, tasto destro sulla cartella `comanda` (la radice) → *New → Directory* → `tests`
2. Trascina `../../tests/test_money.py` dentro `tests/`. Se PyCharm chiede di aggiornare i riferimenti, rispondi sì: non cambia nulla, perché il test fa già `from comanda.money import euro`
3. Esegui:

```powershell
uv run pytest
```

Devi vedere `2 passed`. Il test funziona anche fuori da `src/` proprio perché `comanda` è installato nel venv (vedi sopra).

### 7.2 Rimuovere lo script rotto

In `pyproject.toml` cancella queste righe:

```toml
[project.scripts]
comanda = "comanda:main"
```

**Cosa facevano:** dicevano "crea un comando `comanda` che, quando lo lanci, esegue la funzione `main` del package `comanda`". `uv init` aveva generato quella funzione `main` dentro `__init__.py`. Tu l'hai sostituita con `__version__`, e quindi lo script puntava a una funzione che non esiste più. Lo rimetteremo quando ci servirà una CLI vera.

### 7.3 Versione di Python

In `pyproject.toml` cambia:

```toml
requires-python = ">=3.14"
```

`>=3.14.5` vuol dire "rifiuta qualsiasi Python 3.14 più vecchio della patch 5". È un vincolo troppo stretto e senza motivo: le patch release correggono solo bug. La versione esatta che usi tu la fissa già `.python-version`.

### 7.4 A-capo (CRLF e LF)

Windows termina le righe con due caratteri (`\r\n`, detto CRLF), Linux con uno solo (`\n`, detto LF). I server su cui gira il codice sono Linux.

1. PyCharm → *Settings → Editor → Code Style* → **Line separator: Unix and macOS (\n)**
2. Per convertire i file già esistenti: selezionali nel pannello del progetto → menu *File → File Properties → Line Separators → LF*
3. Poi, nel terminale:

```powershell
git add --renormalize .
git status
```

### 7.5 Import mode di pytest

In `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra --strict-markers --import-mode=importlib"
```

Per ora prendila come una regola di configurazione. Il motivo (due file di test con lo stesso nome in cartelle diverse vanno in conflitto) lo capirai bene nella Lezione 07 sugli import.

Commit:

```powershell
git add .
git commit -m "chore: sistemati test, script e versione python dopo review"
```

---

## 8. Esercizi

Crea la cartella `esercizi/lezione01/` nella radice del progetto, accanto a `src/` e `tests/`. Ogni esercizio è un file a sé.

### Esercizio 1 — Indovina il tipo

File `esercizi/lezione01/tipi.py`:

```python
valori = [42, 3.14, "ciao", True, None, [1, 2], (1, 2), {"a": 1}, {1, 2}]

for valore in valori:
    print(repr(valore), "->", type(valore))
```

**Prima di eseguirlo**, scrivi su carta il tipo che ti aspetti per ciascun valore. Poi lancia:

```powershell
uv run python esercizi/lezione01/tipi.py
```

Output atteso:

```
42 -> <class 'int'>
3.14 -> <class 'float'>
'ciao' -> <class 'str'>
True -> <class 'bool'>
None -> <class 'NoneType'>
[1, 2] -> <class 'list'>
(1, 2) -> <class 'tuple'>
{'a': 1} -> <class 'dict'>
{1, 2} -> <class 'set'>
```

Da notare:
- `None` è l'equivalente di `null`. Ha un tipo tutto suo, `NoneType`.
- `[...]` è una lista, `(...)` è una tupla, `{...}` con le coppie `chiave: valore` è un dizionario, `{...}` senza coppie è un set. Li vedremo per bene nella Lezione 04.
- `repr()` mostra il valore "come lo scriveresti nel codice", per esempio con le virgolette per le stringhe. È più o meno il `ToString()` pensato per chi programma.
- `for valore in valori:` è un `foreach`. In Python il `for` funziona **sempre** così (Lezione 05).

### Esercizio 2 — L'errore nascosto (il più importante)

File `esercizi/lezione01/sconto.py`. **Copialo esattamente, compreso l'errore di battitura** (`percentuale_scnto`):

```python
def prezzo_finale(prezzo, codice_sconto):
    if codice_sconto == "AMICI10":
        return prezzo - prezzo * percentuale_scnto
    return prezzo


print(prezzo_finale(20, None))
print(prezzo_finale(20, "AMICI10"))
```

**Passo A.** Commenta l'ultima riga (metti `#` all'inizio) ed esegui:

```powershell
uv run python esercizi/lezione01/sconto.py
```

Stampa `20` e **nessun errore**. Eppure il codice contiene una variabile che non esiste. In C# non avrebbe nemmeno compilato.

**Passo B.** Togli il commento ed esegui di nuovo. Ora ottieni:

```
NameError: name 'percentuale_scnto' is not defined
```

L'errore esisteva anche prima, ma Python se ne accorge **solo quando esegue quella riga**. Pensa se questo ramo fosse stato il calcolo dello sconto in un ristorante, eseguito una volta al mese.

**Passo C.** Lancia il linter:

```powershell
uv run ruff check esercizi/lezione01/sconto.py
```

```
F821 Undefined name `percentuale_scnto`
```

ruff l'ha trovato **senza eseguire niente**, come avrebbe fatto il compilatore C#. Questo è il motivo per cui ruff e pre-commit ci sono dal primo giorno.

**Passo D.** Correggi: aggiungi `percentuale_sconto = 0.10` come prima riga del file, correggi il nome nella funzione ed esegui. Ora funziona. (Sì, `0.10` è un `float` e coi soldi sarebbe sbagliato: lo sistemiamo nella Lezione 03.)

> Se provi a committare la versione con l'errore, pre-commit la blocca. Provaci pure: è istruttivo.

### Esercizio 3 — `__name__` in azione

Due file nella stessa cartella.

`esercizi/lezione01/modulo_b.py`:

```python
print("modulo_b caricato, __name__ =", __name__)


def saluta():
    return "ciao da modulo_b"
```

`esercizi/lezione01/modulo_a.py`:

```python
import modulo_b

print("modulo_a in esecuzione, __name__ =", __name__)

if __name__ == "__main__":
    print(modulo_b.saluta())
```

**Prima di eseguire**, prova a prevedere: quante righe verranno stampate, in che ordine, e con quali valori di `__name__`?

```powershell
uv run python esercizi/lezione01/modulo_a.py
```

Output:

```
modulo_b caricato, __name__ = modulo_b
modulo_a in esecuzione, __name__ = __main__
ciao da modulo_b
```

Ragionaci su:
1. La **prima riga** arriva da `modulo_b`, perché `import modulo_b` *esegue* il file. Il `print` sta "sciolto" nel modulo, quindi parte durante l'import.
2. In `modulo_b`, `__name__` vale `"modulo_b"` perché è stato *importato*.
3. In `modulo_a`, `__name__` vale `"__main__"` perché è il file che hai *lanciato*.

**Variante:** lancia direttamente `modulo_b.py`. Cosa stampa adesso, e perché?

> ⚠️ `import modulo_b` funziona perché quando lanci uno script, Python aggiunge la sua cartella a quelle in cui cerca i moduli. È un meccanismo che sembra comodo ma è fragile. Nella Lezione 07 vedremo il modo corretto di organizzare gli import.

### Esercizio 4 — Il REPL come calcolatrice da ristorante

Nel REPL, usando solo quello che hai visto oggi:

1. Un tavolo da 4 ordina 2 ceviche da 14 €, 1 lomo saltado da 18 € e 4 chicha da 4 €. Coperto 2 € a persona. Calcola il totale.
2. Dividilo per 4: cosa ottieni con `/` e cosa con `//`? Quale delle due ti serve per dividere il conto?
3. Prova `0.1 + 0.2`. Il risultato ti sembra giusto? (Tienilo a mente per la Lezione 03.)

---

## 9. ✔️ Verifica

Rispondi senza guardare la scheda. Le risposte sono in fondo.

1. Python è compilato o interpretato?
2. Perché un errore di battitura in un nome di variabile può restare nascosto per mesi in Python e non in C#?
3. Che differenza c'è tra "dinamico" e "debole"? Python è dinamico, debole, o tutti e due?
4. Cosa contiene la cartella `.venv` e perché non si committa?
5. Che valore ha `__name__` in un file importato? E in quello lanciato direttamente?
6. Perché i test non vanno dentro `src/comanda/`?
7. Cosa fa `uv run` prima di eseguire il comando?

---

## 10. Glossario C# → Python (da tenere a portata di mano)

| C# | Python |
|---|---|
| `null` | `None` |
| `true` / `false` | `True` / `False` (con la maiuscola!) |
| `&&` / `\|\|` / `!` | `and` / `or` / `not` |
| `//` commento | `#` commento |
| `foreach (var x in lista)` | `for x in lista:` |
| `throw` | `raise` |
| `catch` | `except` |
| `this` | `self` (Lezione 08) |
| `using System.IO;` | `import os` / `from pathlib import Path` (Lezione 07) |
| `static void Main` | `if __name__ == "__main__":` |
| `Console.WriteLine(x)` | `print(x)` |
| `x.ToString()` | `str(x)` |
| `int.Parse("3")` | `int("3")` |
| `list.Count` / `str.Length` | `len(list)` / `len(str)` |
| `PascalCase` metodi | `snake_case` funzioni e metodi |
| NuGet | PyPI |
| `.csproj` | `pyproject.toml` |

---

## ✏️ Appunti

&nbsp;

&nbsp;

&nbsp;

&nbsp;

---

## Risposte alla verifica

1. **Tutte e due.** Python compila il sorgente in bytecode (in automatico, e lo mette in cache in `__pycache__`), poi l'interprete esegue il bytecode. Però non c'è un compilatore che controlla tipi e nomi come in C#.
2. Perché la compilazione in bytecode controlla solo la sintassi. Un nome inesistente viene scoperto solo quando quella riga viene eseguita. Se la riga sta in un ramo raro, l'errore resta lì finché quel ramo non viene eseguito. Il rimedio sono il linter (ruff) e i test.
3. "Dinamico" riguarda *quando* si controllano i tipi: durante l'esecuzione, e le variabili non hanno un tipo fisso. "Debole" riguarda *quanto* il linguaggio converte i tipi da solo. Python è **dinamico ma forte**: `"3" + 4` è un errore, non una conversione silenziosa.
4. Un interprete Python "privato" e i pacchetti installati solo per quel progetto (`Lib/site-packages`). Non si committa perché si può ricreare in qualsiasi momento da `pyproject.toml` + `uv.lock`, come `bin/` e `obj/` in .NET.
5. In un file importato vale il nome del modulo (es. `"modulo_b"`). In quello lanciato direttamente vale `"__main__"`.
6. Perché tutto quello che sta in `src/comanda/` è il prodotto distribuito: i test finirebbero in produzione. Vanno in `tests/`, l'equivalente di un progetto `.Tests` separato.
7. Controlla che `.venv` esista e che i pacchetti installati corrispondano a `uv.lock` (se serve li sincronizza). Poi esegue il comando usando l'interprete e i pacchetti del venv.
