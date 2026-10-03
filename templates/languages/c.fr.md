# C

[English](c.md) · **Français** · [Deutsch](c.de.md)

Il n'y a pas encore de projet C dans ce dépôt. Ce bloc est là pour que le
langage ne disparaisse pas derrière Rust.

J'en ai besoin pour lire de petits outils système, compiler avec les
avertissements activés, et ne pas être perdu quand un programme C affiche
une adresse de crash. Je n'écris pas d'exploits. Si un lab en a besoin,
c'est la VM de cours de quelqu'un d'autre, pas ces notes.

## 25 minutes

```bash
mkdir -p /tmp/c-drill && cd /tmp/c-drill
```

Je l'enregistre sous `lines.c` :

```c
#include <stdio.h>

int main(void) {
    int c;
    unsigned long n = 0;
    while ((c = getchar()) != EOF) {
        if (c == '\n')
            n++;
    }
    printf("%lu\n", n);
    return 0;
}
```

```bash
gcc -std=c11 -Wall -Wextra -Wpedantic -O0 -g -o lines lines.c
printf 'a\nb\n' | ./lines
```

Attendu : `2`. Si les avertissements ne sont pas vides, je les corrige
avant de dire que c'est fini.

## Je retape jusqu'à ce que ça tienne

- `gcc -Wall -Wextra -Wpedantic -g`
- `int` contre `size_t` quand je compte
- vérifier le retour de `fopen` avant `fread`
- `EOF` n'est pas un caractère que je stocke dans un `char` si `char` est
  non signé. La boucle ci-dessus utilise `int c` pour cette raison.

Un plantage que je ne comprends pas encore :

```bash
gdb -q ./lines
run
bt
```

Je veux pouvoir lire `bt`. Je n'ai pas besoin d'écrire une fonction
vulnérable pour m'entraîner à ça. Un `FILE *` nul suffit, sur une copie
jetable, et je la supprime après.

## Exercice

Je modifie le programme pour qu'il prenne un chemin depuis `argv[1]`,
refuse `argc != 2`, et affiche l'échec de `fopen` sur stderr avec
`perror`. Limite : 25 minutes, compilation comprise. Si je ne finis pas,
la fiche du jour dit jusqu'où je suis allé.

## Je mélange encore

- oublier `-Wall` et faire confiance à un bug qui a l'air propre
- `printf` avec le mauvais modificateur de longueur
- « ça marche sur mon échantillon », sans test du fichier vide
