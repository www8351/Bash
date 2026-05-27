# Docker labs → production tooling

Started as 5-year-old interactive bash Docker labs. Now a CI/CD-ready toolkit
with separated concerns: declarative infra, a typed CLI, and a task runner.

## Layout

| Path | Purpose |
|------|---------|
| `compose/docker-compose.yml` | Declarative stack: nginx, httpd, portainer, counter. Replaces the old `docker run` menus. |
| `compose/.env.example` | Ports and image tags. Copy to `compose/.env`. |
| `images/counter/` | Custom image (`Dockerfile` + `counter.sh`), built by compose. |
| `web/index.html` | Static page mounted read-only into nginx. |
| `cli/` | `dockerctl` — non-interactive Python (Typer) CLI for dynamic image/container ops. |
| `Taskfile.yml` | Engineering entrypoint over compose + CLI. |
| `.github/workflows/ci.yml` | Lints compose, Dockerfile, shell, and Python on every push. |

## Quick start

```bash
cp compose/.env.example compose/.env
task up        # start the stack          (or: docker compose -f compose/docker-compose.yml up -d)
task lint      # run all linters
task down      # stop and remove
```

## dockerctl CLI

Non-interactive — flags only, meaningful exit codes, safe to call from CI.

```bash
pip install -e cli
dockerctl images pull nginx:latest
dockerctl containers ls --all
dockerctl containers deploy nginx:latest --name web --port 8080:80
dockerctl containers rm web --force
```

## Design

- **docker-compose** owns container lifecycle and state — not shell scripts.
- **Python (Typer)** owns dynamic logic and error handling.
- **Taskfile** is the single entrypoint wrapping both.
- **CI** runs everything unattended; nothing prompts.
