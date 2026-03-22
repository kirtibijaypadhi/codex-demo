# Convenience targets for live demos (no Composer required for `make demo`).
.PHONY: demo serve check curl

HOST ?= localhost
PORT ?= 8080

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
