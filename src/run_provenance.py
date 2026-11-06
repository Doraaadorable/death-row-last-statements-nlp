"""Capture executed source bytes; do not infer historical generation provenance."""
import hashlib
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path
import numpy
import pandas
import scipy
import sklearn


def code_provenance(script):
    script = Path(script).resolve()
    root = script.parents[1]
    paths = [script, root/'src/text_features.py', Path(__file__).resolve()]
    head = None
    try:
        repo_root = subprocess.check_output(
            ['git', 'rev-parse', '--show-toplevel'], cwd=root,
            stderr=subprocess.DEVNULL, text=True).strip()
        if Path(repo_root).resolve() == root:
            head = subprocess.check_output(
                ['git', 'rev-parse', 'HEAD'], cwd=root,
                stderr=subprocess.DEVNULL, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        pass
    return {
        'status': 'Observed source bytes at this execution; not historical provenance',
        'executed_at_utc': datetime.now(timezone.utc).isoformat(),
        'git_head_if_available': head,
        'code_sha256': {
            str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in paths
        },
        'environment': {
            'python': platform.python_version(), 'numpy': numpy.__version__,
            'pandas': pandas.__version__, 'scipy': scipy.__version__,
            'sklearn': sklearn.__version__,
        },
    }
