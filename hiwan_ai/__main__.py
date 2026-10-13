"""Allow `uv run python -m hiwan_ai ...` without installing a console script."""
from .cli import main

if __name__ == '__main__':
    raise SystemExit(main())
