# **How to Publish a Python Package to PyPI**

## **1. Prepare Your Project Structure**

Your project should look like this:

```
myproject/
├── pyproject.toml
├── README.md
├── LICENSE
├── myproject/
│   ├── __init__.py
│   └── ... (other modules)
└── tests/
    └── ... (optional)
```

* The **outer `myproject/`** is your repo root.
    
* The **inner `myproject/`** is your Python package (should be importable as `import myproject`).
    

* * *

## **2. Create `pyproject.toml`**

This file is now the _standard_ way to specify build system and metadata.

Example **pyproject.toml** for a pure Python package:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "myproject"
version = "0.1.0"
description = "Short description of your project."
readme = "README.md"
requires-python = ">=3.7"
license = { file = "LICENSE" }
authors = [
  { name="Your Name", email="your@email.com" }
]
dependencies = [
  # "requests >=2.0.0",
]

[project.urls]
Homepage = "https://github.com/yourusername/myproject"
Repository = "https://github.com/yourusername/myproject"

[tool.hatch.build.targets.wheel]
packages = ["myproject"]
```

* Replace `"myproject"` with your actual project name.
    
* Adjust the dependencies and metadata as needed.
    

* * *

## **3. Build Your Package**

First, **install build tools** (in a virtualenv is best):

```bash
python -m pip install --upgrade build
```

Then **build your package** (from your project root):

```bash
python -m build
```

This creates a `dist/` directory with `.tar.gz` and `.whl` files.

* * *

## **4. Register and Set Up PyPI Account**

* Go to [https://pypi.org/account/register/](https://pypi.org/account/register/)
    
* Verify your email.
    
* **(Optional but recommended)**: Enable two-factor authentication.
    

* * *

## **5. Upload to PyPI with Twine**

Install Twine:

```bash
python -m pip install --upgrade twine
```

Upload your package:

```bash
python -m twine upload dist/*
```

* Enter your PyPI username and password when prompted.
    

* * *

## **6. Verify Your Package**

* Go to `https://pypi.org/project/myproject/` (replace with your name).
    
* Try installing it:
    
    ```bash
    pip install myproject
    ```
    

* * *

## **7. Tips and Best Practices**

* **Choose a unique name!**  
    Check availability by visiting `https://pypi.org/project/<your-package-name>/`.
    
* **Use underscores in your import name**, but hyphens are fine for the PyPI package name.
    
* **Include a license** and a good README.md.
    
* **Use versioning** (`0.1.0`, `1.0.0`, etc.) and bump the version for every new release.
    
* **Test locally** before uploading.  
    You can test installation from the built `.whl`:
    
    ```bash
    pip install dist/myproject-0.1.0-py3-none-any.whl
    ```
    

* * *

## **8. Optional: Test Uploads to TestPyPI**

To avoid polluting the real PyPI while experimenting, use TestPyPI:

```bash
python -m twine upload --repository testpypi dist/*
```

Install from TestPyPI:

```bash
pip install --index-url https://test.pypi.org/simple/ myproject
```

* * *

## **9. Useful Resources**

* Packaging Python Projects — Official Guide
    
* [PyPI — Managing Projects](https://pypi.org/help/)
    
* Hatchling documentation
    