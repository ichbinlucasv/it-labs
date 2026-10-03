# Java

**English** · [Français](java.fr.md) · [Deutsch](java.de.md)

What I need it for: reading a Java stack trace from the bottom, and small
file tools. A lot of enterprise kit on a helpdesk throws Java at you.
I do not need Spring this month.

## 25 minutes

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

If `javac` is missing, the daily sheet says that. Installing a JDK is the
whole block. I do not pretend I coded.

## Reading a stack trace

The first line is the exception type and message. The first `at` from
**my** package is where I start. `Caused by:` under it is usually the
real reason. I copy those three pieces into the ticket, not the whole 80
frames.

## Exercise

Break the path on purpose. Paste the exception type and the message into
the daily sheet. One sentence: was the useful part the first line or the
`Caused by`?

## I still mix up

- `java Lines` versus `java lines` on a case-sensitive disk
- classpath errors that look like missing code
- catching `Exception` and printing nothing
