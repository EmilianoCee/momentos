# The quiz protocol

How a session quizzes a learner, grades each answer, and writes the evidence back. It is written so that two
different models, following it, ask comparable questions and give the same answer the same grade. The levels and
what they need are in [levels.md](levels.md). The record's format is in [learner-record.md](learner-record.md).

## Entry points

| The learner says | Get the questions with |
|---|---|
| `quiz me EE 120` (a course) | `python3 scripts/learner.py next --course "EE 120"` |
| `quiz me convolution` (a topic) | `python3 scripts/learner.py next --topic convolution` |
| `review` | `python3 scripts/learner.py next --due` |
| `exam prep EE 105 FINAL` | `python3 scripts/learner.py next --exam "EE 105 FINAL"` |
| `where am I` | `python3 scripts/learner.py report` (no questions: print the report) |
| `onboard me` | the `onboard` skill |

`next` prints a list of questions to ask, in order. Each item names the topic, its `essence` and `check`, the
`kind` of question and the level it is pitched at (`aim`), `why` that question moves the topic on, any
`open_misstep`, and the topic's `rubric` when one exists. The script has already chosen the topics, mixed them,
and set the level. Do not reorder, skip or re-pitch them.

## The loop, one question at a time

1. Write the question (rules below). Ask it alone, with nothing after it.
2. Ask for a confidence first: "How sure are you, from 0 to 100?" The learner may give it in the same message as
   the answer. If they give none, record `null`.
3. Wait. Give no hint before an answer. If the learner asks for one, give the smallest hint that helps and record
   `help` as `hint`. If you end up showing the method, record `worked`.
4. Grade the answer against the anchors below, and the topic's rubric if it has one. Decide `shows`.
5. Tell the learner, in this order: the level the answer showed and the one reason why; the first step where the
   reasoning went wrong, if it did; the picture that makes the right answer obvious. Keep it short. This is a quiz,
   not a lecture.
6. Record it straight away, before the next question:
   `python3 scripts/learner.py add --topic T --kind K --aim N --shows N --confidence N --asked "..." --note "..."`,
   with `--misstep "..."` when the reasoning went wrong and `--help-given hint` when a hint came first.
   `asked` is the question in one line. `note` is the learner's reasoning in one line, not "correct" or "wrong".
7. After the last question, print what the script reported for each topic, and the next review dates.

If the learner wants to stop, stop. What is recorded so far stands.

## Writing a question

- **Fresh every time.** New numbers, a new arrangement, new wording. Never a question from course materials, and
  never the topic's `check` question word for word (the learner has seen it on the map).
- **One question.** No parts (a), (b), (c), except in a `transfer` problem, which is one problem with several steps.
- **Real values with units**, in the ranges the course uses. `j` for the imaginary unit.
- **Pitched at `aim`.** Do not make it easier because the learner seems tired, or harder because they are doing well.
- **An open misstep comes first.** If the item has `open_misstep`, write the question so that the same wrong step
  would give a wrong answer.
- **Use the rubric's seeds as starting points, not as scripts.** Change the numbers and the set-up.
- **Do not reveal the kind of answer wanted** ("explain using the pole-zero picture" gives the picture away).

## The kinds of question

| Kind | Pitched at | What it asks | Form |
|---|---|---|---|
| `recall` | L1 | the definition or formula, each symbol and its unit | "State ... and say what each symbol is." |
| `compute` | L2 | a standard problem, done by the standard procedure | numbers in, a number with units out |
| `predict` | L3 | what changes if one thing changes, on a set-up not seen before | "X is doubled. What happens to Y, and why?" The learner commits before any feedback. |
| `explain` | L3 | why it works, in the learner's own words | "Explain to someone who has not seen it why ..." |
| `sketch` | L3 | the graph or the figure, described in words | "Describe the sketch: the axes, the shape, the points that matter, and what moves when ... changes." |
| `limit` | L3 or L4 | L3: both limiting cases and why each makes sense. L4: where the model stops being true. | "Push ... to zero and to infinity." or "How far can ... go before this stops being right? What fails first?" |
| `connect` | L3 or L5 | L3: a link on the map, turned into a question. L5: a connection to another field. | "Why does X lead to Y? What exactly carries over?" |
| `transfer` | L4 | an unfamiliar, exam-style problem that needs this idea, without saying so | several steps, real values, no method named |
| `derive` | L5 | the result from first principles | "Starting from ..., derive ..." |

