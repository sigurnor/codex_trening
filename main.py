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
        "--output-dir",
        required=True,
        help="Sti til mappe der TSV-filer skal skrives (én per n-verdi).",
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
    output_dir = Path(args.output_dir)

    if not input_path.is_file():
        raise SystemExit(f"Inputfil finnes ikke: {input_path}")
    output_dir.mkdir(parents=True, exist_ok=True)

    tokens = read_tokens_from_file(str(input_path))
    n_values = sorted({n for n in args.n if n > 0})
    if not n_values:
        raise SystemExit("Minst én n-verdi > 0 må spesifiseres.")

    ngram_counts = count_multiple_ngrams(tokens, n_values)
    for n in n_values:
        output_file = output_dir / f"{n}-grams.tsv"
        write_ngrams_to_tsv(ngram_counts[n], str(output_file))


if __name__ == "__main__":
    main()