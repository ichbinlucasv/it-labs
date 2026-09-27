# Lab 01 — Writing useful tickets

**Status:** Planned — the template and fictional good/bad ticket examples are written; the exercises have not been practised in an ITSM tool (e.g. GLPI) yet.

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

- Screenshot of a ticket created in GLPI (or other tool) using the template.
- My own rewrites of the bad tickets (add as `my-rewrites.md`).

## What I learned

_To be completed by Lucas._
