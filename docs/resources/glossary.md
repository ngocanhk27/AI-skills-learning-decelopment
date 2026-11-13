---
title: Glossary
description: Short definitions of terms used across the hub.
icon: material/book-alphabet
---

# Glossary

Keep entries to one or two sentences and link to the topic that explains them in depth.
Alphabetical order, please.

Agent
:   A model running in a loop that can decide on and take actions (call tools, read files, run
    commands) toward a goal, observing the result of each step.

Connector
:   A ready-made integration that gives an AI application access to an external service such as a
    document store, code host or calendar.

Context window
:   The maximum amount of text (measured in tokens) a model can consider at once, including both
    the input and its own output.

Embedding
:   A list of numbers representing the meaning of a piece of text (or image), so that similar
    meanings sit close together. The basis of semantic search and RAG.

Eval
:   A repeatable test that measures how well a model, prompt, skill or agent performs on a defined
    set of cases, using code, human or model-based grading.

Fine-tuning
:   Further training a model on your own examples to change its behaviour or style.

Harness
:   The software that wraps a model and turns it into a usable agent — managing the conversation,
    tools, permissions, memory and execution environment.

LLM-as-judge
:   Using a language model to grade another model's output against a rubric.

MCP (Model Context Protocol)
:   An open protocol that standardises how AI applications connect to external tools, data sources
    and prompts through *servers*.

Prompt injection
:   An attack where instructions hidden in content the model reads (a web page, file or email)
    try to override what the user or developer asked for.

RAG (Retrieval-augmented generation)
:   Retrieving relevant documents at question time and adding them to the model's context so its
    answer is grounded in that information.

Skill
:   A packaged set of instructions, and optionally scripts and resources, that an agent can load on
    demand to perform a specific kind of task well.

Token
:   The unit of text a model reads and writes; roughly a short word or part of a word.

Tool use
:   A model's ability to request that the application run a defined function (search, calculate,
    call an API) and use the result. Also called *function calling*.
