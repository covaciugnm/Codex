#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p docs/validation
docker compose run --rm -e TEST_PG=1 -v "$PWD/tests:/app/tests:ro" content npm test | tee docs/validation/backend-tests.txt
TEST_LIVE_EDIT=1 node tests/browser.mjs
node tests/live-variable.mjs
node tests/redesign-browser.mjs
node tests/discovery-browser.mjs
node tests/product-story-browser.mjs
node tests/customer-finder-browser.mjs