A `transfer` problem is unfamiliar when the learner has to decide what to use. A standard problem with different
numbers is `compute`, not `transfer`.

## Grading: what `shows` means

`shows` is the level the answer demonstrated, from 0 to 5. It can be lower or higher than `aim`.

| `shows` | The answer |
|---|---|
| 0 | has nothing usable: wrong, with no relevant idea in it, or "I do not know" |
| 1 | recognises the idea: names the right concept or formula, but cannot use it |
| 2 | is right by procedure: the formula is applied correctly, with no mechanism, or with a wrong one |
| 3 | is right and gives the mechanism in terms of the picture, with the direction and the rough size right |
| 4 | does that on a problem it had to work out how to approach, and names the assumption the answer rests on and what happens when it fails |
| 5 | derives the result from first principles, or connects it soundly to another field |

### Anchors by kind

| Kind | An L2 answer | An L3 answer | An L4 answer |
|---|---|---|---|
| `compute` | the right number and unit by the standard procedure | also says what the number means, or checks it against a limit, unasked | (compute cannot show more than L3) |
| `predict` | the right direction, justified only by quoting the formula ("τ = RC, so it doubles") | the right direction and rough size, with the cause ("twice the resistance lets charge through half as fast; where it ends up does not involve R") | also says, unasked, when the prediction would fail ("as long as nothing loads the output") |
| `explain` | the formula or definition restated in words | a causal story with no step missing, tied to a picture, that a first-year could follow | also says what the story leaves out, or why the nearest wrong explanation is wrong |
| `sketch` | the general shape, with axes or key values missing or wrong | axes named with units, the shape right, the points that matter placed (intercepts, asymptotes, time constant, corner), and what moves with the parameter | also what the sketch does outside the model's range |
| `limit` | the limits found by substituting into the formula | both limits, each with the physical reason it makes sense | names the assumption that fails first, roughly where, and what replaces the model there |
| `connect` | both ideas stated correctly, but not what carries over | exactly what carries from the first to the second, used once on an example | also where the connection stops holding |
| `transfer` | only the parts that match a template | the right approach and structure, with one conceptual gap, or only after being told which idea applies | a complete, correct solution with no help: the method chosen, the units right, the answer checked for sense |

`recall` shows 1 when the definition is right and every symbol and unit is named, and 0 otherwise. `derive` shows
5 for a complete derivation with each step justified and the assumptions named, and 4 when one step is asserted
without justification.

### Rules that settle the hard cases

- **Between two levels, record the lower.**
- **A right answer for a wrong reason shows the level of the reason.** The right number with the wrong mechanism
  is L2.
- **An arithmetic slip with the right set-up, units and structure keeps the level.** Say so, and note the slip.
- **A right answer after a hint is graded as usual and recorded with `help` set to `hint`.** The script does not
  count it toward a level.
- **Grade what was said, not what the learner probably meant.** If a step is missing, ask "why?" once before
  grading. That is not a hint.
- **A problem that used several topics gets one event per topic,** at most three, each graded on its own part.
- **Never record an answer the learner did not give in this session,** and never record a level they report from
  elsewhere as anything but `kind: self`.

## The topic's rubric

`rubrics/<folder>.json` may hold, for a topic, what L1 to L4 look like on that topic, its known missteps, and
seeds for questions. When it exists, it refines the anchors above for that topic. When it does not, the anchors
above and the topic's `essence` are enough.

## Without the repo

A chat that cannot run commands follows [`prompts/quiz-in-chat.md`](../prompts/quiz-in-chat.md). The learner
pastes the output of `python3 scripts/learner.py export`, and the chat ends by printing an evidence block for the
learner to paste back.
