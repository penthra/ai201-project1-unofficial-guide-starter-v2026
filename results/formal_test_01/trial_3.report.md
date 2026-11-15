# Formal Test 01 — Trial 3 stopped at failed warm-up

The user confirmed a separate restart. The runner checked unchanged source
hashes, then saved the following actual results:

1. GET /health: HTTP 200, index_ready:true, detail:ready.
2. First POST /ask (parking-permit question): HTTP 502, HTML error page titled
   "502", no X-Request-ID, Render request ID 7079d3e9-8a1d-4fbb.
   Client elapsed seconds: 1.476675068.

C3 is MISSED under the original target: the post-restart question did not
return a correct sourced answer. The raw HTML is preserved separately in
trial_3.restart_answer_502.html and in trial_3.client.jsonl. Actual client
output was produced by runner.py::send. The error page came from the hosted
HTTP path, not a verified application JSON completion record; no server
exception or memory cause is inferred from this response alone.

The frozen protocol stops when warm-up is unsuccessful. C1, C2, C4, and C5
were NOT RUN; they are not arbitrarily marked MISSED and no successful retry
has replaced the failed C3 observation. Further recovery needs protocol
clarification. No application code, target, settings, or deployment changed.
Criteria and deployment provenance remain as recorded in manifest.json.
