#!/bin/bash
termux-wake-lock 2>/dev/null
echo "🚀 aIValue8 Phone Watchdog Start Ho Raha Hai..."
while true; do
    python phone_watchdog.py
    echo "⚠️ Script ruki! 5 second mein auto-restart ho rahi hai..."
    sleep 5
done
