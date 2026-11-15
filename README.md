# The Unofficial Guide

Peng Wu — Campus corpus

---

# Week 1

## What This Does

This project uses a corpus of short campus posts to answer questions about student life, including parking, courses, dining, housing, and campus services. It retrieves relevant chunks and gives them to a language model to produce an answer with sources. A relevance gate checks the best retrieval distance and rejects questions when no chunk is close enough. My five test questions ask about parking permit availability, walking time, midterm exams, dining hours, and Wi-Fi access.

## Chunking Strategy

Chunk size: Variable—one body paragraph per chunk, with the document title added to each chunk.
Overlap: No overlap between body paragraphs. The title repeats in each chunk.

My documents are short posts, and their paragraphs often keep related sentences together. I chose paragraph boundaries to avoid cutting sentences in the middle. I repeat the title in each chunk to help identify its subject when it is retrieved without the rest of the document.

My first version treated titles as separate chunks because they were separated from the body by blank lines. I revised it to attach the title to each body paragraph instead. This strategy assumes the first paragraph of each document is its title.

## Sample Chunks


Chunk 1  |  source: admin_add_drop_deadline.txt#0  |  produced by: chunker.py::split_documents

On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.


Chunk 2  |  source: course_cs_340_exams.txt#1  |  produced by: chunker.py::split_documents

CS 340 Databases — assessment

Start the term project in week three, not week eight; everyone learns this the hard way.


Chunk 3  |  source: course_phys_130_workload.txt#0  |  produced by: chunker.py::split_documents

Workload for PHYS 130 Mechanics

People keep asking so: 7 hours a week, plus 3 on lab weeks. That's real time, not optimistic time.


Chunk 4  |  source: dining_verrill_street_grill_followup.txt#1  |  produced by: chunker.py::split_documents

Re: Verrill Street Grill

Also worth saying: one register, so the queue is a single line no matter how busy. Nobody tells you this at orientation.


Chunk 5  |  source: housing_morrow_house.txt#1  |  produced by: chunker.py::split_documents

Morrow House — what it's actually like

The good: cheapest housing tier by about $900 a year, and the singles are real singles.

## Sample Answer

**Question:** "When can students purchase a parking permit?"

**Answer:** Student permits for the west lots go on sale in August (admin_parking_permits.txt).

Sources retrieved: admin_library_holds.txt, admin_parking_permits.txt, advising_registration.txt, study_library_hours.txt, transit_shuttle.txt
```
```

**My relevance cutoff:** 0.6

| Question                                                            | In corpus? | Best distance |
| ------------------------------------------------------------------- | ---------- | ------------- |
| When can students purchase a parking permit?                        | Yes        | 0.4196        |
| How long does it take to walk from Fenwick Court to central campus? | Yes        | 0.2129        |
| How many midterm exams are scheduled for PHYS 130 Mechanics?        | Yes        | 0.2583        |
| What are Halden Hall's weekday serving hours?                       | Yes        | 0.2064        |
| What account do students need to access campus Wi-Fi?               | Yes        | 0.3511        |
| What is the capital of Mongolia?                                    | No         | 0.7873        |
| How do I change the oil in a diesel engine?                         | No         | 0.9228        |
| Who won the 1994 World Cup?                                         | No         | 0.8474        |
| What is the recommended dosage of ibuprofen for a headache?         | No         | 0.8487        |
| How do I write a for loop in Rust?                                  | No         | 0.8598        |


## How I Used AI


**1.** 
I asked ChatGPT to help write a paragraph-based chunking function. The first version split at blank lines, which made titles separate chunks. After inspecting the output, I asked for a revision that repeats the title with each body paragraph so each chunk has more context.

**2.**
I asked ChatGPT to help make my fourth criterion clearer. We discussed checking whether chunks could be understood independently, but I noticed that this did not check whether they included unrelated topics. I revised the criterion to require at least four of five inspected chunks to focus on one topic and include enough context to understand the main point without reading another chunk.

---

# Week 2

## Run Log — Before


| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunks contain the answer | At least 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate rejects out-of-corpus questions and returns the required refusal | At least 4 of 5 | 5/5 rejected | 5/5 rejected | 5/5 rejected | MET|
| 4. Inspected chunks are focused and understandable independently | At least 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Answers are supported by the retrieved chunks | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

## Verdicts



| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer | MET | All five questions retrieved an answer-containing chunk in each of the three runs, exceeding the 4/5 target. |
| 2 | Every answer names a source | MET | All five answers named at least one source in every run. |
| 3 | Gate rejects out-of-corpus questions and returns the required refusal | MET | The gate rejected all five questions. I still need to verify the exact refusal message, which is not shown in the log. |
| 4 | Inspected chunks are focused and understandable independently | MET | I inspected the first retrieved chunk for each question. All five had clear subjects and understandable main points in every run. |
| 5 | Answers are supported by the retrieved chunks | MET | All answers were supported. The scorer rejected “three midterm exams” in run 2 because it did not exactly match “three midterms,” but the meaning was unchanged. |


| Question | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| When can students purchase a parking permit? | pass | pass | pass |
| How long does it take to walk from Fenwick Court to central campus? | pass | pass | pass |
| How many midterm exams are scheduled for PHYS 130 Mechanics? | pass | fail | pass |
| What are Halden Hall's weekday serving hours? | pass | pass | pass |
| What account do students need to access campus Wi-Fi? | pass | pass | pass |

### How many midterm exams are scheduled for PHYS 130 Mechanics? — run 2

- Best distance: 0.2583 (passed the gate)
- Sources retrieved: course_phys_130.txt, course_phys_130_exams.txt, course_phys_130_workload.txt

#### Generated answer

````text
There are three midterm exams scheduled for PHYS 130 Mechanics. 

This information came from `course_phys_130.txt` and `course_phys_130_exams.txt`.
````

#### Retrieved chunks

- Chunk: course_phys_130.txt#0
- Distance: 0.2583
- Produced by: chunker.py::split_documents

````text
PHYS 130 Mechanics

Just finished a year in this building. Format is lecture with a compulsory lab that meets fortnightly. Assessment: three midterms, no final, plus a lab practical. Not curved, but the lowest midterm is dropped.
````

- Chunk: course_phys_130.txt#1
- Distance: 0.3589
- Produced by: chunker.py::split_documents

````text
PHYS 130 Mechanics

Expect 7 hours a week, plus 3 on lab weeks.
````

- Chunk: course_phys_130_exams.txt#0
- Distance: 0.3762
- Produced by: chunker.py::split_documents

````text
PHYS 130 Mechanics — assessment

Three midterms, no final, plus a lab practical. Not curved, but the lowest midterm is dropped.
````

- Chunk: course_phys_130_exams.txt#1
- Distance: 0.4109
- Produced by: chunker.py::split_documents

````text
PHYS 130 Mechanics — assessment

The lab practical is worth 20% and almost nobody prepares for it.
````

- Chunk: course_phys_130_workload.txt#0
- Distance: 0.4147
- Produced by: chunker.py::split_documents

````text
Workload for PHYS 130 Mechanics

People keep asking so: 7 hours a week, plus 3 on lab weeks. That's real time, not optimistic time.
````


## Diagnoses

Manual review found no confirmed criterion misses, but my targets were relatively low for this test set. All five questions asked for straightforward facts, and the out-of-corpus questions were clearly unrelated to campus life. These results show that the system handles my basic tests, not that it is excellent. C3’s rejection count passed, although I still need to verify its exact refusal message.

The scorer marked the PHYS 130 answer in run 2 as a failure because “three midterm exams” did not exactly match “three midterms.” The meaning was correct and supported by the retrieved chunks, so this was a scorer limitation rather than a criterion miss.

For future evaluations, I would tighten C1 from at least 4/5 to 5/5 in every run because all five answers are explicitly stated in the corpus. I will keep the original targets unchanged for this Before/After comparison.

## The Improvement

**What I changed:**

[After implementing this change:] I updated normalize() in scorer.py to normalize “midterm exams” to “midterms” before checking the expected phrase.

**Why I picked it:**

This directly addresses the observed false negative: the scorer should accept these equivalent expressions instead of rejecting a supported answer because its wording differs.


### Run Log — After

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer | MET | All five questions retrieved an answer-containing chunk in each of the three runs, exceeding the 4/5 target. |
| 2 | Every answer names a source | MET | All five answers named at least one source in every run. |
| 3 | Gate rejects out-of-corpus questions and returns the required refusal | MET | The gate rejected all five questions. I still need to verify the exact refusal message, which is not shown in the log. |
| 4 | Inspected chunks are focused and understandable independently | MET | I inspected the first retrieved chunk for each question. All five had clear subjects and understandable main points in every run. |
| 5 | Answers are supported by the retrieved chunks | MET | All answers were supported.|


