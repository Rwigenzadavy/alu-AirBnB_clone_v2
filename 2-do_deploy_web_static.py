#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""

from fabric.api import env, put, run, local
from os.path import exists
from datetime import datetime

env.hosts = ['34.227.11.202', '52.90.153.53']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'

def do_deploy(archive_path):
    """Distributes an archive to web servers
    
    Args:
        archive_path (str): Path to the archive to deploy
        
    Returns:
        bool: True if successful, False otherwise
    """
    if not exists(archive_path):
        return False

    try:
        # Upload archive
        put(archive_path, '/tmp/')

        # Create target directory
        file_name = archive_path.split('/')[-1]
        folder_name = file_name.split('.')[0]
        release_path = '/data/web_static/releases/{}/'.format(folder_name)
        run('mkdir -p {}'.format(release_path))

        # Uncompress archive
        run('tar -xzf /tmp/{} -C {}'.format(file_name, release_path))

        # Move files and clean up
        run('mv {}/web_static/* {}'.format(release_path, release_path))
        run('rm -rf {}/web_static'.format(release_path))
        run('rm /tmp/{}'.format(file_name))

        # Update symlink (critical fix)
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(release_path))

        # Verify deployment
        if run('test -f /data/web_static/current/0-index.html').failed:
            return False
        if run('test -f /data/web_static/current/my_index.html').failed:
            return False

        return True
    except Exception as e:
        print("Error:", e)
        return False
