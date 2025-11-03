#!/bin/bash
set -e

DB_PATH="app/database/database.db"
SEED_MODULE="app.database.seed"

# Creates a database folder if it doesn't exist.
mkdir -p "$(dirname "$DB_PATH")"

# It only runs seeds if the database doesn't exist or is empty.
if [ ! -f "$DB_PATH" ] || [ ! -s "$DB_PATH" ]; then
  echo "📂 Database not found or empty. Running seed..."
  python -m $SEED_MODULE
else
  echo "✅ Database already exists and is populated. Skipping seed."
fi

echo "🚀 Starting application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
