import os
import json
import datetime
try:
    from IMDBTraktSyncer import authTrakt
    from IMDBTraktSyncer import errorLogger as EL
except ImportError:
    import authTrakt
    import errorLogger as EL

def prompt_get_credentials():
    # Define the file path
    here = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(here, 'credentials.txt')
    print(f"Your settings are saved at:\n{here}")
    
    default_values = {
        "trakt_access_token": "empty",
        "trakt_refresh_token": "empty",
    }
    
    # Check if the file exists
    if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
        # Changing this, 
        # ~~If the file does not exist or is empty, create it with default values~~
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(default_values, f)

    # Old version support (v1.0.6 and below). Convert old credentials.txt format to json
    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf-8') as txt_file:
            lines = txt_file.readlines()
        if lines[0].startswith("trakt_client_id="):
            values = {}
            for line in lines:
                key, value = line.strip().split("=")
                values[key] = value
            with open(file_path, 'w', encoding='utf-8') as txt_file:
                json.dump(values, txt_file)
            print("Warning: You are using a depreciated credentials.txt file.\nConversion successful: credentials.txt file converted to the new JSON format.")

    # Load the values from the file or initialize with default values
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            values = json.load(f)
        except json.decoder.JSONDecodeError:
            # Handle the case where the file is empty or not a valid JSON
            values = default_values

    for key, value in values.items():
        if value == "empty":
            raise ValueError("Missing Trakt access token or refresh token. Please provide a value in the credentials.txt file for the docker version to work.")

    trakt_client_id = os.getenv("trakt_client_id")
    trakt_client_secret = os.getenv("trakt_client_secret")
    trakt_access_token = values["trakt_access_token"]
    trakt_refresh_token = values["trakt_refresh_token"]
    imdb_username = os.getenv("imdb_username")
    imdb_password = os.getenv("imdb_password")
    
    return trakt_client_id, trakt_client_secret, trakt_access_token, trakt_refresh_token, imdb_username, imdb_password

def prompt_sync_ratings():

    # no no no prompting in docker thank you
    
    sync_ratings = os.getenv("sync_ratings")

    if sync_ratings is None:
        # throw that error
        raise ValueError("Missing value for sync_ratings. Please provide a value in the environment variables for the docker version to work.")

    else:
        # Validate user input
        if sync_ratings.lower() == 'y':
            sync_ratings_value = True
        elif sync_ratings.lower() == 'n':
            sync_ratings_value = False
        else:
            # Invalid input, ask again
            raise ValueError("Fix the sync_ratings environment variable please. It should be either y or n.")

    # return true or false
    return sync_ratings_value

def prompt_sync_watchlist():

    sync_watchlist = os.getenv("sync_watchlist")

    if sync_watchlist is None:
        # throw that error
        raise ValueError("Missing value for sync_watchlist. Please provide a value in the environment variables for the docker version to work.")

    else:
        # Validate user input
        if sync_watchlist.lower() == 'y':
            sync_watchlist_value = True
        elif sync_watchlist.lower() == 'n':
            sync_watchlist_value = False
        else:
            # Invalid input, ask again
            raise ValueError("Fix the sync_watchlist environment variable please. It should be either y or n.")

    # return true or false
    return sync_watchlist_value

# Last run function, used to determine when the last time IMDB reviews were submitted    
def check_imdb_reviews_last_submitted():
    here = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(here, 'credentials.txt')
    
    # Load credentials from credentials.txt
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            credentials = json.load(file)
    else:
        credentials = {}

    imdb_reviews_last_submitted_date_str = credentials.get('imdb_reviews_last_submitted_date')

    # If imdb_reviews_last_submitted_date is not available or not in the correct format, consider it as 10 days ago
    imdb_reviews_last_submitted_date = datetime.datetime.strptime(imdb_reviews_last_submitted_date_str, '%Y-%m-%d %H:%M:%S') if imdb_reviews_last_submitted_date_str else datetime.datetime.now() - datetime.timedelta(hours=240)

    # Check if 240 hours have passed since the last run
    if datetime.datetime.now() - imdb_reviews_last_submitted_date >= datetime.timedelta(hours=240):
        # Update the imdb_reviews_last_submitted_date with the current time
        credentials['imdb_reviews_last_submitted_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Save updated credentials to credentials.txt
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(credentials, file)

        return True
    else:
        return False
        
def prompt_sync_reviews():

    sync_reviews = os.getenv("sync_reviews")

    if sync_reviews is None:
        # throw that error
        raise ValueError("Missing value for sync_reviews. Please provide a value in the environment variables for the docker version to work.")

    else:
        # Validate user input
        if sync_reviews.lower() == 'y':
            sync_reviews_value = True
        elif sync_reviews.lower() == 'n':
            sync_reviews_value = False
        else:
            # Invalid input, ask again
            raise ValueError("Fix the sync_reviews environment variable please. It should be either y or n.")

    # return true or false
    return sync_reviews_value

def prompt_remove_watched_from_watchlists():
    remove_watched_from_watchlists = os.getenv("remove_watched_from_watchlists")

    if remove_watched_from_watchlists is None:
        raise ValueError("Missing value for remove_watched_from_watchlists. Please provide a value in the environment variables for the docker version to work.")

    else:
        # Validate user input
        if remove_watched_from_watchlists.lower() == 'y':
            remove_watched_from_watchlists_value = True
        elif remove_watched_from_watchlists.lower() == 'n':
            remove_watched_from_watchlists_value = False
        else:
            # Invalid input, ask again
            raise ValueError("Fix the remove_watched_from_watchlists environment variable please. It should be either y or n.")

    # return true or false
    return remove_watched_from_watchlists_value

# Save the credential values as variables
trakt_client_id, trakt_client_secret, trakt_access_token, trakt_refresh_token, imdb_username, imdb_password = prompt_get_credentials()
sync_watchlist_value = prompt_sync_watchlist()
sync_ratings_value = prompt_sync_ratings()
remove_watched_from_watchlists_value = prompt_remove_watched_from_watchlists()
sync_reviews_value = prompt_sync_reviews()