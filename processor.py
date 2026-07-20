from booru_url import get_booru_url
from commentary import get_commentary
from tagedit import print_tags, tag_edit_post
from tag_script import write_tag_script
from typing import NamedTuple
import sys
import automode
import parser
import settings
import webbrowser

def print_post_link(args, post_id):
    print(f"\nPost \033]8;;{get_booru_url(args.test_mode)}/posts/{post_id}\033\\#{post_id}\033]8;;\033\\\n")

def print_commentary(commentary):
    print(
        f"Title: \033[0;36m{commentary.og_title}\033[0m\n\n"
        f"Description:\n\n\033[0;36m{commentary.og_description}\033[0m\n\n"
    )
    if len(commentary.tl_title) != 0 or len(commentary.tl_description) != 0:
        print(
            f"TRANSLATED Title: \033[0;36m{commentary.tl_title}\033[0m\n\n"
            f"TRANSLATED Description:\n\n\033[0;36m{commentary.tl_description}\033[0m\n\n"
        )

def post_is_skipped(args, ctx, post_id):
    return not args.ignore_skipped and ctx.skipped_posts.is_skipped(post_id)

def get_user_input(args, commentary, post):
    parsed_input = ""
    while True:
        manual_input = True
        if args.yes_no_tag is not None:
            parsed_input = args.yes_no_tag
            manual_input = False
        elif args.auto:
            parsed_input, manual_input = automode.parse(commentary, args.semi_auto, args.quiet, post.id, post.chartags, args.auto_debug, post.source)

        if manual_input:
            print("(h for help)")
            user_input = input("$ ")
            parsed_input = parser.parse(user_input)

        if isinstance(parsed_input, int) or parsed_input.strip() != "":
            return parsed_input, manual_input

class InputProcessResult(NamedTuple):
    edited: bool
    next_post: bool

def command_help(_ctx, _post, _args, _offline):
    print("Configured tags:")
    for short, tag in settings.TAGS.items():
        if not short.startswith("-"):
            print(f" - {short} = {tag}")
    print("Special commands:")
    for short, tag in parser.SPECIAL_TAGS.items():
        print(f" - {short} = {tag[1]}")
    return InputProcessResult(False, False)

def command_skip(ctx, post, _args, _offline):
    print("User requested skip.")
    ctx.skipped_posts.add(post.id)
    return InputProcessResult(False, True)

def command_quit(ctx, _post, args, offline):
    ctx.skipped_posts.flush()
    if offline:
        write_tag_script(args.offline_output, offline.tag_script)
    print(f"gardened {ctx.edit_count} posts")
    sys.exit(0)

def command_browser(_ctx, post, args, _offline):
    link = f"{get_booru_url(args.test_mode)}/posts/{post.id}"
    print(f"Opening link: {link}")
    webbrowser.open(link)
    return InputProcessResult(False, False)

def command_npskip(_ctx, _post, args, _offline):
    if not args.quiet:
        print("User requested non-permanent skip.")
    return InputProcessResult(False, True)

def command_progress_check(_ctx, _post, _args, offline):
    if not offline:
        print("Only works in offline mode.")
    else:
        print(f"Progress: {offline.index}/{offline.post_count} ({offline.post_count - offline.index} left)")
    return InputProcessResult(False, False)

COMMANDS = {
    parser.HELP: command_help,
    parser.SKIP: command_skip,
    parser.QUIT: command_quit,
    parser.BROWSER: command_browser,
    parser.NONPERMANENT_SKIP: command_npskip,
    parser.PROGRESS_CHECK: command_progress_check
}

def process_user_input(parsed_input, manual_input, args, post, ctx, offline, headers):
    if parsed_input in COMMANDS:
        return COMMANDS[parsed_input](ctx, post, args, offline)

    if parsed_input == parser.UNKNOWN_TAG:
        print("Unknown tag. Try again.")
        return InputProcessResult(False, False)

    if not args.quiet:
        print(f"The following tags will be added. Ok?\n{parsed_input}")
    confirm = ""
    if args.yes_no_tag is not None and not args.yes_no_tag_force:
        manual_input = True
    if manual_input:
        confirm = input("(y/N)$ ")
    if confirm.lower().strip() == "y" or not manual_input or (len(confirm.lower().strip()) == 0 and args.yes_no_tag is not None):
        if args.quiet:
            print(parsed_input)
        else:
            print("Sending out change!")

        if offline:
            offline.tag_script[post.id] = parsed_input
            if manual_input:
                input("press enter...")
            return InputProcessResult(True, True)
        else:
            edit_result = tag_edit_post(post.id, headers, parsed_input, ctx.auth, args.quiet, ctx.edit_count, args.test_mode)
            if manual_input:
                input("press enter...")
            return InputProcessResult(edit_result, True)
    elif args.yes_no_tag is not None:
        print("Skip")
        return InputProcessResult(False, True)
    else:
        print("Try again.")
        return InputProcessResult(False, False)

def process_post(args, post, exec_ctx, offline_ctx, headers, commentary):
    print_post_link(args, post.id)

    if post_is_skipped(args, exec_ctx, post.id):
        print("Skipped by user")
        return 0

    if commentary.is_empty() and not args.no_commentary_check:
        print("No commentary; skipping")
        return 0

    while True:
        if not offline_ctx:
            print_tags(post)

        if not args.quiet:
            print_commentary(commentary)

        parsed_input, manual_input = get_user_input(args, commentary, post)
        result = process_user_input(parsed_input, manual_input, args, post, exec_ctx, offline_ctx, headers)
        if result.next_post:
            return 1 if result.edited else 0

def process_offline(args, post, exec_ctx, offline_ctx):
    commentary = offline_ctx.commentary
    return process_post(args, post, exec_ctx, offline_ctx, None, commentary)

def process_online(args, post, ctx, headers):
    # TODO create a NetworkContext type class that has auth + headers + test mode
    commentary = get_commentary(post.id, ctx.auth, headers, args.test_mode)
    return process_post(args, post, ctx, None, headers, commentary)
