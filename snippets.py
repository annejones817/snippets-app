import logging
import argparse
# Set the log output file, and the log level
# File name is where you want to save the log -- in this case, writes to a file 
# called snippets.log
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

def main(): 
    """Main Function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    arguments = parser.parse_args()

def put(name, snippet):
    """
    Store a snippet with an associated name.

    Returns the name and the snippet
    """
    logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
    return name, snippet

def get(name):
    """Retrieve the snippet with a given name.

    If there is no such snippet, return '404: Snippet Not Found'.

    Returns the snippet.
    """
    logging.error("FIXME: Unimplemented - get({!r})".format(name))
    return ""    
    
if __name__ == "__main__":
    main()