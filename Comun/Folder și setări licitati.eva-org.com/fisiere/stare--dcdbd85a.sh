#!/bin/bash
# Arată starea ambelor site-uri.
docker ps --format 'table {{.Names}}\t{{.Status}}' | grep -iE "NAMES|schaller|dracula|cesiro1|production|evaprint|licitatii"
for U in https://www.ac-wohnart.at/ https://dracula-book.com/ https://cesiro.com/ https://production.cesiro.com/ https://dracula-design.com/ https://dracula-food.com/ https://print.eva-org.com/ https://licitatii.eva-org.com/; do echo "$U -> $(curl -s -o /dev/null -w '%{http_code}' -m 15 "$U")"; done
