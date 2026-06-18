# Kroky z výuky

## Step 01

```bash
python --version
git --version
code --version
```

## Step 02

Fork sdíleného repozitáře na svůj github

## Step 03

Clone do lokálu, do VSCode jako pracovní adresář

## Step 04

Spustit basic_version_terminal.py

## Step 05

```bash
python -m venv .venv
```

Aktivace:
```bash
# Windows
.venv\Scripts\activate
```

Instalace závislostí:
```bash
pip install -r requirements.txt
```

## Step 06

Plánovaná struktura projektu:

```
CrissCross/
├── basic_version_terminal.py   ← referenční implementace (monolitická)
├── README.md                   ← zadání projektu
├── how_to.md                   ← nápověda
├── CONTRIBUTING.md             ← pravidla pro Git
├── requirements.txt            ← závislosti
├── .gitignore                  ← co Git ignoruje
├── .pre-commit-config.yaml     ← konfigurace pre-commit hooků
├── modules/                    ← SEM patří třídy (zatím prázdné)
│   └── __init__.py
├── tests/                      ← testy
│   ├── __init__.py
│   └── test_board.py
└── .github/
    └── workflows/
        └── python-tests.yml    ← CI/CD konfigurace
```

## Step 07

readme.md

## Step 08

`modules/board.py` zatím stačí cvičný, prázdná třída class Board

```bash
git add modules/board.py
git commit -m "feat: přidat prázdnou třídu Board"
git push origin main
```

## Step 09

```bash
git checkout -b feature/board-class
```

```bash
git branch                    # zobrazí všechny lokální větve
git branch -a                 # včetně vzdálených (GitHub)
git checkout main             # přepne na main
git checkout feature/board-class  # přepne na větev
```
## Step 10

`.github/workflows/python-tests.yml`
