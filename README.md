# Komentari

A program for manual and automatic tagging of Danbooru commentaries. This is the software behind the [CommentaryRequestBot](https://danbooru.donmai.us/users/1488227).

## Configuration

`settings.py` contains default settings. Create a new `usersettings.py` file to override settings.

Authentication info is stored in `authsettings.py`. Set `LOGIN`, `APIKEY`, `TEST_LOGIN` and `TEST_APIKEY` variables. (test authentication variables can be left empty if you're not going to use a test instance)

Run `dl_wikilist.py` to create a list of copyright and character names for untranslatable commentary tagging (output in `othernames.json`).

## Usage

`komentari.py` is the main entry point of the program. Use the `--help` option to see the list of available command-line options.

### Convenience scripts

Located in `scripts` directory, execute from the root directory of Komentari.

* `do_user.sh`: quickly semi-automatically tag a specific user's posts. Run with no arguments to see usage.
* `runbot.sh`: run a simple bot instance. Any arguments passed to this script are forwarded to `komentari.py`.

### Offline mode

Komentari can run in offline mode to prepare tag edits locally and apply them all at once.

First, download commentaries using the `commentary_downloader.py` script.

Run `komentari.py` with the `--file` option, set to the file containing commentaries. Specify file to output tag edits to with the `--output` option. `--auto` and `--semi-auto` options can be used in offline mode too.

Once finished, apply tag edits using `script_executor.py`.
