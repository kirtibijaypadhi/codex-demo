# Push Summaries

This directory stores Markdown summaries generated from the Git push demo flow.

The file `latest.md` is refreshed by `.githooks/pre-push`. If the content changes, the hook blocks the push so the summary can be reviewed and committed explicitly.
