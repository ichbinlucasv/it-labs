# Haskell

[English](haskell.md) · [Français](haskell.fr.md) · **Deutsch**

Ich brauche es, um Typen zu lesen und die Sprache nicht zu vergessen,
nachdem HashChat die Desktop-App nach Rust verschoben hat. Ein
Helpdesk- oder SOC-Job wird selten nach Haskell fragen. Ich behalte einen
kurzen Block, damit ein späteres Projekt kein Kaltstart ist.

## 25 Minuten

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

Erwartet: `2`.

Fehlt `ghc`, ist das die Notiz des Tages. Ich installiere nicht die ganze
Haskell-Plattform, um danach so zu tun, als hätte ich Typen geübt.

## Das tippe ich, bis es sitzt

```haskell
failed :: String -> Bool
failed line = "Failed password" `elem` words line

countFailed :: String -> Int
countFailed = length . filter failed . lines
```

Der Typ steht über der Funktion. Kann ich den Typ nicht schreiben, verstehe
ich die Funktion noch nicht.

## Übung

`countFailed` auf einer Zeichenkette aus drei Zeilen, die ich in `ghci`
tippe. Eine Zeile trifft. Ich schreibe den Ausdruck und die Zahl auf.

```bash
ghci
```

```haskell
:load Count.hs
```

Eine zweite Datei zu laden ist erlaubt. Der Punkt ist, den Typ von
`filter` zu raten, ohne vorher `:t filter`. Danach `:t filter`, und ich
korrigiere mich.

## Das verwechsle ich noch

- `String` und `Text`, sobald ein echtes Projekt anfängt. Für diese Übung
  `String`.
- `IO` im Typ, obwohl die Funktion rein ist. `countFailed` braucht kein
  `IO`.
- eine Bibliothek für ein `length` und ein `filter` hinzufügen
