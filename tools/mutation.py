"""Mutationstest: break the code on purpose and see whether the tests notice.

Every test suite is written against the criteria of whoever wrote it. A
passing suite therefore says "this code satisfies my expectations", which
is a weaker statement than it looks. Mutation testing asks a question
that does not depend on the author at all:

    If the code were wrong, would the tests fail?

It answers by deliberately introducing small defects -- one at a time --
and running the suite against each. A defect the suite does not notice is
a **surviving mutant**, and it marks a gap in the *tests*, not in the
code. The score is the fraction of introduced defects that were caught.

WHERE THIS SITS AMONG THE OTHER CRITERIA
----------------------------------------

Roughly in order of how little they depend on the author's judgement:

1. Example tests -- "works for the inputs I chose". The author's
   criteria, start to finish.
2. Property tests -- holds over inputs the author did not choose
   individually, only the space they came from.
3. Metamorphic tests -- relations that must hold between outputs without
   knowing the right answer, e.g. f(2x) == 4*f(x).
4. Differential tests -- two independent routes to the same quantity must
   agree; the disagreement is the signal and belongs to nobody.
5. **Mutation testing -- this file.** Tests the tests.
6. Machine-checked proof. No human judgement at all.

This package has a lot of 1 and 2, and a deliberate amount of 4 (4/3 from
cube counts against 4/3 from the sphere-to-cylinder ratio; Euler's 2 out
of three separate modules; the step eccentricity against
`spirale.eccentricity_squared`). It has none of 6 yet.

A LESSON FROM BUILDING THIS, WORTH NOT REPEATING
------------------------------------------------

The first version of this tool ran only the *matching* test file per
mutant -- `test_spirale.py` for a mutation in `spirale.py` -- because it
is roughly thirty times faster. It reported a score of 81.8% with 35
survivors.

Re-checking eight of those survivors against the **full** suite killed
**eight of eight**. The per-file score was an artefact of the
measurement, not a property of the tests: the cross-module checks are
what catch those mutations, and restricting the run to one file switches
them off. `--scope file` is kept for a fast signal while iterating, but
any score worth quoting comes from `--scope all`.

The tool also crashed, at first, when a survivor's line number exceeded
the length of the *re-printed* source -- `ast.unparse` normalises
docstrings and shifts every line. That took five modules' results with
it and reported them as "0 mutants". Survivor lines are now read from the
original source, where the numbers mean something.

WHAT A SURVIVING MUTANT IS AND IS NOT
-------------------------------------

Some survivors are *equivalent mutants*: the change produces a program
that behaves identically, so no test can catch it and none should try.
Shifting a guard from `<= 0` to `< 0` when the zero case is unreachable
is the common case here. Those are not defects and chasing them produces
tests that assert nothing.

The score is therefore a floor on test strength, not a target to
maximise. 100% is not the goal; knowing *which* survivors are real is.

USAGE
-----

    python tools/mutation.py --module spirale --sample 20
    python tools/mutation.py --all --sample 60 --scope all
    python tools/mutation.py --module waage --scope file

The source file is restored in a `finally` block, so an interrupted run
leaves the tree clean. Verify with `git status` if a run is killed
mid-flight.
"""

from __future__ import annotations

import argparse
import ast
import copy
import os
import random
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKAGE = os.path.join(REPO, "raum27")
PYTHON = sys.executable

COMPARISON_SWAP = {
    ast.Lt: ast.LtE, ast.LtE: ast.Lt,
    ast.Gt: ast.GtE, ast.GtE: ast.Gt,
    ast.Eq: ast.NotEq, ast.NotEq: ast.Eq,
}
ARITHMETIC_SWAP = {
    ast.Add: ast.Sub, ast.Sub: ast.Add,
    ast.Mult: ast.Div, ast.Div: ast.Mult,
}


class SiteCollector(ast.NodeVisitor):
    """Every place a small defect can be introduced, as (kind, line, col, index)."""

    def __init__(self) -> None:
        self.sites: list[tuple[str, int, int, int]] = []

    def visit_Compare(self, node: ast.Compare) -> None:
        for index, op in enumerate(node.ops):
            if type(op) in COMPARISON_SWAP:
                self.sites.append(("cmp", node.lineno, node.col_offset, index))
        self.generic_visit(node)

    def visit_BinOp(self, node: ast.BinOp) -> None:
        if type(node.op) in ARITHMETIC_SWAP:
            self.sites.append(("bin", node.lineno, node.col_offset, 0))
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        self.sites.append(("boolop", node.lineno, node.col_offset, 0))
        self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant) -> None:
        if isinstance(node.value, bool):
            self.sites.append(("bool", node.lineno, node.col_offset, 0))
        elif isinstance(node.value, int):
            self.sites.append(("const", node.lineno, node.col_offset, 0))
        self.generic_visit(node)


