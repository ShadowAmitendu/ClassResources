# Contributing to Class Resources

Thank you for your interest in improving Class Resources! Your contributions help thousands of BCA students access reliable lecture notes, assignments, and exam archives.

---

## Ways to Contribute

1. **Submit New Course Materials:** Notes, lab exercises, assignment solutions, or previous year question papers.
2. **Report Typos or Missing Topics:** Open an issue if a PDF has missing pages or outdated syllabus references.
3. **Enhance the Platform:** Suggest UI improvements, accessibility enhancements, or documentation fixes.

---

## Contribution Workflow

### 1. Working on the `submissions` Branch
All student resource submissions must target the dedicated [`submissions`](https://github.com/ShadowAmitendu/ClassResources/tree/submissions) branch:

```bash
# Clone the repository
git clone https://github.com/ShadowAmitendu/ClassResources.git
cd ClassResources

# Check out the submissions branch
git checkout submissions

# Create your feature/topic branch
git checkout -b add-7th-sem-notes
```

### 2. Directory Hierarchy
Place all uploaded documents into their designated directory structure:

```text
bca/semesters/<semester>/<category>/<subject>/<filename>
```

- `<semester>`: `1st`, `2nd`, `3rd`, `4th`, `5th`, `6th`, `7th`, or `8th`
- `<category>`: `syllabus`, `notes`, `assignments`, or `question-papers`
- `<filename>`: Descriptive and sanitized (e.g. `ML_Module_1_Notes.pdf`, `WebTech_Lab_Assignment_3.pdf`)

### 3. Rebuilding the Resource Index
Whenever you add or move files, run the automated generator script to refresh the JSON metadata index:

```bash
python generate.py
```

Verify that the corresponding file in `bca/data/<semester>.json` has been updated cleanly.

### 4. Submitting a Pull Request
- Commit your changes with a clear summary: `git commit -m "feat(notes): add Module 3 notes for Machine Learning"`
- Push to your fork or branch and open a Pull Request against the `submissions` branch.
- Include a brief description of what materials were added and the source subject.

---

## Attribution Policy
By contributing to Class Resources, you agree that your materials will be shared under our [Open Academic License](LICENSE) and [Terms of Use](terms.html). All public distributions must preserve credit to the project and original authors.
