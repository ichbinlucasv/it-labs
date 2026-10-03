# Password reset or unlock

**English** · [Français](password-reset.fr.md) · [Deutsch](password-reset.de.md)

```text
Ticket:
Account:
Caller:
How I verified the caller:
    [ ] callback to the number on the account
    [ ] manager on a known number
    [ ] in person, I know them
    [ ] I did not, so I stopped

Before:
- LockedOut:
- PasswordExpired:
- Enabled:
- OU:

Action:
- [ ] Unlock-ADAccount only
- [ ] Reset, ChangePasswordAtLogon = true
- [ ] Disabled the account instead (suspected misuse)

Temporary secret stored in the ticket?  NO

After:
- User logged on?  yes / no
- They changed the password themselves?  yes / no / not yet

Command I typed (no secret in it):
```

Lab practice, on `lab.local`, helpdesk account, Staff OU only:

```powershell
Get-ADUser jdoe -Properties LockedOut, PasswordLastSet, PasswordExpired, Enabled, MemberOf
Unlock-ADAccount jdoe
```

I still look up the reset cmdlet. When I can type it, I delete this reminder
from my own copy. Until then it stays.
