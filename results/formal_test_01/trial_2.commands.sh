# Trial 2: restart_health
curl --max-time 55 --silent --show-error --include --request GET https://campus-life-rag.onrender.com/health
# Trial 2: restart_answer_and_excluded_warmup
curl --max-time 55 --silent --show-error --include --request POST https://campus-life-rag.onrender.com/ask --header 'Content-Type: application/json' --data '{"question": "When can students purchase a parking permit?"}'
# Trial 2: project_question_1
curl --max-time 55 --silent --show-error --include --request POST https://campus-life-rag.onrender.com/ask --header 'Content-Type: application/json' --data '{"question": "When can students purchase a parking permit?"}'
# Trial 2: project_question_2
curl --max-time 55 --silent --show-error --include --request POST https://campus-life-rag.onrender.com/ask --header 'Content-Type: application/json' --data '{"question": "How long does it take to walk from Fenwick Court to central campus?"}'
# Trial 2: project_question_3
curl --max-time 55 --silent --show-error --include --request POST https://campus-life-rag.onrender.com/ask --header 'Content-Type: application/json' --data '{"question": "How many midterm exams are scheduled for PHYS 130 Mechanics?"}'
# Trial 2: project_question_4
curl --max-time 55 --silent --show-error --include --request POST https://campus-life-rag.onrender.com/ask --header 'Content-Type: application/json' --data '{"question": "What are Halden Hall'"'"'s weekday serving hours?"}'
# Trial 2: project_question_5
curl --max-time 55 --silent --show-error --include --request POST https://campus-life-rag.onrender.com/ask --header 'Content-Type: application/json' --data '{"question": "What account do students need to access campus Wi-Fi?"}'
# Trial 2: invalid_non_string
curl --max-time 55 --silent --show-error --include --request POST https://campus-life-rag.onrender.com/ask --header 'Content-Type: application/json' --data '{"question": 123}'
# Trial 2: valid_after_invalid
curl --max-time 55 --silent --show-error --include --request POST https://campus-life-rag.onrender.com/ask --header 'Content-Type: application/json' --data '{"question": "When can students purchase a parking permit?"}'
# Trial 2: out_of_scope_1
curl --max-time 55 --silent --show-error --include --request POST https://campus-life-rag.onrender.com/ask --header 'Content-Type: application/json' --data '{"question": "What is the capital of Mongolia?"}'
# Trial 2: out_of_scope_2
curl --max-time 55 --silent --show-error --include --request POST https://campus-life-rag.onrender.com/ask --header 'Content-Type: application/json' --data '{"question": "How do I change the oil in a diesel engine?"}'
# Trial 2: out_of_scope_3
curl --max-time 55 --silent --show-error --include --request POST https://campus-life-rag.onrender.com/ask --header 'Content-Type: application/json' --data '{"question": "Who won the 1994 World Cup?"}'
# Trial 2: out_of_scope_4
curl --max-time 55 --silent --show-error --include --request POST https://campus-life-rag.onrender.com/ask --header 'Content-Type: application/json' --data '{"question": "What is the recommended dosage of ibuprofen for a headache?"}'
# Trial 2: out_of_scope_5
curl --max-time 55 --silent --show-error --include --request POST https://campus-life-rag.onrender.com/ask --header 'Content-Type: application/json' --data '{"question": "How do I write a for loop in Rust?"}'
