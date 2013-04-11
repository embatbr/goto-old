#!/usr/bin/env python
import sys
from goto import goto_main, label_main, list_main#, goback_main


def bootstrap():
    # Remove bootstrap-like string from argv
    del sys.argv[0]

    if 'goto' in sys.argv[0]:
        return goto_main()
    if 'label' in sys.argv[0]:
        return label_main()
    elif 'list' in sys.argv[0]:
        return list_main()
    elif 'goback' in sys.argv[0]:
        # return goback_main()
        print 'TODO goback'
    sys.exit(-1)


if __name__ == '__main__':
    bootstrap()
