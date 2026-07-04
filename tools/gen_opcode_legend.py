#!/usr/bin/env python3
"""Generate OPCODES.md, a descriptive legend of every step op-code emitted.

The scratchpad vocabulary belongs to the model: generators may introduce new
op-codes freely, and this legend is *descriptive*, not prescriptive. It is
produced by scanning the generator source (every step flows through
helpers.step(), so an AST scan sees the full vocabulary) and sampling each
generator for an example step.

Usage:
    python tools/gen_opcode_legend.py            # rewrite OPCODES.md
    python tools/gen_opcode_legend.py --check    # exit 1 if OPCODES.md is stale
"""
import argparse
import ast
import os
import random
import re
import sys

# Op-codes are ALL-CAPS tokens (letters, digits, underscores).
OPCODE_RE = re.compile(r"[A-Z][A-Z0-9_]*\Z")

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

GENERATORS_DIR = os.path.join(REPO_ROOT, "generators")
DEFAULT_OUTPUT = os.path.join(REPO_ROOT, "OPCODES.md")

# Fixed seed so repeated runs produce identical examples (enables --check).
EXAMPLE_SEED = 0
SAMPLES_PER_GENERATOR = 300


class OpInfo:
    """Aggregated facts about one op-code across all generator source files."""

    def __init__(self):
        self.arities = set()   # payload field counts observed at call sites
        self.files = set()     # generator file basenames using the code


def _opcodes_from_first_arg(node):
    """Resolve the op-code literal(s) from the first argument of a step() call.

    Returns a list of string codes, or None if the argument cannot be
    resolved statically (reported as a dynamic site).
    """
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return [node.value]
    if isinstance(node, ast.IfExp):
        body = _opcodes_from_first_arg(node.body)
        orelse = _opcodes_from_first_arg(node.orelse)
        if body is not None and orelse is not None:
            return body + orelse
    return None


def _harvest_catalog_codes(tree):
    """Op-codes declared in a module's data catalog (data-driven step
    paths), for modules that emit codes dynamically from a table.

    Returns {code: set(arities)}. A catalog entry is a tuple/list
    literal whose first element is an op-code token; the arity counts
    the payload elements that survive the usual ``step(code, f1[, f2])``
    emit, where empty-string fields are omitted.
    """
    found = {}
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Tuple, ast.List)) or not node.elts:
            continue
        head = node.elts[0]
        if not (isinstance(head, ast.Constant)
                and isinstance(head.value, str)
                and OPCODE_RE.match(head.value)):
            continue
        arity = 0
        for elt in node.elts[1:]:
            if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                if elt.value != "":
                    arity += 1  # empty payload string is omitted at emit
            else:
                arity += 1
        found.setdefault(head.value, set()).add(arity)
    return found


def scan_opcodes(generators_dir=GENERATORS_DIR):
    """AST-scan generator modules for step(...) calls.

    Returns (opcodes, dynamic_sites) where opcodes maps code -> OpInfo and
    dynamic_sites lists "file:line" locations whose op-code could not be
    resolved statically.
    """
    opcodes = {}
    dynamic_sites = []
    for fname in sorted(os.listdir(generators_dir)):
        if not fname.endswith(".py") or fname == "__init__.py":
            continue
        path = os.path.join(generators_dir, fname)
        with open(path, encoding="utf-8") as fp:
            tree = ast.parse(fp.read(), filename=path)
        catalog_site = False
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            is_step = (isinstance(func, ast.Name) and func.id == "step") or (
                isinstance(func, ast.Attribute) and func.attr == "step"
            )
            if not is_step or not node.args:
                continue
            codes = _opcodes_from_first_arg(node.args[0])
            if codes is None:
                # A bare Name means the code is pulled from a data
                # catalog (e.g. `for code, ... in path:`); resolve it
                # by harvesting the module's catalog rather than warning.
                if isinstance(node.args[0], ast.Name):
                    catalog_site = True
                else:
                    dynamic_sites.append(f"{fname}:{node.lineno}")
                continue
            arity = len(node.args) - 1
            for code in codes:
                info = opcodes.setdefault(code, OpInfo())
                info.arities.add(arity)
                info.files.add(fname)
        if catalog_site:
            for code, arities in _harvest_catalog_codes(tree).items():
                info = opcodes.setdefault(code, OpInfo())
                info.arities |= arities
                info.files.add(fname)
    return opcodes, dynamic_sites


def collect_examples(seed=EXAMPLE_SEED, samples_per_gen=SAMPLES_PER_GENERATOR):
    """Sample every registered generator and record one example step per code."""
    from dolphin_math_datagen import ALL_GENERATORS

    random.seed(seed)
    examples = {}
    for gen in ALL_GENERATORS:
        for _ in range(samples_per_gen):
            try:
                result = gen.generate()
            except Exception:
                continue
            for s in result.get("steps", []):
                code = s.split("|", 1)[0]
                examples.setdefault(code, s)
    return examples


def render_markdown(opcodes, examples, dynamic_sites):
    """Render the legend as markdown."""
    lines = [
        "# Op-Code Legend",
        "",
        "**Generated file — do not hand-edit.** Regenerate with "
        "`python tools/gen_opcode_legend.py` (verify freshness with `--check`).",
        "",
        "The scratchpad vocabulary belongs to the model and evolves organically: "
        "generators may introduce new op-codes freely, and this legend is "
        "*descriptive*, not prescriptive. Steps are pipe-delimited strings "
        "(`CODE|field|field|...`, at most 4 payload fields) built with "
        "`helpers.step()`; the final step of every problem is `Z|<final_answer>`.",
        "",
        f"{len(opcodes)} distinct op-codes observed.",
        "",
        "| Code | Payload fields | Example | Used by |",
        "|---|---|---|---|",
    ]
    for code in sorted(opcodes):
        info = opcodes[code]
        arities = ", ".join(str(a) for a in sorted(info.arities))
        example = examples.get(code, "*(not observed in sampling)*")
        if not example.startswith("*"):
            example = "`" + example.replace("|", "\\|") + "`"
        files = ", ".join(sorted(info.files))
        lines.append(f"| `{code}` | {arities} | {example} | {files} |")
    if dynamic_sites:
        lines += [
            "",
            "## Warnings: unresolved dynamic op-codes",
            "",
            "These step() call sites pass a non-literal op-code that the scanner "
            "could not resolve; their codes may be missing from the table above:",
            "",
        ]
        lines += [f"- {site}" for site in dynamic_sites]
    lines.append("")
    return "\n".join(lines)


def build_legend():
    opcodes, dynamic_sites = scan_opcodes()
    examples = collect_examples()
    return render_markdown(opcodes, examples, dynamic_sites)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT,
                        help="Output path (default: OPCODES.md at repo root).")
    parser.add_argument("--check", action="store_true",
                        help="Exit 1 if the output file is missing or stale.")
    args = parser.parse_args()

    content = build_legend()
    if args.check:
        if not os.path.exists(args.output):
            print(f"STALE: {args.output} does not exist.")
            return 1
        with open(args.output, encoding="utf-8") as fp:
            on_disk = fp.read()
        if on_disk != content:
            print(f"STALE: {args.output} is out of date. "
                  f"Regenerate with: python tools/gen_opcode_legend.py")
            return 1
        print(f"OK: {args.output} is up to date.")
        return 0

    with open(args.output, "w", encoding="utf-8") as fp:
        fp.write(content)
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
