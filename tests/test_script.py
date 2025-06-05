import subprocess

def test_script_runs():
    result = subprocess.run(
        ["python", "listar_workflows.py"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Script failed to run"
    assert "workflow" in result.stdout.lower() or result.stdout.strip() != "", "No output detected"
