# Formal test 01 — frozen protocol

Status: prepared; no formal requests have been sent. Three separate Render
restarts and new trial batches are required. Prior smoke/cost measurements are
not formal evidence and will not be reused as Runs 1–3.

## Version and criteria

Live origin: https://campus-life-rag.onrender.com (RUNNING.md).
Repository revision and user-attested latest deployment:
`1694a57b3e19cebdcb769480faf6480a491f92d9`.
The API does not expose a Git SHA, so the deployed revision is user-attested,
not independently verified. A dashboard SHA would provide stronger evidence.
Do not deploy, push application changes, edit environment settings, or change
plans between trials. After each restart confirm it is the same revision.
Dashboard build/start commands are still unverified; the repo specifies
`sh build.sh` and `sh start.sh`. No secret values are requested.

The criteria commit is `6f8923ecf1939529f5fd7daf0abdc05eed0b86f4`, an ancestor of the
repository revision, and predates preparation and all future requests in this
campaign. Its original bytes and targets are saved in `criteria_snapshot.md`.
The application, questions, and criteria matched that revision after newline
normalization. Hashes and provenance are in `manifest.json`.

## Conditions and independence

For each trial numbered 1, 2, 3:

1. The user selects Render > Manual Deploy > Restart service on the existing
   service, without redeploying. Wait for its dashboard restart to complete,
   then tell the agent which trial's restart completed. Preserve the startup
   log text and the live deployment SHA for restart/version evidence.
2. GET `/health`, then POST the parking-permit question for C3. This first
   post-restart question may load the embedding model and is not timed for C1.
   Require a successful non-refused response before labeling subsequent
   requests warm. The successful C3 question is the one excluded C1 warm-up.
3. Send the five original in-corpus questions sequentially, once each in the
   order in `inputs.json`. These five IDs are shared evidence for C1 and C2
   within the trial, but not reused in other trials. No deliberate idle gap.
4. For C4, send `{"question":123}`, then a new valid parking question. Capture
   both responses and both application JSON log records.
5. For C5, send the five existing OUT_OF_SCOPE questions once each, in order.
6. Save each raw response, headers, HTTP status, request ID, UTC timestamp,
   monotonic elapsed time, and exact curl-equivalent command immediately.
   Export the corresponding Render `rag_request` messages promptly before
   moving to another trial. Keep each trial's JSONL and restart text separate.

The three restart boundaries separate independent trials. Repeated questions
must not be served by the application response cache; confirm all exported
records show `cache_enabled: false`. If not, stop and clarify validity rather
than silently turning caching off or counting cached answers as independent.
No secret, model, retrieval, gate, prompt, quota, or code settings are changed.

## Original targets and scoring

| Criterion | Inputs and original target | Expected observations and conditions |
| --- | --- | --- |
| C1 | Five Project 1 questions; at least 4/5 supported responses within 5 seconds each. | Warm requests only, after the excluded successful C3 warm-up. Measure from immediately before dispatch until the full response body is read. Judge each response independently; no averaging or rounding a duration down to five seconds. Manually check every factual claim against the committed corpus material in its returned sources. User approved this source-file method because actual chunk text is not exposed live. Factual support without meeting the time limit, or meeting time without support, fails that question. |
| C2 | The same five Project 1 requests; every one emits exactly one complete valid JSON record. | Match by X-Request-ID/request_id. Require timestamp, request ID, question, answer, model, sources, best distance, refusal flag, HTTP status, duration, and error type when applicable. Check each record agrees with its response. Null error_type is appropriate on a normal success. Distinguish platform access/health lines from application records. |
| C3 | One real restart, `/health`, then parking question. | Require index_ready: true and a correct August answer with a supporting source, without manual indexing. Record first post-restart conditions; exclude its latency from C1. Restart evidence must be user/dashboard evidence, not a normal request or simulated local restart. |
| C4 | Non-string question followed by a new valid parking question. | First response HTTP 400 with one structured ValidationError record; subsequent valid response HTTP 200, non-refused, with a correct sourced answer. Both are new requests on the same running instance/trial. |
| C5 | Five existing out-of-scope questions; at least 4/5 exact required refusals. | Required text is gate.REFUSAL: "I don't have enough information about that." For a passing question, both response and matching application record must have refused: true. A gate refusal is HTTP 200, not a service failure. |

