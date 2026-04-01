import os
import subprocess
import shutil
import time
import sys
import re
import signal
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- FIX ENCODING ON WINDOWS ---
encoding = getattr(sys.stdout, "encoding", None)
# pylint: disable=no-member
if encoding is None or not hasattr(encoding, "lower") or encoding.lower() != "utf-8":
    # pylint: enable=no-member
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # pylint: disable=broad-exception-caught
        pass

# --- PATH CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GECO5_SCRIPT_PATH = os.path.join(BASE_DIR, "src_python", "generate_config.py")
GECO5_OUTPUT_DIR = os.path.join(BASE_DIR, "generated_output")
CONFIG_DIR = os.path.join(BASE_DIR, "generated_output")
GA18_SCRIPT_PATH = os.path.join(BASE_DIR, "src_python", "config_inject.py")
WEBAPP_BASE_DIR = os.path.join(BASE_DIR, "generated_output")
# Maximum number of builds to run in parallel. Adjust based on your CPU.
MAX_WORKERS = 4


# --- SIGNAL MANAGEMENT ---
CURRENT_SUBPROCESS = None

def signal_handler(sig, frame):
    """Gestisce l'interruzione (Ctrl+C) terminando in modo pulito i processi figli."""
    global CURRENT_SUBPROCESS
    print("\n\n[!] INTERRUPT DETECTED (SIGINT/Ctrl+C). Cleaning up...")
    
    if CURRENT_SUBPROCESS:
        try:
            print(f"  -> Terminating active subprocess (PID: {CURRENT_SUBPROCESS.pid})...")
            if sys.platform == "win32":
                # Forziamo la chiusura dell'albero dei processi su Windows
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(CURRENT_SUBPROCESS.pid)], capture_output=True)
            else:
                CURRENT_SUBPROCESS.terminate()
        except Exception:
            pass
            
    print("  -> Cleanup complete. Exiting orchestrator.")
    sys.exit(0)

# Registrazione immediata del segnale
signal.signal(signal.SIGINT, signal_handler)


def clean_workspace(config_dir):
    """Removes stale config .py files to prepare for regeneration.
    Does NOT remove generated app folders to preserve concurrent/iterative builds."""
    print(f"\n--- [PHASE] Cleaning stale config files: {config_dir} ---")
    if os.path.isdir(config_dir):
        # Remove config_*.py and geco_*.py files only
        removed_files = 0
        for item in os.listdir(config_dir):
            item_path = os.path.join(config_dir, item)

            if os.path.isfile(item_path) and (
                item.endswith(".py")
                and (item.startswith("config_") or item.startswith("geco_"))
            ):
                try:
                    os.remove(item_path)
                    removed_files += 1
                except Exception:
                    pass

        # Remove specific __pycache__ folders
        pycache = os.path.join(config_dir, "__pycache__")
        if os.path.exists(pycache):
            try:
                shutil.rmtree(pycache)
            except Exception:
                pass

        print(
            f"  -> Cleanup completed: {removed_files} stale config files removed."
        )


def run_script(script_path, script_name, error_log):
    """Executes a Python script, captures output and logs any errors."""
    print(f"\n--- [PHASE] Starting script: {script_name} ---")
    if not os.path.exists(script_path):
        error_message = f"Script '{script_name}' not found at path: {script_path}"
        print(f"CRITICAL ERROR: {error_message}")
        error_log.append(f"SCRIPT EXECUTION ERROR: {error_message}")
        return False

    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=os.environ,
            check=False,  # We manually handle returncode below
        )

        # Always print stdout (contains execution logs)
        if result.stdout:
            print(result.stdout)

        if result.returncode != 0:
            # If stderr is empty, the real Python error is at the end of stdout
            errore_reale = result.stderr if result.stderr else result.stdout
            print(
                f"\n[!] CRITICAL STOP: {script_name} failed (exit code {result.returncode})."
            )
            print(f"--- ERROR DETAIL ---\n{errore_reale}\n------------------------")
            error_log.append(f"SCRIPT EXECUTION ERROR ({script_name}):\n{errore_reale}")
            print(f"❌ Pipeline aborted due to errors in '{script_name}'.")
            return False

        print(f"--- Script {script_name} completed successfully. ---")
        return True
    except Exception as e:  # pylint: disable=broad-exception-caught
        error_message = f"Unexpected exception during execution of '{script_name}': {e}"
        print(f"CRITICAL ERROR: {error_message}")
        error_log.append(error_message)
        return False


