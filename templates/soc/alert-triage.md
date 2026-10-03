# One alert

**English** · [Français](alert-triage.fr.md) · [Deutsch](alert-triage.de.md)

One alert per sheet. UTC. I answer from the log before I open a second tool.

```text
Alert name / rule:
ID:
Arrived (UTC):
Asset:
User:
Severity in the tool:

What the rule thinks happened (one sentence):

First event I opened (ID, time UTC):
Parent process, if this is endpoint:
Logon type, if this is a logon:

Seen on this asset before?  unknown / yes, ticket / no

Benign reason I can name:
    [ ] admin tool we use
    [ ] patch / backup window
    [ ] the user did the thing
    [ ] I cannot name one

Decision:
    [ ] close, reason:
    [ ] monitor, what would change my mind:
    [ ] escalate, with the timeline sheet

What I did not do: run the file, click the link, or try the password.
```

Practice on the synthetic logs in
[soc-analyst/02](../../soc-analyst/02-sysmon-auditd-logs/) or on IR-03.
A sheet with no event ID does not count.
