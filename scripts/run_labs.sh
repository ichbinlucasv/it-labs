#!/usr/bin/env bash
# Run every lab check that does not need root. From the repository root.
set -u
ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT"
fail=0

run() {
    echo
    echo "======== $* ========"
    if "$@"; then
        echo "-------- OK: $* --------"
    else
        echo "-------- FAIL: $* --------"
        fail=1
    fi
}

run python3 networking/01-subnetting/check_answers.py
run python3 helpdesk/01-ticket-writing/check_tickets.py
run python3 helpdesk/02-windows-troubleshooting/triage.py --check
run bash helpdesk/02-windows-troubleshooting/dns-break.sh
run python3 helpdesk/04-samba-ad-lab/verify_evidence.py
run python3 helpdesk/05-m365-basics/identity_lab.py
run python3 helpdesk/06-windows-domain/verify_evidence.py
run python3 soc-analyst/01-wazuh-homelab/detect.py --check
run python3 soc-analyst/03-incident-writeups/investigate_sql.py --check
run python3 security-plus/quiz.py --check --sample
run python3 scripts/check_repo.py

if [[ -x python/.venv/bin/pytest ]]; then
    run python/.venv/bin/pytest -q python/tests
else
    echo "skip pytest (python/.venv is missing)"
fi

echo
if [[ $fail -eq 0 ]]; then
    echo "run_labs: OK"
else
    echo "run_labs: FAILED"
fi
exit $fail
