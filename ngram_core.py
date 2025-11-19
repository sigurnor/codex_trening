from collections import Counter
from typing import List, Iterable, Tuple


def read_tokens_from_file(path: str) -> List[str]:
    """Leser en tekstfil og returnerer en liste med tokens (veldig enkel tokenisering)."""
    tokens: List[str] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            tokens.extend(line.split())
    return tokens


def generate_ngrams(tokens: List[str], n: int) -> Iterable[Tuple[str, ...]]:
    """Genererer n-grammer (som tuples) fra en liste med tokens."""
    if n <= 0:
        raise ValueError("n must be >= 1")
    for i in range(len(tokens) - n + 1):
        yield tuple(tokens[i:i + n])


def count_ngrams(tokens: List[str], n: int) -> Counter:
    """Returnerer en Counter med frekvenser for alle n-grammer."""
    ngram_counter: Counter = Counter()
    for ng in generate_ngrams(tokens, n):
        ngram_counter[ng] += 1
    return ngram_counter


def write_ngrams_to_tsv(counter: Counter, out_path: str) -> None:
    """Skriver n-grammer og frekvenser til en TSV-fil."""
    with open(out_path, "w", encoding="utf-8") as f:
        for ngram, count in counter.most_common():
            ngram_str = " ".join(ngram)
            f.write(f"{ngram_str}\t{count}\n")