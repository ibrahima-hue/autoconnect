#!/usr/bin/env bash
# =============================================================================
#  AutoConnect — Setup automatique du backend (Linux/macOS)
#  Cree env/, installe les dependances, applique les migrations, seed la DB.
# =============================================================================

set -e

echo
echo "=== [1/5] Creation de l'environnement virtuel env/ ==="
if [ ! -d "env" ]; then
    python3 -m venv env
else
    echo "env/ existe deja, on saute."
fi

echo
echo "=== [2/5] Activation de env/ ==="
# shellcheck disable=SC1091
source env/bin/activate

echo
echo "=== [3/5] Installation des dependances ==="
python -m pip install --upgrade pip
pip install -r requirements.txt

echo
echo "=== [4/5] Application des migrations ==="
python manage.py makemigrations users cars
python manage.py migrate

echo
echo "=== [5/5] Chargement des donnees de demo ==="
python manage.py seed_data || true

echo
echo "============================================================================"
echo " Setup termine ! Pour lancer le serveur :"
echo "    source env/bin/activate"
echo "    python manage.py runserver"
echo "============================================================================"
