# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none, because the grader can't
> read it.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Week 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

## Chunking Strategy

Chunk size: Variable—one body paragraph per chunk, with the document title added to each chunk.
Overlap: No overlap between body paragraphs. The title repeats in each chunk.

my documents are short posts, paragraph boundaries preserve related sentences, and repeating the title helps identify the subject. The first version I produced is title-only chunks, so I revised it to attach titles to body paragraphs.

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

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

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->
python app.py ask "When can students purchase a parking permit?"
python app.py ask "How long does it take to walk from Fenwick Court to central campus?"
python app.py ask "How many midterm exams are scheduled for PHYS 130 Mechanics?"
python app.py ask "What are Halden Hall's weekday serving hours?"
python app.py ask "What account do students need to access campus Wi-Fi?"

python app.py ask "What is the capital of Mongolia?"
python app.py ask "How do I change the oil in a diesel engine?"
python app.py ask "Who won the 1994 World Cup?"
python app.py ask "What is the recommended dosage of ibuprofen for a headache?"
python app.py ask "How do I write a for loop in Rust?"

python app.py retrieve "When can students purchase a parking permit?"
python app.py retrieve "How long does it take to walk from Fenwick Court to central campus?"
python app.py retrieve "How many midterm exams are scheduled for PHYS 130 Mechanics?"
python app.py retrieve "What are Halden Hall's weekday serving hours?"
python app.py retrieve "What account do students need to access campus Wi-Fi?"

python app.py retrieve "What is the capital of Mongolia?"
python app.py retrieve "How do I change the oil in a diesel engine?"
python app.py retrieve "Who won the 1994 World Cup?"
python app.py retrieve "What is the recommended dosage of ibuprofen for a headache?"
python app.py retrieve "How do I write a for loop in Rust?"

**Question:** "When can students purchase a parking permit?"
**Answer:** Student permits for the west lots go on sale in August (admin_parking_permits.txt).
Sources retrieved: admin_library_holds.txt, admin_parking_permits.txt, advising_registration.txt, study_library_hours.txt, transit_shuttle.txt

**Question:** "How long does it take to walk from Fenwick Court to central campus?"
**Answer:** It takes about 18 minutes on foot to walk from Fenwick Court to central campus.
Source: `transit_walking.txt` (also mentioned in `housing_fenwick_court.txt`).
Sources retrieved: housing_fenwick_court.txt, housing_fenwick_court_noise.txt, transit_shuttle.txt, transit_walking.txt

**Question:** "How many midterm exams are scheduled for PHYS 130 Mechanics?"
**Answer:** There are three midterm exams scheduled for PHYS 130 Mechanics.
Source: `course_phys_130.txt` (and also found in `course_phys_130_exams.txt`).
Sources retrieved: course_phys_130.txt, course_phys_130_exams.txt, course_phys_130_workload.txt

**Question:** "What are Halden Hall's weekday serving hours?"
**Answer:** Halden Hall's weekday hours are 7:30am to 7:00pm (dining_halden_hall.txt).
Sources retrieved: dining_halden_hall.txt, dining_halden_hall_followup.txt, dining_the_atrium.txt

**Question:** "What account do students need to access campus Wi-Fi?"
**Answer:** Students need a student account to access campus Wi-Fi. This comes from `admin_wifi_and_accounts.txt`.
Sources retrieved: admin_wifi_and_accounts.txt, money_jobs.txt, money_textbooks.txt, transit_shuttle.txt
```
```

**My relevance cutoff:**

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

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

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.**

**2.**

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

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
