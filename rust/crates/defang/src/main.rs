use std::process::ExitCode;

const USAGE: &str = "\
usage:
  defang <indicator>          print a non-clickable form
  defang --refang <text>      turn that form back, for parsing only

This does not connect anywhere. Do not click the refanged result.";

fn main() -> ExitCode {
    let mut args = std::env::args().skip(1);
    match (args.next().as_deref(), args.next()) {
        (Some("-h" | "--help"), _) => {
            println!("{USAGE}");
            ExitCode::SUCCESS
        }
        (Some("--refang"), Some(text)) if args.next().is_none() => {
            println!("{}", defang::refang(&text));
            ExitCode::SUCCESS
        }
        (Some(value), None) if !value.starts_with('-') => {
            println!("{}", defang::defang(value));
            ExitCode::SUCCESS
        }
        _ => {
            eprintln!("{USAGE}");
            ExitCode::from(2)
        }
    }
}
