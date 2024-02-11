# SyllabusScribe v1.0.0-rc.1

## Introduction

Welcome to SyllabusScribe, the comprehensive educational platform designed to simplify content creation for lesson instructors across a diverse range of education topics! Whether you're a teacher or professor, SyllabusScribe offers an extensive suite of tools to cater to the needs of educators at every grade level.

## Naming Conventions and Guidelines:

- **ClassNames** = PascalCase
- **AppNames** = PascalCase
- **directories** = snake_case
- **file_names** = snake_case
- **variable_names** = snake_case
- **function_names** = snake_case
- **db_name & db_tables** = snake_case
- **CONSTANTS** = SCREAMING_SNAKE_CASE
- **url-patterns** = kebab-case

## Installation Instructions:

1. **Create a New Python environment and Activate it (optional but recommended):**

   **Windows:**

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   **Linux/MacOS:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   ### Windows Setup for GPU Acceleration (Optional):

   If you wish to leverage GPU acceleration for improved performance in llama-cpp-python, ensure that your environment is configured as follows before proceeding with Step 2. Although the primary execution occurs on the CPU, this setup enables the option to offload computations to the GPU for faster processing.

   - **Install Visual Studio Community Edition (Free) or Any Other Version:**<br>
     [Download Visual Studio](https://visualstudio.microsoft.com/downloads/) from the official Visual Studio website.<br>
     During installation, make sure to select the "Desktop development with C++" workload.<br>

   - **Download and Install the CUDA Toolkit:**<br>
     [Download the CUDA Toolkit](https://developer.nvidia.com/cuda-downloads) from the official NVIDIA website and follow the installation instructions.<br>

   - **Download and Install CMake**:<br>
     [Download CMake](https://cmake.org/download/) from the official CMake website and follow the installation instructions.<br>

   - Open a PowerShell terminal.

   - Set the `CMAKE_ARGS` environment variable to include the `-DLLAMA_CUBLAS=on` flag:

     ```powershell
     $env:CMAKE_ARGS = "-DLLAMA_CUBLAS=on"
     ```

   - Set the `FORCE_CMAKE` environment variable to 1:

     ```powershell
     $env:FORCE_CMAKE=1
     ```

   - Set the `CUDAToolkit_ROOT` environment variable to the path where CUDA Toolkit is installed. Replace `'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.2'` with the actual path on your system:

     ```powershell
     $env:CUDAToolkit_ROOT = 'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.2'
     ```

2. **Download dependencies:**

   ```powershell
   pip install -r requirements.txt
   ```

3. **Setup the database:**<br>
   We're currently using a mysql database, make sure to configure your own database within the _settings.py_ file and then migrating.<br>
   (**WARNING**: you might need to delete all migration files before migrating to your new database)

4. **Setup environment variables:**<br>
   Create a '.env' file in the base directory of the project containing the following fields:

   - `DB_USER`: Your database username.
   - `DB_PASSWORD`: Your database password.
   - `SECRET_KEY`: A secret key for your application. Ensure this key is kept secure and not shared publicly.

5. **Setup log file:**<br>
   Create the 'SyllabusScribe.log' file within the /logs directory

6. **You're good to go!**

## Additional Information:

- **.python-version file**: This file helps manage the Python version for your project using pyenv. It specifies which Python version
  should be used when working on the project. (3.11.5)
- **requirements.txt file**: This file lists all the Python packages and their versions needed to run your project.
- **.gitignore file**: This file tells Git which files or directories to ignore when tracking changes in your project. It's handy
  for excluding stuff you don't want in your repository, like generated files, sensitive data, or temporary files.
