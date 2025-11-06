import argparse

def parse_args():
    aparser = argparse.ArgumentParser()
    aparser.add_argument("--page", type=int, default=1)
    aparser.add_argument("--query", type=str, default="-commentary+-commentary_request")
    aparser.add_argument("--mode", type=str, default="garden", help="garden: gardening commentary tags. add: add posts with no commentary to fav group")
    aparser.add_argument("--group", type=int, default=0, help="posts with no commentary will be added to this fav group (necessary if mode is add)")
    aparser.add_argument("--random", action="store_true", help="select posts at random")
    aparser.add_argument("--limit", type=int, default=None, help="change the post limit")
    aparser.add_argument("--ynt", type=str, default=None, help="yes/no tag: press enter to apply tag for each post found, any key + enter to skip")
    aparser.add_argument("--ynty", action="store_true", help="automatically add the chosen tag when using yes/no tag. (warning: dangerous. only use if you know what you're doing.)")
    aparser.add_argument("--auto", action="store_true", help="automatically detect language and add tag. if language not detected, skip post")
    aparser.add_argument("--semi-auto", action="store_true", help="auto mode but don't skip post, ask user instead")
    aparser.add_argument("--en-log", action="store_true", help="logs enlgish commentaries into files, for analysis")
    aparser.add_argument("--quiet", action="store_true", help="removes unnecessary input, only for auto mode")
    aparser.add_argument("--same-page", action="store_true", help="stay on the same page")
    args = aparser.parse_args()
    return args