`inputs.json` fixes the exact questions before the first trial. The expected
phrases in that file help locate supporting facts but are not an exact-phrase
scorer: correct paraphrases may pass; unsupported added claims may not.
Client timing and server duration_ms remain different measurements. Only the
client time decides the C1 user-visible limit. The ten-run cost sample showed
clock differences, so do not derive network overhead by subtracting them.

A per-trial criterion is MET only if it reaches its original target in that
trial; otherwise MISSED. The overall row is MET only if all three independent
trials meet the target. Show each run's counts/evidence, not only the aggregate.
A missing log export, unconfirmed restart, or unconfirmed warm-up is an
unverified/not-run result, not an invented MET or an automatic criterion miss.
Report transport timeouts and HTTP/model errors as observed; do not discard,
replace, or automatically retry timed questions. The request safety timeout is
55 seconds, not a relaxation of the C1 five-second target. A failed warm-up
prevents warm C1 timing; pause and resolve conditions instead of calling a
cold/failed sample warm. No application changes occur during this first test.

## Repeating the protocol

Use the same source revision, the original criteria_snapshot.md, inputs.json,
request order, client timer/timeout, warm-up policy, log schema checks, and
manual support review for a retest. Label any later changed revision separately;
never overwrite these first-test inputs or evidence. For each trial run:

```bash
python results/formal_test_01/runner.py --trial 1 --restart-confirmed
```

Replace only trial number with 2 or 3 after that trial's separate restart.
The runner uses only standard-library HTTP calls to the hosted URL. It records
exact curl-equivalent commands and appends/syncs each completion immediately.
It does not restart Render, read secrets, deploy, or automatically claim final
verdicts. Final logs, manual support reviews, and version/restart confirmations
are required before writing the five-row README Run Log and Verdicts table.

Actual client output is produced by `results/formal_test_01/runner.py::send`.
Actual application JSON is produced by `serve.py::finish_ask_log`; answers use
`app.py::ask_pipeline`, and readiness uses `serve.py::health` with
`store.py::index_exists`. The final report will paste actual text from at least
one trial for every criterion and name these file/function sources.


## Trial 3 recovery clarification (recorded after the initial failure)

The initial Trial 3 health request returned ready, but the first parking request
returned gateway HTTP 502 with no application request ID. The user then said
the service may not have been online when completion was reported and asked
to try again. The user supplied an application success record for the same
question/time, but its ID cannot be matched to the gateway response; both
observations remain preserved without treating them as a confirmed match.

One separately labeled recovery warm-up was authorized on the unchanged code,
followed by the remaining C1/C2/C4/C5 requests if it succeeded. The initial
trial_3.client.jsonl and error HTML are not replaced. Recovery evidence uses
trial_3.recovery.client.jsonl and trial_3.recovery.commands.sh. Warm conditions
for C1 start after that new successful warm-up; no timed question is retried.
The original targets and application hashes remain unchanged. The eligibility
of the initial C3 observation requires explicit restart-timing clarification;
a recovery success does not by itself erase or invalidate its HTTP 502.

The exact additional runner is archived as recovery_runner.py, using the
original runner.py::send function. It is already executed evidence, not a
command to repeat during this campaign. Any future retest must record restart
completion before its first C3 request; never reuse an output filename or
silently use recovery as the original outcome.


## Predeclared C3-only completion check

After all third-batch recovery records were verified, the user explicitly
said they were unsure whether the original third restart had completed.
C1/C2/C4/C5 have three completed MET batches and will not be rerun. The
original third C3 attempt is INCONCLUSIVE because its prerequisite cannot
be confirmed; its client HTTP 502 and supplied server HTTP 200 are retained.

Before any new C3 request, ask for one fresh restart and confirmation that
Render reports the restarted service live, preferably with the new startup
lines. Then send exactly one GET /health and one parking-permit question on
the unchanged source/configuration. This is the third valid C3 observation
alongside trials 1 and 2. Score its actual readiness and sourced answer under
the original target, including a failure if it occurs. Do not retry this
final observation to seek a pass. Save it in separate c3_final.* files;
never overwrite original trial_3 evidence. There is no C3 latency target.
