# Running this project

- [Original Project 1 CLI](#original-project-1-cli)
- [Capstone: live app, Render, and local API](#capstone-running-it)

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

---

## Capstone: Running It

**Shape A: Deploy and instrument · Path A: Hosted on Render.**
The HTTP API uses the original `app.py::ask_pipeline`.

- [Try the live app](#try-the-live-app)
- [Render settings](#render-settings)
- [Run the API locally](#run-the-api-locally)
- [Dependencies and model assets](#dependencies-and-model-assets)
- [Verification and logs](#verification-and-logs)

### Try the live app

**Live URL:** https://campus-life-rag.onrender.com

Send a question with **POST `/ask`**. There is no question form at `/`.

**PowerShell — paste this whole line:**

```powershell
'{"question":"What account do students need to access campus Wi-Fi?"}' | curl.exe --include --max-time 180 --request POST "https://campus-life-rag.onrender.com/ask" --header "Content-Type: application/json" --data-binary "@-"
```

**Bash / Linux / WSL:**

```bash
curl --include --max-time 180 -X POST https://campus-life-rag.onrender.com/ask -H 'Content-Type: application/json' -d '{"question":"What account do students need to access campus Wi-Fi?"}'
```

Verified live: **HTTP 200**, `refused: false`, and this answer:

> Students need a student account to access campus Wi-Fi.
>
> Source: admin_wifi_and_accounts.txt

Check index readiness with **GET `/health`**:

```powershell
curl.exe --max-time 180 https://campus-life-rag.onrender.com/health
```

In Bash, use `curl` instead of `curl.exe`. Expect HTTP 200 and
`index_ready: true`. A sleeping free service or first model load may take longer.

### Render settings

Use the existing **campus-life-rag** service and repository-root `render.yaml`.

| Setting | Command / configuration |
| --- | --- |
| Runtime / plan | Python / Free |
| Python pin | 3.13.7 (`.python-version`) |
| Build Command | `sh build.sh` — installs dependencies, rebuilds portable HNSW, downloads the model, and indexes the corpus |
| Start Command | `sh start.sh` — starts one Gunicorn worker serving `serve:app` |
| Health Check Path | `/health` |
| Port binding | `0.0.0.0:${PORT:-5000}`; Render supplies `PORT` |
| Automatic deploys | Off |

The owner confirmed Live commit `1694a57b3e19cebdcb769480faf6480a491f92d9`
and matching repository settings. Dashboard overrides and the current hosted
Python build-log version were not independently inspected.

Set variables in **Render → campus-life-rag → Environment**. Names only:

| Name | Purpose |
| --- | --- |
| `GEMINI_API_KEY` | Required secret; enter privately |
| `AI201_CORPUS` | Corpus selection from `render.yaml` |
| `AI201_CACHE` | Cache setting from `render.yaml` |
| `AI201_EMBED_BATCH_SIZE` | Memory-control setting from `render.yaml` |
| `AI201_MODEL` | Optional hosted Gemini model override |
| `PORT` | Provided by Render |
| `PYTHON_VERSION` | Optional override; must agree with the intended Python pin |

Scripts set `AI201_EMBED_CACHE_DIR`, `PYTHONUNBUFFERED`, and
`PYTHONFAULTHANDLER`; the build also sets `HNSWLIB_NO_NATIVE`.
Keep credentials out of Git. Do not enable `AI201_FAKE_EMBEDDINGS` for real runs.

### Run the API locally

**Use Python 3.13.7 on Linux or WSL**, with a C++ compiler and matching Python
development headers. `.python-version` records the version; it does not install
Python. Start with a fresh clone (or use your existing repository):

```bash
git clone https://github.com/penthra/ai201-project1-unofficial-guide-starter-v2026.git
cd ai201-project1-unofficial-guide-starter-v2026
```

Run the following in Bash from the repository root.

**1. Create an environment and prepare dependencies, model, and index:**

```bash
python --version
python -m venv .venv
. .venv/bin/activate
export AI201_CORPUS=campus_life
export AI201_CACHE=0
export AI201_EMBED_BATCH_SIZE=1
sh build.sh
```

These exports match the hosted corpus, disabled response cache, and embedding
batch size. The build needs internet access to install packages and download assets.

**2. Enter the API key privately and export it:**

```bash
read -r -s -p 'Gemini API key: ' GEMINI_API_KEY
printf '\n'
export GEMINI_API_KEY
```

`start.sh` requires an exported key; it does not load `.env` itself.

**3. Start the API with the virtual environment active:**

```bash
sh start.sh
```

Local URL: **http://127.0.0.1:5000** (default port). Startup reuses the built
index and model assets. In another Bash terminal, send a local question:

```bash
curl --include --max-time 180 -X POST http://127.0.0.1:5000/ask -H 'Content-Type: application/json' -d '{"question":"What account do students need to access campus Wi-Fi?"}'
```

Expect HTTP 200 with `answer`, `sources`, and `refused`. Press **Ctrl+C** in
the server terminal to stop it.

### Dependencies and model assets

`sh build.sh` installs `requirements-runtime.txt` with `requirements.txt`
constraints, then rebuilds `chroma-hnswlib`. Direct pins:

| Package | Version |
| --- | --- |
| python-dotenv | 1.1.1 |
| chromadb | 0.6.3 |
| posthog | 3.25.0 |
| google-genai | 1.75.0 |
| rank-bm25 | 0.2.2 |
| Flask | 3.1.3 |
| Gunicorn | 23.0.0 |
| chroma-hnswlib | 0.7.6, rebuilt from source |

Transitive dependencies are not fully locked. The clean build resolved
ONNX Runtime 1.32.0 and NumPy 2.5.4.

The build automatically downloads **all-MiniLM-L6-v2** for local ONNX
embeddings to `.cache/embedding-models/all-MiniLM-L6-v2/`.

| Asset | Measured size |
| --- | ---: |
| Download archive | 83,178,821 bytes (79.33 MiB) |
| `onnx/model.onnx` | 90,387,606 bytes (86.20 MiB) |
| All extracted files, including tokenizer/config files | 91,332,068 bytes (87.10 MiB) |
| Archive + extracted cache | 174,510,889 bytes (166.43 MiB) |
| Generated `chroma_db/` index | 2,593,508 bytes (2.47 MiB) |

Required companions: `tokenizer.json`, `vocab.txt`, `config.json`,
`tokenizer_config.json`, and `special_tokens_map.json`. These are disk sizes;
peak hosted RAM against the 512 MiB limit remains unmeasured. Generation uses
the hosted Gemini API; no local generation weights are needed.

### Verification and logs

Clean checkout tested: `5e26c4718212816f89e888f8ec7b65208bc66ec1`,
CPython 3.13.7, Debian Bookworm x86_64, in a separate clone.

| Check | Result |
| --- | --- |
| Venv, `sh build.sh`, model download and indexing | Passed; 88 documents → 183 chunks |
| `sh start.sh` and `/health` | Passed; `index_ready: true` |
| Local unsupported question using real ONNX retrieval | HTTP 200, `refused: true`, matching request ID |
| Runtime container limited to 512 MiB | Remained healthy; no OOM kills during the check |
| Full local generated campus answer | Not verified with a valid key; owner requested skipping the additional check |
| Live campus answer | HTTP 200; actual answer shown above |

The local refusal check used a placeholder key and skipped Gemini generation.
The build was not memory-limited. Native Windows/macOS startup and concurrent
traffic were not tested.

**Read logs:** Render → campus-life-rag → **Logs**, search `rag_request`.
Each completed `POST /ask` emits JSON; match its `request_id` to the response's
`X-Request-ID`. Copy needed JSON records promptly; free-host logs may not persist.
See [README Capstone](README.md#capstone) for log evidence,
cost measurements, and formal results.
