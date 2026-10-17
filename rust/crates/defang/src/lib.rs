//! Defang and refang indicators the same way `seclab.ioc` does in Python.
//!
//! Defang is for a ticket or a chat: the text should not be a link someone
//! clicks by accident. Refang is for parsing a report that arrived already
//! defanged. This crate does not look the indicator up, and it does not
//! connect anywhere.

/// Make an indicator non-clickable.
///
/// `https://a.example` becomes `hxxps://a[.]example`. Dots in the path stay.
pub fn defang(value: &str) -> String {
    let mut v = value.to_string();
    if has_ascii_prefix(&v, "http") {
        v.replace_range(0..4, "hxxp");
    } else if has_ascii_prefix(&v, "ftp") {
        v.replace_range(0..3, "fxp");
    }
    v = v.replace('@', "[@]");
    if let Some(idx) = v.find("://") {
        let scheme = &v[..idx];
        let rest = &v[idx + 3..];
        let (host, path) = match rest.find('/') {
            Some(i) => (&rest[..i], &rest[i..]),
            None => (rest, ""),
        };
        return format!("{scheme}://{}{path}", host.replace('.', "[.]"));
    }
    if v.matches(':').count() >= 2 {
        return v.replace(':', "[:]");
    }
    v.replace('.', "[.]")
}

/// Turn common defanged notation back into a live indicator, for parsing only.
pub fn refang(text: &str) -> String {
    let mut s = replace_scheme_word(text, "hxxp", "http");
    s = replace_scheme_word(&s, "fxp", "ftp");
    s = s.replace("[://]", "://");
    s = s.replace("[:]", ":");
    for token in ["[.]", "(.)", "{.}", "[dot]", "(dot)"] {
        s = replace_ci(&s, token, ".");
    }
    for token in ["[@]", "(@)", "[at]", "(at)"] {
        s = replace_ci(&s, token, "@");
    }
    s
}

fn has_ascii_prefix(value: &str, prefix: &str) -> bool {
    value.len() >= prefix.len() && value[..prefix.len()].eq_ignore_ascii_case(prefix)
}

/// Replace `from` with `to` when it is a whole scheme word. An optional
/// trailing `s` is kept (`hxxps` -> `https`).
fn replace_scheme_word(hay: &str, from: &str, to: &str) -> String {
    let b = hay.as_bytes();
    let mut out = String::new();
    let mut i = 0;
    while i < b.len() {
        let prev_ok = i == 0 || !b[i - 1].is_ascii_alphanumeric();
        let tail = &hay[i..];
        if prev_ok && has_ascii_prefix(tail, from) {
            let mut end = i + from.len();
            let mut https = false;
            if end < b.len() && b[end].eq_ignore_ascii_case(&b's') {
                let after = end + 1;
                if after >= b.len() || !b[after].is_ascii_alphanumeric() {
                    https = true;
                    end = after;
                }
            }
            let next_ok = end >= b.len() || !b[end].is_ascii_alphanumeric();
            if next_ok {
                out.push_str(to);
                if https {
                    out.push('s');
                }
                i = end;
                continue;
            }
        }
        out.push(b[i] as char);
        i += 1;
    }
    out
}

fn replace_ci(hay: &str, needle: &str, repl: &str) -> String {
    let lower_needle = needle.to_ascii_lowercase();
    let mut out = String::new();
    let mut rest = hay;
    while !rest.is_empty() {
        let lower = rest.to_ascii_lowercase();
        if let Some(pos) = lower.find(&lower_needle) {
            out.push_str(&rest[..pos]);
            out.push_str(repl);
            rest = &rest[pos + needle.len()..];
        } else {
            out.push_str(rest);
            break;
        }
    }
    out
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn refang_matches_the_python_tool() {
        let cases = [
            ("hxxps://evil[.]example/path", "https://evil.example/path"),
            ("hXXp://198.51.100[.]7:8080/a", "http://198.51.100.7:8080/a"),
            ("user[@]example[.]com", "user@example.com"),
            ("bad(.)example(dot)net", "bad.example.net"),
            ("fxp://files{.}example[.]org", "ftp://files.example.org"),
            ("https[://]a[.]example", "https://a.example"),
        ];
        for (defanged, live) in cases {
            assert_eq!(refang(defanged), live, "{defanged}");
        }
    }

    #[test]
    fn defang_matches_the_python_tool() {
        let cases = [
            ("https://evil.example/a.b/c", "hxxps://evil[.]example/a.b/c"),
            ("203.0.113.9", "203[.]0[.]113[.]9"),
            ("evil.example.net", "evil[.]example[.]net"),
            ("a@b.example", "a[@]b[.]example"),
            ("2001:db8::1", "2001[:]db8[:][:]1"),
        ];
        for (live, defanged) in cases {
            assert_eq!(defang(live), defanged, "{live}");
        }
    }

    #[test]
    fn roundtrip_and_no_live_scheme() {
        for v in [
            "https://x.example/p?q=1",
            "198.51.100.1",
            "mail@x.example",
            "sub.x.example",
            "2001:db8::1",
        ] {
            let out = defang(v);
            assert_eq!(refang(&out), v, "{v}");
            assert!(!out.to_ascii_lowercase().contains("http"));
            assert!(!out.to_ascii_lowercase().starts_with("ftp"));
        }
    }
}
