# Run the notebooks on your computer

Local setup is optional. [Binder](binder_instructions.md) and [Colab](colab_instructions.md) remain available if installation is difficult. Ask your instructor before installing software on a managed computer.

## 1. Get Python and the course files

Install **Python 3.11** from [python.org](https://www.python.org/downloads/), or use an instructor-supported installation. Download this repository using **Code → Download ZIP** on [GitHub](https://github.com/ntious/python_foundation), then extract it. Open a terminal in the extracted `python_foundation` folder (the folder containing `notebooks` and `.binder`). You do not need Git.

## 2. Create an isolated environment

On **Windows**, use PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .binder/requirements.txt
.\.venv\Scripts\python.exe -m jupyterlab
```

On **macOS or Linux**, use Terminal:

```sh
python3.11 -m venv .venv
.venv/bin/python -m pip install -r .binder/requirements.txt
.venv/bin/python -m jupyterlab
```

The first install needs an internet connection. Direct paths avoid activation-policy problems on Windows. If `py` or `python3.11` is not found, check the Python installation with your instructor. On Linux, the operating system may also require its Python venv package. Do not use `sudo pip` or install course tools into the system Python.

## 3. Start with notebook 00

JupyterLab should open in your browser. Open `notebooks/00_getting_started.ipynb`. Select the environment's Python kernel if asked. Run one cell at a time. Some cells deliberately contain errors: read the surrounding instructions, fix the example when asked, and continue. An `input()` prompt waits for your response.

Save your notebook with **Ctrl+S** (Windows/Linux) or **Cmd+S** (macOS). Files are saved on your computer. Keep an unedited original if your instructor asks you to submit a working copy. Shut down the kernel and stop the terminal server when finished.

For later sessions, open the same folder and run the last command above again. You do not need to reinstall each time. The Python examples use the standard library; website and maintainer-test dependencies are separate and are not student requirements.

See [troubleshooting](troubleshooting.md) for kernel, input, and lost-work help. Never share a Jupyter login token or expose the local server to a public network.
