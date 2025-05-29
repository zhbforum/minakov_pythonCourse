import argparse
from fetcher import MovieFetcher


def ask_int(prompt: str, default: int | None = None) -> int:
    suffix = f" [{default}]" if default is not None else ""
    while True:
        raw = input(f"{prompt}{suffix}: ").strip()
        if not raw:
            if default is not None:
                return default
            print("Input is required.")
            continue
        try:
            value = int(raw)
            if value > 0:
                return value
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def ask_path(prompt: str, default: str = "movies.csv") -> str:
    suffix = f" [{default}]" if default else ""
    raw = input(f"{prompt}{suffix}: ").strip()
    return raw or default


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch movie data and export to CSV.")
    parser.add_argument("--pages", type=int,
                        help="Number of pages to fetch from the API")
    parser.add_argument("--output", type=str, help="Path to output CSV file")

    args = parser.parse_args()

    print("\nWelcome to the Movie DB data fetcher!\n")

    pages = (args.pages if args.pages else
             ask_int("How many pages would you like to fetch", 2))
    output = (args.output if args.output else
             ask_path("Where should I save the CSV file", "movies.csv"))

    fetcher = MovieFetcher(pages=pages)
    print(f"\nFetching {pages} page(s)…")
    fetcher.fetch_data()

    print("Most popular movie:", fetcher.most_popular_title())
    print(f"Writing processed data to «{output}»…")
    fetcher.csv_export(output)

    print("Done ✓")


if __name__ == "__main__":
    main()
