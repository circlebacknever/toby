import re, json, sys
from pathlib import Path
HERE = Path(__file__).parent
R = Path('/Users/happy/code/toby')
tok = lambda s: round(len(s) / 4)
ENTRY = {
"toby-build": "Changes what code does in the smallest step that leaves the design at least as good as before. It proves each change with one check run before the edit and again after it. Use it when the user asks to add, build, implement, wire up, or finish a behavior. The behavior can be a feature, a ticket, an endpoint, a method, a screen, a job, or a flag. Skip it for wrong output, which toby-bug-fix covers, and for slow code, which toby-optimize covers. Skip it when behavior stays the same, which toby-refactor covers, and for a throwaway, which toby-swd-experiment covers. Skip it for a one-file edit that copies a pattern already in that file.",
"toby-bug-fix": "Fixes behavior that is wrong today. It reproduces the failure, finds the cause at a file and line, fixes that cause, and proves the fix with a run before and after. Use it when the user reports a bug, a crash, an error message, a regression, or wrong output and wants it fixed. Use it when the user pastes a stack trace, or says a build or a test started failing. Skip it for a question about why something fails with no fix asked for, which toby-explain covers. Skip it for a flaky test, which toby-swd-testing covers, and for slow code, which toby-optimize covers.",
"toby-optimize": "Makes working code faster or lighter from a measured baseline, with one change per measurement. It covers whether a cache, a batch, a queue, or parallel work is worth what it adds. Use it when the user says code is slow, or asks to speed it up or to cut latency, memory, or query count. Use it when the user asks to add a cache to code that already works. Skip it for new behavior that includes a cache, which toby-build covers, and for wrong output, which toby-bug-fix covers. Skip it for a speed question with no change asked for, which toby-explain covers, and for a throwaway sweep, which toby-swd-experiment covers.",
"toby-refactor": "Changes how code is arranged or reads and keeps its behavior and tests the same. Use it when the user asks to simplify, tidy, refactor, de-duplicate, extract, split, merge, move, or rename code. Use it to add, fix, or delete comments and docstrings. Skip it when behavior should change, which toby-build, toby-bug-fix, or toby-optimize covers. Skip it when the user wants findings with no edit, which toby-code-review covers.",
"toby-swd-testing": "Keeps tests an executable specification of behavior, and classifies a failing test before anyone edits it. Use it when the user asks to write, rewrite, delete, or weaken a test, raise coverage, update snapshots, or fix a flaky test. Skip it when production code changes too, which toby-build or toby-bug-fix covers. Skip it for a throwaway spike, which toby-swd-experiment covers, and for a run of the suite alone, which toby-swd-environment covers.",
"toby-code-review": "Reports the proven risks in a change and edits nothing. Use it when the user asks to review, check, or audit a diff, a PR, a commit, a branch, or the working tree. Use it when the user asks what is wrong with a change. Skip it when the user wants the code changed, which toby-refactor or toby-bug-fix covers. Skip it for a question about how code works, which toby-explain covers.",
"toby-explain": "Answers a question in plain words, then stops, and edits no files. Use it when the user asks why, how, what the difference is, which option fits, or where code should go, on any subject. Use it for \"walk me through\", \"help me understand\", and any request for a clear, short, or simple explanation. Skip it when the user asks for a diagram, a chart, or a deck, which toby-artifact-style covers. Skip it when the user wants a fix, which toby-bug-fix covers.",
"toby-swd-experiment": "Runs a short, reversible discovery loop while the behavior is still undecided. Use it when the user says spike, prototype, proof of concept, throwaway, try a few values, compare options, tweak settings, or let me test. The word throwaway decides the route even when the request also names retries, timeouts, or tests. Skip it for work the user intends to keep, which toby-build covers. Skip it for starting or stopping a server alone, which toby-swd-environment covers.",
"toby-swd-environment": "Classifies each command before it runs and asks before any command that changes the user's machine. Use it when the user asks to run a migration or a seed script, or to install a dependency. Use it to start or stop a server, free a port, clear a cache, or run the full test suite. Skip it for a code edit with nothing to run, and for a snapshot update, which toby-swd-testing covers.",
"toby-voice": "Applies Toby's writing rules to prose and runs the voice checker on it. Use it for a commit message, a PR description, a README, an AGENTS.md, a doc, a plan, or a rewrite of any text. Use it when the user says voice, toby voice, check the voice, voice pass, or voice standards, or asks for wording or tone help. Skip it as the first skill for names and comments inside code, which toby-refactor covers.",
"toby-artifact-style": "Applies Toby's visual design system to a visual and to the copy inside it. The visual can be a diagram, chart, dashboard, slide deck, HTML or React page, SVG, mockup, or reference card. Use it when the user asks to draw, show, chart, diagram, or build a visual, including a visual that explains something. Skip it for a text answer in chat, which toby-explain covers, and for a game, which only /toby-game starts.",
}
TAIL = " Entry skills open this file by path. Do not load it from a user request alone."
METHOD = {
"toby-swd-strategy": "Contains Toby's design pass, run before a change." + TAIL,
"toby-swd-modules": "Contains Toby's checks for where code goes and when to split or merge modules." + TAIL,
"toby-swd-interfaces": "Contains Toby's procedure for designing a callable surface before its body." + TAIL,
"toby-swd-errors": "Contains Toby's error ladder for deciding how code handles a failure." + TAIL,
"toby-swd-clarity": "Contains Toby's rules for names, comments, and docstrings inside code." + TAIL,
"toby-swd-docs": "Contains Toby's rules for a module's README.md and AGENTS.md." + TAIL,
}
def cur_desc(name):
    t = (R / 'skills' / name / 'SKILL.md').read_text()
    end = t.find('\n---', 4) + 4; fm = t[:end]
    m = re.search(r'description:\s*(>-\n(?:  .*\n?)+|".*"|.*)', fm)
    return ' '.join(l.strip() for l in m.group(1).replace('>-', '').splitlines()).strip().strip('"')
