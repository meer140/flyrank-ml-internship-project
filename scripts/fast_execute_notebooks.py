import os
import glob
import json
import sys
import io
import contextlib
import traceback

notebooks = sorted(glob.glob("work/notebooks/*.ipynb"))
print(f"Executing {len(notebooks)} notebooks via direct python execution context...")

for nb_path in notebooks:
    print(f"\nProcessing {nb_path}...")
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)
    
    # Global environment for notebook execution
    exec_globals = {
        "__name__": "__main__",
        "__file__": os.path.abspath(nb_path)
    }
    
    # Change working directory context to work/notebooks
    current_dir = os.getcwd()
    os.chdir(os.path.dirname(os.path.abspath(nb_path)))
    
    cell_errors = 0
    for idx, cell in enumerate(nb.get("cells", [])):
        if cell.get("cell_type") == "code":
            code = "".join(cell.get("source", []))
            if not code.strip():
                continue
            
            output_buf = io.StringIO()
            error_msg = None
            try:
                with contextlib.redirect_stdout(output_buf), contextlib.redirect_stderr(output_buf):
                    exec(code, exec_globals)
            except Exception as e:
                cell_errors += 1
                error_msg = traceback.format_exc()
                print(f"  × Error in cell {idx}: {e}")
            
            out_text = output_buf.getvalue()
            outputs = []
            if out_text:
                outputs.append({"name": "stdout", "output_type": "stream", "text": out_text})
            if error_msg:
                outputs.append({"ename": type(e).__name__, "evalue": str(e), "output_type": "error", "traceback": error_msg.splitlines()})
            
            cell["outputs"] = outputs
            cell["execution_count"] = idx + 1
            
    os.chdir(current_dir)
    
    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)
        
    if cell_errors == 0:
        print(f"  ✓ Clean execution: {nb_path}")
    else:
        print(f"  ! {cell_errors} errors in {nb_path}")

print("\n=== ALL NOTEBOOKS DIRECTLY EXECUTED AND SAVED ===")
