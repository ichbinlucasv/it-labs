# C++

[English](cpp.md) · **Français** · [Deutsch](cpp.de.md)

J'en ai besoin pour lire du C++ moderne dans des outils que je n'ai pas
écrits, et pour compiler un seul fichier sans un week-end de CMake. Même
règle que pour le C. Ce n'est pas un cahier d'exploits.

## 25 minutes

`/tmp/cpp-drill/count.cpp` :

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

Attendu : `2`.

## Je retape jusqu'à ce que ça tienne

- RAII : le `ifstream` se ferme quand il meurt. Je n'appelle pas `close()`
  en plus, sauf si j'ai besoin de l'erreur.
- `std::string`, pas un tampon fixe dont j'ai choisi la taille en espérant.
- vérifier `argc` avant `argv[1]`.

## Exercice

Le faire compter seulement les lignes qui contiennent `Failed`. Un fichier
d'exemple que je crée moi-même, trois lignes, une correspondance. J'écris
la commande et le nombre sur la fiche du jour.

## Je mélange encore

- un `#include` que j'ai copié et dont je n'ai pas besoin
- `std::endl` partout, qui vide le tampon à chaque ligne sans raison
- traiter un avertissement du compilateur comme facultatif
