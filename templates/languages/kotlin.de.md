# Kotlin

[English](kotlin.md) · [Français](kotlin.fr.md) · **Deutsch**

Später brauche ich es für Android rund um HashChat, und für JVM-Firmen, die
Kotlin statt Java schreiben. Jetzt muss ich nur eine Datei kompilieren und
dieselben Stacktraces lesen wie bei Java.

## 25 Minuten

Wenn `kotlinc` installiert ist:

```bash
mkdir -p /tmp/kt-drill && cd /tmp/kt-drill
```

`Count.kt`:

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

Wenn `kotlinc` nicht installiert ist, schreibe ich das auf und nutze die
25 Minuten stattdessen für die Java-Seite. Zwei JVM-Sprachen in einem
Block, so behalte ich keine von beiden.

## Das tippe ich, bis es sitzt

- `val`, außer ich muss neu zuweisen
- null ist `String?`, und kein `!!` auf einen Pfad, den ich nicht geprüft
  habe
- der Stacktrace bleibt ein Java-Stacktrace

## Übung

Eine `data class` mit `time`, `user`, `host`. Eine Liste aus zwei
erfundenen fehlgeschlagenen Anmeldungen bauen und die Benutzer ausgeben.
Kein Android-SDK. Kein Gradle, außer die Datei zum Kompilieren hat mich
schon gelangweilt und ich habe noch zehn Minuten.

## Das verwechsle ich noch

- Kotlin-null gegen Java-null, das von `Files` zurückkommt
- ein Android-Projekt starten, obwohl die Aufgabe eine Datei von 30 Zeilen war
