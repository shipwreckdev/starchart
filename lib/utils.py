# Colors.
white = '\033[97m'
green = '\033[92m'
red = '\033[91m'
yellow = '\033[93m'

# Symbols.
info = '\033[93m[!]\033[0m'
failure = '\033[91m[x]\033[0m'
success = '\033[92m[✓]\033[0m'

# Text modifiers.


def bold(t):
    return str('\033[1m%s\033[0m' % t)


def italics(t):
    return str('\033[3m%s\033[0m' % t)


# Remove formatting.
reset = '\033[0m'
