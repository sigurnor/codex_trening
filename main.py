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
    parser.add_argument(
        "--top",
        type=int,
        default=0,
        help=(
            "Begrens antall n-gram som skrives per fil. 0 betyr ingen begrensning."
        ),
    )
    parser.add_argument(
        "--case-fold",
        action="store_true",
        help="Konverter alle tokens til lowercase for case-insensitive telling.",
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
    if args.case_fold:
        tokens = [token.casefold() for token in tokens]
    n_values = sorted({n for n in args.n if n > 0})
    if not n_values:
        raise SystemExit("Minst én n-verdi > 0 må spesifiseres.")

    if args.top < 0:
        raise SystemExit("--top kan ikke være negativ.")
    top_limit = args.top if args.top > 0 else None

    ngram_counts = count_multiple_ngrams(tokens, n_values)
    for n in n_values:
        output_file = output_dir / f"{n}-grams.tsv"
        write_ngrams_to_tsv(ngram_counts[n], str(output_file), limit=top_limit)


if __name__ == "__main__":
    main()
