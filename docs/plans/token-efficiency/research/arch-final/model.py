"""Token model for the merged skill set: the open proposal plus grafts.

Sections of current SKILL.md files are measured with the len/4 ruler of
scripts/token-budget.py. New text is drafted here and measured the same way.
No rewritten file exists, so every body number is a projection.
"""
import re, io, contextlib, json
from pathlib import Path

HERE = Path(__file__).parent
R = Path('/Users/happy/code/toby/skills')
tok = lambda s: round(len(s) / 4)

# Reuse the open proposal's measured model, silently.
src = (HERE.parent / 'arch-open' / 'model.py').read_text()
ns = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src, 'model.py', 'exec'), ns)
S = dict(ns['S']); sections = ns['sections']; subsec = ns['subsec']; rest = ns['rest']; total = ns['total']

def sec(skill, name): return sections(skill)[name]

# ---------- drafted text ----------
NEW = {}
NEW['build_methods'] = """## Method skills
Open each file below by path, at the step named. Each is the SKILL.md of a sibling folder in the skills folder that holds this skill.
- Before the design pass, open `toby-swd-strategy`, unless the surrounding code already settles the structure.
- When the design adds or changes a signature, open `toby-swd-interfaces`.
- When the design adds a module, moves code, or gives a module a new job, open `toby-swd-modules`.
- When a criterion has a failure case, a retry, a timeout, or validation, open `toby-swd-errors`.
- When a criterion states a time or memory budget, or the design adds a cache, a batch, or a queue for speed, open `toby-optimize`.
- Before the first edit of a behavior change, open `toby-swd-testing`.
- When module structure or a public API changes, open `toby-swd-docs`.
- Before any command beyond safe inspection, open `toby-swd-environment`.
- Before the handoff, open `toby-swd-clarity` when the diff adds a public name or an interface comment.
"""
NEW['proof_pointer'] = "Prove each criterion with the two-run form in `toby-swd-testing`, section Prove a change.\n"
NEW['optimize_entry'] = """# Toby Optimize

Make working code faster or lighter, and keep only the changes a measurement supports.

## Steps
1. Record a baseline with one named command, and quote its output.
2. Look for a better algorithm, a missing index, or a cache before code-level tuning.
3. Change one thing, then run the same command again.
4. Revert a change with no measured effect unless it also made the code simpler.
5. When the path has a stated budget, measure its worst case under load.

## Report
Give the baseline, the result, the command, and what stays unmeasured, such as production load.
"""
NEW['explain_chain'] = """For a question about this code, open the method file that answers it by path. Open `toby-swd-modules` for placement, `toby-swd-strategy/references/design-note.md` for a design choice, `toby-swd-errors` for an error path, and `toby-optimize` for a cache or a speed-up.
"""
NEW['refactor_scope'] = """## Pick the scope
Pick one scope from the request, say it in one line, and open only the files it lists.
- Names, comments, or docstrings only: open `toby-swd-clarity`.
- A local cleanup inside changed code: open `references/cleanup.md` and `references/smells.md`.
- A split, merge, move, or extraction across files: open `toby-swd-strategy`, then `toby-swd-modules`. Open `toby-swd-interfaces` when a signature changes, and `toby-swd-docs` when module structure changes.
- An error check for a condition that cannot occur: open `toby-swd-errors`.
Behavior drift rules below apply to every scope.
"""
NEW['second_approach'] = "Sketch a second approach, and make it the strongest option a competent engineer would pick.\n"

# ---------- bodies ----------
M = {}
# toby-build: open proposal's body, minus the two-run proof bullet (moved to testing),
# with the method table redrawn for errors and optimize.
proof = subsec('toby-feature-dev', 'Prove the slice before starting the next',
               '- A criterion counts as met', '- A green type-check')
M['build'] = S['build/SKILL.md'] - tok(ns['NEW']['build_methods']) + tok(NEW['build_methods']) - tok(proof) + tok(NEW['proof_pointer'])
M['build/strategic.md'] = S['build/references/strategic.md']

# toby-bug-fix: the drafted body from the decision proposal, minus step 4,
# because toby-explain answers a why question with no fix asked for.
bf = (HERE.parent / 'ad-bugfix-draft.md').read_text()
step4 = bf[bf.find('4. **Stop when'):bf.find('5. **Choose')]
M['bug-fix'] = tok(bf) - tok(step4)

# toby-optimize: the performance half of toby-swd-complexity plus the entry steps.
cx_red = sec('toby-swd-complexity', 'Red flags')
perf_flags = '\n'.join(l for l in cx_red.splitlines() if re.search(r'optimi|[Pp]erformance|cache|baseline', l))
err_flags = '\n'.join(l for l in cx_red.splitlines() if l.startswith('- ') and l not in perf_flags)
bw = sec('toby-swd-complexity', 'Brownfield Work')
refs = sec('toby-swd-complexity', 'References')
M['optimize'] = (tok(NEW['optimize_entry']) + tok(sec('toby-swd-complexity', 'Performance design'))
                 + tok(sec('toby-swd-complexity', 'Proportionality')) + tok(perf_flags)
                 + round(tok(bw) / 2) + round(tok(refs) / 2))
