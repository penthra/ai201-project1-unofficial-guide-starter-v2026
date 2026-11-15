# Submission check — November 14, 2026 (Pacific)

**Not fully ready against the requested checklist:** the capstone baseline is
complete, but there is no implemented/measured improvement and no separate
three-trial retest set. The user said they do not have enough time and do not
want to retest. No improvement, trial results, or completion claims were
invented to fill that gap. No retesting or application changes were performed.

## Ready and checked

| Item | Evidence and result |
| --- | --- |
| Original repository | https://github.com/penthra/ai201-project1-unofficial-guide-starter-v2026 — verified from origin. This is the repository to submit, with the Render URL in its README. |
| README structure | One final `## Capstone`; all nine required labels each on a separate bold line. Project 1 write-up preserved. |
| Hosted path | Existing Render service, https://campus-life-rag.onrender.com. Audit GET /health returned HTTP 200, campus_life, index_ready:true, detail:ready. It took 42.222118 client seconds; initial cold/warm state was unknown, so it is not a new timed acceptance trial. |
| Local start command | RUNNING.md specifies `sh start.sh` after setup. It matches the separately cloned, previously tested copy under /tmp/ai201-deploy-verify-DHhSYY/repo. Its built index/model assets still exist. Prior clean Python 3.13.7 build/start/health passed; full local answer generation failed due API_KEY_INVALID and remains unverified with valid credentials. The setup was not rerun in this audit. |
| Five original capstone criteria | Original targets/reasons in criteria.md match the frozen baseline snapshot; future C5 is appended separately. Targets were user-selected/approved with AI-assisted drafting. They are not represented as wholly independently worded by the student. |
| Baseline formal results | results/formal_test_01/final_verdicts.json: C1–C5 MET across three valid observations each. C1: 5/5, 4/5, 5/5; the 6.783-second slow answer remains counted. |
| Restart qualification | Original ambiguous third-restart HTTP 502 preserved; user-corrected eligibility and separately confirmed final C3 check disclosed. Version/restart facts are user-attested, not independently exposed by the API. |
| Structured log evidence | Cost sample has ten actual measured records and one rejection; formal baseline has 39 matched JSON records across three batches, with response caching disabled. Raw client/server files are preserved. |
| Cost | Ten-run client mean 3.6954362995 s/run. For 100 people/day × 1 run/person: 100 runs/day × 3.6954362995 s/run = 369.5436299500 s/day ≈ 6.16 aggregate elapsed minutes/day under similar warm sequential conditions. This is not measured money, CPU time, hosting uptime, or tested concurrency capacity. |
| Existing scope | Original campus_life corpus, retrieval, gate, and prompt retained; hosted JSON API with structured logs. |

## Commit history and order

Local HEAD: `5e26c4718212816f89e888f8ec7b65208bc66ec1`.
GitHub origin/main read directly with read-only `git ls-remote --heads origin`:
`1694a57b3e19cebdcb769480faf6480a491f92d9`.

- **13 local capstone commits**, beginning at c707c69 (first Capstone scope).
- **11 published capstone commits** through origin/main. Both counts exceed eight.
- At least three substantive runtime/build commits are present in published history:

| Commit | Build implementation evidence |
| --- | --- |
| 13623cd | Python/runtime pins, Render configuration, start.sh, and HTTP input validation. |
| 6d6b26a | build.sh compiles portable chroma-hnswlib and render.yaml selects that build script. |
| efa901e | Build packages the corpus index/model assets; startup launches the web worker. |

The criterion/results order is verified by commit timestamps **and ancestry**:

| Commit | Pacific commit time | Role |
| --- | --- | --- |
| 6f8923e | November 14, 12:05:53 PM | Original five capstone criteria. |
| 97d99ee | November 14, 1:05:57 PM | First saved structured request-preflight observations and application logging. |
| 1694a57 | November 14, 6:37:02 PM | First cost-sample results and structured exports. |
| 7844e56 | November 14, 7:29:47 PM | **Named first formal-results commit**, containing formal_test_01. |

Thus named criteria commit **6f8923e precedes named first formal-results commit
7844e56**, and also precedes the named request/cost result commits. Earlier
setup/smoke checks are not mislabeled as formal results; their separate
criteria-before-runs exception remains in the historical record.

GitHub main does not yet include local commits **7844e56** (formal results) or
**5e26c47** (separate future C5 target). Today's README/RUNNING/audit edits are
also uncommitted. Publishing these remains the user's responsibility. No
fetch, staging, commit, push, or submission was performed by the assistant.

## Missing or unverified

| Item | Status |
| --- | --- |
| One measured post-baseline improvement | **Missing.** Stage timing fields were proposed but are not implemented or measured. Earlier deployment fixes occurred before the baseline; they are not a controlled post-baseline improvement study. |
| Second set of three trials per criterion | **Missing.** Only formal_test_01 exists. Its extra recovery/C3 completion observations are part of one baseline campaign, not a separate after set. September Project 1 before/after reports are a different project stage. |
| Actual deployed SHA and dashboard commands | Still user-attested/repo-configured; no current independent dashboard SHA/settings export. Public health proves readiness, not the deployed SHA. |
| Full local generated answer | Prior clean setup/start succeeded, but local Gemini credential was invalid. Requires a valid privately supplied local key and a later smoke check; none requested from the user here. |
| Current peak Render memory | Not measured; existing bounded local sample does not establish peak hosted RAM. |
| Publication | Two later local commits and final documentation edits need user-controlled publication. |

## README updates completed

- All nine requested bold labels, in order, under one final Capstone section.
- Cost method, measured units, exact mean, and explicit 100-people/day arithmetic.
- The Improvement honestly labeled proposed/unimplemented/unmeasured.
- What's Still Broken lists observed slow request, ambiguous gateway/startup
  failure, local-key limitation, and missing improvement/retest; possible
  remedies are conditional and not claimed implemented.
- Stopping reason uses the user's actual answer: insufficient time and choosing
  not to retest. First next step is stage timing to identify the slow component.
- Future C5 tightening is 5/5 each trial, separately labeled, supported by 15/15
  baseline refusals. Original 4/5 target and baseline records remain unchanged.
- Two genuine AI examples drawn from this session: hnswlib deployment diagnosis
  and criteria drafting/tightening. No invented independent authorship claim.

Submit the **original GitHub repository URL above**, not a new fork or only
the Render URL. This audit does not claim the missing measured improvement
or retest requirement is satisfied. All staging, commits, pushes, and actual
submission remain with the user.
