# Kotlin

What I need it for later: Android around HashChat, and JVM shops that
write Kotlin instead of Java. Right now I only need to compile a file
and read the same stack traces as Java.

## 25 minutes

If `kotlinc` is installed:

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

If `kotlinc` is not installed, I write that down and spend the 25 minutes
on the Java page instead. Two JVM languages in one slot is how I retain
neither.

## Type this until it sticks

- `val` unless I must reassign
- null is `String?`, and I do not `!!` a path I have not checked
- the stack trace is still a Java stack trace

## Exercise

A `data class` with `time`, `user`, `host`. Build a list of two fake
failed logons and print the users. No Android SDK. No Gradle unless the
compiler file already bored me and I still have ten minutes.

## I still mix up

- Kotlin null versus Java null coming back from `Files`
- starting an Android project when the task was a 30-line file
