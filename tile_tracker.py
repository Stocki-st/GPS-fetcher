import sqlite3
import time
import asyncio
import ssl
from cryptography.fernet import Fernet
from pytile.errors import TileError
from aiohttp import ClientSession, TCPConnector
from pytile import async_login

def decrypt_password():
    from config import TILE_PASSWORD_ENCRYPTED, ENCRYPTION_KEY
    
    cipher_suite = Fernet(ENCRYPTION_KEY)
    decrypted_password = cipher_suite.decrypt(TILE_PASSWORD_ENCRYPTED).decode()
    return decrypted_password

from config import TILE_USERNAME
TILE_PASSWORD = decrypt_password()  
DB_PATH = "tile_tracker.db"

def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tile_locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tile_name TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_location(tile_name, latitude, longitude, timestamp):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tile_locations (tile_name, latitude, longitude, timestamp)
        VALUES (?, ?, ?, ?)
    """, (tile_name, latitude, longitude, timestamp))
    conn.commit()
    conn.close()

async def fetch_tile_locations():
    try:
        async with ClientSession(connector=TCPConnector(ssl=False)) as session:
            api = await async_login(TILE_USERNAME, TILE_PASSWORD, session)

            tiles = await api.async_get_tiles()

            for tile_uuid, tile in tiles.items():
               # print("#tile: ", tile)
               # print("#name: ", tile.name)
               # members = dir(tile)
               # print(members)
                tile_name = tile.name
                latitude = tile.latitude
                longitude = tile.longitude
                timestamp = tile.last_timestamp

                print(f"Tile: {tile_name}, Lat: {latitude}, Lon: {longitude}, Time: {timestamp}")
                save_location(tile_name, latitude, longitude, timestamp)
    except TileError as e:
        print(f"Error fetching Tile data: {e}")

async def main():
    print("Start Tile-Tracker...")
    setup_database()

    while True:
        print("Get tracker locations...")
        await fetch_tile_locations()
        print("Wait 10 minutes...")
        await asyncio.sleep(600)

if __name__ == "__main__":
    asyncio.run(main())