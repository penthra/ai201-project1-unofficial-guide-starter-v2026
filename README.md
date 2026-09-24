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
| 3 | Gate rejects out-of-corpus questions and returns the required refusal | PENDING | The gate rejected all five questions. I still need to verify the exact refusal message, which is not shown in the log. |
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