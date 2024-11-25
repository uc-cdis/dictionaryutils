import argparse

from datasimulator import main as simulator


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--path", required=True, help="path to save files to", nargs="?"
    )
    parser.add_argument(
        "--program", required=False, help="program to generate data", nargs="?"
    )
    parser.add_argument(
        "--project", required=False, help="project to generate data", nargs="?"
    )
    parser.add_argument(
        "--max_samples",
        required=False,
        help="max number of samples for each node",
        default=1,
        nargs="?",
    )
    parser.add_argument(
        "--node_num_instances_file",
        required=False,
        help="max number of samples for each node stored in a file",
        nargs="?",
    )
    parser.add_argument(
        "--random", help="randomly generate data numbers for nodes", action="store_true"
    )
    parser.add_argument(
        "--required_only", help="generate only required fields", action="store_true"
    )
    parser.add_argument(
        "--skip", help="skip raising an exception if gets an error", action="store_true"
    )
    parser.add_argument("--url", required=False, help="s3 dictionary link.", nargs="?")

    return parser.parse_args()


def main():

    args = parse_arguments()

    graph = simulator.initialize_graph(
        dictionary_url=args.url if hasattr(args, "url") else None,
        program=args.program if hasattr(args, "program") else None,
        project=args.project if hasattr(args, "project") else None,
        consent_codes=args.consent_codes if hasattr(args, "consent_codes") else None,
    )

    simulator.run_simulation(
        graph,
        args.path,
        args.max_samples,
        args.node_num_instances_file,
        args.random,
        args.required_only,
        args.skip,
    )


main()
