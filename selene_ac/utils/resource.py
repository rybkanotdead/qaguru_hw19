from pathlib import Path
import tests

def path(file_name: str) -> str:
    tests_dir = Path(tests.__file__).parent
    apk_path = (tests_dir / '..' / 'apk' / file_name).resolve()
    return str(apk_path)