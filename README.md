# momentos

Interactive visuals, simulations and small tools for building **intuition** in linear algebra, signals & systems, and circuits, held together by a map of how the ideas connect.

The goal isn't to replace the textbook or problem sets. It's to have a place to *see* the ideas: drag a vector and watch the transformation, sweep a cutoff frequency and watch the Bode plot move, step an RC circuit and watch the capacitor charge. Each tool should leave you thinking "oh, *that's* why."

Most tools here are built with an LLM (Claude) and then checked against course material. See [Accuracy](#accuracy).

---

## Start here: the knowledge map

Open **[`index.html`](index.html)** in a browser. It is the front door of the repo.

- Every **folder** is a circle. A subfolder is a circle inside its parent.
- Every **topic** is a piece of text inside the circle of the folder it lives in. Upright text has a tool behind it. *Italic* text is planned: it is on the map because something else depends on it, and nothing teaches it yet.
- Every **hairline** is a connection, pointing from a foundation to what it makes possible. Each one carries a sentence saying what exactly carries over, which is how you see which maths feeds which EE topic.

Click a topic to see what it builds on, what it leads to, a question to check yourself with, and a link to its tool. Scroll to zoom, drag to pan, press `/` to search, click a folder's name to zoom to it.

The whole map is one file, and its data is the JSON block at the top of `index.html`. **Every time a topic enters the repo, it gets an entry there.** See [Adding a new tool](#adding-a-new-tool).

---

## What's inside

```
momentos/
├── index.html            # the knowledge map (its data is the JSON block at the top)
├── maths/
│   ├── linear-algebra/   # vector products, transformations, eigen-stuff, SVD, least squares
│   └── complex-numbers/  # the complex plane, Euler's formula (taught for now by the signals tool)
├── signals/              # complex exponentials, periodicity, Fourier, sampling, convolution
├── systems/              # LTI systems, impulse/step response, Bode, poles & zeros, z-transform
├── circuits/             # KCL/KVL, dividers, RC/RL/RLC, op-amps, diodes, transistors, filters
├── physics/              # work and energy, fields and forces (planned topics only, so far)
├── unspecified/          # parking lot for tools that don't have a home yet
├── prompts/              # the learning pre-prompt to paste in front of LLM conversations
├── templates/            # the starting point for a new tool (shared look, drag and keyboard handling)
├── scripts/              # check-map.py: does the map still match the repo?
└── CLAUDE.md             # the short rules Claude Code follows in this repo
```

`course-materials/` is a local-only folder for lecture notes and handouts. It's in `.gitignore` and never pushed.

### Topics by course

| Topic | Where it shows up |
|---|---|
| Linear algebra (eigenvalues, SVD, PCA, least squares, change of basis) | EECS 16A, EECS 16B |
| Signals & systems (Fourier, Laplace, z-transform, sampling, filtering) | EE 120 |
| Circuits (KCL/KVL, transient response, op-amps, filters, device models) | EECS 16A, EECS 16B, EE 105 |

---

## Tool index

Add a row every time a tool is added. The map is the picture; this table is the same thing as text.

| Tool | Topics on the map | Format | What should click |
|---|---|---|---|
| [`maths/linear-algebra/vector-products.html`](maths/linear-algebra/vector-products.html) | dot product, cross product, projection | HTML | Both products come out of one right triangle: split **b** into the part along **a** and the part across it. Dot measures the first, cross the second. |
| [`signals/complex-periodicity.html`](signals/complex-periodicity.html) | complex plane, Euler's formula, complex exponential, periodicity | HTML | Multiplying by e^(jΩ) is a turn. A signal repeats when the walk round the circle closes: always in continuous time, in discrete time only if a whole number of steps makes a whole number of turns. |
| [`circuits/kcl-kvl-resistors.html`](circuits/kcl-kvl-resistors.html) | Ohm's law, KCL, KVL, dividers, nodal analysis | HTML | Current in equals current out at every node, and voltage is a height you return to round every loop. Practice problems with hints, plus sliders to explore. |

---

## Learning with an LLM

[`prompts/learning-preprompt.md`](prompts/learning-preprompt.md) is a block of text to paste at the start of a conversation with any LLM. In this repo Claude Code loads it by itself through `CLAUDE.md`.

It does three things.

**1. It makes the LLM find your level before it teaches.** Understanding belongs to a topic, not to a person, so the level is asked per topic:

| Level | You can… |
|---|---|
| L0 unseen | only recognise the name |
| L1 recognise | state the definition with notes open |
| L2 compute | solve the standard problems by procedure |
| L3 picture | explain why, sketch it, predict what a parameter change does |
| L4 use | reach for it on an unfamiliar problem, and know where it breaks |
| L5 teach | derive it from scratch and connect it to other fields |

Most of what this repo is for is the step from L2 to L3: you can compute it, and now you want to see it.

**2. The level picks the way of teaching.**

| Level | Mode | Who leads | What it looks like |
|---|---|---|---|
| L0 to L1 | pedagogy | the LLM | why it matters, a bridge from what you know, one worked example, one for you to finish |
| L2 to L3 | andragogy | shared | start from a real circuit or signal, you try first, hints before answers |
| L4 to L5 | heutagogy | you | you set the question, the LLM probes assumptions and brings counter-examples |

Why the modes change with the level: guidance that helps a beginner gets in the way of someone who already has the procedure. Worked examples are the fastest route in for a novice and a drag on an expert (the "expertise reversal effect", Kalyuga and colleagues). So pedagogy, andragogy (Knowles) and heutagogy (Hase and Kenyon) are not rival philosophies here. They are three settings of one dial, and the dial is how much you already know about this one topic.

**3. It fixes the shape of an explanation:** the essence in a sentence, the picture before the formula, one example with real numbers and units, the limiting cases, the connections, and one question at the end that you have to answer. The closing question is there because recalling an idea does more for memory than rereading it.

Shortcuts you can type once the pre-prompt is in place: `L2 → L3` (skip the level questions), `mode P` / `mode A` / `mode H`, `quiz me`, `tool` (propose a tool for this idea), and `map it` (get the topic's entry and links in the map's JSON format, ready to paste into `index.html`).

---

## Running the tools

| File type | How to open it |
|---|---|
| `.html` | Double-click to open in any browser. No install, no server. |
| `.py` | `python file.py` (needs NumPy and Matplotlib: `pip install numpy matplotlib`) |
| `.ipynb` | Open in Jupyter, VS Code, or upload to Google Colab |
| `.m` | Run in MATLAB, or in GNU Octave for most scripts |
| `.asc` | Open in LTspice, then click **Run** |

Every HTML tool has a `← map` link back to its topic, and a light/dark button (◐).

One thing to know: a file preview inside an editor or the Claude desktop app shows a single file at a time and cannot follow the links between the map and the tools. Open `index.html` in a normal browser for that.

---

## Software worth knowing

**Core**

- **Browser (HTML + JavaScript):** the default for interactive visuals. Nothing to install, and it works on any device.
- **Python** (NumPy, Matplotlib, Jupyter): computation, plots and quick experiments.
- **MATLAB:** the standard tool in many EE courses, and good for signals, control and matrix work. Students often get it free through a campus license. **GNU Octave** is a free alternative that runs most `.m` files.
- **LTspice:** a free SPICE circuit simulator from Analog Devices. Draw a schematic, then run transient, AC (frequency sweep) or DC analyses.

**Worth looking into**

- **[Falstad CircuitJS](https://www.falstad.com/circuit/):** a circuit simulator in the browser that animates current flow. Very good for building intuition fast.
- **[manim](https://www.manim.community/):** the animation library behind 3Blue1Brown's videos. Good for linear algebra animations.
- **Desmos / GeoGebra:** quick sliders-and-graphs sketches before building a full tool.
- **ngspice + PySpice:** open-source SPICE you can script from Python, useful once LTspice feels limiting.

---

## Adding a new tool

1. **Start from confusion.** Pick a concept that doesn't feel intuitive yet: something you can compute but can't picture.
2. **Ask for a visual, not an explanation.** For example:
   > Build a single-file HTML tool that shows how a 2×2 matrix transforms the plane. Let me drag the matrix entries, show the eigenvectors, and highlight when the determinant goes negative.

   In this repo, Claude Code starts from [`templates/tool-template.html`](templates/tool-template.html), which carries the shared look and the drag and keyboard handling.
3. **Check it** against lecture notes or the textbook (see [Accuracy](#accuracy)).
4. **Save it** in the right topic folder, using the naming rules below.
5. **Put it on the map.** In the JSON block at the top of `index.html`, add the topic (or add the file to an existing topic's `tools`) and at least one link:

   ```json
   {
     "id": "rc-step-response",
     "title": "RC step response",
     "folder": "circuits",
     "essence": "A capacitor charges toward the source voltage, covering 63% of what is left every RC seconds.",
     "check": "You double R. What happens to the final voltage, and to how long it takes to get there?",
     "tools": ["circuits/rc-step-response.html"]
   }
   ```
   ```json
   { "from": "kvl", "to": "rc-step-response", "why": "KVL round the loop is what turns into the differential equation." }
   ```

   A topic with no `tools` is allowed: it shows up in italics as planned. Typing `map it` to an LLM that has the pre-prompt gives you these entries ready-made.
6. **Add a row** to the [Tool index](#tool-index).
7. **Run the checker:**

   ```bash
   python3 scripts/check-map.py
   ```

   It fails if a tool file exists that the map doesn't mention, if the map points at a file that isn't there, if a link names a topic that doesn't exist, or if a tool is missing from the tool index.

### Naming

- Use lowercase kebab-case, starting with the concept: `eigenvectors-2x2.html`, `rc-step-response.asc`, `aliasing-demo.py`.
- Give related files the same name with different extensions: `rc-lowpass.asc`, `rc-lowpass.m`, `rc-lowpass.html`.
- Put a single-file tool straight in its topic folder. A tool with several files gets its own subfolder with a short `README.md`.

### File header

Start every tool with a short comment block, so you remember why it exists when you open it a month later:

```html
<!--
  Concept:     Eigenvectors are the directions a matrix only stretches, never rotates
  Course:      EECS 16B
  Play with:   Drag the matrix entries; watch which arrows stay on their own line
  Should click: Why repeated multiplication by A lines up with the dominant eigenvector
  Checked:     Against lecture notes on eigendecomposition
-->
```

Use the same fields as `#` comments in Python, `%` in MATLAB, or a text block on the LTspice schematic.

---

## Accuracy

LLM-generated tools can look convincing and still be subtly wrong: a sign error, a mislabeled axis, an approximation that only holds in a special case. Before trusting a tool:

- Check at least one case against a known result, such as a worked example from lecture, a textbook figure, or a hand calculation.
- Push the extreme values (zero, very large, negative) and confirm the behavior makes physical sense.
- Write down what you checked in the file header's `Checked:` line.

The three tools here were checked against hand calculations, and each header says which cases. That is not the same as checking them against your lecture notes, which is still worth doing the first time you use one.

If something turns out wrong, fix it or delete it. A wrong intuition is worse than none.
