import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--normalizer",
        choices=["deterministic"],
        default="deterministic",
    )
    parser.add_argument(
        "--dataset-name",
        default="deterministic",
    )

    group = parser.add_argument_group("Normalizer arguments", description='''
Normalizer arguments. Available:
    --review-normalization
    --cache-path''')
    group.add_argument(
        "--review-normalization",
        action="store_true"
    )
    return parser.parse_args()


args = parse_args()
print(args.normalizer)
print(args.dataset_name)
print(args.review_normalization)