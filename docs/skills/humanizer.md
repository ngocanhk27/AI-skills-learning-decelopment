---
title: "Humanizer skill"
description: Review of the open-source Humanizer skill, which rewrites AI-sounding prose using 26 patterns from Wikipedia's "Signs of AI writing", with eight practice exercises.
status: draft            # planned | draft | stable | needs-update
level: beginner          # beginner | intermediate | advanced
time: 90 min             # rough time to learn and try it
last_reviewed: 2026-11-13  # bump this whenever you re-check the content
tags:
  - skills
  - writing
---

# Humanizer skill

!!! abstract "TL;DR"
    Humanizer is an MIT-licensed [skill](../resources/glossary.md) that rewrites AI-sounding text so it
    reads like a person wrote it, without changing what it says. It checks 26 patterns ranked by
    strength, checks facts before style, and leaves code and front matter alone. Give it a sample of
    your writing (otherwise it strips every dash), diff what it changes, and don't use it to get past
    AI detectors. Reviewed at version 4.0.0 (checked 2026-11).

## Why it matters

You can usually tell within two sentences. "Great question!" A dash. "It's not just a tool, it's a
mindset." By the time a paragraph ends on "Let that sink in," most readers have stopped trusting it.
Agents now write a lot of what we publish (docs, PR descriptions, release notes, posts), so a
repeatable edit pass for this voice pays off quickly.

The patterns come from Wikipedia. WikiProject AI Cleanup maintains a field guide called "Signs of AI
writing," a catalog of the phrasing and formatting that keeps showing up in generated text. Humanizer
turns that guide into instructions an agent can follow and adds a before-and-after example for every
pattern. It runs in Claude Code, Codex, and other agents that support skills.

Reach for it when you're editing prose an agent drafted, or reviewing your own writing for habits
you've picked up from reading model output. Skip it for code comments, data, and short chat replies,
where the context cost outweighs the edit.

## Core concepts

### Why AI text sounds the way it does

The skill opens with a theory, and it's the most useful paragraph in the file. A language model writes
the most likely next word, so by default it makes the choice that fits the widest range of readers and
subjects. A person writes for one reader and one subject, so their choices are uneven and specific.
Every pattern in the list is a version of that default: a sentence that signals importance instead of
adding a fact, rhythm applied by rule, an ordinary fact dressed up as pivotal, formatting on every
item, leftovers from the chat, or a reply that re-explains what the reader already knows.

A list of banned words goes stale with each model release, and the skill says so itself. Structural
habits last longer, so they lead the list.

### Anatomy

Humanizer is a single `SKILL.md` of about 5,200 words, with no scripts or reference files. The
`description` in its front matter tells the agent when to load it: when editing or reviewing prose for
AI tells. Everything else is instructions, which makes it a good example of an instruction-only skill.

### 26 patterns in six groups

| Group | Patterns | Examples |
| --- | --- | --- |
| Staging instead of stating | 1 to 5 | "not X but Y" contrasts, one-line closers, sayings that sound deep, "Here's the thing," arguing with an objection nobody raised |
| Rhythm by rule | 6 to 11 | forced triads, repeated sentence openings, dashes everywhere, stacked qualifiers, hyphenated pairs, passive voice |
| Inflation and borrowed authority | 12 to 18 | delve, tapestry, testament, pivotal; inflated significance; vague "associated with"; shallow -ing phrases; sales language; unnamed experts; "serves as" for "is" |
| Formatting by rule | 19 to 21 | bold on every item, title-case or emoji headings, curly quotes |
| Leftovers from the chat and the draft | 22 to 25 | "I hope this helps," knowledge-cutoff disclaimers, a heading repeated in the first sentence, text that describes itself |
| Writing for the wrong reader | 26 | a reply that walks through the whole diagnosis before it reaches the decision |

The numbering carries weight. Patterns 1 to 5 justify an edit the first time they appear. Patterns
marked *weak alone* (dashes, qualifiers, hyphenation, passive voice, curly quotes) need company from
other tells in the same passage before the agent acts, because careful writers use each of them on
purpose.

### The four-step workflow

1. Mark the tells, strongest first, including paragraph-scale ones such as the same closer after every
   section.
2. Draft a rewrite that keeps every supported claim.
3. Check the draft. First look for any fact, name, number, date, quote, or ranking that was dropped or
   changed. Then read it aloud for anything that still sounds generated. Then search again for the
   tells that most often survive a rewrite: contrasts, closers, triads, dashes, and bold labels.
4. Write the final version, rewriting whole paragraphs instead of patching flagged phrases.

The order of step 3 is worth copying into any editing skill. Style fixes are where facts go missing, so
the fact check comes first.

### Output modes