class MutationApplier(ast.NodeTransformer):
    """Apply exactly one mutation, at the given site."""

    def __init__(self, site: tuple[str, int, int, int]) -> None:
        self.site = site
        self.applied = False

    def _matches(self, node: ast.AST, kind: str, index: int = 0) -> bool:
        want_kind, line, col, want_index = self.site
        return (
            not self.applied
            and kind == want_kind
            and getattr(node, "lineno", None) == line
            and getattr(node, "col_offset", None) == col
            and index == want_index
        )

    def visit_Compare(self, node: ast.Compare) -> ast.AST:
        self.generic_visit(node)
        for index, op in enumerate(node.ops):
            if self._matches(node, "cmp", index) and type(op) in COMPARISON_SWAP:
                node.ops[index] = COMPARISON_SWAP[type(op)]()
                self.applied = True
        return node

    def visit_BinOp(self, node: ast.BinOp) -> ast.AST:
        self.generic_visit(node)
        if self._matches(node, "bin") and type(node.op) in ARITHMETIC_SWAP:
            node.op = ARITHMETIC_SWAP[type(node.op)]()
            self.applied = True
        return node

    def visit_BoolOp(self, node: ast.BoolOp) -> ast.AST:
        self.generic_visit(node)
        if self._matches(node, "boolop"):
            node.op = ast.Or() if isinstance(node.op, ast.And) else ast.And()
            self.applied = True
        return node

    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        if self._matches(node, "bool") and isinstance(node.value, bool):
            self.applied = True
            return ast.copy_location(ast.Constant(value=not node.value), node)
        if (
            self._matches(node, "const")
            and isinstance(node.value, int)
            and not isinstance(node.value, bool)
        ):
            self.applied = True
            return ast.copy_location(ast.Constant(value=node.value + 1), node)
        return node


def collect_sites(module: str) -> list[tuple[str, int, int, int]]:
    source = open(os.path.join(PACKAGE, module + ".py")).read()
    collector = SiteCollector()
    collector.visit(ast.parse(source))
    return sorted(set(collector.sites))


def all_modules() -> list[str]:
    return [
        name[:-3]
        for name in sorted(os.listdir(PACKAGE))
        if name.endswith(".py") and name != "__init__.py"
    ]


def run_suite(scope: str, module: str) -> bool:
    """True if the suite failed, i.e. the mutant was caught."""
    target = ["-x", "-q"]
    if scope == "file":
        test_file = os.path.join(REPO, "tests", f"test_{module}.py")
        if not os.path.exists(test_file):
            return False
        target.append(f"tests/test_{module}.py")
    environment = dict(os.environ)
    environment.pop("PYTHONPATH", None)
    result = subprocess.run(
        [PYTHON, "-m", "pytest", *target],
        cwd=REPO,
        capture_output=True,
        env=environment,
        timeout=1800,
    )
    return result.returncode != 0


def mutate_and_test(module: str, site, scope: str) -> tuple[str, str]:
    """Returns (outcome, original source line). Restores the file always."""
    path = os.path.join(PACKAGE, module + ".py")
    source = open(path).read()
    lines = source.split("\n")
    index = site[1] - 1
    original_line = lines[index].strip() if 0 <= index < len(lines) else "<unknown>"

    tree = MutationApplier(site).visit(copy.deepcopy(ast.parse(source)))
    ast.fix_missing_locations(tree)
    try:
        mutated = ast.unparse(tree)
    except Exception:
        return "invalid", original_line
    if mutated == ast.unparse(ast.parse(source)):
        return "invalid", original_line

    try:
        open(path, "w").write(mutated)
        caught = run_suite(scope, module)
    finally:
        open(path, "w").write(source)
    return ("killed" if caught else "survived"), original_line


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--module", help="a single module in raum27/")
    group.add_argument("--all", action="store_true", help="sample across the package")
    parser.add_argument("--sample", type=int, default=20, help="how many mutants")
    parser.add_argument(
        "--scope",
        choices=("all", "file"),
        default="all",
        help="'all' runs the whole suite per mutant and is the only score worth "
             "quoting; 'file' runs one test file and is ~30x faster but reported "
             "8 false survivors out of 8 when it was checked",
    )
    parser.add_argument("--seed", type=int, default=11)
    arguments = parser.parse_args()

    pool: list[tuple[str, tuple]] = []
    for module in all_modules() if arguments.all else [arguments.module]:
        pool.extend((module, site) for site in collect_sites(module))

    random.Random(arguments.seed).shuffle(pool)
    sample = pool[: arguments.sample]
    print(
        f"{len(pool)} mutation sites; testing {len(sample)} "
        f"with scope={arguments.scope}\n"
    )

    killed = survived = invalid = 0
    survivors: list[tuple[str, tuple, str]] = []
    for position, (module, site) in enumerate(sample, 1):
        outcome, line = mutate_and_test(module, site, arguments.scope)
        if outcome == "killed":
            killed += 1
        elif outcome == "survived":
            survived += 1
            survivors.append((module, site, line))
        else:
            invalid += 1
        print(f"  [{position}/{len(sample)}] {module:<26} {outcome}")

    total = killed + survived
    print(f"\nkilled {killed}, survived {survived}, invalid {invalid}")
    if total:
        print(f"mutation score: {killed / total * 100:.1f}%  (n={total})")
    if survivors:
        print("\nsurvivors -- gaps in the TESTS, to be triaged for equivalence:")
        for module, site, line in survivors:
            print(f"  {module}: {site[0]}@line {site[1]} | {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
