import argparse
from pathlib import Path

from ngram_core import (
    read_tokens_from_file,
    count_multiple_ngrams,
    write_ngrams_to_tsv,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="En enkel n-gram-bygger for tekstfiler."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Sti til inputfil (tekst).",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Sti til outputfil (TSV med ngram og count).",
    )
    parser.add_argument(
        "--n",
        type=int,
        nargs="+",
        default=[1, 2, 3],
        help="Størrelser på n-gram (default: 1 2 3).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.is_file():
        raise SystemExit(f"Inputfil finnes ikke: {input_path}")

    tokens = read_tokens_from_file(str(input_path))
    n_values = sorted({n for n in args.n if n > 0})
    if not n_values:
        raise SystemExit("Minst én n-verdi > 0 må spesifiseres.")

    ngram_counts = count_multiple_ngrams(tokens, n_values)
    write_ngrams_to_tsv(ngram_counts, str(output_path))


if __name__ == "__main__":
    main()