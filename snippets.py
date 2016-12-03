import logging
import argparse
import psycopg2
# Set the log output file, and the log level
# File name is where you want to save the log -- in this case, writes to a file 
# called snippets.log
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect(database="snippets")
logging.debug("Database connection established")

def main(): 
    """Main Function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    #Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="Name of the snippet")
    put_parser.add_argument("snippet", help="Snippet of text")
    
    #Subparser for the get command
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    get_parser.add_argument("name", help="Name of the snippet")
    
    #Subparser for the catalog function
    logging.debug("Constructing catalog subparser")
    catalog_parser = subparsers.add_parser("catalog", help="Retrieve catalog of snippet keywords")
    
    arguments = parser.parse_args()
    
    #Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")
    
    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))
    elif command == "catalog": 
        keywords = catalog()
        print("Keywords: {!r}".format(keywords))

def put(name, snippet):
    """
    Store a snippet with an associated name.

    Returns the name and the snippet
    """
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    with connection, connection.cursor() as cursor:
        try:
            command = "insert into snippets values (%s, %s)"
            cursor.execute(command, (name, snippet))
        except psycopg2.IntegrityError as e: 
            connection.rollback()
            command = "update snippets set message=%s where keyword=%s"
            cursor.execute(command, (snippet, name))
    logging.debug("Snippet stored successfully")
    return name, snippet

def get(name):
    """Retrieve the snippet with a given name.

    If there is no such snippet, return '404: Snippet Not Found'.

    Returns the snippet.
    """
    logging.info("Retrieving snippet {!r}".format(name))
    # the next lines of code make sure that something is either committed or rolled back
    with connection, connection.cursor() as cursor: 
        cursor.execute("select message from snippets where keyword=%s", (name,))
        snippet = cursor.fetchone()
    logging.debug("Snippet retrieved successfully")
    if not snippet: 
        return "404: Snippet Not Found"
    return snippet[0]    

def catalog():
    """Retrieve a list of all keywords"""
    logging.info("Retrieveing list of keywords")
    with connection, connection.cursor() as cursor: 
        cursor.execute("select keyword from snippets order by keyword")
        keywords = cursor.fetchall()
    logging.debug("List of keywords retrieved successfully")
    if not keywords: 
        return "404: There are no keywords to list"
    return keywords    
    
if __name__ == "__main__":
    main()