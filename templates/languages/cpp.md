# C++

What I need it for: reading modern C++ in tools I did not write, and
compiling a single file without a weekend of CMake. Same rule as C. This
is not an exploit notebook.

## 25 minutes

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

Expected: `2`.

## Type this until it sticks

- RAII: the `ifstream` closes when it dies. I do not also `close()` unless
  I need the error.
- `std::string`, not a fixed buffer I sized by hope.
- `argc` check before `argv[1]`.

## Exercise

Make it count only lines that contain `Failed`. One sample file I create
myself, three lines, one match. Write the command and the number in the
daily sheet.

## I still mix up

- `#include` I copied and do not need
- `std::endl` everywhere, flushing every line for no reason
- treating a compiler warning as optional
