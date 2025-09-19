from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import os
import importlib.resources as pkg_resources
from packaging.version import Version

TOOLS = {
    "php": {
        "dockerfile": {
            "mod": "shenvy.tools.php"
        },
        "versions": ["7.4", "8.0", "8.1", "8.2", "8.3", "8.4", "8.5-rc"],
        "default": "8.4",
        "entrypoint": "php",
        "aliases": {
            "composer": "composer",
            "symfony": "symfony",
        }
    },
}

def get_template_env():
    with pkg_resources.path("shenvy.templates", "") as path:
        env = Environment(loader=FileSystemLoader(path))
        return env

def generate_shims():
    template = get_template_env().get_template('shim.sh.j2')

    bin_dir = Path(os.environ.get("SHENVY_HOME", Path.home() / ".shenvy")) / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)

    for tool, cfg in TOOLS.items():
        print(f"Generating shim for {tool}")

        for version in cfg["versions"]:
            print(f"Generating shim for {tool} {version}")
            with pkg_resources.path(cfg["dockerfile"]["mod"], "Dockerfile") as dockerfile_path:
                v = Version(version)
                normalized_version = f"{v.major}{v.minor}"
                script_name = f"{tool}{normalized_version}"
                output_path = bin_dir / script_name

                script = template.render(
                    tool=tool,
                    version=version,
                    dockerfile=dockerfile_path,
                    entrypoint=cfg["entrypoint"],
                )

                output_path.write_text(script)
                output_path.chmod(0o755)

                for alias in cfg["aliases"].keys():
                    print(f"Generating aliases for {alias} -- {tool} {version}")
                    alias_filename = f"{alias}{version.replace('.', '')}"
                    alias_path = bin_dir / alias_filename

                    shim = template.render(
                        tool=tool,
                        normalized_version=normalized_version,
                        version=version,
                        entrypoint=alias,
                        dockerfile=dockerfile_path,
                    )

                    alias_path.write_text(shim)
                    alias_path.chmod(0o755)

    print(f"✔ Generated shims in {bin_dir}")