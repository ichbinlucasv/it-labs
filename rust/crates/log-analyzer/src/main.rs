use std::io::{self, Read};
use std::process::ExitCode;

use log_analyzer::Summary;

const USAGE: &str = "usage: log-analyzer [--top N] [--min-errors N] [FILE|-]\n\
Summarise an Apache/Nginx combined-format access log (default: stdin).";

fn main() -> ExitCode {
    let mut top = 10usize;
    let mut min_errors = 10usize;
    let mut file: Option<String> = None;

    let mut args = std::env::args().skip(1);
    while let Some(a) = args.next() {
        match a.as_str() {
            "-h" | "--help" => {
                println!("{USAGE}");
                return ExitCode::SUCCESS;
            }
            "--top" | "--min-errors" => {
                let Some(v) = args.next().and_then(|v| v.parse().ok()) else {
                    eprintln!("{a} needs a number\n{USAGE}");
                    return ExitCode::from(2);
                };
                if a == "--top" {
                    top = v;
                } else {
                    min_errors = v;
                }
            }
            _ => file = Some(a),
        }
    }

    let mut text = String::new();
    let res = match file.as_deref() {
        None | Some("-") => io::stdin().read_to_string(&mut text).map(|_| ()),
        Some(path) => std::fs::read(path).map(|b| text = String::from_utf8_lossy(&b).into_owned()),
    };
    if let Err(e) = res {
        eprintln!("error reading input: {e}");
        return ExitCode::from(2);
    }

    let summary = Summary::from_lines(text.lines());
    print!("{}", summary.report(top, min_errors));
    ExitCode::SUCCESS
}
