# C#

[English](csharp.md) · [Français](csharp.fr.md) · **Deutsch**

Ich brauche es für Windows-Dienste, für einen .NET-Stacktrace, und für
kleine Konsolenwerkzeuge auf der SOC-VM. Ich stehe damit noch am Anfang.
Die Übung ist: „ein Projekt machen, eine Datei lesen, die Exception nicht
schlucken“.

## 25 Minuten

```bash
mkdir -p /tmp/cs-drill && cd /tmp/cs-drill
dotnet new console -n Lines --framework net8.0
cd Lines
```

Ich ersetze `Program.cs`:

```csharp
if (args.Length != 1) {
    Console.Error.WriteLine("usage: Lines FILE");
    return 2;
}
try {
    var n = File.ReadLines(args[0]).LongCount();
    Console.WriteLine(n);
    return 0;
} catch (Exception ex) {
    Console.Error.WriteLine(ex.GetType().Name + ": " + ex.Message);
    return 1;
}
```

```bash
dotnet run -- /etc/hostname
dotnet run -- /no/such/file
```

Der zweite muss den Typ der Exception ausgeben, nicht einen Stackdump, den
ich nicht verlangt habe, und mit Code 1 enden.

## Das tippe ich, bis es sitzt

- `dotnet new console`, `dotnet run -- file`
- `File.ReadLines` lädt nicht die ganze Datei als eine Zeichenkette
- den Typ fangen, den ich erwarte (`IOException`, `UnauthorizedAccessException`),
  sobald ich ihn gesehen habe. Ein nacktes `Exception` nur für diese erste
  Übung.

## Übung

Einen Windows-Ereignisexport oder ein Textlog lesen und ausgeben, wie viele
Zeilen `4625` enthalten. Habe ich keinen Export, nehme ich eine Datei mit
drei Zeilen, die ich selbst schreibe. Ich notiere die Zahl.

## Das verwechsle ich noch

- der Projektordner gegen das Verzeichnis, aus dem ich `dotnet` gestartet habe
- Zeichenketten-`+` in einer Schleife über ein großes Log. Für eine Übung
  in Ordnung. Nicht für eine Umwandlung von 2 GB evtx. Dafür sind
  `StringBuilder` oder zeilenweises Schreiben da.
