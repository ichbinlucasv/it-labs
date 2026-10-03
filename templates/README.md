# Day-to-day templates

Copy one file, fill the blanks, keep the copy in my notes. The blanks stay
blank in git.

I do not open all of these every day. A useful day is one helpdesk or SOC
sheet, plus **one** language block. The language list is long so I do not
drop one for six months. It is not a list I finish before breakfast.

## This morning

1. Copy [career/daily.md](career/daily.md).
2. Pick the column for today.
3. Stop when the timer ends. Write one line on what I could not do from memory.

| Day | Job practice | Language (25 min) |
| --- | --- | --- |
| Mon | [Helpdesk ticket](helpdesk/ticket.md) | [bash](languages/bash.md) |
| Tue | [Can't log on](helpdesk/cant-log-on.md) or [password reset](helpdesk/password-reset.md) | [PowerShell](languages/powershell.md) |
| Wed | [Alert triage](soc/alert-triage.md) | [Python](languages/python.md) |
| Thu | [Timeline](soc/timeline.md) on one old alert | [Rust](languages/rust.md) or [C](languages/c.md), alternate weeks |
| Fri | [Weekly review](career/weekly.md) | One of [C++](languages/cpp.md), [C#](languages/csharp.md), [Java](languages/java.md), [Kotlin](languages/kotlin.md), [Haskell](languages/haskell.md). Rotate. Do not do all five. |
| Sat | Lab, if the guests are on. [Lab 06](../helpdesk/06-windows-domain/) or a Linux break/fix. | Only if Friday's language is still fuzzy. |
| Sun | Off, or [interview story](career/story.md) from a real lab note. | Off. |

## Helpdesk

The long ticket shape already lives in
[helpdesk/01-ticket-writing/template.md](../helpdesk/01-ticket-writing/template.md).
These are the ones I want on a shift.

| Form | Use it when |
| --- | --- |
| [ticket.md](helpdesk/ticket.md) | Any new request |
| [ticket-fr.md](helpdesk/ticket-fr.md) | Same thing in French, for a French desk |
| [shift-start.md](helpdesk/shift-start.md) | First 15 minutes |
| [cant-log-on.md](helpdesk/cant-log-on.md) | "I can't get in" |
| [password-reset.md](helpdesk/password-reset.md) | Reset or unlock. Check who is asking. |
| [new-user.md](helpdesk/new-user.md) | Starter |
| [leaver.md](helpdesk/leaver.md) | Someone left |
| [escalation.md](helpdesk/escalation.md) | I am stuck and handing it on |
| [remote-session.md](helpdesk/remote-session.md) | I am on their screen |
| [kb.md](helpdesk/kb.md) | The same fix happened twice |

## SOC

| Form | Use it when |
| --- | --- |
| [shift-handover.md](soc/shift-handover.md) | I take the queue, or I leave it |
| [alert-triage.md](soc/alert-triage.md) | One alert. Not five tools. |
| [timeline.md](soc/timeline.md) | Times in UTC, oldest first |
| [ioc-note.md](soc/ioc-note.md) | Something to look up, defanged |
| [detection-idea.md](soc/detection-idea.md) | What I would want an alert for, and what would be noise |
| [end-of-shift.md](soc/end-of-shift.md) | What is still open |

## Career

| Form | Use it when |
| --- | --- |
| [daily.md](career/daily.md) | Every study day |
| [weekly.md](career/weekly.md) | Friday |
| [story.md](career/story.md) | One real story for an interview. Only after I did the work. |

## Rules I keep breaking

- No passwords, cookies, or client names in a note I might paste into git.
- Quote the error. Do not write "it failed".
- One change, then check. Then the next change.
- If I only installed a tool, the note says installed. It does not say I know it.
- UTC on SOC notes. Local time is fine on a helpdesk ticket if I say the zone.
