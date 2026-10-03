# C++

[English](cpp.md) · [Français](cpp.fr.md) · **Deutsch**

Ich brauche es, um modernes C++ in Werkzeugen zu lesen, die ich nicht
geschrieben habe, und um eine einzelne Datei zu kompilieren, ohne ein
Wochenende mit CMake. Dieselbe Regel wie bei C. Das ist kein Notizbuch
für Exploits.

## 25 Minuten

`/tmp/cpp-drill/count.cpp`:

```cpp
#include <fstream>
#include <iostream>
#include <string>

int main(int argc, char** argv) {
    if (argc != 2) {
        std::cerr << "usage: count FILE\n";
        return 2;
    }
    std::ifstream in(argv[1]);
    if (!in) {
        std::cerr << "cannot open\n";
        return 1;
    }
    unsigned long n = 0;
    std::string line;
    while (std::getline(in, line))
        n++;
    std::cout << n << '\n';
    return 0;
}
```

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic -O0 -g -o count count.cpp
printf 'a\nb\n' > /tmp/two.txt
./count /tmp/two.txt
```

Erwartet: `2`.

## Das tippe ich, bis es sitzt

- RAII: der `ifstream` schließt sich, wenn er stirbt. Zusätzlich `close()`
  nur, wenn ich den Fehler brauche.
- `std::string`, kein fester Puffer, dessen Größe ich gehofft habe.
- `argc` prüfen, vor `argv[1]`.

## Übung

Nur Zeilen zählen lassen, die `Failed` enthalten. Eine Beispieldatei, die
ich selbst anlege, drei Zeilen, ein Treffer. Den Befehl und die Zahl auf
den Tageszettel schreiben.

## Das verwechsle ich noch

- ein `#include`, das ich kopiert habe und nicht brauche
- `std::endl` überall, und damit bei jeder Zeile ein Flush ohne Grund
- eine Compilerwarnung als optional behandeln
