# ⚠️ Note on Installing Pipenv in Ubuntu 22.04+ or Debian 12+

Ubuntu-based systems (since 22.04) implement [PEP 668](https://peps.python.org/pep-0668/), which prevents direct use of `pip install` on the system-wide Python environment to protect system integrity.

If you try:

```bash
pip install pipenv
````

You may encounter this error:

```
error: externally-managed-environment
```

### ✅ Recommended Solution

Instead, install Pipenv using Ubuntu’s package manager:

```bash
sudo apt install pipenv
```

This avoids the restriction and installs Pipenv system-wide as a CLI tool.

> Alternatively, you can install Pipenv safely using `pipx` or from within a virtual environment:

```bash
# Using pipx (preferred for CLI tools)
sudo apt install pipx
pipx install pipenv

# Or using venv (manually):
python3 -m venv .venv
source .venv/bin/activate
pip install pipenv
```

This ensures Pipenv works correctly without conflicting with Ubuntu’s system-managed Python environment.


# 🐳 Docker Consideration: Installing Pipenv

On Ubuntu or Debian systems, it's common to install Pipenv using:

```bash
sudo apt install pipenv
```

This works well on your local machine, especially when avoiding Python’s system-managed environment restrictions (PEP 668).

However, in Docker (especially with slim images like `python:3.9.7-slim`), using `apt` or `sudo` is **not recommended**, because:

* The base image doesn't include `apt` or `sudo` by default.
* It increases image size and build time.
* It goes against the lightweight design of slim images.

### ✅ Best practice in Docker

Install Pipenv using `pip` with an environment override:

```dockerfile
ENV PIP_BREAK_SYSTEM_PACKAGES=1
RUN pip install pipenv
```

This keeps the image lean, fast, and functional while bypassing system restrictions safely inside the container.