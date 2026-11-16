COURSES = {
 "EE 120": dict(tier=1, scope_term="FA26", flag_not_yet=True,
   tsv=["ee120-fa26-hw-dis.tsv", "ee120-exams-2015-2020.tsv", "ee120-exams-2021-2023.tsv", "ee120-exams-2024-2026.tsv"],
   built_from=["Homework 1 to 10 and discussions 1 to 11 of Fall 2026, which define the current scope", "40 past exams from Spring 2015 to Fall 2026, tagged question by question"],
   notes=["The course writes i for the imaginary unit and uses ω for both continuous and discrete frequency. This repo writes j.",
          "Fall 2026 examines state space (modes, Cayley-Hamilton, internal stability) alongside the usual signals material.",
          "Sampling, the Laplace transform and the z-transform had not appeared in homework by November 2026. Past exams put them in scope, so they are flagged not-yet-assessed and kept.",
          "The course's own conventions: Fourier series coefficients carry the 1/p on the analysis side; transforms are in ω with the 1/(2π) on the inverse; u(0) = 1."]),
}
