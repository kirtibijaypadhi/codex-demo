# Convenience targets for live demos (no Composer required for `make demo`).
.PHONY: demo serve check curl install-hooks push-summary refresh-summary implement-ticket

HOST ?= localhost
PORT ?= 8080
PUSH_LINE ?=
TICKET ?=

# Start the demo API (same behavior as: composer run demo)
demo serve:
	php -S $(HOST):$(PORT) -t src

# Syntax check before presenting
check:
	php -v
	php -l src/index.php

# Smoke-test the JSON endpoint (run demo in another terminal first)
curl:
	curl -sS "http://$(HOST):$(PORT)/index.php" | head -c 400
	@echo ""

install-hooks:
	./scripts/install-hooks.sh

push-summary:
	python3 tools/git_summary.py --push-line "$(PUSH_LINE)"

refresh-summary:
	python3 tools/git_summary.py --push-line "refs/heads/main $$(git rev-parse HEAD) refs/heads/main $$(git rev-parse origin/main 2>/dev/null || printf '%040d' 0)"

implement-ticket:
	./scripts/implement-ticket.sh "$(TICKET)"
