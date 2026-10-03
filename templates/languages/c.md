# C

**English** · [Français](c.fr.md) · [Deutsch](c.de.md)

There is no C project in this repo yet. This block is so the language does
not disappear behind Rust.

What I need it for: reading small system tools, compiling with the warnings
on, and not being lost when a C program prints a crash address. I am not
writing exploits. If a lab needs that, it is someone else's course VM, and
it is not these notes.

## 25 minutes

```bash
mkdir -p /tmp/c-drill && cd /tmp/c-drill
```

Save this as `lines.c`:

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

Expected: `2`. If the warnings are not empty, I fix them before I call it done.

## Type this until it sticks

- `gcc -Wall -Wextra -Wpedantic -g`
- `int` versus `size_t` when I am counting
- check the return of `fopen` before `fread`
- `EOF` is not a char I store in a `char` if `char` is unsigned. The loop
  above uses `int c` for that reason.

A crash I do not understand yet:

```bash
gdb -q ./lines
run
bt
```

I want to be able to read `bt`. I do not need to write a vulnerable
function to practise that. A null `FILE *` is enough on a throwaway copy,
and I delete it after.

## Exercise

Change the program to take a path from `argv[1]`, refuse `argc != 2`, and
print `fopen` failure on stderr with `perror`. Time limit 25 minutes
including the compile. If I do not finish, the daily sheet says how far
I got.

## I still mix up

- forgetting `-Wall` and trusting a clean-looking bug
- `printf` with the wrong length modifier
- "it works on my sample" with no empty-file test
