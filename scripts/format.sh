set -x

# Sort imports one per line, so autoflake can remove unused imports
isort --recursive  --force-single-line-imports --force-alphabetical-sort-within-sections --apply src

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place src --exclude=__init__.py
black src --line-length 88
isort --recursive --apply src