goto project - easy'n'fast cd'ing
=================================


Instalation
-----------

    $ git clone git://github.com/pauloborges/goto.git
    $ cd goto && [sudo] python setup install


goto
----

The `goto` command is used to navigate through shortcuts.

Using it without parameters returns a list of all currently labels:

    $ goto
    home    /home/borges
    ws      /home/borges/workspace
    docs    /home/borges/Documents

When you pass a label name, `goto` changes the current directory:

    /old/dir$ goto home
    /home/borges$

But if the label does not exists, an error is thrown:

    $ goto connman
    connman is not a valid label.


label
-----

The `label` command is used to save shortcuts to directories.

Using it without parameters returns a list of all currently labels (same as `goto`):

    $ label
    home    /home/borges
    ws      /home/borges/workspace
    docs    /home/borges/Documents

When you pass a simple string, the current directory is saved:

    /home/borges/Downloads$ label downloads
    downloads label points to /home/borges/Downloads.

If the label already exists and points to another directory, an error is thrown:

    /home/borges/workspace$ label ws
    ws label already exists. Use --replace.

The replacement can be ensured by `--replace`:

    { o diretório atual é /home/borges/workspace }
    /home/borges/my_new_workspace$ label --replace ws
    ws label now points to /home/borges/my_new_workspace.

You can remove a label using `--remove`:

    $ label --remove docs
    docs label was removed.

But if the label does not exists:

    $ label --remove connman
    connman is not a valid label.


.goto file
----------

All label information are stored in `~/.goto`. See an example:

    $ cat ~/.goto
    [labels]
    home = /home/borges
    ws = /home/borges/workspace
    docs = /home/borges/Documents


License
-------

See `LICENSE` file.
