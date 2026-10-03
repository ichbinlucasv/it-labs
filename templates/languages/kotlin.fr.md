# Kotlin

[English](kotlin.md) · **Français** · [Deutsch](kotlin.de.md)

Plus tard, j'en aurai besoin pour Android autour de HashChat, et pour les
boîtes JVM qui écrivent du Kotlin à la place de Java. Là, j'ai seulement
besoin de compiler un fichier et de lire les mêmes stack traces qu'en Java.

## 25 minutes

Si `kotlinc` est installé :

```bash
mkdir -p /tmp/kt-drill && cd /tmp/kt-drill
```

`Count.kt` :

```kotlin
import java.nio.file.Files
import java.nio.file.Path
import kotlin.streams.asSequence

fun main(args: Array<String>) {
    if (args.size != 1) {
        System.err.println("usage: Count FILE")
        kotlin.system.exitProcess(2)
    }
    val n = Files.lines(Path.of(args[0])).asSequence().count()
    println(n)
}
```

```bash
kotlinc Count.kt -include-runtime -d count.jar
java -jar count.jar /etc/hostname
```

Si `kotlinc` n'est pas installé, je le note et je passe les 25 minutes sur
la page Java à la place. Deux langages JVM dans le même créneau, c'est
comme ça que je ne retiens ni l'un ni l'autre.

## Je retape jusqu'à ce que ça tienne

- `val`, sauf si je dois réaffecter
- null, c'est `String?`, et je ne mets pas `!!` sur un chemin que je n'ai
  pas vérifié
- la stack trace reste une stack trace Java

## Exercice

Une `data class` avec `time`, `user`, `host`. Je construis une liste de
deux ouvertures de session échouées, fictives, et j'affiche les
utilisateurs. Pas de SDK Android. Pas de Gradle, sauf si le fichier à
compiler m'a déjà ennuyé et qu'il me reste dix minutes.

## Je mélange encore

- le null de Kotlin contre le null Java qui revient de `Files`
- démarrer un projet Android alors que la tâche était un fichier de 30 lignes
