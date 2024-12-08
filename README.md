# GPS-fetcher

fetch location of tile trackers and stores it in a database.
# Tile Tracker Location Logger

This Python script uses the [pytile](https://github.com/bachya/pytile) library to fetch the locations of your Tile trackers every 10 minutes and logs the data into an SQLite database.

## Features
- Fetches locations of active Tile trackers.
- Stores location data (name, latitude, longitude, timestamp) in a local SQLite database.
- Runs continuously with a 10-minute interval between queries.

## Requirements
- Python 3.7 or higher
- Tile account (free version supported)
- Required libraries are listed in the `requirements.txt` file.

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/tile-tracker-logger.git
   cd tile-tracker-logger
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your Tile credentials (using encryption):

  * Run the encrypt_password.py script to generate your encrypted password and save the key:
   ```bash
   python encrypt_password.py
   ```
4. Run the script:
   ```bash
   python tile_tracker.py
   ```

## Database Schema
The script automatically creates a SQLite database (`tile_tracker.db`) with the following table:

| Column      | Type    | Description                     |
|-------------|---------|---------------------------------|
| id          | INTEGER | Primary key                    |
| tile_name   | TEXT    | Name of the Tile tracker        |
| latitude    | REAL    | Latitude of the tracker         |
| longitude   | REAL    | Longitude of the tracker        |
| timestamp   | TEXT    | Timestamp of the location data  |

## Usage
The script runs indefinitely and fetches Tile tracker locations every 10 minutes.  
To stop the script, use `Ctrl+C`.

## Security Considerations
### Store your credentials securely:
- Use a separate `config.py` file and ensure it's not tracked by version control by adding it to `.gitignore`.

### Protect the SQLite database:
Futher extension:
- Restrict file permissions to prevent unauthorized access.
- Consider encrypting the database using tools like SQLCipher for added security.
