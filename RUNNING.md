# Running the Campus Life RAG

## Capstone: Running It

CodePath AI201 Project 1 extension: **Shape A — Deploy and instrument; Path A — Hosted**.
The existing Flask API calls the original `app.py::ask_pipeline`.

### 1. Try the live app

**Render URL:** https://campus-life-rag.onrender.com

This is a JSON API. Use `/ask` for questions; the root `/` has no form.

```bash
curl --silent --show-error --max-time 55 \
  --request POST https://campus-life-rag.onrender.com/ask \
  --header 'Content-Type: application/json' \
  --data '{"question":"When can students purchase a parking permit?"}'
```

The endpoint is **POST `/ask`**, with a JSON body containing `question`.
Verified on November 14, 2026 (Pacific): **HTTP 200**, with this actual answer:

> Student permits for the west lots go on sale in August (admin_parking_permits.txt).

The response had `refused: false`, `best_distance: 0.4196`, `threshold: 0.6`,
and `admin_parking_permits.txt` among its sources. Client elapsed time was
**15.765645 seconds**; initial cold/warm state was unknown. This was a functional
check, not another formal latency trial.

Readiness check:

```bash
curl --silent --show-error --max-time 55 \
  https://campus-life-rag.onrender.com/health
```

Verified response: HTTP 200 with `corpus: campus_life`, `status: ok`,
`detail: ready`, and **`index_ready: true`**. That flag confirms the index,
not that the embedding model is already loaded or a Gemini call will succeed.
First requests can be slower while the free service starts or loads assets.

### 2. Reproduce the Render configuration

The owner reports that the existing service uses this repository's configuration.
The following settings are read from `render.yaml` and the scripts; they have
not been independently copied from the current Render dashboard.

| Setting | Repository configuration |
| --- | --- |
| Service | Existing `campus-life-rag` Render Web Service |
| Runtime / plan | Python / Free |
| Root directory | Repository root, containing `render.yaml` |
| Python | `3.13.7` from `.python-version` |
| Build command | `sh build.sh` |
| Start command | `sh start.sh` |
| Health check path | `/health` |
| Automatic deploys | Off |

`build.sh` installs the exact direct dependency pins, rebuilds
`chroma-hnswlib` for a portable CPU target, checks dependencies/imports, and
builds the index and model cache. `start.sh` checks the key and built index,
then launches one Gunicorn worker serving `serve:app`, bound to `0.0.0.0` on
Render's supplied port. Startup does not repeat corpus indexing.

**Environment variable names only:** set manual variables in
**Render Dashboard → campus-life-rag → Environment**. Keep non-secret settings
from `render.yaml`; supply the API key privately. No credential values belong
in Git, this guide, screenshots, or chat.

| Name | Required / where it comes from |
| --- | --- |
| `GEMINI_API_KEY` | Required secret; enter privately in Render Environment. |
| `AI201_CORPUS` | Non-secret selection defined in `render.yaml`; scripts also have a default. |
| `AI201_CACHE` | Non-secret response-cache setting defined in `render.yaml`. |
| `AI201_EMBED_BATCH_SIZE` | Non-secret memory-control setting defined in `render.yaml`. |
| `AI201_MODEL` | Optional override supported by `config.py`; only set if needed. |
| `PORT` | Supplied by Render; do not replace it to fix a startup failure. |
| `PYTHON_VERSION` | Optional Render override, if present; it must agree with the intended Python pin. |

The scripts set `AI201_EMBED_CACHE_DIR`, `PYTHONUNBUFFERED`, and
`PYTHONFAULTHANDLER` themselves. `build.sh` sets `HNSWLIB_NO_NATIVE` for the
portable native build. Do not enable the staff-only `AI201_FAKE_EMBEDDINGS`.

**Still needed for independent dashboard verification:** copy the currently
Live deploy's full Git SHA, Settings → **Build Command**, **Start Command**,
**Runtime**, **Instance Type**, and **Health Check Path**; the Python version
line from that successful build; and Environment **names only**. The public
API does not expose these settings or its Git SHA. Earlier baseline revision
`1694a57` was user-attested; the clean checkout below is a repository revision,
not proof of what Render is currently running. Do not send secret values.

### 3. Run locally after a clean setup

**Tested environment:** CPython **3.13.7**, Linux x86_64, Debian Bookworm.
Use Linux or WSL for this Gunicorn path. Native Windows and macOS were not tested.
A C++ compiler, matching Python development headers, outbound package/model
access, and writable repository/cache directories are needed.

From a fresh clone, select Python 3.13.7 first. `.python-version` records the
version but does not install it. Then run from the repository root:

```bash
python --version
python -m venv .venv
. .venv/bin/activate
sh build.sh
```

`sh build.sh` is the dependency installation and asset-preparation command.
It runs `python -m pip install -r requirements-runtime.txt`, rebuilds the
portable native library, runs `pip check`, and indexes the corpus. Expect
`No broken requirements found`, `hnswlib import OK`, and `stored 183 chunks`.

