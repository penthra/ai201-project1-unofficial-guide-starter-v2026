# Running this project

## Capstone: Running It

Shape A (Deploy and instrument), hosted Path A. Hosting platform: **Render**.
Live URL: **https://campus-life-rag.onrender.com** (from the established service
in this conversation; the latest request contained a URL placeholder).
This is a JSON API, with `GET /health` and `POST /ask`; `/` has no question form.
Keep the existing service in place. This guide does not require creating a new
service, changing plans, or running formal trials.

### Deployment version and settings

| Item | Verified state |
| --- | --- |
| Repository revision tested in a separate clean clone | `efa901e55ea2d7e68496b22457b91276ac9d1bbc` |
| Actual deployed Git revision | **Not independently verified.** The public API exposes no commit SHA. |
| Repository build command | `sh build.sh` in `render.yaml` |
| Repository start command | `sh start.sh` in `render.yaml` |
| Actual Render dashboard build/start commands | **Awaiting dashboard confirmation.** Repository configuration alone does not establish the service settings. |
| Repository runtime/plan | Python / Free; dashboard plan remains unconfirmed. |
| Repository Python pin | `3.13.7` in `.python-version` |
| Clean-checkout Python tested | CPython **3.13.7**, Linux x86_64, Debian Bookworm container |
| Hosted Python version | Earlier supplied crash logs showed Python 3.13.7; current live deployment's version still needs its build-log confirmation. |
| Health-check path configured in repo | `/health`; inspect JSON `index_ready`, not only HTTP 200. |

