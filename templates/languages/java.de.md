# Java

[English](java.md) · [Français](java.fr.md) · **Deutsch**

Ich brauche es, um einen Java-Stacktrace von unten zu lesen, und für kleine
Werkzeuge für Dateien. Am Helpdesk wirft mir viel Firmensoftware Java
entgegen. Spring brauche ich diesen Monat nicht.

## 25 Minuten

`/tmp/java-drill/Lines.java`:

```java
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public final class Lines {
    public static void main(String[] args) throws IOException {
        if (args.length != 1) {
            System.err.println("usage: Lines FILE");
            System.exit(2);
        }
        long n = Files.lines(Path.of(args[0])).count();
        System.out.println(n);
    }
}
```

```bash
javac --release 21 Lines.java
java Lines /etc/hostname
```

Fehlt `javac`, steht das auf dem Tageszettel. Ein JDK zu installieren ist
der ganze Block. Ich tue nicht so, als hätte ich programmiert.

## Einen Stacktrace lesen

Die erste Zeile ist Typ und Meldung der Exception. Das erste `at` aus
**meinem** Paket ist die Stelle, an der ich anfange. `Caused by:` darunter
ist meist der eigentliche Grund. Diese drei Stücke kopiere ich ins Ticket,
nicht alle 80 Frames.

## Übung

Ich mache den Pfad mit Absicht kaputt. Den Exception-Typ und die Meldung
setze ich auf den Tageszettel. Ein Satz: war der nützliche Teil die erste
Zeile oder das `Caused by`?

## Das verwechsle ich noch

- `java Lines` gegen `java lines` auf einem Datenträger, der Groß- und
  Kleinschreibung unterscheidet
- Classpath-Fehler, die wie fehlender Code aussehen
- `Exception` fangen und nichts ausgeben
