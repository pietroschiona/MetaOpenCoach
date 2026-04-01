# Usage: Getting Started with MetaOpenCoach

MetaOpenCoach provides an automated environment for elite professionals to build and deploy their proprietary software.

## TL;DR

Setup is minimal: ensure you have Python and Node.js installed, clone the repository, install dependencies, and run the Python GUI to begin the generation process.

## Prerequisites

- **Python 3.10+**: Required for the orchestrator and build scripts.
- **Node.js 18+**: Required during the build phase (not required for the final `.exe`).

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/MetaOpenCoach/MetaOpenCoach.git
   cd MetaOpenCoach
   ```
2. **Quick Start (One-Click)**:
   The easiest way is to use the double-clickable scripts:

   - **Windows**: [start_here_windows.bat](file:///c:/Users/pietr/Desktop/github/metaopencoach/start_here_windows.bat)
   - **Linux**: [start_here_linux.sh](file:///c:/Users/pietr/Desktop/github/metaopencoach/start_here_linux.sh)
   - **macOS**: [start_here_macos.command](file:///c:/Users/pietr/Desktop/github/metaopencoach/start_here_macos.command)
3. **Manual Setup**:
   (Only if you don't use the scripts above)

   ```bash
   pip install -r requirements.txt
   ```

## The Generation Workflow

### 1. Launch the Builder Interface

MetaOpenCoach includes a specialized GUI for managing the injection process:

```bash
python src_python/app_builder_ui.py
```

From this interface, you can upload your methodology files, configure your AI provider (**LM Studio/Ollama** are recommended for total privacy), and customize your app's identity.

> [!TIP]
> **LM Studio** is the suggested local provider as it offers high performance with models like `qwen3.5-2b` by default.

### 2. Run the Orchestrator

Once configured, the orchestrator handles the heavy lifting of distillation and injection:

```bash
python src_python/orchestrator.py
```

### 3. Access Your Application

After a successful build, your standalone application will be located in the `generated_output/` folder. Simply run the `.exe` (or the `npm start` equivalent for dev) to launch your coaching environment.

## Advanced: Demo Mode

To experience the full capabilities without manually adding data, use the integrated Mock Data Generators in the `tools` folder:

```bash
python tools/generator-mock-escalada-fr.py
```

This script populates your application with 30 "Digital Twin" users, 15,000 tokens of historical chat per profile, and simulated risk scenarios to test the dashboard and analytics.

---

← [Back: Documentation Index](./Documentation_Index.md) | [Next: Technical Structure →](./structure.md)
