# Shenvy

**Shenvy** is a lightweight shim manager for dockerized tools (PHP, Composer, Python, etc).  
It allows you to run different tool versions in isolated Docker containers while keeping your environment clean.

---

## Features

- Automatic generation of shims for various tools and versions.
- Dockerized environments, so no need to install multiple versions on the host.
- Easy integration with Zsh (`eval "$(shenvy init zsh)"`).
- Self-contained; works with a dedicated Python venv.
- Per-directory configuration.

---

## Requirements

- Python 3.10+
- Docker
- Git

Optional but recommended: [`virtualenv`](https://virtualenv.pypa.io/) to isolate Shenvy installation.

---

## Available tools
- PHP: 7.4, 8.0, 8.1, 8.2, 8.3, 8.4, 8.5-rc with Composer and Symfony CLI.

_(Customize `TOOLS` in `shenvy/shims.py` to add more tools. You can also add `shenvy/tools/<tool>` to the `Dockerfile` to add custom versions.)_

---
## Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/shenvy.git
cd shenvy

```

### 2. Create a dedicated virtual environment

```
python -m venv ~/.shenvy/venv
source ~/.shenvy/venv/bin/activate
```

### 3. Install dependencies

```
pip install --upgrade pip
pip install -e .
```

> This installs shenvy in **editable mode**, so any changes you make in the repo are immediately available.

### 4. Shell integration

#### Zsh

Add the following line to your `.zshrc` file:

```
# shenvy
export SHENVY_HOME:"$HOME/.shenvy"
eval "$($SHENVY_HOME/venv/bin/python -m shenvy.cli init zsh)"
# shenvy end
```

And reload your shell:

```
source ~/.zshrc
```

### 5. Per-directory configuration

You can create a `.shenvy/init.zsh` file in your CWD to customize and extend shenvy.

For example, let's say you're building a project on top of [dunglas/symfony-docker](https://github.com/dunglas/symfony-docker):

```
# .shenvy/init.zsh

echo "Aliasing 'php'..."
alias php='docker compose exec php php -d memory_limit=512M "$@"'

echo "Aliasing 'composer'..."
alias composer='docker compose exec php composer "$@"'

echo "Aliasing command: 'asset-build'..."
alias asset-build='clear; php bin/console cache:clear && composer asset:build && pnpm dev'

echo "Aliasing command: 'diff-and-migrate'"
alias diff-and-migrate='clear; php bin/console doctrine:migrations:diff && php bin/console doctrine:migrations:migrate -n'

echo "Aliasing command: 'load-fixtures'"
alias load-fixtures='clear; php bin/console doctrine:fixtures:load -n'

```

---

## Usage

### Generate shims

```
shenvy generate
```
This will generate shim scripts in `~/.shenvy/bin/` for all configured tools and versions.

