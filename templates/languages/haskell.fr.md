# Haskell

[English](haskell.md) · **Français** · [Deutsch](haskell.de.md)

J'en ai besoin pour lire les types, et pour ne pas oublier le langage après
que HashChat a déplacé son application de bureau vers Rust. Un poste
helpdesk ou SOC demandera rarement du Haskell. Je garde un bloc court pour
qu'un projet plus tard ne soit pas un démarrage à froid.

## 25 minutes

`/tmp/hs-drill/Count.hs` :

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

Attendu : `2`.

Si `ghc` manque, c'est la note du jour. Je n'installe pas une plateforme
Haskell complète en faisant semblant d'avoir pratiqué les types.

## Je retape jusqu'à ce que ça tienne

```haskell
failed :: String -> Bool
failed line = "Failed password" `elem` words line

countFailed :: String -> Int
countFailed = length . filter failed . lines
```

Le type se place au-dessus de la fonction. Si je ne peux pas écrire le
type, je ne comprends pas encore la fonction.

## Exercice

`countFailed` sur une chaîne de trois lignes que je tape dans `ghci`. Une
ligne correspond. J'écris l'expression et le nombre.

```bash
ghci
```

```haskell
:load Count.hs
```

Charger un second fichier est permis. Le but, c'est de deviner le type de
`filter` sans faire `:t filter` d'abord. Puis `:t filter`, et je me
corrige.

## Je mélange encore

- `String` et `Text` dès qu'un vrai projet commence. Pour cet exercice,
  `String`.
- `IO` dans le type alors que la fonction est pure. `countFailed` n'a pas
  besoin d'`IO`.
- ajouter une bibliothèque pour un `length` et un `filter`
