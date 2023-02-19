import click
import requests
import yt_dlp
from pyfiglet import Figlet
from columnar import columnar

BASE_URL: str = 'https://piped.privacydev.net/'
API_URL: str = 'https://api.piped.privacydev.net/'

print(f'''{Figlet(font="chunky").renderText("Pipyt")}
A YT Music searcher/downloader using Piped's API. 🎧🎶
      ''')


@click.group()
@click.version_option('0.1.0', prog_name='pipyt')
def main() -> None:
    pass


@main.command()
@click.argument('query', type=str, nargs=1)
@click.option('-s', '--song', is_flag=True, help='Search for YT Music songs. (default)')
@click.option('-a', '--album', is_flag=True, help='Search for YT Music albums.')
@click.option('-aS', '--album-show', is_flag=True, help='Search for YT Music albums and show its tracks.')
@click.option('-n', '--result-number', help='Number of search results. Say 0 to return all results.', default=5, show_default=True)
def find(query: str, song, album, album_show, result_number) -> None:
    '''
    The search command.

    \b
    EXAMPLES
        pipyt find "i thought you wanted to dance"
        pipyt find -an 1 "call me if you get lost"
    '''

    API_SEARCH_URL: str = API_URL + 'search/'

    if result_number == 0:
        result_number: int = 20

    def find_music_songs(query: str) -> None:
        click.echo(f'Searching for {query}...')
        try:
            res = requests.get(API_SEARCH_URL, params={
                               'q': query, 'filter': 'music_songs'})
            # RequestsJSONDecodeError
            data: dict = res.json()
        except requests.exceptions.ConnectionError:
            click.echo(
                '\n\033[0;31mERROR:\033[0m Could not establish connection. Please check your network or try again.')
            return

        headers: list = ['', 'music/song name', 'uploader', 'url']
        index: int = 0
        music_songs: list = []
        for music_song in data['items']:
            name: str = music_song['title']
            uploader: str = music_song['uploaderName']
            _id: str = music_song['url'].replace('/watch?v=', '')
            url: str = 'https://youtu.be/' + _id
            if index == result_number:
                break
            index += 1
            music_songs.append([str(index) + '.', name, uploader, url])

        return click.echo(columnar(music_songs, headers, no_borders=True))

    def find_albums(query: str) -> None:
        click.echo(f'Searching for {query}...')
        res = requests.get(API_SEARCH_URL, params={
                           'q': query, 'filter': 'music_albums'})
        data: dict = res.json()

        headers: list = ['', 'album name', 'uploader', 'url']
        index: int = 0
        albums_list: list = []
        for album in data['items']:
            name: str = album['name']
            uploader: str = album['uploaderName']
            url: str = 'https://youtube.com' + album['url']
            if index == result_number:
                break
            index += 1
            albums_list.append([str(index) + '.', name, uploader, url])

        return click.echo(columnar(albums_list, headers, no_borders=True))

    def search_find_album_tracks(query: str) -> None:
        click.echo(f'Searching for {query}...')
        res = requests.get(API_SEARCH_URL, params={
                           'q': query, 'filter': 'music_albums'})
        data: dict = res.json()

        headers: list = ['', 'album name', 'uploader', 'url']
        index: int = 0
        albums_list: list = []
        for album in data['items']:
            name: str = album['name']
            uploader: str = album['uploaderName']
            url: str = 'https://youtube.com' + album['url']
            if index == result_number:
                break
            index += 1
            albums_list.append([str(index) + '.', name, uploader, url])

        click.echo(columnar(albums_list, headers, no_borders=True))

        while True:
            try:
                users_choice: int = int(
                    input('Choose an album (by index) or press "CTRL+C" to exit. '))
                if users_choice > len(albums_list) or users_choice == 0:
                    click.echo(
                        f'\033[0;31mERROR:\033[0m {users_choice} does not exist. Please enter a valid index.\n')
                    continue
            except ValueError:
                click.echo(
                    '\033[0;31mERROR:\033[0m Only integers are allowed. Please enter a valid index.\n')
                continue
            break

        album_id: str = data['items'][users_choice -
                                      1]['url'].replace('/playlist?list=', '')

        click.clear()
        res = requests.get(API_URL + 'playlists/' + album_id)
        data: dict = res.json()

        headers: list = ['', 'track name', 'url']
        index: int = 0
        track_list: list = []
        for track in data['relatedStreams']:
            name: str = track['title']
            _id: str = track['url'].replace('/watch?v=', '')
            url: str = 'https://youtu.be/' + _id
            index += 1
            track_list.append([str(index).zfill(2), name, url])

        return click.echo(columnar(track_list, headers, no_borders=True))

    if song:
        find_music_songs(query)
    elif album:
        find_albums(query)
    elif album_show:
        search_find_album_tracks(query)
    else:
        find_music_songs(query)


@main.command()
@click.argument('url', nargs=-1)
@click.option('-m', '--mp3', is_flag=True, help='Converts audio to MP3. (default)')
@click.option('-f', '--flac', is_flag=True, help='Converts audio to FLAC.')
@click.option('-q', '--quality', default=320, show_default=True, help="Set audio's bitrate.")
@click.option('-o', '--output', default='.', help='File(s) output directory.')
def down(url, mp3, flac, quality, output):
    '''
    The download command.

    \b
    EXAMPLES
        pipyt down ejlmxPm1fQY (only the ID)
        pipyt down -q 256 https://youtu.be/jFigcd4JTtE
        pipyt down -f https://youtu.be/6tnv-JDJC0Q
    '''

    class Logger(object):
        def debug(self, msg: str) -> None:
            pass

        def warning(self, msg: str) -> None:
            pass

        def error(self, msg: str) -> None:
            pass

    def hooks(down_progress: dict) -> None:
        if down_progress['status'] == 'finished':
            click.echo('Done.')
            click.echo(f'Converting to {audio_format}...')

    if url == int:
        url: str = 'https://youtu.be/' + url
    if mp3:
        audio_format: str = 'MP3'
    elif flac:
        audio_format: str = 'FLAC'
    else:
        audio_format: str = 'MP3'

    ytdl_opts: dict = {
        'outtmpl': f'{output}/%(track)s.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': audio_format,
            'preferredquality': quality
        }],
        'progress_hooks': [hooks],
        'logger': Logger(),
    }

    try:
        with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
            for url in url:
                info: dict = ytdl.extract_info(url, download=False)
                click.echo(f'Downloading "{info["title"]}"...')
                ytdl.download(url)
    except yt_dlp.utils.DownloadError:
        click.echo(
            f'\033[0;31mERROR:\033[0m [youtube] Link unavailable, try another please.')


main()
