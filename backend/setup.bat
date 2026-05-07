@echo off
REM ============================================================================
REM  AutoConnect — Setup automatique du backend (Windows)
REM  Cree env/, installe les dependances, applique les migrations, seed la DB.
REM ============================================================================

echo.
echo === [1/5] Creation de l'environnement virtuel env/ ===
if not exist env (
    python -m venv env
    if errorlevel 1 (
        echo ERREUR: impossible de creer l'environnement virtuel.
        exit /b 1
    )
) else (
    echo env/ existe deja, on saute.
)

echo.
echo === [2/5] Activation de env/ ===
call env\Scripts\activate.bat

echo.
echo === [3/5] Installation des dependances ===
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo === [4/5] Application des migrations ===
python manage.py makemigrations users cars
python manage.py migrate

echo.
echo === [5/5] Chargement des donnees de demo ===
python manage.py seed_data

echo.
echo ============================================================================
echo  Setup termine ! Pour lancer le serveur :
echo     env\Scripts\activate
echo     python manage.py runserver
echo ============================================================================