# toby-swd-errors: intro, error design, error red flags, half of brownfield and references.
M['errors'] = (tok(sec('toby-swd-complexity', '[intro]')) + tok(sec('toby-swd-complexity', 'Error design'))
               + tok('## Red flags\n\nBefore finishing, check the change against every red flag below and fix anything that applies.\n') + tok(err_flags)
               + round(tok(bw) / 2) + round(tok(refs) / 2))

# Method skills keep their own Brownfield Work sections, so the shared rule leaves build and refactor.
shared_bw = tok(ns['NEW']['brownfield_shared'])
M['refactor'] = S['refactor/SKILL.md'] - tok(ns['NEW']['refactor_scope']) + tok(NEW['refactor_scope']) - shared_bw
M['build'] -= 0  # the open model never added the shared rule to build
M['refactor/cleanup.md'] = S['refactor/references/cleanup.md']
M['strategy'] = S['strategy/SKILL.md'] + tok(sec('toby-swd-strategy', 'Brownfield Work')) + tok(NEW['second_approach'])
M['strategy/design-note.md'] = S['strategy/references/design-note.md']
M['modules'] = S['modules/SKILL.md'] + tok(sec('toby-swd-modules', 'Brownfield Work'))
M['interfaces'] = S['interfaces/SKILL.md'] + tok(sec('toby-swd-interfaces', 'Brownfield Work')) - 20
M['interfaces/design-it-twice.md'] = S['interfaces/references/design-it-twice.md']
M['clarity'] = S['clarity/SKILL.md'] + tok(sec('toby-swd-clarity', 'Brownfield Work')) - 70
M['clarity/comments.md'] = S['clarity/references/comments.md']
M['docs'] = rest('toby-swd-docs', [])
exp_loops = subsec('toby-swd-testing', 'Test-first, with judgment', '### Experiment loops')
M['testing'] = rest('toby-swd-testing', []) - tok(exp_loops) + tok(proof) + tok('## Prove a change\n')
M['experiment'] = S['experiment/SKILL.md'] + tok(exp_loops) - tok(sec('toby-swd-experiment', 'Testing Boundary')) + 40
M['environment'] = S['environment/SKILL.md']
M['explain'] = S['explain/SKILL.md'] - tok(ns['NEW']['explain_chain']) + tok(NEW['explain_chain'])
M['review'] = S['review/SKILL.md']
M['voice'] = S['voice/SKILL.md']
M['artifact'] = S['artifact/SKILL.md']
M['learning'] = S['learning/SKILL.md']

for k, v in M.items(): print(f"{v:6d}  {k}")

SCEN = {
    "a question, answered": ['explain'],
    "a rename": ['refactor', 'clarity'],
    "a command or migration": ['environment'],
    "review my changes": ['review'],
    "a throwaway spike": ['experiment'],
    "one method on a repository": ['build', 'interfaces', 'errors', 'testing'],
    "split a module": ['refactor', 'strategy', 'modules', 'docs'],
    "a feature, tactical": ['build', 'strategy', 'testing'],
    "a feature, strategic": ['build', 'build/strategic.md', 'strategy', 'modules', 'interfaces', 'errors', 'testing', 'docs'],
    "learning, invoked": ['learning'],
    "a visual artifact": ['artifact'],
}
EXTRA = {
    "a bug fix": ['bug-fix', 'testing'],
    "a bug fix in an error path": ['bug-fix', 'testing', 'errors'],
    "make it faster": ['optimize', 'environment'],
    "a feature, strategic, with a time budget": SCEN["a feature, strategic"] + ['optimize'],
    "a feature, strategic, new public API": SCEN["a feature, strategic"] + ['interfaces/design-it-twice.md'],
}
CUR = ns['CUR']
OPEN = {"a question, answered":1516,"a rename":2635,"a command or migration":1637,"review my changes":3138,"a throwaway spike":1199,"one method on a repository":11279,"split a module":8166,"a feature, tactical":7353,"a feature, strategic":20176,"learning, invoked":3083,"a visual artifact":5452}
print()
tc = to = tm = 0
for n, files in SCEN.items():
    v = sum(M[f] for f in files); tc += CUR[n]; to += OPEN[n]; tm += v
    print(f"{n:42s} today {CUR[n]:6d}  open {OPEN[n]:6d}  merged {v:6d}  {v-CUR[n]:+6d}")
print(f"{'sum of 11':42s} today {tc:6d}  open {to:6d}  merged {tm:6d}  {tm-tc:+6d}")
for n, files in EXTRA.items():
    print(f"{n:42s} merged {sum(M[f] for f in files):6d}")
group = ['strategy','modules','interfaces','errors','optimize','clarity','testing','docs']
print('method co-load group', sum(M[g] for g in group))
json.dump(M, open(HERE / 'bodies.json', 'w'), indent=1)
