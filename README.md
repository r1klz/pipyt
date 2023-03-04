```
 ______ __               __
|   __ \__|.-----.--.--.|  |_
|    __/  ||  _  |  |  ||   _|
|___|  |__||   __|___  ||____|
           |__|  |_____|
```

A basic CLI application that searches and downloads YT Music songs

## INSTALLATION

### PyPI

`pip install -U pipyt`

## BASIC USAGE

```
pipyt COMMAND [OPTIONS] INPUT
```

- `pipyt <command> --help` for more helping.

### EXAMPLES

`pipyt find <song_name>`

`pipyt down <url/video_id>`

## TODO

- Add a config file ~for setting a default instance of Piped and~ for setting the default output directory to save downloaded songs;
- Refact all code and remove click's dependency.
