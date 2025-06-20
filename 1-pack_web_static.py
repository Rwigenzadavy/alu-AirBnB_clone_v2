#!/usr/bin/python3
"""
Fabric script to generate a .tgz archive from web_static folder
"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Generates a .tgz archive from web_static folder contents
    Returns archive path if successful, otherwise None
    """
    try:
        # Create versions/ folder if it doesn't exist
        if not os.path.exists("versions"):
            local("mkdir -p versions")

        # Generate timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = f"versions/web_static_{timestamp}.tgz"

        # Create archive
        print(f"Packing web_static to {archive_name}")
        result = local(f"tar -cvzf {archive_name} web_static")

        # Confirm success
        if result.succeeded:
            size = os.path.getsize(archive_name)
            print(f"web_static packed: {archive_name} -> {size}Bytes")
            return archive_name
        else:
            return None

    except Exception as e:
        print(f"Error during packing: {e}")
        return None


if __name__ == "__main__":
    do_pack()
