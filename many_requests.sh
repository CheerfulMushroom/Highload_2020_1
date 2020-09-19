(printf '%s\n' {1..2}) | xargs -I % -P 8 curl "http://127.0.0.1:8888/lol_%.txt"

