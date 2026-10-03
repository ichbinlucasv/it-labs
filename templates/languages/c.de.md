# C

[English](c.md) · [Français](c.fr.md) · **Deutsch**

Ein C-Projekt liegt in diesem Repo noch nicht. Dieser Block ist da, damit
die Sprache nicht hinter Rust verschwindet.

Ich brauche es, um kleine Systemwerkzeuge zu lesen, mit eingeschalteten
Warnungen zu kompilieren, und nicht verloren zu sein, wenn ein C-Programm
eine Absturzadresse ausgibt. Ich schreibe keine Exploits. Wenn ein Lab das
braucht, ist das die Kurs-VM von jemand anderem, und nicht diese Notizen.

## 25 Minuten

```bash
mkdir -p /tmp/c-drill && cd /tmp/c-drill
```

Ich speichere das als `lines.c`:

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

Erwartet: `2`. Wenn die Warnungen nicht leer sind, behebe ich sie, bevor
ich es als fertig bezeichne.

## Das tippe ich, bis es sitzt

- `gcc -Wall -Wextra -Wpedantic -g`
- `int` gegen `size_t`, wenn ich zähle
- den Rückgabewert von `fopen` vor `fread` prüfen
- `EOF` ist kein Zeichen, das ich in einem `char` speichere, wenn `char`
  vorzeichenlos ist. Die Schleife oben benutzt deshalb `int c`.

Ein Absturz, den ich noch nicht verstehe:

```bash
gdb -q ./lines
run
bt
```

Ich will `bt` lesen können. Ich muss keine verwundbare Funktion schreiben,
um das zu üben. Ein `FILE *` mit NULL reicht, auf einer Wegwerfkopie, und
ich lösche sie danach.

## Übung

Das Programm ändern: einen Pfad aus `argv[1]` nehmen, `argc != 2`
ablehnen, und einen `fopen`-Fehler mit `perror` auf stderr ausgeben.
Zeitlimit 25 Minuten, inklusive Kompilieren. Wenn ich nicht fertig werde,
steht auf dem Tageszettel, wie weit ich gekommen bin.

## Das verwechsle ich noch

- `-Wall` vergessen und einem Bug trauen, der sauber aussieht
- `printf` mit dem falschen Längenmodifikator
- „läuft auf meinem Beispiel“, ohne Test mit leerer Datei
