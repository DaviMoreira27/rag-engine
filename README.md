1. Install `pipx`: https://pipx.pypa.io/stable/installation/
2. Install `poetry`: https://python-poetry.org/docs/
3. Run `poetry install`, if it does not work run `poetry lock`
4. Run test command with `poetry run task test`
5. To run the database:
```sh
docker run -d \
  --name rag-postgres \
  --env-file .env \
  -p 5432:5432 \
  postgres:16-alpine
  ```
