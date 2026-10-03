# Haskell

**English** · [Français](haskell.fr.md) · [Deutsch](haskell.de.md)

What I need it for: reading types, and not forgetting the language after
HashChat moved its desktop to Rust. A helpdesk or SOC job will rarely ask
for Haskell. I keep a short block so a later project is not a cold start.

## 25 minutes

`/tmp/hs-drill/Count.hs`:

```haskell
module Main where

main :: IO ()
main = do
  text <- getContents
  print (length (lines text))
```

```bash
ghc -Wall -O0 -o count Count.hs
printf 'a\nb\n' | ./count
```

Expected: `2`.

If `ghc` is missing, that is the note for the day. I do not install a
full Haskell platform and also pretend I practised types.

## Type this until it sticks

```haskell
failed :: String -> Bool
failed line = "Failed password" `elem` words line

countFailed :: String -> Int
countFailed = length . filter failed . lines
```

The type goes above the function. If I cannot write the type, I do not
understand the function yet.

## Exercise

`countFailed` on a three-line string I type in `ghci`. One line matches.
Write the expression and the number.

```bash
ghci
```

```haskell
:load Count.hs
```

Loading a second file is allowed. Guessing the type of `filter` without
`:t filter` first is the point. Then `:t filter` and correct myself.

## I still mix up

- `String` and `Text` once a real project starts. For this drill, `String`.
- IO in the type when the function is pure. `countFailed` does not need `IO`.
- adding a library for a `length` and a `filter`
