# First formal hosted test — final results

Original criteria: criteria_snapshot.md, committed in `6f8923ecf1939529f5fd7daf0abdc05eed0b86f4`
before all formal requests. Live origin: https://campus-life-rag.onrender.com.
Frozen application revision: `1694a57b3e19cebdcb769480faf6480a491f92d9`.
The user attests this is the unchanged live deployment; the public service does
not expose a Git SHA. Source/configuration/criteria hashes stayed unchanged.
Actual dashboard build/start settings remain independently unverified; repo
settings are `sh build.sh` and `sh start.sh`. No secret values were requested.

| Criterion | Original target | Run 1 | Run 2 | Run 3 | Verdict |
| --- | --- | --- | --- | --- | --- |
| C1 | At least 4/5 supported answers within five seconds on warm requests | MET 5/5 | MET 4/5 | MET 5/5 after separately recorded warm-up | MET |
| C2 | Each of five Project 1 requests has exactly one complete JSON log | MET 5/5 | MET 5/5 | MET 5/5 | MET |
| C3 | After one restart, index_ready:true and a correct sourced parking answer | MET | MET | MET on separate explicitly confirmed completion check | MET |
| C4 | Non-string request returns 400 + structured error; next valid request succeeds | MET | MET | MET | MET |
| C5 | At least 4/5 exact refusals with refused:true in response and log | MET 5/5 | MET 5/5 | MET 5/5 | MET |

## Conditions and evidence

For C1/C2, five original questions were sent sequentially after a successful
excluded warm-up. Client time runs from dispatch through the complete response
body; it includes network and server handling. Request safety timeout was 55
seconds but the C1 target stayed exactly five seconds. Every factual claim
was manually checked against frozen source text under the user-approved method;
this is source-file verification, not inspection of hidden live chunk bodies.
C1 met the per-trial 4/5 target in all three batches. The Trial 2 dining answer
at 6.783053922 seconds remains a counted miss. No timed question was retried,
replaced, or removed. Server timer values were not substituted for client times.

All three batches' 39 POST records were exported by the user from Render,
matched by ID/status/response fields, and archived. They show response caching
disabled. Complete JSON log schemas and one-record-per-ID counts were checked
for all 15 C2 questions. Three C4 rejection/recovery pairs and 15 C5 exact
response/log refusals were verified. The fixed inputs, original expected
observations, commands, raw responses, UTC timestamps, conditions, manual
review, and record IDs are under this directory for a repeatable retest.

C3 uses three separate user-confirmed completed restarts (Trials 1, 2, and
the final C3-only check). Its target has no latency limit. The user corrected
the original third restart-completion assumption and could not establish its
timing. That initial candidate returned client HTTP 502 despite health being
ready; it is retained as an inconclusive-eligibility observation, together
with the supplied unmatched application success record and its separate
recovery. It is not silently removed or treated as a successful first attempt.
The final C3-only restart check was declared before execution, completion/Live
was explicitly confirmed, and it was scored once. See c3_final.report.md and
protocol_clarifications.jsonl. Thus the test includes this disclosed protocol
clarification rather than pretending all original attempts succeeded.

## Files and functions producing actual output

- trial_1.client.jsonl, trial_2.client.jsonl, trial_3.recovery.client.jsonl,
  c3_final.client.jsonl: actual client output from runner.py::send, including
  curl-equivalent commands and raw HTTP JSON text.
- trial_1.render.jsonl, trial_2.render.jsonl, trial_3.recovery.render.jsonl:
  actual JSON messages from serve.py::finish_ask_log, copied from Render.
- HTTP health JSON: serve.py::health / store.py::index_exists.
- HTTP answer/refusal JSON: serve.py::ask / app.py::ask_pipeline / gate.py::check.
- Source review: trial_1.review.json, trial_2.review.json,
  trial_3.recovery.review.json, and source_review_material/.
- All five actual-output examples are pasted under README's Run Log and
  Verdicts; the final C3 check's actual body is also pasted there.
- final_verdicts.json is the machine-readable overall score, retaining the
  version, restart, and source-review provenance qualifications.

No code, model, retrieval setting, target, service, or deployment setting was
changed to improve results. No further requests or fixes are required for this
first test. Git staging, commits, and pushes remain with the user. Stop here
before diagnosing/fixing the preserved gateway failure or running a retest.
