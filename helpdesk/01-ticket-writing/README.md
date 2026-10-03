# Lab 01 — Writing useful tickets

**English** · [Français](README.fr.md) · [Deutsch](README.de.md)

**English** · [Deutsch](README.de.md)

**Status:** Done — rewrites, priority exercise, escalation and closure notes written in [`my-rewrites.md`](my-rewrites.md), including tickets built from my own Linux lab evidence; done in Markdown, not yet in an ITSM tool such as GLPI.

## Goal

Practise writing tickets that another technician can pick up without asking
questions: clear summary, impact, reproduction steps, what was tried, and a
next action. Good tickets reduce resolution time and are also evidence during
audits and incident reviews (Security+ D4 — incident/change documentation).

## Setup

- Any ITSM tool or plain Markdown. Planned tool: the free self-hosted
  [GLPI](https://glpi-project.org/) (widely used in France); the templates in
  this folder are plain Markdown.
- Fictional organisation: *Exemple SARL*, 40 users, Windows 11 laptops,
  Microsoft 365, one Linux file server.

## Steps

1. Read the template in [`template.md`](template.md).
2. Compare the bad and good examples in [`examples.md`](examples.md) and note
   what makes each "good" ticket actionable.
3. Rewrite each "bad" ticket yourself before reading the improved version.
4. Write an escalation note (L1 → L2) and a closure note for one ticket.
5. Classify each ticket by **impact** and **urgency** to derive a priority
   using the matrix below.

| Impact \ Urgency | High | Medium | Low |
|------------------|------|--------|-----|
| **High** (many users / business stopped) | P1 | P2 | P3 |
| **Medium** (team or VIP degraded) | P2 | P3 | P4 |
| **Low** (single user, workaround exists) | P3 | P4 | P4 |

## Evidence

- [`my-rewrites.md`](my-rewrites.md): my rewrites of the three bad tickets
  (compared with the reference versions), the priority table, three
  tickets written from real troubleshooting output of
  [lab 03](../03-linux-troubleshooting/), an L1 → L2 escalation and a closure note.
- Not done: screenshot of a ticket in GLPI — the template works in any tool,
  but I have not installed GLPI yet.

## What I learned

- A ticket that only records the action ("reset done") is useless later; a
  useful one records the evidence and the root cause, so the next person does not start over.
- "What changed?" (new dock, recent config change) is the question that most
  often leads to the cause.
- Writing tickets from my own lab output was much easier than inventing them:
  exact commands and error messages make the ticket actionable.
- The priority matrix gives a default; security impact can justify raising
  it, and the reason belongs in the ticket.
- An escalation note should say what I did, what I think, and what I need —
  not just "doesn't work, please check".
