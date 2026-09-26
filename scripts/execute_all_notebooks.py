import os
import glob
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

notebooks = sorted(glob.glob("work/notebooks/*.ipynb"))
print(f"Found {len(notebooks)} notebooks to execute.")

ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

for nb_path in notebooks:
    print(f"\nExecuting {nb_path}...")
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
    
    try:
        # Change working directory context relative to notebook path
        cwd = os.path.dirname(os.path.abspath(nb_path))
        ep.preprocess(nb, {'metadata': {'path': cwd}})
        print(f"✓ Successfully executed {nb_path}")
    except Exception as e:
        print(f"× Error executing {nb_path}: {e}")
    
    with open(nb_path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)

print("\n=== ALL NOTEBOOKS EXECUTED AND SAVED ===")
