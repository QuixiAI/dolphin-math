"""Generate PROBLEM_TYPES.md — a user-facing catalog of every problem
type the dataset can produce.

For each registered generator class it emits: a human title, the
class docstring's lead description, the grade band and difficulty, the
list of internal `operation` variants (sampled), and one real worked
example (problem, scratchpad steps, answer). Like OPCODES.md this file
is generated, not hand-edited.

Usage:
    uv run python tools/gen_problem_types.py            # write the file
    uv run python tools/gen_problem_types.py --check    # verify fresh
"""
import argparse
import inspect
import os
import random
import re
import sys

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

BANDS = [
    ("elementary", "Elementary (grades 3–5)"),
    ("middle", "Middle School (grades 6–8)"),
    ("high", "High School"),
    ("college", "College"),
    ("graduate", "Graduate"),
]

STOP_HEADINGS = ("Variants:", "Variant ", "Op-codes", "Op codes",
                 "Op-code")


def title_for(class_name):
    """MultiDigitAdditionGenerator -> 'Multi Digit Addition'."""
    name = class_name[:-len("Generator")] if \
        class_name.endswith("Generator") else class_name
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", name)


def description_for(cls):
    """Lead paragraph of the docstring, stopping before Variants/Op-codes."""
    doc = inspect.getdoc(cls) or ""
    lines = []
    for line in doc.splitlines():
        if line.strip().startswith(STOP_HEADINGS):
            break
        if not line.strip() and lines:
            break
        lines.append(line.strip())
    text = " ".join(x for x in lines if x)
    return re.sub(r"\s+", " ", text).strip() or "(no description)"


def render_example(example):
    out = [f"Problem: {example['problem']}", "Steps:"]
    for s in example["steps"]:
        out.append(f"  {s}")
    out.append(f"Answer: {example['final_answer']}")
    return "\n".join(out)


def collect(seed=0):
    """Group registered instances by class, preserving registration order."""
    from dolphin_math_datagen import ALL_GENERATORS
    from curriculum import CURRICULUM

    order = []
    by_class = {}
    for gen in ALL_GENERATORS:
        name = type(gen).__name__
        if name not in by_class:
            by_class[name] = []
            order.append(name)
        by_class[name].append(gen)

    entries = []
    for name in order:
        instances = by_class[name]
        cls = type(instances[0])
        meta = CURRICULUM.get(name, {})
        # Sample variant operation strings across all instances.
        variants = set()
        example = None
        random.seed(seed)
        for gen in instances:
            for _ in range(80 // len(instances) + 1):
                ex = gen.generate()
                variants.add(ex["operation"])
                if example is None:
                    example = ex
        entries.append({
            "class": name,
            "title": title_for(name),
            "description": description_for(cls),
            "grade": meta.get("grade_level", "?"),
            "difficulty": meta.get("difficulty", "?"),
            "variants": sorted(variants),
            "example": example,
            "n_instances": len(instances),
        })
    return entries


def render(entries):
    total = len(entries)
    lines = [
        "# Problem Types",
        "",
        "Every problem type this dataset can generate. For each type: a "
        "one-line description, the grade band and coarse difficulty "
        "(1–5, read relative to the band), the internal operation "
        "variants, and one real worked example (the pipe-delimited "
        "`steps` are the model's scratchpad).",
        "",
        f"**{total} problem types.** This file is generated — do not "
        "hand-edit. Regenerate with "
        "`uv run python tools/gen_problem_types.py`.",
        "",
    ]
    by_band = {b: [] for b, _ in BANDS}
    other = []
    for e in entries:
        (by_band.get(e["grade"], other)).append(e)

    for band, heading in BANDS:
        group = by_band[band]
        if not group:
            continue
        lines.append(f"## {heading}")
        lines.append("")
        for e in group:
            lines.extend(_render_entry(e))
    if other:
        lines.append("## Other")
        lines.append("")
        for e in other:
            lines.extend(_render_entry(e))
    return "\n".join(lines).rstrip() + "\n"


def _render_entry(e):
    diff = e["difficulty"]
    head = (f"### {e['title']} — `{e['class']}`  ·  {e['grade']} · "
            f"difficulty {diff}")
    variants = ", ".join(f"`{v}`" for v in e["variants"])
    block = [
        head,
        "",
        e["description"],
        "",
        f"**Variants:** {variants}",
        "",
        "```",
        render_example(e["example"]),
        "```",
        "",
    ]
    return block


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output",
                    default=os.path.join(repo_root, "PROBLEM_TYPES.md"))
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if the file on disk is stale")
    args = ap.parse_args()

    content = render(collect())
    if args.check:
        try:
            with open(args.output, encoding="utf-8") as fh:
                current = fh.read()
        except FileNotFoundError:
            current = None
        if current != content:
            print(f"STALE: {args.output} is out of date. Regenerate "
                  f"with: uv run python tools/gen_problem_types.py")
            return 1
        print(f"OK: {args.output} is up to date.")
        return 0
    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
