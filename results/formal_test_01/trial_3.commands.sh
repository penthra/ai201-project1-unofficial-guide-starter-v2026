# Trial 3: restart_health
curl --max-time 55 --silent --show-error --include --request GET https://campus-life-rag.onrender.com/health
# Trial 3: restart_answer_and_excluded_warmup
curl --max-time 55 --silent --show-error --include --request POST https://campus-life-rag.onrender.com/ask --header 'Content-Type: application/json' --data '{"question": "When can students purchase a parking permit?"}'
