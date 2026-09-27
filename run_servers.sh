#!/bin/bash
cd /workspace/garmin-upgrade
for m in ok:5101 bad:5102 custom:5103 empty:5104; do MODE=${m%%:*} .venv/bin/python app.py ${m##*:} > /tmp/app_${m%%:*}.log 2>&1 & done
wait