| Mode | Triggered by | Returns |
| --- | --- | --- |
| Pasted text (default) | `/humanizer` plus pasted text | A first draft, a short list of what still sounds artificial, and the final rewrite |
| File | Naming a file path | Edits the prose in place and reports how many sections it covered. Code blocks, commands, paths, YAML front matter, and link targets stay untouched |
| Embedded | Another task calling it (commit message, PR description) | The final text only |

### Voice and restraint

A writing sample overrides the rules, the dash rule included. Without one, the skill takes its voice
from the genre: blog posts keep their opinions, humor, and asides, while technical and reference text
stays plain. A closing "When not to act" section protects quotations, titles, proper names, letter
sign-offs, and anything written before November 30, 2022. It also protects the details that make
writing sound like a particular person, such as an oddly specific memory or a mixed feeling the writer
never resolves.

### Review: what it gets right

- It explains before it instructs. Giving the model a reason ("this is the statistically safe choice")
  lets it recognize tells the list never names. Anyone writing their own skills can borrow that
  structure.
- The strength ranking and the *weak alone* threshold stop it from flattening every passive sentence on
  sight, which is the usual failure of style checkers.
- Every pattern comes with an example. In 4.0.0 the maintainers reworked 15 of the "after" examples
  because some were vaguer or stiffer than the text they replaced.
- It treats the text as material. Since 4.0.0, notes addressed to "the AI" or fake system messages
  inside the text get edited like any other words and are never obeyed, a useful guard against
  [prompt injection](../resources/glossary.md) when you point it at documents someone else wrote.
