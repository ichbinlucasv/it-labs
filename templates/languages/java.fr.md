# Java

[English](java.md) · **Français** · [Deutsch](java.de.md)

J'en ai besoin pour lire une stack trace Java depuis le bas, et pour de
petits outils sur des fichiers. Au helpdesk, beaucoup d'outils d'entreprise
me jettent du Java. Je n'ai pas besoin de Spring ce mois-ci.

## 25 minutes

`/tmp/java-drill/Lines.java` :

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

Si `javac` manque, la fiche du jour le dit. Installer un JDK, c'est tout le
bloc. Je ne prétends pas avoir codé.

## Lire une stack trace

La première ligne, c'est le type de l'exception et le message. Le premier
`at` de **mon** package, c'est là que je commence. Le `Caused by:` en dessous
est en général la vraie raison. Je copie ces trois morceaux dans le ticket,
pas les 80 frames au complet.

## Exercice

Je casse le chemin exprès. Je colle le type de l'exception et le message sur
la fiche du jour. Une phrase : la partie utile, c'était la première ligne ou
le `Caused by` ?

## Je mélange encore

- `java Lines` contre `java lines`, sur un disque sensible à la casse
- les erreurs de classpath qui ressemblent à du code manquant
- attraper `Exception` et ne rien afficher
