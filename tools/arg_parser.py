import argparse


def build_parser(description = None) -> argparse.ArgumentParser:
    '''
    Function that returns a Argument Parser.
    '''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("simulation_type", type=str, help=f"Insert a number (0, 1, 2, 3...) representing a simulation type.")

    return parser