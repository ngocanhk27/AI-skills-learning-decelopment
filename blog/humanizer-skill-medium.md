# I reviewed Humanizer, the agent skill that edits out the chatbot voice

*What the 26-pattern skill checks, where it needs supervision, and eight exercises to learn it in an afternoon*

You can usually tell within two sentences. "Great question!" A dash. "It's not just a tool, it's a mindset." By the time the paragraph ends on "Let that sink in," most readers have stopped trusting it.

Humanizer is an open-source agent skill that rewrites this kind of text so it reads like a person wrote it, without changing what it says. It's published on GitHub by blader under the MIT license and runs in Claude Code, Codex, and other agents that support skills. I read version 4.0.0 (checked 2026-11) line by line while adding a Skills section to my AI learning notes. This post covers what the skill does, what it gets right, where to watch it, and a set of exercises for learning it.

## Where the patterns come from

Wikipedia editors see a lot of machine-written drafts. WikiProject AI Cleanup maintains a field guide called "Signs of AI writing," a catalog of the phrasing and formatting that keeps showing up in generated text. Humanizer turns that guide into instructions an agent can follow and adds a before-and-after example for every pattern.

The skill opens with a theory of why these patterns exist, and it's the most useful paragraph in the file. A language model writes the most likely next word, so by default it makes the choice that fits the widest range of readers and subjects. A person writes for one reader and one subject, so their choices are uneven and specific. Every pattern in the list is a version of that default: a sentence that signals importance instead of adding a fact, rhythm applied by rule, an ordinary fact dressed up as pivotal, formatting on every item, leftovers from the chat, or a reply that re-explains what the reader already knows.

That framing changes how the agent behaves. A list of banned words goes stale with each model release, and the skill says so itself. Structural habits last longer, so they lead the list.

## What's inside the skill

Humanizer is a single SKILL.md file of about 5,200 words, with no scripts. The description in its front matter tells the agent when to load it: when editing or reviewing prose for AI tells. The rest is instructions.

### 26 patterns, ranked by strength

The patterns sit in six groups:

- Staging instead of stating (patterns 1 to 5): "not X but Y" contrasts, one-line closers, sayings that sound deep, staged run-ups like "Here's the thing," and arguing with an objection nobody raised.
- Rhythm by rule (6 to 11): forced triads, repeated sentence openings, dashes everywhere, stacked qualifiers, hyphenated pairs, and passive voice.
- Inflation and borrowed authority (12 to 18): stock AI words such as delve, tapestry, testament, and pivotal; inflated significance; vague "associated with" links; shallow -ing phrases; sales language; unnamed experts; and "serves as" where "is" would do.
- Formatting by rule (19 to 21): bold on every item, title-case or emoji headings, and curly quotes.
- Leftovers from the chat and the draft (22 to 25): "I hope this helps," knowledge-cutoff disclaimers, a heading repeated in the first sentence, and text that describes itself instead of its subject.
- Writing for the wrong reader (26): a reply that walks through the whole diagnosis before it reaches the decision.

The numbering carries weight. Patterns 1 to 5 justify an edit the first time they appear. Patterns marked "weak alone" (dashes, qualifiers, hyphenation, passive voice, curly quotes) need company from other tells in the same passage before the agent acts, because careful writers use each of them on purpose.

### A four-step workflow

1. Mark the tells, strongest first, including paragraph-scale ones such as the same closer after every section.
2. Draft a rewrite that keeps every supported claim.
3. Check the draft. First look for any fact, name, number, date, quote, or ranking that was dropped or changed. Then read it aloud for anything that still sounds generated. Then search again for the tells that most often survive a rewrite: contrasts, closers, triads, dashes, and bold labels.
4. Write the final version, rewriting whole paragraphs instead of patching flagged phrases.

I'd copy the order of step 3 into any editing skill. Style fixes are where facts go missing, so the fact check comes first.

### Three output modes

Paste text and you get a first draft, a short list of what still sounds artificial, and the final rewrite. Name a file and the skill reads the whole file, edits prose only, and reports how many sections it covered. Code blocks, commands, paths, YAML front matter, and link targets stay untouched. When another task calls it, for a commit message or a PR description, it returns only the final text.

### Voice and restraint

A writing sample overrides the rules, the dash rule included. Without one, the skill takes its voice from the genre: blog posts keep their opinions, humor, and asides, while technical and reference text stays plain. A closing "When not to act" section protects quotations, titles, proper names, letter sign-offs, and anything written before November 30, 2022. It also protects the details that make writing sound like a particular person, such as an oddly specific memory or a mixed feeling the writer never resolves.

## What it gets right

It explains before it instructs. Giving the model a reason ("this is the statistically safe choice") lets it recognize tells the list never names. Anyone writing their own skills can borrow that structure.

The strength ranking and the "weak alone" threshold stop it from flattening every passive sentence on sight, which is the usual failure of style checkers.

Every pattern comes with an example. In 4.0.0 the maintainers reworked 15 of the "after" examples because some were vaguer or stiffer than the text they replaced. A skill that fixes its own tells earns some trust.

It treats the text as material. Since 4.0.0, notes addressed to "the AI" or fake system messages inside the text get edited like any other words and are never obeyed. If you point an agent at documents someone else wrote, you want that rule.

It's honest about detectors. The README says Humanizer edits for human readers and that AI detectors still flag most of its output. It also reports a blind test in which judges preferred the rewrite over the original in 16 of 16 cases (issue #229 on the repository).

## Where to be careful