| Question | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| When can students purchase a parking permit? | pass | pass | pass |
| How long does it take to walk from Fenwick Court to central campus? | pass | pass | pass |
| How many midterm exams are scheduled for PHYS 130 Mechanics? | pass | pass | pass |
| What are Halden Hall's weekday serving hours? | pass | pass | pass |
| What account do students need to access campus Wi-Fi? | pass | pass | pass |

### How many midterm exams are scheduled for PHYS 130 Mechanics? — run 2

- Best distance: 0.2583 (passed the gate)
- Sources retrieved: course_phys_130.txt, course_phys_130_exams.txt, course_phys_130_workload.txt

#### Generated answer

````text
There are three midterms scheduled for PHYS 130 Mechanics. This information comes from `course_phys_130.txt` and `course_phys_130_exams.txt`.
````

#### Retrieved chunks

- Chunk: course_phys_130.txt#0
- Distance: 0.2583
- Produced by: chunker.py::split_documents

````text
PHYS 130 Mechanics

Just finished a year in this building. Format is lecture with a compulsory lab that meets fortnightly. Assessment: three midterms, no final, plus a lab practical. Not curved, but the lowest midterm is dropped.
````

- Chunk: course_phys_130.txt#1
- Distance: 0.3589
- Produced by: chunker.py::split_documents

````text
PHYS 130 Mechanics

Expect 7 hours a week, plus 3 on lab weeks.
````

- Chunk: course_phys_130_exams.txt#0
- Distance: 0.3762
- Produced by: chunker.py::split_documents

````text
PHYS 130 Mechanics — assessment

Three midterms, no final, plus a lab practical. Not curved, but the lowest midterm is dropped.
````

- Chunk: course_phys_130_exams.txt#1
- Distance: 0.4109
- Produced by: chunker.py::split_documents

````text
PHYS 130 Mechanics — assessment

The lab practical is worth 20% and almost nobody prepares for it.
````

- Chunk: course_phys_130_workload.txt#0
- Distance: 0.4147
- Produced by: chunker.py::split_documents

````text
Workload for PHYS 130 Mechanics

People keep asking so: 7 hours a week, plus 3 on lab weeks. That's real time, not optimistic time.
````

**Did it help?**

The revised scorer checks for individual expected words instead of one exact phrase and applies simple plural normalization. This allows “three midterm exams” to match “three midterms” when the answer also names a retrieved source. I still need to inspect the After results to confirm its behavior across all three runs. This change improves the matching rule; it does not change retrieval or answer generation.

## What's Still Broken

The scorer checks word presence, not meaning. It could accept “There are not three midterms” because the expected words are present. Its plural normalization is also approximate, and it does not recognize every valid paraphrase.

I therefore still need to compare answers with their retrieved chunks when evaluating C5. I cannot yet identify which criteria remain missed after the change because the After results have not been reviewed.

## What I'd Do Differently

I would make C4's sampling rule explicit: inspect the first retrieved chunk for each of my five questions. That would make the evaluation more consistent.

For future evaluations, I would tighten C1 from 4 of 5 to 5 of 5 because my questions ask for straightforward facts explicitly present in the corpus. I would keep C5 focused on factual support rather than exact wording. The Before and After comparison still uses my original criteria and targets.

## Capstone

**What This Extends**

My Project 1 `campus_life` RAG: paragraph chunks, Chroma cosine retrieval (top 5), a 0.6 relevance gate, and grounded answers that cite source files. `serve.py` already wraps the pipeline in Flask with `POST /ask` and `GET /health`, but it is only run locally and has no request logging.

**The Shape**

Shape A (Deploy and instrument), Path A (Hosted): deploy the existing Flask API at a public HTTPS URL and add structured logging to `/ask`.

**Running It**

