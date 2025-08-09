# Packaging and Distributing the `obk` CLI for ChatGPT 5 with Vendored Dependencies

This article explains how to create a **self-contained release zip** of the `obk` CLI that works specifically in **ChatGPT 5's execution environment**. Many LLMs cannot handle `.zip` archives or `.whl` wheels for offline installation, but ChatGPT 5 supports working with these formats when they are uploaded. This workflow ensures you can provide a fully packaged CLI, ready for execution without internet access.

The release zip will include:

* Your built package (`.whl` and `.tar.gz`)
* All **runtime dependency wheels** (direct and transitive)
* All tracked source files, including `prompts/`
* A reproducible, `.gitignore`-aware source archive

⚠ **Platform-Specific Wheel Note:** ChatGPT’s runtime is **Linux x86\_64 (manylinux)** with **Python 3.11**. If you build on Windows, wheels for compiled packages (like `dependency-injector`) may be Windows-only (`win_amd64`) and **will not install** in ChatGPT. To avoid this, configure your `build-and-vendor.ps1` to also download manylinux wheels with:

```powershell
-IncludeLinuxWheels
```

This ensures your `dist/` folder works both locally and in ChatGPT.

The workflow is built around **three scripts** in `scripts/` for both **PowerShell** and **Bash** environments.

---

## 1. Build & Vendor Dependencies

### PowerShell: `build-and-vendor.ps1`

Creates a clean build environment, builds the `obk` package, and downloads all runtime dependency wheels into the `dist/` folder. With `-IncludeLinuxWheels`, also fetches Linux-compatible wheels for ChatGPT.

**Usage:**

```powershell
./scripts/build-and-vendor.ps1 -IncludeLinuxWheels
```

### Bash: `build-and-vendor.sh`

Same logic for macOS/Linux.

**Usage:**

```bash
./scripts/build-and-vendor.sh --include-linux-wheels
```

---

## 2. Create a Clean Git Archive

### PowerShell: `make-zip.ps1`

Creates a `.gitignore`-aware zip and adds the `dist/` directory.

```powershell
./scripts/make-zip.ps1
```

### Bash: `make-zip.sh`

Same logic for macOS/Linux.

```bash
./scripts/make-zip.sh
```

---

## 3. One-Click Build + Zip

### PowerShell: `package.ps1`

Runs both build/vendor and zip steps. Recommended to pass `-IncludeLinuxWheels` for ChatGPT.

```powershell
./scripts/package.ps1 -IncludeLinuxWheels
```

### Bash: `package.sh`

Same logic for macOS/Linux.

```bash
./scripts/package.sh --include-linux-wheels
```

---

## Why This Works in ChatGPT 5

ChatGPT 5 supports:

* Uploading `.zip` archives
* Unpacking and reading vendored `.whl` files
* Installing from `--no-index` local wheels

This approach ensures the CLI can be tested entirely offline inside ChatGPT 5, with no dependency on PyPI or external downloads.

Offline install after unzipping:

```bash
pip install --no-index --find-links <unzipped-folder>/dist obk
```

Perfect for restricted environments and reproducible ChatGPT 5 tests.
