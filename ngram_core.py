from collections import Counter
from typing import Dict, Iterable, List, Mapping, Tuple


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


def count_multiple_ngrams(tokens: List[str], n_values: Iterable[int]) -> Dict[int, Counter]:
    """Returnerer en mapping fra n til Counter med frekvenser."""
    counts: Dict[int, Counter] = {}
    for n in n_values:
        counts[n] = count_ngrams(tokens, n)
    return counts


def write_ngrams_to_tsv(counter: Mapping[int, Counter], out_path: str) -> None:
    """Skriver n-grammer og frekvenser til en TSV-fil gruppert per n."""
    with open(out_path, "w", encoding="utf-8") as f:
        for n in sorted(counter.keys()):
            for ngram, count in counter[n].most_common():
                ngram_str = " ".join(ngram)
                f.write(f"{n}\t{ngram_str}\t{count}\n")