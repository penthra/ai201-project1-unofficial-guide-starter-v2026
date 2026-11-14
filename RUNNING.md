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
