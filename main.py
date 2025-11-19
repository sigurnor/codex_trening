import argparse
from pathlib import Path

from ngram_core import read_tokens_from_file, count_ngrams, write_ngrams_to_tsv


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
        default=2,
        help="Størrelse på n-gram (default: 2).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.is_file():
        raise SystemExit(f"Inputfil finnes ikke: {input_path}")

    tokens = read_tokens_from_file(str(input_path))
    ngram_counts = count_ngrams(tokens, args.n)
    write_ngrams_to_tsv(ngram_counts, str(output_path))


if __name__ == "__main__":
    main()