def run_script_with_args(args, script_name, error_log):
    """Sostituisce run_script permettendo il passaggio di argomenti CLI e gestione segnali."""
    print(f"\n--- [PHASE] Starting script: {script_name} ---")
    global CURRENT_SUBPROCESS
    try:
        process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=os.environ,
            bufsize=1
        )
        CURRENT_SUBPROCESS = process
        stdout_acc = []
        for line in process.stdout:
            print(line, end='', flush=True)
            stdout_acc.append(line)

        process.wait()
        full_stdout = "".join(stdout_acc)

        if process.returncode != 0:
            print(f"\n[!] CRITICAL STOP: {script_name} failed (exit code {process.returncode}).")
            error_log.append(f"SCRIPT EXECUTION ERROR ({script_name}):\n{full_stdout}")
            return False, full_stdout

        print(f"--- Script {script_name} completed successfully. ---")
        return True, full_stdout
    except Exception as e:
        error_log.append(f"EXCEPTION in {script_name}: {e}")
        return False, str(e)


def copy_new_files(source_dir, dest_dir, error_log):
    """Copies only new files from source to destination."""
    print("\n--- [PHASE] Starting copy of new configuration files ---")
    if not os.path.isdir(source_dir):
        msg = f"Source folder '{source_dir}' does not exist. Skipping copy."
        print(f"ERROR: {msg}")
        error_log.append(f"FILE COPY ERROR: {msg}")
        return
    os.makedirs(dest_dir, exist_ok=True)

    copied_count, skipped_count = 0, 0
    for filename in os.listdir(source_dir):
        source_file = os.path.join(source_dir, filename)
        dest_file = os.path.join(dest_dir, filename)
        if os.path.isfile(source_file) and not os.path.exists(dest_file):
            try:
                shutil.copy2(source_file, dest_file)
                copied_count += 1
            except Exception as e:  # pylint: disable=broad-exception-caught
                msg = f"Unable to copy file '{filename}'. Details: {e}"
                print(f"  -> ERROR: {msg}")
                error_log.append(f"FILE COPY ERROR: {msg}")
        else:
            skipped_count += 1
    print(
        f"--- Copy completed: {copied_count} new files copied, {skipped_count} skipped. ---"
    )


def kill_exe_locks():
    """Kill node.exe processes that may hold file locks in the dist/ folder,
    preventing EPERM errors when pkg tries to overwrite the .exe."""
    if sys.platform == "win32":
        try:
            subprocess.run(
                ["taskkill", "/F", "/IM", "node.exe", "/T"],
                capture_output=True,
                shell=True,
                check=False,
            )
            print("  -> Zombie Killer: node.exe processes terminated before build.")
        except OSError:
            pass
    # Small delay to ensure OS releases file handles
    time.sleep(1)