Provide a valid Gemini API key **locally**. Having it only in Render does not
make it available on your laptop. In Bash, enter it without recording the
value in a command-history assignment:

```bash
read -r -s -p 'Gemini API key: ' GEMINI_API_KEY
printf '\n'
export GEMINI_API_KEY
```

**Exact start command after setup**, with the virtual environment active:

```bash
sh start.sh
```

It listens on `http://127.0.0.1:5000` unless a port is supplied. In another
terminal, use the live curl commands above with that local origin. A valid
local key is needed for an in-corpus generated answer.

The shell script requires an **exported** key; it does not source `.env`.
Although `config.py` supports an ignored `.env` for CLI/development use,
a file alone does not satisfy `start.sh`'s shell-level check. Keep `.env`,
`.venv`, model assets, and `chroma_db/` out of Git.

#### Pinned dependencies

| Package | Exact runtime pin |
| --- | --- |
| python-dotenv | 1.1.1 |
| chromadb | 0.6.3 |
| posthog | 3.25.0 |
| google-genai | 1.75.0 |
| rank-bm25 | 0.2.2 |
| Flask | 3.1.3 |
| Gunicorn | 23.0.0 |
| chroma-hnswlib | 0.7.6, explicitly rebuilt by `build.sh` |

`requirements-runtime.txt` retains the course ranges as constraints. These
are direct pins, **not a complete transitive lockfile**. The clean test also
resolved ONNX Runtime 1.32.0 and NumPy 2.5.4; those are observed versions,
not additional pins. Installing only the course ranges skips the exact direct
pins and portable-native rebuild used by the documented build path.

#### Required model assets

Embeddings use **all-MiniLM-L6-v2**, a local ONNX model producing 384-dimensional
vectors. The build downloads its archive from:
`https://chroma-onnx-models.s3.amazonaws.com/all-MiniLM-L6-v2/onnx.tar.gz`.
No manual model-file copy is required. Measured clean-download sizes:

| File | Bytes |
| --- | ---: |
| `onnx.tar.gz` | 83,178,821 |
| `onnx/model.onnx` | 90,387,606 |
| `onnx/tokenizer.json` | 711,661 |
| `onnx/vocab.txt` | 231,508 |
| `onnx/config.json` | 650 |
| `onnx/tokenizer_config.json` | 518 |
| `onnx/special_tokens_map.json` | 125 |

The archive is **79.33 MiB**; extracted files total **87.10 MiB**. Both are
retained, requiring about **166.43 MiB** of model-cache disk space, plus the
index and Python packages. The clean index occupied about **2.47 MiB**.
These are disk sizes, not RAM requirements.

Both scripts use `.cache/embedding-models/all-MiniLM-L6-v2/` in the build/runtime
artifact and `chroma_db/` for the generated index. The corpus documents are
already tracked under `corpora/campus_life/documents/`. Generation uses Google's
hosted Gemini API; `config.py` defaults to `gemini-3.5-flash-lite`. No local
Gemini weights, sentence-transformers, or PyTorch installation is required.

#### Clean-checkout verification

A new separate clone of **`5e26c4718212816f89e888f8ec7b65208bc66ec1`** was made at
`/tmp/ai201-running-check-kaTjmf/repo`. No dependency environment, index, model
cache, or credentials were copied from the working repo. The following
commands were actually exercised in the fresh Python 3.13.7 container:

| Check | Result |
| --- | --- |
| Create and activate a venv | Passed; system site-packages disabled. |
| `sh build.sh` | Passed pinned install, portable compilation/import, and dependency check. |
| Real model download and index build | Passed: 88 documents → 183 chunks. |
| `sh start.sh` | Passed; Gunicorn started on the local port. |
| Local `/health` | HTTP 200, `index_ready: true`. |
| Local `/ask` with an unrelated question | HTTP 200, exact refusal, `refused: true`, and an application request ID. Real ONNX retrieval was used. |
| Health after the request | HTTP 200; no OOM kills in the 512 MiB runtime container. |

A placeholder key was used only to satisfy the startup guard. The unrelated
question was rejected before Gemini generation, so **full local generated
answers were not tested with a valid key**. The real campus answer was verified
at the live Render URL instead. Peak hosted RAM, concurrent traffic, a new
Render deployment, and native Windows/macOS startup were not tested. The
container's build phase was not constrained to 512 MiB. This was a functional
setup check, not a repetition of formal acceptance trials.

### Logs and further evidence

In the existing Render service's **Logs** page, search for `rag_request`.
Every `POST /ask` logs one JSON completion record; its `request_id` matches
the response's `X-Request-ID`. Health traffic is separate. The original
baseline results, log tables, cost measurements, and submission limitations
remain in the README and linked `results/` evidence. This guide does not
create another Render service, trigger a deploy, or perform Git actions.
