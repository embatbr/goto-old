#!/usr/bin/env python
import sys
from goto import goto_main, label_main, list_main


def bootstrap():
    # Remove bootstrap-like string from argv
    del sys.argv[0]

    if sys.argv[0] == 'goto':
        return goto_main()
    if sys.argv[0] == 'goto-label':
        return label_main()
    elif sys.argv[0] == 'goto-list':
        return list_main()
    elif sys.argv[0] == 'goto-back':
        print 'TODO goto-back'
        sys.exit(0)

    sys.exit(-1)


if __name__ == '__main__':
    bootstrap()