`criteria.md` exists in Git. Its five Project 1 acceptance criteria were committed
in `1cc0672c720721a809f8ba16748ebf3de3f64b11` ("Milestone 2: Write your acceptance
criteria"). No separate capstone criteria commit was found. The user explicitly
authorized smoke checks as an exception to the earlier criteria-before-runs
requirement. These checks are not the Milestone 5 formal trials.

To finish verifying the existing deployment, copy the following from Render:

1. Events/Deploys: the **full Git commit SHA of the currently live deploy**,
   not a failed or superseded deploy.
2. Settings: the exact **Build Command** and **Start Command** text, runtime,
   instance plan, and health-check path.
3. The current successful deploy's build log line showing its **Python version**.
4. Environment: **variable names only**. Do not share values, API keys, secret
   files, database URLs, or deploy-hook URLs.

### What the commands do

`sh build.sh` installs `requirements-runtime.txt`, rebuilds
`chroma-hnswlib==0.7.6` from source with `HNSWLIB_NO_NATIVE=1`, checks dependencies
and native import, then indexes `campus_life`. This avoids the previously seen
illegal instruction from a CPU-specific native library. It requires a C++
compiler, Python development headers, and outbound access to package/model hosts.
Indexing produced **183 chunks from 88 documents** in the clean test.

The build packages `chroma_db/` and `.cache/embedding-models/`. `sh start.sh`
checks for the packaged index and an exported `GEMINI_API_KEY`, then executes:

```bash
python -m gunicorn --workers 1 --bind "0.0.0.0:${PORT:-5000}" --timeout 120 serve:app
```

Startup does not re-embed the corpus. Render supplies `PORT`; the local default
is 5000. `serve.py` imports and calls `app.ask_pipeline`, the same handler used
by the original CLI. Neither the original RAG algorithm nor CLI was replaced.

### Local setup (Linux or WSL)

Use Python **3.13.7**; `.python-version` records the selection but does not
install Python. Gunicorn's documented path here is Linux; native Windows and
macOS setup were not tested. On Debian-based systems, install a C++ compiler
and development headers appropriate to the selected Python first.

From a clean clone of this repository, with Python 3.13.7 selected:

```bash
python --version
python -m venv .venv
. .venv/bin/activate
export AI201_CORPUS=campus_life
export AI201_CACHE=0
export AI201_EMBED_BATCH_SIZE=1
sh build.sh
```

Provide a valid Gemini key privately in your terminal. In Bash, this prompt
avoids entering its value as a shell-history command:

```bash
read -r -s -p 'Gemini API key: ' GEMINI_API_KEY
printf '\n'
export GEMINI_API_KEY
```

One exact local start command after setup:

```bash
sh start.sh
```

The start script requires an **exported** key; it does not source `.env`.
`config.py` can read an ignored `.env` for ordinary CLI/development use, but
that alone does not satisfy the shell script's secret check. Never commit
`.env`, model assets, index files, or response caches.

The clean-checkout test used the isolated Python container's interpreter
instead of a nested venv. The same `sh build.sh` and `sh start.sh` commands
were exercised against the committed source, with no project dependencies,
model cache, index, or secrets copied into the checkout beforehand.

### Dependencies and model assets

`requirements-runtime.txt` pins these direct dependencies and retains the
course ranges in `requirements.txt` as constraints:

| Dependency | Pin |
| --- | --- |
| python-dotenv | 1.1.1 |
| chromadb | 0.6.3 |
| posthog | 3.25.0 |
| google-genai | 1.75.0 |
| rank-bm25 | 0.2.2 |
| Flask | 3.1.3 |
| Gunicorn | 23.0.0 |

`build.sh` explicitly rebuilds `chroma-hnswlib==0.7.6`. The clean Linux install
also resolved `onnxruntime==1.32.0` and `numpy==2.5.4`. These two are observed
versions, not additional pins: **transitive dependencies are not fully locked**.
`python -m pip check` reported no broken requirements.

Embeddings use **all-MiniLM-L6-v2**, locally through ONNX, with 384 dimensions.
The hosted adapter defaults to a batch size of one to limit inference memory.
The build downloads the archive from Chroma's CDN:
`https://chroma-onnx-models.s3.amazonaws.com/all-MiniLM-L6-v2/onnx.tar.gz`.
Measured sizes in the clean build:

| Asset | Bytes | Approximate size |
| --- | ---: | ---: |
| Download archive `onnx.tar.gz` | 83,178,821 | 79.33 MiB |
| Extracted `onnx/model.onnx` | 90,387,606 | 86.20 MiB |
| All extracted model/tokenizer files | 91,332,068 | 87.10 MiB |
| Archive plus extracted files retained in cache | 174,510,889 | 166.43 MiB |
| Generated Chroma index files, including SQLite | 2,593,508 | 2.47 MiB |

Required companion files are `tokenizer.json`, `vocab.txt`, `config.json`,
`special_tokens_map.json`, and `tokenizer_config.json`. Index size can change
with SQLite bookkeeping and corpus updates. Disk size is not process RAM.
Generation calls Google's hosted Gemini API; no generation model weights or
optional sentence-transformers/PyTorch installation are needed.

### Environment variable names

| Name | Purpose |
| --- | --- |
| `GEMINI_API_KEY` | Required exported secret for the start script and Gemini API. Supply privately. |
| `AI201_CORPUS` | Corpus selection; scripts default to `campus_life`. |
| `AI201_MODEL` | Optional Gemini model override; repo default is `gemini-3.5-flash-lite`. Actual live model cannot be read from the API. |
| `AI201_CACHE` | Response cache switch; repo Render configuration sets `0` for uncached smoke/evaluation runs. |
| `AI201_EMBED_BATCH_SIZE` | Positive embedding batch size; repo Render configuration sets `1`. |
| `PORT` | Host-provided HTTP port; local fallback 5000. |
| `AI201_EMBED_CACHE_DIR` | Set by both scripts to `$PWD/.cache/embedding-models`; not a secret. |
| `PYTHONUNBUFFERED`, `PYTHONFAULTHANDLER` | Set by scripts for immediate output and native-crash traceback diagnostics. |
| `AI201_DEBUG` | Local Flask development option only; leave unset for Gunicorn. |
| `ANONYMIZED_TELEMETRY` | Disabled by `store.py` unless already supplied. |

Do not enable the staff-only `AI201_FAKE_EMBEDDINGS` switch for real runs.
The actual names configured in Render remain pending dashboard confirmation;
the table describes variables supported/set by this repository, not an export
of Render's environment. No secret values are needed for that confirmation.

### Send a question

From Bash or a terminal with curl:

```bash
curl --max-time 60 --silent --show-error \
  https://campus-life-rag.onrender.com/health

curl --max-time 60 --silent --show-error \
  -X POST https://campus-life-rag.onrender.com/ask \
  -H 'Content-Type: application/json' \
  --data '{"question":"When can students purchase a parking permit?"}'
```

For the local service, substitute `http://127.0.0.1:5000` for the Render origin.
A valid response includes `answer`, `sources`, `refused`, `best_distance`,
`threshold`, and `corpus`. A relevance-gate refusal is a normal HTTP 200.

### Verification record — November 14, 2026 (America/Los_Angeles)

- Live: one real parking-permit question returned **HTTP 200 in 4.360 seconds**:
  `Student permits for the west lots go on sale in August (admin_parking_permits.txt).`
  The answer agrees with the local corpus source. The response had
  `refused: false`, `best_distance: 0.4196`, and `threshold: 0.6`.
- Live health afterward: **HTTP 200**, `corpus: campus_life`,
  `index_ready: true`, `detail: ready`.
- Separate clean clone of the revision above: pinned install, portable native
  compilation/import, dependency check, real ONNX download, and indexing passed.
  The index contained 183 chunks. No stand-in embeddings were used.
- Local `sh start.sh`: Gunicorn and `/health` passed under a **512 MiB Docker
  memory limit**. A real campus question reached Gemini, but returned HTTP 500
  because the local credential was rejected upstream with **API_KEY_INVALID**.
  No credential values were printed or written into the clean checkout.
  Full local answer generation therefore remains blocked on a valid local key;
  the hosted key worked for the live question. Do not paste either key here.
- Local service remained healthy after the failed generation request. Sampled
  container memory was **387.2 MiB / 512 MiB** after model initialization;
  cgroup counters showed no OOM or OOM kill. This is a point-in-time sample,
  not peak RAM or evidence of Render memory headroom under concurrent traffic.
- Actual deployed commit, dashboard commands/environment names, current hosted
  Python/model, and Render peak-memory measurements remain unverified pending
  the dashboard details above. No service settings were changed and no deploy
  was triggered. Structured request logging is still unfinished in `serve.py`.

Formal repeated trials and criterion scoring are reserved for **Milestone 5**.

## Original Project 1 CLI

After dependency setup, the original CLI remains available:

```bash
python app.py --corpus campus_life index
python app.py --corpus campus_life ask "When can students purchase a parking permit?"
python app.py --corpus campus_life retrieve "When can students purchase a parking permit?"
```

The CLI uses Chroma's normal home cache unless `AI201_EMBED_CACHE_DIR` is set.
Use the build script when preparing assets for `sh start.sh`. `python serve.py`
is a local Flask development server, while `sh start.sh` is the tested Gunicorn
start path. Do not run `run_eval.py` as part of this smoke check; formal trials
remain separate.


## Structured logging: redeploy before cost evidence

The five capstone criteria are now committed in `6f8923e` (`criterion`). The
older verification record above describes the earlier repository state.

`serve.py` now uses Flask before/after-request hooks to emit one JSON line to
stdout per `POST /ask`, covering normal responses, gate refusals, HTTP 400
validation rejections, and handled pipeline errors. A generated `X-Request-ID`
response header matches `request_id` in the log. `duration_ms` uses a monotonic
clock and covers server request handling; it excludes client/network time and
is not a token or billing measurement. The `model` field is the configured
model name. `cache_enabled` records the actual server cache configuration.
No environment values, system prompts, or exception messages are logged.

Push the changed `serve.py` and the accompanying README/RUNNING documentation,
then manually deploy the latest commit on the **existing** Render service.
Keep Build Command `sh build.sh`, Start Command `sh start.sh`, and
`AI201_CACHE=0`. No new service or plan change is needed. Neither Git actions
nor deployment is performed by this preparation step.

After deployment, check both a normal `/ask` response and an invalid request
such as `{"question":123}`. Each should have `X-Request-ID`; Render > existing
service > Logs should show exactly one `rag_request` JSON line with the matching
ID and HTTP status. Copy the JSON **message** text, not screenshots or secrets.
The platform's `Rndr-Id` header is different from the application's request ID.
Runtime stdout logs are private to your Render account and cannot be fetched
from the public `/ask` endpoint. See https://render.com/docs/logging.

Once live logging is confirmed, collect the ten-run warm elapsed-time sample
and the extra failed/rejected record described under **What It Costs** and
**Instrumentation** in README.md. Save each client measurement immediately to
`results/` as JSONL, then save the matching Render JSON lines promptly and paste
them as text into the README. Do not count a warm-up or the extra invalid-input
request in the ten-run average, and do not substitute local test records for
actual deployed logs. Formal acceptance trials remain for Milestone 5.


### Live cost measurement and log export — November 14, 2026

The new request-ID behavior is live. Ten sequential measured requests after
one excluded successful warm-up all returned HTTP 200. Mean client-observed
elapsed time was **3.695436 seconds/request**. The matching server log mean
was **3.6614819 seconds/request** (3661.4819 ms), measured by the handler.
Neither metric measures API spend or tokens.

Each client's full response and timing was synced to
[client JSONL](results/hosted_cost_20261114T211124Z.jsonl) immediately.
The user then supplied actual `rag_request` messages from Render's private
Logs page. Those thirteen messages are preserved in
[server JSONL](results/hosted_cost_20261114T211124Z.render.jsonl), including
an initial rejected preflight, the warm-up, ten measured requests, and the
extra invalid-input request. All ten measured responses match the server
records by ID and response fields. Cache-disabled status is verified in all
ten; their configured model is `gemini-3.5-flash-lite`. The extra rejection
returned HTTP 400 and logged `ValidationError`.

README's **Instrumentation** now pastes the ten actual server records plus
the rejection as JSONL text. **What It Costs** describes units, calculation,
warm conditions, and exclusions. The [summary](results/hosted_cost_20261114T211124Z.summary.json)
retains both averages. Two measured server durations and the warm-up exceed
the corresponding client durations; the timing discrepancy is unexplained.
The two clock series must not be subtracted to derive network overhead.

No requests were repeated to recover server evidence. The service was left
in place, and no deploy or Git write action was performed. Formal acceptance
trials remain for Milestone 5. Current hosted revision, peak RAM, API spend,
and token counts remain outside what this measurement establishes.


## Capstone criteria: implementation coverage

The five approved criteria in `criteria.md` have implementation support.
This audit checks readiness to verify them; it does not declare that they
passed formal acceptance trials or guarantee the latency target.

| Criterion | Existing implementation | What remains to verify live |
| --- | --- | --- |
| C1: supported answers within five seconds on warm requests | `serve.ask` calls the original `app.ask_pipeline`; `generate.build_prompt` supplies retrieved text, and the grounding instruction requires supported answers. The HTTP response and log expose sources, distance, and outcome; the log has `duration_ms`. | Warm the service first, then time the five Project 1 questions and review factual support using the retrieved material. Use client elapsed time for the user-visible limit, not the server timer. Model quality and a five-second limit cannot be guaranteed by a code check. |
| C2: exactly one complete JSON log per request | `start_ask_log` and `finish_ask_log` wrap each `POST /ask`. Each completed request prints one JSON record with all required fields and a matching `X-Request-ID`. | Match the five actual responses to the exported Render JSON lines and check one record per ID. The existing cost evidence already demonstrates this logging path, but it is not formal scoring. |
| C3: readiness and a sourced answer after restart | `build.sh` packages the real index and model assets; `start.sh` reuses those artifacts and starts one worker. `/health` checks the selected Chroma collection through `store.index_exists`. | Perform the approved restart of the existing Render service, then check `index_ready: true` and ask the parking question. No actual Render restart was performed during this audit. |
| C4: rejected non-string input, then continued service | `serve.ask` rejects non-string questions before invoking the pipeline; the after-request hook logs HTTP 400 with `ValidationError`. Request-local Flask `g` state prevents one error from contaminating the next request. | Verify a non-string request and its error record, followed by a successful real question. Local checks cover this sequence with controlled retrieval/generation. |
| C5: refusals appear in response and log | `gate.check` rejects distances at/above the threshold or empty results. `ask_pipeline` returns the exact `gate.REFUSAL` and skips generation; the response and completion log copy the refusal flag. | Use the five existing `OUT_OF_SCOPE` questions against the real index and compare the response and log. Controlled local distances cannot establish real embedding quality for those questions. |

No production implementation gap was found in this audit, so no RAG behavior,
model, retrieval parameter, start command, or live service was changed just to
make a check pass. In particular, forcing a short timeout would not guarantee
a supported answer within the C1 limit. Actual acceptance verdicts belong to
the later formal trials.

### Repeatable local implementation checks

After installing the project dependencies in the selected Python environment:

```bash
python -m unittest discover -s tests -p 'test_capstone_contracts.py' -v
```

The eight checks in `tests/test_capstone_contracts.py` passed during this
audit. They exercise the real HTTP handler, original pipeline, gate, and prompt
builder, using controlled stand-ins only for retrieval and answer generation.
They check a supported-answer path, one complete log, input rejection followed
by recovery, refusal with no generation call, empty retrieval, handled errors,
health flags, and startup-script artifact/port handling. The startup checks use
a stand-in executable and a placeholder index file: they check shell wiring,
not actual SQLite persistence or a restart of Render. These checks make no
network/API calls, download no models, require no secret values, and do not
score the five acceptance criteria.

The audit ran with host Python 3.12.3 and Flask dependencies available from the
existing local environment; the deployed runtime remains pinned to Python
3.13.7. The earlier clean-checkout build used that pinned version. Changes
from this audit are the new local check script and updated documentation;
there is no production-code change to redeploy from this audit.


## First formal test completed

See README's **Run Log and Verdicts** and
[results/formal_test_01/final_report.md](results/formal_test_01/final_report.md).
The original criteria commit `6f8923e` predates the runs. Application/criteria
hashes remained frozen at user-attested deployed revision `1694a57`.
All five criteria are MET across three valid observations each; C1 achieved
5/5, 4/5, 5/5 within the original time/support target. Complete actual client
responses, commands, source reviews, and exported server JSON are saved.

The ambiguous original third-restart HTTP 502 is retained. A user-corrected
restart-completion assumption led to a separate recovery and a predeclared,
explicitly confirmed C3-only completion check. The final report describes this
protocol clarification, source-file review limitation, and user-attested
version/restart provenance. No failure was silently replaced. Retest inputs
and method are preserved in results/formal_test_01/protocol.md and inputs.json;
use a new evidence directory for any later changed version. No application
code or deployment changes were made, and no fixes/retest were started.