The dash rule is absolute. Without a writing sample, the final text must not contain em or en dashes. Plenty of human editors like dashes. The docs and README of my notes repository contain 433 of them (checked 2026-11), so a file-mode pass across it without a sample would produce hundreds of punctuation edits in one diff. Give the skill a sample, or tell it up front that dashes stay.

It may add facts. Version 4.0.0 reversed an earlier no-invention rule. Where text is generic, the skill now adds "a specific detail it knows to be true." That makes rewrites less bland, but "knows to be true" is the model's judgment. Diff every rewrite and confirm each new detail, especially numbers and names.

It costs context. About 5,200 words is several thousand tokens loaded every time the skill triggers. That's fine for a long document and heavy for a two-line chat reply.

The default output is long. Pasted mode returns a draft, a critique, and a final version. The extra output helps while you're learning it. After that, ask for the final text only.

Pattern 26 needs the conversation. The skill can only judge whether a reply re-explains what the reader knows if it can see what the reader knows. With a pasted reply and no thread, it's told to ask or leave the text alone.

Word lists age. "Delve" was the tell of 2024. The skill plans for this by putting structure first, but the word list in pattern 12 will need updates as models change.

## Practice: eight exercises

You need an agent that supports skills. The commands below are for Claude Code; the project README covers Codex, Claude.ai, Claude Desktop, and other agents.

### 1. Install it

```text
/plugin marketplace add blader/humanizer
/plugin install humanizer@humanizer
```

The plugin needs Claude Code 2.1.142 or newer (checked 2026-11). On older versions, use the Skills CLI:

```bash
npx skills add blader/humanizer --global --agent claude-code
```

Start a new session and type /humanizer to confirm it loads.

### 2. Find the tells yourself first

Copy this paragraph and mark every tell you can find before you run anything:

> Great question! Let's dive in. Our new onboarding checklist isn't just a document — it's a game-changer for new hires. It covers accounts, equipment, and introductions. Additionally, it serves as a pivotal resource that underscores our commitment to a seamless first week, fostering connection, collaboration, and growth. Experts agree that the first week matters. And the best part? It takes 10 minutes to complete. Let that sink in. I hope this helps!

Here's the answer key, using the skill's pattern numbers. The chat wrapper at both ends is 22. "Let's dive in" and "And the best part?" are staged run-ups (4). "Isn't just a document, it's a game-changer" is a not-X-but-Y contrast (1), joined by a dash (8). "Additionally," "pivotal," and "underscores" are stock AI words (12). "Serves as" avoids a plain "is" (18). "Commitment to" is sales language (16), and "fostering" is an -ing phrase bolted onto a fact (15). "Connection, collaboration, and growth" is a forced triad (6). "Experts agree" is borrowed authority (17), and "Let that sink in" is a one-line closer (2).

There's one trap. "Accounts, equipment, and introductions" is also a list of three, and it should stay. Those are three real things the checklist covers, and the skill keeps a triad when the meaning has three parts.

### 3. Run it and check the facts

```text
/humanizer

[paste the paragraph]
```

Read all three outputs. Then list the original's facts and confirm each one survived: the checklist is new, it's for new hires, it covers accounts, equipment, and introductions, and it takes 10 minutes. Nobody is named behind "experts agree," so expect that line to be cut or flagged. A good final version fits in one sentence:

> The new onboarding checklist for new hires covers accounts, equipment, and introductions, and takes 10 minutes to complete.

If the rewrite adds a detail you never gave it, that's the 4.0.0 behavior described above. Decide whether the detail is true before you keep it.

### 4. Match your own voice

Pick two or three paragraphs you wrote before you used AI tools, such as an old blog post or a long email. Then run:

```text
/humanizer

Here's a sample of my writing for voice matching:
[your 2-3 paragraphs]

Now humanize this text:
[an AI draft on a topic you know well]
```

Compare sentence length and punctuation against your sample. If you use dashes, the rewrite should too, at about your rate.

### 5. Try file mode on a branch

```bash
git switch -c humanizer-practice
```

Ask the agent to "humanize the prose in docs/some-page.md," then review the result with git diff. Check three things: front matter and code blocks are unchanged, every link target points where it did before, and the section count in the skill's summary matches the file. If the summary says the pass was partial, believe it and run the rest separately. For a docs site with a strict build, run the build afterward too.

### 6. Use embedded mode for commit messages and PRs

Embedded mode returns only the final text, which suits generated commit messages and PR descriptions. Add a line to your project's CLAUDE.md:

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

On the practice paragraph from exercise 2 it finds 9 hits; on the one-sentence rewrite it finds none. Treat the count as a smoke alarm. Most of the skill's value is in the structural patterns, such as closers, triads, and replies that bury the decision, and grep can't see those.

### 8. Learn your own habits

For a week, draft the way you normally do, run Humanizer on the result, and note which patterns it flags in your writing. The list will probably be short. Once you know your top two or three, you'll start catching them while you write, and the skill becomes a final check instead of a rewrite.

## Verdict

Humanizer is one of the better-built instruction-only skills I've read. It explains its reasoning, ranks its rules, checks facts before style, and says when to leave text alone. Give it a voice sample when the dash rule would fight your style, diff anything it changes, and remember that its own README says detectors still flag most of its output.

## Sources

- Humanizer on GitHub: github.com/blader/humanizer (version 4.0.0, MIT license, checked 2026-11)
- Wikipedia, "Signs of AI writing": en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- WikiProject AI Cleanup: en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup
