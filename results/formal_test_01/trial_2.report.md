# Formal Test 01 — Trial 2: MET for all five criteria

The separate restart was user-confirmed before requests. The same frozen
application/criteria hashes were checked. All 14 client requests were saved,
and the user supplied all 13 matching application JSON records in log.txt.
The raw export is preserved verbatim as trial_2.render_export.txt. Every
request has exactly one matching complete JSON record in the supplied export,
with cache_enabled:false. All response fields match the client evidence.

| Criterion | Original target | Trial 2 |
| --- | --- | --- |
| C1 | At least 4/5 supported warm answers within 5 seconds | MET: 4/5 |
| C2 | One complete structured JSON record per Project 1 request | MET: 5/5 |
| C3 | Ready and correct sourced parking answer after restart | MET: user-confirmed restart, ready=true, correct August answer |
| C4 | Invalid input 400 + error log, followed by valid success | MET: 400/ValidationError, then correct 200 |
| C5 | At least 4/5 exact refusals, refused=true in response and log | MET: 5/5 |

All five Project 1 answers were supported. Client elapsed seconds:
4.804581461, 4.916785431, 4.425333995, 6.783053922, 3.955734336.
The dining-hours answer took 6.783053922 seconds and counts as one missed
question for C1; the original 4/5 target still passes. No result was discarded,
replaced, or retried. The 15.252834603-second initial post-restart answer was
the excluded warm-up. Five out-of-scope responses and matching records all
contain the exact refusal and refused:true. The invalid-input record is
ValidationError, and the next valid request returns a correct sourced answer.

Code version is user-attested latest 1694a57; criteria were committed earlier
in 6f8923e. No independent public SHA or dashboard startup transcript is
available. These provenance qualifications are retained. Actual server JSON
is produced by serve.py::finish_ask_log; HTTP bodies by serve.py::ask and
serve.py::health, with app.py::ask_pipeline producing answers. Client evidence
is produced by runner.py::send. See trial_2.commands.sh for exact commands,
inputs.json/protocol.md for expected observations and conditions, and
trial_2.review.json for per-question factual review using saved source material.

Trial 3 still requires a separate restart and independent requests.
No application code, setting, original target, or deployment was changed.
