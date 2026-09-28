import parser
import settings

def test_parser():
    # Simple
    assert parser.parse("r") == "commentary_request"

    # Random spacing
    assert parser.parse(" r ee   c") == "commentary_request english_commentary commentary commentary"

    # Invalid
    assert parser.parse("asdf") == parser.UNKNOWN_TAG

    # Invalid and valid
    assert parser.parse("r asdf") == parser.UNKNOWN_TAG

    # Literal tags
    assert parser.parse("~1girl") == "1girl"

    # Negative tags
    assert parser.parse("-r") == "-commentary_request"
    assert parser.parse("-ee") == "-english_commentary -commentary"

    # Special commands
    assert parser.parse("h") == parser.HELP
    assert parser.parse("sk") == parser.SKIP
    assert parser.parse("q") == parser.QUIT
    assert parser.parse("b") == parser.BROWSER
    assert parser.parse("skk") == parser.NONPERMANENT_SKIP