def run_build_task(folder_path):
    """Executes 'npm install' and multi-platform binary build via 'npx pkg'."""
    folder_name = os.path.basename(folder_path)
    os_target = os.environ.get("OS_TARGET", "Windows (.exe) - Default")

    # 1. Target definition (pkg string comma-separated)
    pkg_targets = "node18-win-x64"  # Default fallback
    if "Linux" in os_target:
        pkg_targets = "node18-linux-x64"
    elif "macOS" in os_target:
        pkg_targets = "node18-macos-x64"
    elif "Tutti" in os_target:
        pkg_targets = "node18-win-x64,node18-linux-x64,node18-macos-x64"

    # 2. Run 'npm install'
    try:
        subprocess.run(
            ["npm", "install"],
            cwd=folder_path,
            check=True,
            shell=True,
            capture_output=True,
            text=True,
            errors="replace",
        )
    except subprocess.CalledProcessError as e:
        # VISIBILITY: We report full logs if npm install fails
        return (
            folder_name,
            f"'npm install' failed:\n[STDOUT]:\n{e.stdout}\n[STDERR]:\n{e.stderr}",
        )

    # 3. Run Cross-Platform Compilation via DIRECT invocation of pkg
    # Avoid 'npx' which on Windows often has path resolution issues (e.g. spaces or x86)
    try:
        # FIX EPERM: Kill zombie node.exe processes before pkg tries to write .exe
        kill_exe_locks()

        dist_dir = os.path.join(folder_path, "dist")
        os.makedirs(dist_dir, exist_ok=True)

        # Direct path to locally installed pkg binary
        pkg_bin_path = os.path.join(
            folder_path, "node_modules", "pkg", "lib-es5", "bin.js"
        )

        if not os.path.exists(pkg_bin_path):
            return (
                folder_name,
                f"Error: pkg binary not found at {pkg_bin_path}. Verify npm install.",
            )

        subprocess.run(
            [
                "node",
                pkg_bin_path,
                ".",
                "--targets",
                pkg_targets,
                "--out-path",
                "dist/",
                "--no-bytecode",
                "--public",
            ],
            cwd=folder_path,
            check=True,
            shell=True,
            capture_output=True,
            text=True,
            errors="replace",
        )
    except subprocess.CalledProcessError as e:
        full_error = f"Multi-platform 'pkg' compilation failed:\n[STDOUT]:\n{e.stdout}\n[STDERR]:\n{e.stderr}"
        return folder_name, full_error

    return folder_name, "Success"


