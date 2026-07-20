import argparse
from dataclasses import dataclass

@dataclass
class CLIArgs:
    initial_page: int
    query: str
    add_favgroup_id: int
    random: bool
    limit: int
    yes_no_tag: str
    yes_no_tag_force: bool
    auto: bool
    semi_auto: bool
    quiet: bool
    same_page: bool
    auto_debug: bool
    override_domain: str
    override_login: str
    override_apikey: str
    offline_file: str
    offline_output: str
    file_resume: int
    ignore_skipped: bool
    test_mode: bool
    no_commentary_check: bool

def parse_args():
    aparser = argparse.ArgumentParser()
    aparser.add_argument("--page", type=int, default=1)
    aparser.add_argument("--query", type=str, default="-commentary+-commentary_request")
    aparser.add_argument("--group", type=int, default=0, help="posts with no commentary will be added to this fav group (necessary if mode is add)")
    aparser.add_argument("--random", action="store_true", help="select posts at random")
    aparser.add_argument("--limit", type=int, default=None, help="change the post limit")
    aparser.add_argument("--ynt", type=str, default=None, help="yes/no tag: press enter to apply tag for each post found, any key + enter to skip")
    aparser.add_argument("--ynty", action="store_true", help="automatically add yes/no tag without confirmation")
    aparser.add_argument("--auto", action="store_true", help="automatically detect language and add tag. if language not detected, skip post")
    aparser.add_argument("--semi-auto", action="store_true", help="auto mode but don't skip post, ask user instead")
    aparser.add_argument("--quiet", action="store_true", help="removes unnecessary input, only for auto mode")
    aparser.add_argument("--same-page", action="store_true", help="stay on the same page")
    aparser.add_argument("--auto-dbg", action="store_true", help="dry-run auto mode")
    aparser.add_argument("--domain", type=str, help="override booru domain for this session")
    aparser.add_argument("--login", type=str, help="override login for this session")
    aparser.add_argument("--apikey", type=str, help="override api key for this session")
    aparser.add_argument("--file", type=str, help="use a file with commentaries")
    aparser.add_argument("--output", type=str, help="file to output tag script")
    aparser.add_argument("--file-resume", type=int, help="resume from this post when using file mode", default=0)
    aparser.add_argument("--ignore-skip", action="store_true", help="ignore skipped posts")
    aparser.add_argument("--test", action="store_true", help="run in test mode")
    aparser.add_argument("--ncpc", action="store_true", help="no commentary presence check")
    args = aparser.parse_args()

    auto = args.auto
    semi_auto = args.semi_auto
    quiet = args.quiet
    if not auto or args.semi_auto:
        quiet = False
    if semi_auto and not auto:
        auto = True

    return CLIArgs(
        args.page,
        args.query,
        args.group,
        args.random,
        args.limit,
        args.ynt,
        args.ynty,
        auto,
        semi_auto,
        quiet,
        args.same_page,
        args.auto_dbg,
        args.domain,
        args.login,
        args.apikey,
        args.file,
        args.output,
        args.file_resume,
        args.ignore_skip,
        args.test,
        args.ncpc
    )
