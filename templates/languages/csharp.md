# C#

What I need it for: Windows services, reading a .NET stack trace, small
console tools on the SOC VM. I am early at this. The drill is "make a
project, read a file, do not swallow the exception".

## 25 minutes

```bash
mkdir -p /tmp/cs-drill && cd /tmp/cs-drill
dotnet new console -n Lines --framework net8.0
cd Lines
```

Replace `Program.cs`:

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

The second one must print the exception type, not a stack dump I did not
ask for, and exit 1.

## Type this until it sticks

- `dotnet new console`, `dotnet run -- file`
- `File.ReadLines` does not load the whole file as one string
- catch the type I expect (`IOException`, `UnauthorizedAccessException`)
  once I have seen it. A bare `Exception` is only for this first drill.

## Exercise

Read a Windows event export or a text log and print how many lines contain
`4625`. If I have no export, use a three-line file I write myself. Record
the count.

## I still mix up

- the project folder versus the directory I launched `dotnet` from
- string `+` in a loop on a large log. Fine for a drill. Not fine for a
  2 GB evtx conversion. That is what `StringBuilder` or writing line by
  line is for.