- It's honest about detectors. The README says Humanizer edits for human readers and that AI detectors
  still flag most of its output. It also reports a blind test in which judges preferred the rewrite
  over the original in 16 of 16 cases (issue #229 on the repository).

## Hands-on

Eight exercises, roughly in order of difficulty. You need an agent that supports skills; the commands
are for Claude Code, and the project README covers Codex, Claude.ai, Claude Desktop, and other agents.

### 1. Install it

```text
/plugin marketplace add blader/humanizer
/plugin install humanizer@humanizer
```

The plugin needs Claude Code 2.1.142 or newer (checked 2026-11). On older versions, use the Skills CLI:

```bash
npx skills add blader/humanizer --global --agent claude-code
```

Start a new session and type `/humanizer` to confirm it loads.

### 2. Find the tells yourself first

Copy this paragraph and mark every tell you can find before you run anything:

> Great question! Let's dive in. Our new onboarding checklist isn't just a document — it's a
> game-changer for new hires. It covers accounts, equipment, and introductions. Additionally, it serves
> as a pivotal resource that underscores our commitment to a seamless first week, fostering connection,
> collaboration, and growth. Experts agree that the first week matters. And the best part? It takes 10
> minutes to complete. Let that sink in. I hope this helps!

??? success "Answer key (open after you've tried)"
    ==Great question!==<sup>22</sup> ==Let's dive in.==<sup>4</sup> Our new onboarding checklist
    ==isn't just a document — it's a game-changer==<sup>1, 8</sup> for new hires. It covers accounts,
    equipment, and introductions. ==Additionally,==<sup>12</sup> it ==serves as==<sup>18</sup> a
    ==pivotal==<sup>12</sup> resource that ==underscores==<sup>12</sup> our
    ==commitment to==<sup>16</sup> a seamless first week, ==fostering==<sup>15</sup>
    ==connection, collaboration, and growth==<sup>6</sup>. ==Experts agree==<sup>17</sup> that the
    first week matters. ==And the best part?==<sup>4</sup> It takes 10 minutes to complete.
    ==Let that sink in.==<sup>2</sup> ==I hope this helps!==<sup>22</sup>

    - 22: chat wrapper at both ends
    - 4: staged run-ups ("Let's dive in", "And the best part?")
    - 1 and 8: a not-X-but-Y contrast joined by a dash
    - 12: stock AI words ("Additionally", "pivotal", "underscores")
    - 18: "serves as" where "is" would do
    - 16: sales language ("commitment to")
    - 15: an -ing phrase bolted onto a fact ("fostering")
    - 6: a forced triad ("connection, collaboration, and growth")
    - 17: borrowed authority ("Experts agree")
    - 2: a one-line closer ("Let that sink in")

    The trap: "accounts, equipment, and introductions" is also a list of three, and it should stay.
    Those are three real things the checklist covers, and the skill keeps a triad when the meaning has
    three parts.

### 3. Run it and check the facts

```text
/humanizer

[paste the paragraph]
```

Read all three outputs. Then list the original's facts and confirm each one survived: the checklist is
new, it's for new hires, it covers accounts, equipment, and introductions, and it takes 10 minutes.
Nobody is named behind "experts agree," so expect that line to be cut or flagged. A good final version
fits in one sentence:

> The new onboarding checklist for new hires covers accounts, equipment, and introductions, and takes
> 10 minutes to complete.

If the rewrite adds a detail you never gave it, that's the 4.0.0 behavior described under
[Pitfalls](#pitfalls-gotchas). Decide whether the detail is true before you keep it.

### 4. Match your own voice

Pick two or three paragraphs you wrote before you used AI tools, such as an old blog post or a long
email. Then run:

```text
/humanizer

Here's a sample of my writing for voice matching:
[your 2-3 paragraphs]

Now humanize this text:
[an AI draft on a topic you know well]
```

Compare sentence length and punctuation against your sample. If you use dashes, the rewrite should too,
at about your rate.

### 5. Try file mode on a branch

```bash
git switch -c humanizer-practice
```

Ask the agent to "humanize the prose in docs/some-page.md," then review the result with `git diff`.
Check three things: front matter and code blocks are unchanged, every link target points where it did
before, and the section count in the skill's summary matches the file. If the summary says the pass was
partial, believe it and run the rest separately. In this hub, finish with `make build`; the strict build
catches any link the edit broke.

### 6. Use embedded mode for commit messages and PRs

Embedded mode returns only the final text, which suits generated commit messages and PR descriptions.
Add a line to your project's `CLAUDE.md`:

```markdown
- Run the humanizer skill on PR descriptions and release notes before posting them.
```

After a week, compare those descriptions with the ones from the week before.

### 7. Count tells before and after

A grep can't judge structure, but it gives you a number to track across drafts:

```bash
tells() {
  grep -oiE "—|–|isn't just|not just|let's dive|here's the thing|let that sink in|great question|i hope this helps|delve|pivotal|testament|underscore|tapestry|showcas|serves as|boasts|nestled|vibrant" "$1" |
    tr '[:upper:]' '[:lower:]' | sort | uniq -c | sort -rn
}
tells draft.md
```

Expected result: 9 hits on the practice paragraph from exercise 2, none on the one-sentence rewrite
(checked 2026-11). Treat the count as a smoke alarm. Most of the skill's value is in the structural
patterns, such as closers, triads, and replies that bury the decision, and grep can't see those.

### 8. Learn your own habits

For a week, draft the way you normally do, run Humanizer on the result, and note which patterns it
flags in your writing. The list will probably be short. Once you know your top two or three, you'll
start catching them while you write, and the skill becomes a final check instead of a rewrite.

## Practical applications

| Use case | How to apply it | Notes |
| --- | --- | --- |
| Blog posts and announcements | Pasted mode with a voice sample | Keeps opinions and asides; check any detail it adds |
| Docs pages in this hub | File mode on a branch, then `make build` | Say up front that dashes stay, or supply a sample |
| PR descriptions and commit messages | Embedded mode via a `CLAUDE.md` rule | Returns final text only, so no extra output to trim |
| Replies in a review thread | Pasted mode with the thread included | Pattern 26 needs the conversation to judge what the reader knows |
| Training your own eye | Exercise 2, then exercise 8 | Find the tells before the agent does |

## Pitfalls & gotchas

- **The dash rule is absolute.** Without a writing sample, the final text must not contain em or en
  dashes. This hub's docs and README contain 433 of them (checked 2026-11), so a file-mode pass across
  it without a sample would produce hundreds of punctuation edits in one diff. Give the skill a sample,
  or tell it up front that dashes stay.
- **It may add facts.** Version 4.0.0 reversed an earlier no-invention rule. Where text is generic, the
  skill now adds "a specific detail it knows to be true." That's the model's judgment, so diff every
  rewrite and confirm each new detail, especially numbers and names.
- **It costs context.** About 5,200 words is several thousand [tokens](../resources/glossary.md)
  loaded every time the skill triggers. Fine for a long document, heavy for a two-line reply.
- **The default output is long.** Pasted mode returns a draft, a critique, and a final version. That
  helps while you're learning; after that, ask for the final text only.
- **Pattern 26 needs the conversation.** Without the thread, the skill can't know what the reader
  already knows, and it's told to ask or leave the text alone.
- **Word lists age.** "Delve" was the tell of 2024. Structure leads the list for this reason, but the
  word list in pattern 12 will need updates as models change.
- **It isn't a detector bypass.** Its own README says detectors still flag most of its output.

## Checklist

- [ ] I can explain why AI text drifts toward the "default choice" in one paragraph
- [ ] I found at least 8 of the 10 tell types in the practice paragraph before opening the answer key
- [ ] I ran the skill and confirmed every fact in the original survived the rewrite
- [ ] I ran it with a voice sample and compared punctuation against my own writing
- [ ] I ran file mode on a branch and reviewed the diff and the strict build
- [ ] I know my own top two or three patterns

## Resources

- Official source: [blader/humanizer on GitHub](https://github.com/blader/humanizer) (version 4.0.0,
  MIT license, checked 2026-11)
- Pattern source: [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- Maintainers of that guide: [WikiProject AI Cleanup](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup)

## Changelog

| Date | Change |
| --- | --- |
| 2026-11-13 | Created: review of version 4.0.0 and eight practice exercises |