INVOKE = {n: cur_desc(n) for n in ['toby-learning', 'toby-squall', 'toby-game']}
def fm(name, desc, extra=''):
    return f"---\nname: {name}\ndescription: >-\n  {desc}\n{extra}---\n"
def listing(d): return sum(len(n) + len(v) + 5 for n, v in d.items())
if __name__ == '__main__':
    for n, d in {**ENTRY, **METHOD}.items():
        words = [len(s.split()) for s in re.split(r'(?<=[.])\s+', d)]
        print(f"  {n:22s} {len(d):4d} chars, longest sentence {max(words)} words")
    hide = 'disable-model-invocation: true\n'
    e = sum(tok(fm(n, d)) for n, d in ENTRY.items())
    m = sum(tok(fm(n, d, hide)) for n, d in METHOD.items())
    i = sum(tok(fm(n, d, hide)) for n, d in INVOKE.items())
    print('frontmatter ruler, 20 skills:', e + m + i, '| entry', e, 'method', m, 'invoke-only', i)
    le, lm, li = listing(ENTRY), listing(METHOD), listing(INVOKE)
    cur = {p.name: cur_desc(p.name) for p in sorted((R / 'skills').iterdir()) if p.is_dir()}
    print(f'listing chars: hidden hosts {le} (~{round(le/4)} tok), Kiro {le+lm+li} (~{round((le+lm+li)/4)} tok), today {listing(cur)}')
    print(f'listing with old claude.ai copies beside it: {le + listing(cur)}')
    guide = (R / 'base' / 'toby.md').read_text()
    old_r = guide[guide.find('## Skill Routing'):guide.find('## Environment Safety')]
    old_w = guide[guide.find('## Work Modes'):guide.find('## Skill Routing')]
    new_r = (HERE / 'routing.md').read_text()
    new_w = (HERE.parent / 'arch-open' / 'workmodes.md').read_text()
    g = tok(guide) - tok(old_r) - tok(old_w) + tok(new_r) + tok(new_w)
    print('guide', tok(guide), '->', g, '| routing', tok(old_r), '->', tok(new_r), '| work modes', tok(old_w), '->', tok(new_w))
    print('resident', tok(guide) + 2649, '->', g + e + m + i)
    json.dump({'ENTRY': ENTRY, 'METHOD': METHOD}, open(HERE / 'descs.json', 'w'), indent=1)
