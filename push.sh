rm ./dist/*
lordhelp dev set-version ./pyproject.toml
python3.10 -m build
twine upload --repository gitea dist/*
