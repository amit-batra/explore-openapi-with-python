# explore-openapi-with-python

A small, self-contained example of the **OpenAPI standard** in practice: one
OpenAPI 3.1 document (`openapi.yaml`) is the single source of truth, and from it
we generate

- a **typed async/sync HTTP client** (`openapi-python-client`), and
- the **shared Pydantic data models** that a FastAPI **server** imports.

The point is to show how OpenAPI replaces hand-written API docs: the contract is
machine-checkable and drives code on both sides.

## Layout

```
openapi.yaml                       # the single source of truth (OpenAPI 3.1)
scripts/
  generate.sh                      # regenerates both client + server models
  generate-client.sh               # client only (openapi-python-client)
  generate-server.sh               # server models only (datamodel-code-generator)
src/
  app.py                           # FastAPI server (stubs) importing generated models
  __main__.py                      # `python -m src` runs the server
  generated/
    client/                        # generated: typed httpx client (do not edit)
    models/models.py               # generated: shared Pydantic models (do not edit)
```

## Prerequisites

- [uv](https://docs.astral.sh/uv/)
- Python >= 3.13 (pinned in `.python-version`)

```bash
uv sync            # create .venv and install runtime + dev dependencies
```

## The API (from `openapi.yaml`)

| Operation   | Method & path        | Notes                                  |
|-------------|----------------------|----------------------------------------|
| `healthCheck` | `GET /health`      | public liveness probe                  |
| `listBooks`   | `GET /books`        | query: `genre` (enum), `page` (int)    |
| `createBook`  | `POST /books`       | body `BookInput` -> `201` + `Book`     |
| `getBook`     | `GET /books/{id}`   | -> `200` `Book`, `404`, default        |
| `deleteBook`  | `DELETE /books/{id}` | -> `204`, `404`                       |

Authentication is declared as a global `Bearer` security scheme
(`components.securitySchemes.BearerAuth`); `/health` opts out with `security: []`.

## Regenerate the code

```bash
uv run bash scripts/generate.sh
# or individually:
uv run bash scripts/generate-client.sh
uv run bash scripts/generate-server.sh
```

The generators are declared in the `dev` dependency group of `pyproject.toml`, so
`uv sync` makes them available without a global install.

> The generated files under `src/generated/` are **committed** so the repo
> builds standalone. Treat them as output: edit `openapi.yaml`, then regenerate.

## Run the server

```bash
uv run python -m src
# then:
curl -s localhost:8000/health
open  http://localhost:8000/docs   # interactive Swagger UI
```

The routes in `app.py` are **stubs** — each raises `NotImplementedError` except
`/health`. That is the scaffolding OpenAPI gives you: correct paths, params,
request/response models, and status codes, with bodies left for you to fill in.

## Design notes

- **Two living generators, not one.** The canonical FastAPI route generator
  (`fastapi-codegen`) is no longer published on PyPI, so this project splits the
  concern: `openapi-python-client` for the client, and `datamodel-code-generator`
  for the shared server models. FastAPI's decorators are hand-authored in
  `app.py` and import the generated models, so request/response shapes never drift
  from the contract.
- **OpenAPI 3.1.** `BookInput` is modeled as a flat "omit `id`" schema rather than
  a JSON-Schema `allOf` + `id: null`, because the client generator does not yet
  merge `null` into a typed field. The intent (a create payload without a client
  `id`) is the same.

## License

MIT