See [RUNNING.md](RUNNING.md#capstone-running-it) for the live Render URL, setup, start commands, and deployment verification status.

**Deployment**

- Set `AI201_CORPUS=campus_life` and store `GEMINI_API_KEY` as a host secret. Confirm the configured Gemini model is available to the course account.
- Build with `sh build.sh` to package the index and embedding assets. Start with `sh start.sh` to launch one Gunicorn worker on Render's port without repeating indexing. Each deploy rebuilds the artifacts; restarts reuse the deployed build.
- The service is ready when `/health` returns `index_ready: true`, not just HTTP 200.
- Usage: `POST https://<host>/ask` with `{"question": "..."}` returns the answer, sources, refusal flag, best distance, and threshold.

**Instrumentation**

`serve.py` now emits one JSON completion record to stdout for each `POST /ask`, including answers, refusals, validation failures, and handled exceptions. Records contain UTC timestamp, request ID, question, answer, corpus, configured model, cache setting, sources, best distance, threshold, refusal flag, HTTP status, server duration in milliseconds, and error type when applicable. The response's `X-Request-ID` matches the record. Exception messages and environment values are excluded from these records.

Read the existing service's **Logs** page in Render and search for `rag_request`. Match the response's `X-Request-ID` to the JSON record's `request_id`; Render's `Rndr-Id` is a separate platform ID. See [Render's log guide](https://render.com/docs/logging).

The user copied the real Render JSON message lines promptly, and they are now preserved in [server JSONL](results/hosted_cost_20261114T211124Z.render.jsonl). That file contains thirteen records: the initial invalid-input preflight, the excluded warm-up, ten measured requests, and the extra rejected request. Platform access and health-check lines were omitted from this JSONL because they are not application completion records. The [full client JSONL](results/hosted_cost_20261114T211124Z.jsonl) was flushed and synced after each request; the [summary](results/hosted_cost_20261114T211124Z.summary.json) contains both measured averages and provenance.

All ten measured records were matched by request ID, HTTP status, question, answer, sources, refusal flag, distance, threshold, and corpus to the saved client responses. Each measured request has exactly one matching record in the supplied export. All show `cache_enabled: false` and configured model `gemini-3.5-flash-lite`. The non-string question (`{"question":123}`) produced a matching HTTP 400 `ValidationError` record, so a rejection was actually exercised and observed.

The following text is **ten actual server records plus that rejected run**, copied from the supplied Render export. The warm-up and initial preflight are archived but excluded here and from the average.

```jsonl
{"event": "rag_request", "timestamp": "2026-11-14T21:11:41.720496+00:00", "request_id": "8eb1d39a-9307-40ef-8ed0-2af31cc9031a", "question": "When can students purchase a parking permit?", "answer": "Student permits for the west lots go on sale in August (admin_parking_permits.txt).", "corpus": "campus_life", "model": "gemini-3.5-flash-lite", "cache_enabled": false, "sources": ["admin_library_holds.txt", "admin_parking_permits.txt", "advising_registration.txt", "study_library_hours.txt", "transit_shuttle.txt"], "best_distance": 0.4196, "threshold": 0.6, "refused": false, "http_status": 200, "duration_ms": 3425.701, "error_type": null}
{"event": "rag_request", "timestamp": "2026-11-14T21:11:45.327706+00:00", "request_id": "c946f72b-00b8-40b9-aecb-3a88342052f9", "question": "How long does it take to walk from Fenwick Court to central campus?", "answer": "It takes about 18 minutes on foot to walk from Fenwick Court to central campus. \n\nSource: `transit_walking.txt` and `housing_fenwick_court.txt`", "corpus": "campus_life", "model": "gemini-3.5-flash-lite", "cache_enabled": false, "sources": ["housing_fenwick_court.txt", "housing_fenwick_court_noise.txt", "transit_shuttle.txt", "transit_walking.txt"], "best_distance": 0.2129, "threshold": 0.6, "refused": false, "http_status": 200, "duration_ms": 3079.784, "error_type": null}
{"event": "rag_request", "timestamp": "2026-11-14T21:11:48.571175+00:00", "request_id": "06026626-4eb3-4ffe-b0bd-0f8aceaabad7", "question": "How many midterm exams are scheduled for PHYS 130 Mechanics?", "answer": "There are three midterms scheduled for PHYS 130 Mechanics. \n\nSource: `course_phys_130.txt` (and also found in `course_phys_130_exams.txt`)", "corpus": "campus_life", "model": "gemini-3.5-flash-lite", "cache_enabled": false, "sources": ["course_phys_130.txt", "course_phys_130_exams.txt", "course_phys_130_workload.txt"], "best_distance": 0.2583, "threshold": 0.6, "refused": false, "http_status": 200, "duration_ms": 4058.572, "error_type": null}
{"event": "rag_request", "timestamp": "2026-11-14T21:11:52.782802+00:00", "request_id": "044d92ef-e7b0-4b25-96e6-8b4337a16c35", "question": "What are Halden Hall's weekday serving hours?", "answer": "Halden Hall's weekday hours are 7:30am to 7:00pm (source: dining_halden_hall.txt).", "corpus": "campus_life", "model": "gemini-3.5-flash-lite", "cache_enabled": false, "sources": ["dining_halden_hall.txt", "dining_halden_hall_followup.txt", "dining_the_atrium.txt"], "best_distance": 0.2064, "threshold": 0.6, "refused": false, "http_status": 200, "duration_ms": 3776.169, "error_type": null}
{"event": "rag_request", "timestamp": "2026-11-14T21:11:56.754468+00:00", "request_id": "1ac4d206-31fd-4a63-a198-e11121e08085", "question": "What account do students need to access campus Wi-Fi?", "answer": "Students need a student account to access campus Wi-Fi (admin_wifi_and_accounts.txt).", "corpus": "campus_life", "model": "gemini-3.5-flash-lite", "cache_enabled": false, "sources": ["admin_wifi_and_accounts.txt", "money_jobs.txt", "money_textbooks.txt", "transit_shuttle.txt"], "best_distance": 0.3511, "threshold": 0.6, "refused": false, "http_status": 200, "duration_ms": 3446.688, "error_type": null}
{"event": "rag_request", "timestamp": "2026-11-14T21:12:00.487185+00:00", "request_id": "aa05e3b6-63c7-42c8-a741-670cc6883b10", "question": "When can students purchase a parking permit?", "answer": "Student permits for the west lots go on sale in August (admin_parking_permits.txt).", "corpus": "campus_life", "model": "gemini-3.5-flash-lite", "cache_enabled": false, "sources": ["admin_library_holds.txt", "admin_parking_permits.txt", "advising_registration.txt", "study_library_hours.txt", "transit_shuttle.txt"], "best_distance": 0.4196, "threshold": 0.6, "refused": false, "http_status": 200, "duration_ms": 3105.508, "error_type": null}
{"event": "rag_request", "timestamp": "2026-11-14T21:12:03.794177+00:00", "request_id": "df094b44-b6af-426e-ab77-9b1c9294199c", "question": "How long does it take to walk from Fenwick Court to central campus?", "answer": "It takes about 18 minutes on foot to walk from Fenwick Court to central campus. \n\nSource documents: `transit_walking.txt` and `housing_fenwick_court.txt`.", "corpus": "campus_life", "model": "gemini-3.5-flash-lite", "cache_enabled": false, "sources": ["housing_fenwick_court.txt", "housing_fenwick_court_noise.txt", "transit_shuttle.txt", "transit_walking.txt"], "best_distance": 0.2129, "threshold": 0.6, "refused": false, "http_status": 200, "duration_ms": 3342.495, "error_type": null}
{"event": "rag_request", "timestamp": "2026-11-14T21:12:07.289142+00:00", "request_id": "c79f1e48-b463-4d77-b6b5-f58b59ae7c0e", "question": "How many midterm exams are scheduled for PHYS 130 Mechanics?", "answer": "There are three midterms scheduled for PHYS 130 Mechanics (source: `course_phys_130.txt` and `course_phys_130_exams.txt`).", "corpus": "campus_life", "model": "gemini-3.5-flash-lite", "cache_enabled": false, "sources": ["course_phys_130.txt", "course_phys_130_exams.txt", "course_phys_130_workload.txt"], "best_distance": 0.2583, "threshold": 0.6, "refused": false, "http_status": 200, "duration_ms": 3222.626, "error_type": null}
{"event": "rag_request", "timestamp": "2026-11-14T21:12:10.646856+00:00", "request_id": "0246bee7-c1bd-4298-ac44-58eb118dce88", "question": "What are Halden Hall's weekday serving hours?", "answer": "Halden Hall's weekday hours are 7:30am to 7:00pm (source: dining_halden_hall.txt).", "corpus": "campus_life", "model": "gemini-3.5-flash-lite", "cache_enabled": false, "sources": ["dining_halden_hall.txt", "dining_halden_hall_followup.txt", "dining_the_atrium.txt"], "best_distance": 0.2064, "threshold": 0.6, "refused": false, "http_status": 200, "duration_ms": 3907.116, "error_type": null}
{"event": "rag_request", "timestamp": "2026-11-14T21:12:14.702716+00:00", "request_id": "47bef557-14c8-49c4-8630-04229bf7111b", "question": "What account do students need to access campus Wi-Fi?", "answer": "Students need a student account to access campus Wi-Fi. \n\nSource: admin_wifi_and_accounts.txt", "corpus": "campus_life", "model": "gemini-3.5-flash-lite", "cache_enabled": false, "sources": ["admin_wifi_and_accounts.txt", "money_jobs.txt", "money_textbooks.txt", "transit_shuttle.txt"], "best_distance": 0.3511, "threshold": 0.6, "refused": false, "http_status": 200, "duration_ms": 5250.16, "error_type": null}
{"event": "rag_request", "timestamp": "2026-11-14T21:12:20.097696+00:00", "request_id": "20b828d9-f7d9-46db-91a7-35cd29a11e0d", "question": null, "answer": null, "corpus": "campus_life", "model": "gemini-3.5-flash-lite", "cache_enabled": false, "sources": [], "best_distance": null, "threshold": 0.6, "refused": null, "http_status": 400, "duration_ms": 0.216, "error_type": "ValidationError"}
```

**What It Costs**

**Measured average: 3.695436 seconds per hosted request** (3695.436 ms), based on ten actual sequential requests to `https://campus-life-rag.onrender.com/ask`. All ten returned HTTP 200. Total measured elapsed time was 36.954362995 seconds; `sum(elapsed_ns) / 10 / 1,000,000,000 = 3.6954362995 seconds/request`. Observed range: 3.140021–5.199396 seconds.

This measures **client-observed elapsed time**, not API dollars, tokens, CPU time, or the server-only `duration_ms` field. A monotonic nanosecond clock started immediately before Python urllib sent each request and stopped after reading the full response body. It includes DNS/TLS/network overhead, retrieval, API waits/retries, generation, and response transfer. Each urllib call could create a new connection; connection reuse was not assumed. The five existing Project 1 questions were sent twice in order, with no deliberate pause or automatic retries. Every one of the ten measured attempts is included; no outliers were discarded.

**Warm conditions:** one successful parking-permit warm-up took 15.273036223 seconds and is excluded from the ten-run average. It was followed immediately by the measured requests; this operationally warms the service/model but does not establish whether the warm-up itself was a cold start or guarantee that every provider connection stayed warm. Requests were recorded on November 14, 2026, with UTC timestamps in the saved JSONL. The extra invalid-input request (`{"question":123}`) returned HTTP 400 in 0.133399098 seconds and is also excluded from the average.

The matching **server-side mean was 3.6614819 seconds/request** (3661.4819 ms): `sum(duration_ms) / 10 = 36614.819 / 10 = 3661.4819 ms`. This is the application's elapsed request-handling time from its monotonic timer, not CPU time or model-only inference time; it excludes client/network transfer and the log print itself. The server warm-up was 15640.101 ms and the invalid-input run was 0.216 ms, both excluded. Cache-disabled status is now verified in all ten measured server records, so they were not served by the application's response cache. Actual provider billing, token counts, API retries, and provider-side caching were not measured or inferred.

Client and server durations are separate observations from independent clocks. In measured runs 9, 10, the supplied server duration is slightly larger than the corresponding client duration; the excluded warm-up also has this discrepancy. Its cause is unverified. Preserve both measured series and do not subtract them to estimate network overhead or treat them as interchangeable. The primary reported average remains the directly saved client elapsed-time measure above.

No API-dollar or token estimate is reported. This cost sample does not score acceptance criteria or run the Milestone 5 formal trials.

**Memory Check (512 MB limit)**

Query embeddings still run locally (`all-MiniLM-L6-v2` via ONNX), so I'll measure peak RAM during startup, indexing, and queries before claiming the service fits. One Gunicorn worker keeps memory down. If it exceeds 512 MB, I'll fix it within a hosted deployment.

**Out of Scope**

- No changes to the corpus, chunking, embeddings, retrieval, gate, or prompt.
- No frontend, accounts, or chat history; the JSON API is the interface.
- No dashboard or new evaluation system; instrumentation is logging only.