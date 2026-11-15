# Formal Test 01 — separately recorded Trial 3 recovery

The original failed attempt is preserved in trial_3.client.jsonl and its
separate HTML artifact. The user then said the service may not have been
online when they reported completion, and asked to try again. A single new
health/warm-up and the remaining test requests were authorized and recorded
separately; no timed C1 question was replaced, and no application code changed.

- Recovery health: HTTP 200, index_ready:true.
- Recovery parking question: HTTP 200, correct sourced August answer,
  14.568022858 seconds, excluded from C1.
- C1: 5/5 factually supported warm answers within the original five seconds.
  Client elapsed seconds: 4.475453527, 4.456571887, 3.813972269, 4.01745124, 4.462383662.
  Cache-disabled condition still requires the matching server records.
- C2: five normal request IDs captured; complete one-per-request JSON records pending.
- C4: HTTP 400 for the non-string input, then correct sourced HTTP 200 answer;
  structured ValidationError record pending.
- C5: 5/5 exact refusals with refused:true in responses; server flags pending.

C3 eligibility is pending clarification: original health was ready but its
first question returned gateway HTTP 502. The user-supplied application 200
record for a similar question/time has an ID absent from the gateway response,
so an ID match cannot be verified. If the restart was not actually complete,
the original attempt had an invalid prerequisite; if it was complete, the 502
is an observed failure under the original protocol. Recovery success alone
cannot decide that question or erase the failure. Preserve both outcomes and
record any final eligibility decision with its provenance.

Actual client output is produced by the unchanged runner.py::send, invoked
by the archived recovery_runner.py. Exact commands are saved in
trial_3.recovery.commands.sh; expected inputs/conditions remain in inputs.json
and protocol.md, with the explicit recovery clarification appended. Actual
server records must be exported from serve.py::finish_ask_log, not reconstructed.


## Complete server export verified

All 13 recovery application records were supplied in the updated log.txt,
archived verbatim as trial_3.recovery.render_export.txt, and extracted into
trial_3.recovery.render.jsonl. Each client ID has exactly one matching complete
record; every response field agrees, and all show cache_enabled:false.
C1, C2, C4, and C5 are MET for this third independent request batch. The user
explicitly said they are unsure about the original restart completion timing,
so C3 remains INCONCLUSIVE rather than a fabricated pass or a definitive miss
for a possibly unmet prerequisite. Both original HTTP 502 and subsequent
server/client success records remain intact. A separately predeclared, clearly
confirmed C3-only restart check is needed to obtain a fair third valid C3
observation without rerunning or changing the four completed criteria.
