import subprocess
import sys
from pathlib import Path

import typer

from shenvy.shims import generate_shims

app = typer.Typer()


@app.command()
def generate():
    """Generate all shims"""
    generate_shims()


@app.command()
def check():
    """Check environment sanity."""

    @app.command()
    def check():
        """Check Shenvy environment sanity."""
        errors = []

        shenvy_home = Path.home() / ".shenvy"
        bin_path = shenvy_home / "bin"

        # 1. SHENVY_HOME exists
        if not shenvy_home.exists():
            errors.append(f"❌ $SHENVY_HOME not found at {shenvy_home}")
        else:
            typer.echo(f"✅ $SHENVY_HOME exists at {shenvy_home}")

        # 2. bin in PATH
        if str(bin_path) not in sys.path and str(bin_path) not in (p.strip() for p in sys.path):
            typer.echo(f"⚠️ {bin_path} might not be in PATH")
        else:
            typer.echo(f"✅ {bin_path} is in PATH")

        # 3. Docker available
        try:
            subprocess.run(["docker", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            typer.echo("✅ Docker is installed")
        except Exception:
            errors.append("❌ Docker not found or not working")

        # TODO: docker image availability checks.

        # final
        if errors:
            typer.echo("\nSome checks failed:", err=True)
            for e in errors:
                typer.echo(f"  - {e}", err=True)
            raise typer.Exit(code=1)
        else:
            typer.echo("\nAll checks passed! 🎉")


@app.command()
def init(shell: str = typer.Argument(..., help="Shell to initialize, e.g. zsh")):
    """Generate shell init code."""
    shenvy_home = Path.home() / ".shenvy"
    bin_path = shenvy_home / "bin"

    if shell == "zsh":
        print(f"""\
if [[ -f "$SHENVY_HOME/venv/bin/activate" ]]; then
    source "$SHENVY_HOME/venv/bin/activate"
    echo "✅ Activated shenvy venv"
else
    echo "Cannot activate shenvy venv: $SHENVY_HOME/venv/bin/activate not found"
fi

# shenvy init for zsh
if [[ ":$PATH:" != *":{shenvy_home}/bin:"* ]]; then
    export PATH="{shenvy_home}/bin:$PATH"
    echo "✅ Added shenvy to path!"
fi

if [[ -f "$PWD/.shenvy/init.zsh" ]]; then
    if [[ $PWD != $HOME ]]; then
        source "$PWD/.shenvy/init.zsh"
        echo "✅ Sourced: $PWD/.shenvy/init.zsh"
    fi
fi
""")
    else:
        typer.echo(f"Shell {shell} not supported", err=True)


if __name__ == "__main__":
    app()
