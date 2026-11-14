# momentos

Interactive visuals, simulations and small tools for building **intuition** in linear algebra, signals & systems, and circuits.

The goal isn't to replace the textbook or problem sets. It's to have a place to *see* the ideas: drag a vector and watch the transformation, sweep a cutoff frequency and watch the Bode plot move, step an RC circuit and watch the capacitor charge. Each tool should leave you thinking "oh, *that's* why."

Most tools here are built with an LLM (Claude) and then checked against course material. See [Accuracy](#accuracy).

---

## What's inside

```
momentos/
├── maths/
│   └── linear-algebra/   # transformations, eigen-stuff, SVD, projections, least squares
├── signals/              # Fourier series/transforms, sampling, aliasing, convolution
├── systems/              # LTI systems, impulse/step response, Bode, poles & zeros, z-transform
├── circuits/             # RC/RL/RLC, op-amps, diodes, transistors, filters
└── unspecified/          # parking lot for tools that don't have a home yet
```

`course-materials/` is a local-only folder for lecture notes and handouts. It's in `.gitignore` and never pushed.

### Topics by course

| Topic | Where it shows up |
|---|---|
| Linear algebra (eigenvalues, SVD, PCA, least squares, change of basis) | EECS 16B |
| Signals & systems (Fourier, Laplace, z-transform, sampling, filtering) | EE 120 |
| Circuits (transient response, op-amps, filters, device models) | EECS 16B, EE 105 |

---

## Tool index

Add a row every time a tool is added, so this table stays the map of the repo.

| Tool | Topic | Format | What should click |
|---|---|---|---|
| _Nothing yet._ | | | |

---

## Running the tools

| File type | How to open it |
|---|---|
| `.html` | Double-click to open in any browser. No install, no server. |
| `.py` | `python file.py` (needs NumPy and Matplotlib: `pip install numpy matplotlib`) |
| `.ipynb` | Open in Jupyter, VS Code, or upload to Google Colab |
| `.m` | Run in MATLAB, or in GNU Octave for most scripts |
| `.asc` | Open in LTspice, then click **Run** |

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
3. **Check it** against lecture notes or the textbook (see [Accuracy](#accuracy)).
4. **Save it** in the right topic folder, using the naming rules below.
5. **Add a row** to the [Tool index](#tool-index).

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

If something turns out wrong, fix it or delete it. A wrong intuition is worse than none.