def build_executables_sequential(base_dir, error_log, target_folder=None):
    """Executes build for each valid subfolder sequentially to avoid npm concurrency issues."""
    if not os.path.isdir(base_dir):
        msg = f"Base directory '{base_dir}' does not exist."
        print(f"ERROR: {msg}")
        error_log.append(f"BUILD ERROR: {msg}")
        return

    # Filter only folders that are valid Node.js projects
    if target_folder:
        # If target_folder is just a name, make it absolute
        if not os.path.isabs(target_folder):
            target_path = os.path.join(base_dir, target_folder)
        else:
            target_path = target_folder
        
        if os.path.exists(os.path.join(target_path, "package.json")):
            app_folders = [target_path]
            print(f"  -> Targeting specific build folder: {os.path.basename(target_path)}")
        else:
            print(f"  -> WARNING: Target folder {target_folder} does not contain package.json. Falling back to scan.")
            app_folders = [
                f.path
                for f in os.scandir(base_dir)
                if f.is_dir() and os.path.exists(os.path.join(f.path, "package.json"))
            ]
    else:
        app_folders = [
            f.path
            for f in os.scandir(base_dir)
            if f.is_dir() and os.path.exists(os.path.join(f.path, "package.json"))
        ]

    invalid_folders = [
        f.name
        for f in os.scandir(base_dir)
        if f.is_dir() and not os.path.exists(os.path.join(f.path, "package.json"))
    ]

    if invalid_folders:
        print(
            f"INFO: The following folders will be skipped because they don't contain 'package.json': {', '.join(invalid_folders)}"
        )

    if not app_folders:
        print("INFO: No valid projects found to build.")
        return

    print(f"--- [PHASE] Starting sequential build process for {len(app_folders)} apps ---")
    results = []

    for index, folder in enumerate(app_folders):
        print(f"\n[{index + 1}/{len(app_folders)}] Building '{os.path.basename(folder)}'...")
        try:
            print("  -> Running 'npm install'...")
            install_process = subprocess.run(
                ["npm", "install", "--no-audit", "--no-fund"], 
                cwd=folder, 
                shell=True,
                capture_output=True, 
                text=True
            )
            
            if install_process.returncode != 0:
                print(f"  -> ❌ FAILED at 'npm install'.\nLog:\n{install_process.stderr}")
                results.append((folder, False))
                error_log.append(f"NPM INSTALL ERROR ({os.path.basename(folder)}):\n{install_process.stderr}")
                continue
                
            print("  -> Running build command (pkg)...")
            # Replacement: pkg command logic from original run_build_task
            folder_name = os.path.basename(folder)
            os_target = os.environ.get("OS_TARGET", "Windows (.exe) - Default")
            pkg_targets = "node18-win-x64"
            if "Linux" in os_target: pkg_targets = "node18-linux-x64"
            elif "macOS" in os_target: pkg_targets = "node18-macos-x64"
            elif "Tutti" in os_target: pkg_targets = "node18-win-x64,node18-linux-x64,node18-macos-x64"
            
            kill_exe_locks()
            dist_dir = os.path.join(folder, "dist")
            os.makedirs(dist_dir, exist_ok=True)
            pkg_bin_path = os.path.join(folder, "node_modules", "pkg", "lib-es5", "bin.js")
            
            if not os.path.exists(pkg_bin_path):
                print(f"  -> ❌ ERROR: pkg binary not found.")
                results.append((folder, False))
                error_log.append(f"BUILD ERROR ({folder_name}): pkg binary not found")
                continue

            build_process = subprocess.run(
                [
                    "node",
                    pkg_bin_path,
                    ".",
                    "--targets",
                    pkg_targets,
                    "--out-path",
                    "dist/",
                    "--no-bytecode",
                    "--public",
                ],
                cwd=folder,
                shell=True,
                capture_output=True,
                text=True,
                errors="replace"
            )
            
            if build_process.returncode != 0:
                print(f"  -> ❌ FAILED at build.\nLog:\n{build_process.stderr}")
                results.append((folder, False))
                error_log.append(f"BUILD ERROR ({folder_name}):\n{build_process.stderr}")
            else:
                print("  -> ✅ Completed successfully.")
                results.append((folder, True))
                
        except Exception as e:
            print(f"  -> ❌ ERROR: {str(e)}")
            results.append((folder, False))
            error_log.append(f"UNEXPECTED ERROR ({os.path.basename(folder)}): {str(e)}")

    successes = sum(1 for r in results if r[1])
    print(f"\n--- Build process completed. Successful builds: {successes}/{len(app_folders)} ---")


def clean_generated_configs(config_dir):
    """Removes generated .py files from output folder to allow a clean retry."""
    removed = 0
    if os.path.isdir(config_dir):
        for f in os.listdir(config_dir):
            if f.endswith(".py") and f.startswith("config_"):
                try:
                    os.remove(os.path.join(config_dir, f))
                    removed += 1
                except Exception:  # pylint: disable=broad-exception-caught
                    pass
    print(f"  -> Output folder cleanup: {removed} files removed for retry.")


def verify_build_artifacts(base_dir, error_log):
    """Verifies existence of executables in dist/ subfolders and logs paths."""
    print("\n--- [PHASE] Verifying build artifacts ---")
    found_any = False
    if not os.path.isdir(base_dir):
        return
    for entry in os.scandir(base_dir):
        if not entry.is_dir():
            continue
        dist_dir = os.path.join(entry.path, "dist")
        if not os.path.isdir(dist_dir):
            continue
        executables = [
            f for f in os.listdir(dist_dir) if os.path.isfile(os.path.join(dist_dir, f))
        ]
        if executables:
            found_any = True
            for exe in executables:
                full_path = os.path.join(dist_dir, exe)
                print(f"  ✅ Artifact ready: {full_path}")
        else:
            msg = f"No executables found in '{dist_dir}'."
            print(f"  ⚠️  {msg}")
            error_log.append(f"INCOMPLETE BUILD: {msg}")
    if not found_any:
        print("  ⚠️  No artifacts found in any dist/ folder.")


