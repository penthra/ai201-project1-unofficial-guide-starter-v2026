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

======================================================================
Chunk 1  |  source: admin_add_drop_deadline.txt#0  |  produced by: chunker.py::split_documents
======================================================================
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.

======================================================================
Chunk 2  |  source: course_cs_340_exams.txt#1  |  produced by: chunker.py::split_documents
======================================================================
CS 340 Databases — assessment

Start the term project in week three, not week eight; everyone learns this the hard way.

======================================================================
Chunk 3  |  source: course_phys_130_workload.txt#0  |  produced by: chunker.py::split_documents
======================================================================
Workload for PHYS 130 Mechanics

People keep asking so: 7 hours a week, plus 3 on lab weeks. That's real time, not optimistic time.

======================================================================
Chunk 4  |  source: dining_verrill_street_grill_followup.txt#1  |  produced by: chunker.py::split_documents
======================================================================
Re: Verrill Street Grill

Also worth saying: one register, so the queue is a single line no matter how busy. Nobody tells you this at orientation.

======================================================================
Chunk 5  |  source: housing_morrow_house.txt#1  |  produced by: chunker.py::split_documents
======================================================================
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

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

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
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

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
