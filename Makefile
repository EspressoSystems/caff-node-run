.PHONY: setup validate help

setup:
	@echo "Setting up development environment..."
	git config core.hooksPath .githooks
	@echo "✅ Git hooks configured!"
	@echo "   Pre-commit validation will now run automatically"

validate:
	python3 ./scripts/validate_schema.py

help:
	@echo "Available commands:"
	@echo "  make setup      - Configure git hooks (run once after cloning)"
	@echo "  make validate   - Validate all config files"
	@echo "  make help       - Show this help message"

.DEFAULT_GOAL := help