import click
import hashlib
import requests
import time
from pathlib import Path
from tqdm import tqdm

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

URL_BASE = 'https://amp-spacemaps-technical-challenge.s3-ap-northeast-1.amazonaws.com'

URLS = [
    f'{URL_BASE}/spacemaps_technical_challenge.txt'
]

DOWNLOAD_FOLDER = Path('.')
"""pathlib.Path: Points to the target directory of downloads."""


def downloader(url_position: int, resume_byte_pos: int = None):
    """Download url in ``URLS[position]`` to disk with possible resumption.

    Parameters
    ----------
    position: int
        Position of url.
    resume_byte_pos: int
        Position of byte from where to resume the download

    """
    # Get size of file
    url = URLS[url_position]
    r = requests.head(url)
    file_size = int(r.headers.get('content-length', 0))

    # Append information to resume download at specific byte position
    # to header
    resume_header = ({'Range': f'bytes={resume_byte_pos}-'}
                     if resume_byte_pos else None)

    # Establish connection
    r = requests.get(url, stream=True, headers=resume_header)

    # Set configuration
    block_size = 1024
    initial_pos = resume_byte_pos if resume_byte_pos else 0
    # mode = 'ab' if resume_byte_pos else 'wb'
    mode = 'a' if resume_byte_pos else 'w'
    file = DOWNLOAD_FOLDER / url.split('/')[-1]

    progress_bar = tqdm(total=file_size, unit='iB', unit_scale=True)
    with open(file, mode) as f:
        curr_pos = initial_pos
        leftover_chunk = b''
        read_chunk_size = 4*block_size
        for chunk in r.iter_content(read_chunk_size):
            progress_bar.update(len(chunk))
            curr_pos = curr_pos + len(chunk)
            last_chunk = False if curr_pos  < file_size else True
            #print(last_chunk)
            lines, leftover_chunk = process_chunk(chunk,last_chunk, leftover_chunk)
            for line in lines:
                f.write("%s\n" % line)
            time.sleep(1.0)
    progress_bar.close()

# can use resume_byte_pos to skip initial 500 bytes
def get_response_handle(url: str, resume_byte_pos: int = None):
    # resume header if needed
    resume_header = ({'Range': f'bytes={resume_byte_pos}-'}
                    if resume_byte_pos else None)
    res_handle = requests.get(url, stream = True, headers= resume_header)
    return res_handle

# trying to do a callback from the main class
def get_chunks(response_handle, chunk_size, initial_pos, callback):
    file_size = int(response_handle.headers.get('content-length', 0))
    current_pos = initial_pos
    block_size = 1024
    read_chunk_size = chunk_size * block_size
    leftover_chunk = b''
    for chunk in response_handle.iter_content(read_chunk_size):
        current_pos = current_pos + len(chunk)
        last_chunk = False if current_pos < file_size else True
        lines, leftover_chunk = process_chunk(chunk, last_chunk, leftover_chunk)
        callback(lines, last_chunk, len(chunk))

def process_chunk(chunk, is_last, leftover):

    # Add previous leftover to current chunk
    chunk = leftover + chunk
    batch = chunk.split(b'\n')

    # If this chunk is not the last one,
    # pop the last item as that will be an incomplete sentence
    # We return this leftover to use in the next chunk
    if not is_last:
        leftover = batch.pop(-1) 

    return [s.decode('utf-8') for s in filter(None, batch)], leftover
    # return [s for s in filter(None, batch)], leftover

def download_file(url_pos: int) -> None:
    # Execute the correct download operation.

    # Depending on the size of the file online and offline, resume the
    # download if the file offline is smaller than online.

    # Parameters
    # ----------
    # position: int
    #     Position of url.

    
    # Establish connection to header of file
    url = URLS[url_pos]
    r = requests.head(url)

    # Get filesize of online and offline file
    file_size_online = int(r.headers.get('content-length', 0))
    file = DOWNLOAD_FOLDER / url.split('/')[-1]

    # if file.exists():
    #     file_size_offline = file.stat().st_size

    #     if file_size_online != file_size_offline:
    #         click.echo(f'File {file} is incomplete. Resume download.')
    #         # file_size_offline is the new start positon for resume
    #         downloader(url, file_size_offline)
    #     else:
    #         click.echo(f'File {file} is complete. Skip download.')
    #         pass
    # else:
    #     click.echo(f'File {file} does not exist. Start download.')
    #     downloader(url)
    downloader(url_pos)


@click.group(context_settings=CONTEXT_SETTINGS, chain=True)
def cli():
    # Program for downloading in chunks and fixing each chunk 
    # $python FileDownloader.py download 
    
    pass


@cli.command()
def download():
    # Download files specified in ``URLS``
    click.echo('\n### Start downloading required files.\n')
    for url in range(len(URLS)):
        download_file(url)
    click.echo('\n### End\n')


if __name__ == '__main__':
    cli()
