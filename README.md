# ProgSecureSysCA2
This is a temporary, vulnerable website used solely to demonstrate some cybersecurity concepts.

This software should only be used in a controlled, educational environment.

/app        Web vulnerable to SQL Injection and Cross Site Scripting
/scripts    SQL Injection Vulnerability Scanner and Log Analyzer scripts

## Requirements
- Docker

## Instructions

### To have the vulnerable version run:

```
git checkout d33b8003e36d50757fa40579297a84637fc0cbb5
cd app
bash stop-rm-build-and-run-server.sh
```

### To have the "secure" version run:
docker exec -it server_ca2_container bash
```
git checkout main
cd app
cp server/.env.example server/.env
bash stop-rm-build-and-run-server.sh
```

### To analyze the database using command run:
```
docker exec -it server_ca2_container bash
sqlite3 noticeboard.db "SELECT * FROM users;"
```