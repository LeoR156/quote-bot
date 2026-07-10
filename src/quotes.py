import random
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "quotes.txt"


def _read_all() -> list[str]:
    """Читает все цитаты из файла. Возвращает пустой список, если файл пуст или не существует."""
    if not DATA_FILE.exists():
        return []
    lines = DATA_FILE.read_text(encoding="utf-8").splitlines()
    return [line for line in lines if line.strip()]


def get_random_quote() -> str | None:
    """Возвращает случайную цитату или None, если их нет."""
    quotes = _read_all()
    if not quotes:
        return None
    return random.choice(quotes)


def add_quote(text: str) -> bool:
    """
    Добавляет новую цитату в файл.
    Возвращает False, если такая цитата уже существует, иначе True.
    """
    quotes = _read_all()
    if text in quotes:
        return False
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("a", encoding="utf-8") as f:
        f.write(text + "\n")
    return True


def count_quotes() -> int:
    """Возвращает количество цитат в базе."""
    return len(_read_all())
