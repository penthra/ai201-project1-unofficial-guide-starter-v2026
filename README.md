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

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     week 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     week — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer | MET | All five questions retrieved an answer-containing chunk in each of the three runs, exceeding the 4/5 target. |
| 2 | Every answer names a source | MET | All five answers named at least one source in every run. |
| 3 | Gate rejects out-of-corpus questions and returns the required refusal | PENDING | The gate rejected all five questions. I still need to verify the exact refusal message, which is not shown in the log. |
| 4 | Inspected chunks are focused and understandable independently | MET | I inspected the first retrieved chunk for each question. All five had clear subjects and understandable main points in every run. |
| 5 | Answers are supported by the retrieved chunks | MET | All answers were supported. The scorer rejected “three midterm exams” in run 2 because it did not exactly match “three midterms,” but the meaning was unchanged. |


### When can students purchase a parking permit? — run 1

- Best distance: 0.4196 (passed the gate)
- Sources retrieved: admin_library_holds.txt, admin_parking_permits.txt, advising_registration.txt, study_library_hours.txt, transit_shuttle.txt

#### Generated answer

````text
Student permits for the west lots go on sale in August (admin_parking_permits.txt).
````

#### Retrieved chunks

- Chunk: admin_parking_permits.txt#0
- Distance: 0.4196
- Produced by: chunker.py::split_documents

````text
On the parking permits

Student permits for the west lots go on sale in August and sell out in about three days. The east lot never sells out because it's a 12-minute walk. There is no waitlist — people who miss the window park on Verrill Street and walk in, which is legal but unmarked and confuses everyone.
````

- Chunk: transit_shuttle.txt#1
- Distance: 0.6248
- Produced by: chunker.py::split_documents

````text
The campus shuttle

It's free with a student ID. The stop outside Fenwick Court is the one that gets skipped when the driver is behind, which is worth knowing if you live there.
````

- Chunk: advising_registration.txt#1
- Distance: 0.6675
- Produced by: chunker.py::split_documents

````text
Registration and your adviser

Registration times are staggered by credit hours, same as the housing lottery. Popular courses fill in the first two days.
````

- Chunk: admin_library_holds.txt#0
- Distance: 0.7013
- Produced by: chunker.py::split_documents

````text
On the library holds

You can place a hold on a checked-out book and it usually arrives in two to three days. What isn't advertised: the interlibrary system covers eleven other institutions and requests through it take about a week but almost never fail.
````

- Chunk: study_library_hours.txt#0
- Distance: 0.7134
- Produced by: chunker.py::split_documents

````text
Library hours and where to actually sit

Open until 2am during term, until 10pm during reading week, which is backwards and catches everyone out every single year.
````


## Diagnoses

Manual review found no confirmed misses in C1, C2, C4, or C5. The gate rejected all five out-of-corpus questions, but I still need to verify C3's exact refusal message.

The scorer marked the PHYS 130 answer in run 2 as a failure because it expected “three midterms,” while the answer said “three midterm exams.” Both expressions match the retrieved information. The cause was exact phrase matching in scorer.py, not incorrect retrieval or generation.

My questions are straightforward factual lookups, so the tests cover a limited range of behavior. I would tighten C1 from 4/5 to 5/5 in future because all five questions ask for facts explicitly stated in the corpus. I will keep the original targets unchanged for this Before/After comparison.

## The Improvement

**What I changed:**

[After implementing this change:] I updated normalize() in scorer.py to normalize “midterm exams” to “midterms” before checking the expected phrase.

**Why I picked it:**

This directly addresses the observed false negative: the scorer should accept these equivalent expressions instead of rejecting a supported answer because its wording differs.


### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
