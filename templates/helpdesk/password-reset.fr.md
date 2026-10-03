# Réinitialisation ou déverrouillage

[English](password-reset.md) · **Français** · [Deutsch](password-reset.de.md)

```text
Ticket :
Compte :
Appelant :
Comment j'ai vérifié l'appelant :
    [ ] rappel au numéro du compte
    [ ] responsable sur un numéro connu
    [ ] en personne, je connais la personne
    [ ] je ne l'ai pas fait, donc je me suis arrêté

Avant :
- LockedOut:
- PasswordExpired:
- Enabled:
- OU:

Action :
- [ ] Unlock-ADAccount seulement
- [ ] Réinitialisation, ChangePasswordAtLogon = true
- [ ] Compte désactivé à la place (usage abusif soupçonné)

Secret temporaire stocké dans le ticket ?  NON

Après :
- L'utilisateur s'est connecté ?  oui / non
- Il a changé le mot de passe lui-même ?  oui / non / pas encore

Commande que j'ai tapée (sans le secret dedans) :
```

Exercice de labo, sur `lab.local`, compte helpdesk, OU Staff seulement :

```powershell
Get-ADUser jdoe -Properties LockedOut, PasswordLastSet, PasswordExpired, Enabled, MemberOf
Unlock-ADAccount jdoe
```

Je cherche encore la cmdlet de réinitialisation. Quand je sais la taper,
j'efface ce rappel de ma copie. Jusque-là, il reste.
