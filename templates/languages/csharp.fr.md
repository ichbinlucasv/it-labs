# C#

[English](csharp.md) · **Français** · [Deutsch](csharp.de.md)

J'en ai besoin pour les services Windows, pour lire une stack trace .NET,
et pour de petits outils console sur la VM SOC. J'en suis au début.
L'exercice, c'est « faire un projet, lire un fichier, ne pas avaler
l'exception ».

## 25 minutes

```bash
mkdir -p /tmp/cs-drill && cd /tmp/cs-drill
dotnet new console -n Lines --framework net8.0
cd Lines
```

Je remplace `Program.cs` :

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

Le second doit afficher le type de l'exception, pas un dump de pile que je
n'ai pas demandé, et sortir avec le code 1.

## Je retape jusqu'à ce que ça tienne

- `dotnet new console`, `dotnet run -- file`
- `File.ReadLines` ne charge pas tout le fichier comme une seule chaîne
- attraper le type que j'attends (`IOException`, `UnauthorizedAccessException`)
  une fois que je l'ai vu. Un `Exception` nu, seulement pour ce premier
  exercice.

## Exercice

Lire un export d'événements Windows ou un log texte, et afficher combien de
lignes contiennent `4625`. Si je n'ai pas d'export, j'utilise un fichier de
trois lignes que j'écris moi-même. Je note le nombre.

## Je mélange encore

- le dossier du projet, contre le répertoire d'où j'ai lancé `dotnet`
- le `+` de chaînes dans une boucle, sur un gros log. Correct pour un
  exercice. Pas pour une conversion d'evtx de 2 Go. `StringBuilder`, ou
  écrire ligne par ligne, c'est fait pour ça.
