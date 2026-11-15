# Formal Test 01 — Trial 1: MET for all five criteria

All 14 client requests (one health check plus 13 POST requests) were saved.
The user's full log.txt was archived verbatim as trial_1.render_export.txt.
All 13 actual application records in trial_1.render.jsonl match their saved
client IDs/statuses; every response field matches, including refusals. Each
POST has exactly one record in the supplied export, with caching disabled.

| Criterion | Original target | Trial 1 |
| --- | --- | --- |
| C1 | At least 4/5 supported warm responses within 5 seconds | MET: 5/5 |
| C2 | One complete structured JSON record for each of five requests | MET: 5/5 |
| C3 | Ready and correct sourced parking answer after one restart | MET: user-confirmed restart, ready=true, correct August answer |
| C4 | Non-string input returns 400 + error log, followed by valid success | MET: 400/ValidationError, then correct 200 |
| C5 | At least 4/5 exact refusals with refused=true in response and log | MET: 5/5 |

C1 client elapsed seconds: 3.827942508, 3.423628606, 4.133164484, 3.211268463, 3.561190799.
The initial post-restart parking request was excluded from
C1 as its successful warm-up. Factual support was manually reviewed using the
user-approved tracked-source method; passages are in source_review_material/.

Version qualification: criteria commit 6f8923e predates the trial. Deployment
1694a57 is user-attested as latest; public endpoints do not expose its SHA.
The user explicitly confirmed the restart before requests; no independent
dashboard startup transcript was supplied. These provenance limits are
retained rather than presenting the version/restart as API-verified.

Inputs and expected observations: inputs.json / criteria_snapshot.md /
protocol.md. Exact commands: trial_1.commands.sh. Actual client text and
response bodies: trial_1.client.jsonl, produced by runner.py::send. Actual
server JSON: trial_1.render.jsonl, produced by serve.py::finish_ask_log and
copied by the user from Render. Responses originate from serve.py::ask and
serve.py::health; generated answers use app.py::ask_pipeline. Manual review
is in trial_1.review.json, with final per-trial decisions in trial_1.verdicts.json.

Runs 2 and 3 still require separate restarts and independent new requests.
No application code, target, or deployment setting was changed.
