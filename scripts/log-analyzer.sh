#!/usr/bin/env bash
# Analizer minimal of failed attempts (FAILED_LOGIN)

# Ask for log file and threshold (default values)
read -p "Log file (default: noticeboard.auth.log): " LOGFILE
LOGFILE=${LOGFILE:-noticeboard.auth.log}

read -p "Threshold of failed attempts to alert (default: 10): " THRESHOLD
THRESHOLD=${THRESHOLD:-10}

# Validate file exist
if [ ! -f "$LOGFILE" ]; then
  echo "[ERROR] Log file not found: $LOGFILE"
  exit 1
fi

# Filter:
# 1) Grep lines with FAILED_LOGIN
# 2) Extract ip= value
# 3) Sort, count and show IPs with count > threshold
grep "FAILED_LOGIN" "$LOGFILE" \
  | sed -n 's/.*ip=\([^ ]*\).*/\1/p' \
  | sort \
  | uniq -c \
  | sort -rn \
  | awk -v t="$THRESHOLD" '$1 > t { printf("%s - %d failed login\n", $2, $1) }'

