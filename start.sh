#!/bin/bash

# Funktion zum Starten des Bots
start_bot() {
    python main.py &
    BOT_PID=$!
}

# Funktion zum Stoppen des Bots
stop_bot() {
    if [ ! -z "$BOT_PID" ]; then
        kill $BOT_PID
        wait $BOT_PID
    fi
}

# Initialer Bot-Start
start_bot

# Endlosschleife zum Überprüfen auf Updates
while true; do
    sleep 300  # Warte 5 Minuten

    git fetch origin
    LOCAL=$(git rev-parse @)
    REMOTE=$(git rev-parse @{u})

    if [ $LOCAL != $REMOTE ]; then
        echo "Änderungen gefunden, ziehe Updates..."
        stop_bot
        git pull
        chmod +x start.sh
        start_bot
    fi
done