if __name__ == "__main__":
    start_time = time.time()
    error_summary = []

    print("=" * 60)
    print("========= BUILD ORCHESTRATOR STARTED (v2.2) =========")
    print(f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # --- PHASE 0: WORKSPACE CLEANUP ---
    # FIX: Config files are no longer deleted to preserve debugging and scalability.
    # clean_workspace(GECO5_OUTPUT_DIR)

    # --- SELF-HEALING LOOP: max 3 attempts for geco ---
    GECO_MAX_RETRIES = 3
    geco_ok = False
    for attempt in range(1, GECO_MAX_RETRIES + 1):
        print(f"\n[GECO] Attempt {attempt}/{GECO_MAX_RETRIES}...")
        
        # --- [PHASE] Running configuration generation ---
        process_config = subprocess.Popen(
            [sys.executable, "-u", GECO5_SCRIPT_PATH],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        CURRENT_SUBPROCESS = process_config
        output_config_file = None
        for line in process_config.stdout:
            print(line, end='', flush=True)
            # Catch the generated filename: "Saved to: '...'"
            if "Saved to:" in line:
                match = re.search(r"'(.*?)'", line)
                if match:
                    output_config_file = match.group(1)

        process_config.wait()

        if process_config.returncode == 0:
            geco_ok = True
            break
        else:
            print(f"❌ ERROR: Configuration generation failed (Attempt {attempt}).")
            if attempt < GECO_MAX_RETRIES:
                print("[GECO] Retrying generation...")
            else:
                error_summary.append(
                    f"PROCESS ABORTED: generate_config.py failed after {GECO_MAX_RETRIES} attempts."
                )

    if geco_ok:
        # We find the specific app folder created by looking at the config in output_config_file
        # or by looking at the most recent folder in generated_output.
        # But wait, config_inject.py knows what it's doing.
        
        inject_args = [sys.executable, GA18_SCRIPT_PATH]
        if output_config_file:
            inject_args.extend(["--file", output_config_file])
            print(f"  -> Atomic Injection: {os.path.basename(output_config_file)}")

        success, inject_stdout = run_script_with_args(inject_args, "config_inject.py", error_summary)
        if success:
            # Extract target app name/folder from config_inject's output
            # Look for: "Files are located in folder: '...'"
            target_build_folder = None
            if inject_stdout:
                folder_match = re.search(r"Files are located in folder: '(.*?)'", inject_stdout)
                if folder_match:
                    target_build_folder = folder_match.group(1).strip()
                    print(f"  -> Targeted Build Folder Identified: {os.path.basename(target_build_folder)}")

            build_executables_sequential(WEBAPP_BASE_DIR, error_summary, target_folder=target_build_folder)
            verify_build_artifacts(WEBAPP_BASE_DIR, error_summary)
        else:
            print("\nconfig_inject.py execution failed. Build process will not be started.")
            error_summary.append(
                "PROCESS ABORTED: config_inject.py failed, cannot proceed with build."
            )
    else:
        print(
            "\nCRITICAL ERROR: generate_config.py execution failed after all attempts. Process aborted."
        )

    end_time = time.time()
    minutes, seconds = divmod(end_time - start_time, 60)

    print("\n\n" + "=" * 60)
    print("============ BUILD PROCESS COMPLETED ============")
    print("=" * 60)

    if not error_summary:
        print("\n✅ 🎉 Process completed with no recorded errors.")
    else:
        print(
            f"\n❌ WARNING: {len(error_summary)} errors were encountered during the process."
        )
        print("-" * 60)
        print("---------------- ERROR SUMMARY ----------------")
        for i, error in enumerate(error_summary, 1):
            print(f"\n--- ERROR #{i} ---\n{error}")
        print("\n" + "-" * 60)

    print(f"\nTotal execution time: {int(minutes)} minutes and {seconds:.2f} seconds.")
    print("=" * 60)

    if error_summary:
        sys.exit(1)
    else:
        sys.exit(0)
