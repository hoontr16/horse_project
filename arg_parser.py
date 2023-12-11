import argparse

def parse_args():
    """ parse command line arguments
    """
    
    parser = argparse.ArgumentParser(description = "Game of Horse")
    
    #adds arguments for the different kind of players (Human or CPU)
    parser.add_argument("humans", type=int, default=1, help="number of human players") 
    parser.add_argument("CPUs", type=int, default=1, help="number of computer players)
    
    #add argument for file name
    parser.add_argument("file name", type=str, default = None, help="File to write shot history to")
    
    return parser.parse_args()