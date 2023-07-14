"""
  Author: roberto.polli@par-tec.it

  This file contains an introduction
    to the python for sysadmins course.
    You are welcome to run the follwing examples
    in your ipython shell.
"""


def importing_new_features():
    # ..is easy. Features are collected
    # in packages or modules. Just
    import telnetlib  # to use a

    telnetlib.Telnet  # client

    # We can even import single classes
    #  from a module, like
    from telnetlib import Telnet

    # And read the module or class docs
    help(telnetlib)
    help(Telnet)


def string_formatting():
    # you can print with the print() function
    print("Hello world!")

    # concatenate string with a + sign
    # and using hex notation
    print("Hello" + " " + "World\x21")

    # prefixing a string with 'r' disables the
    # interpretation of the string content
    print("Hello" * 2 + r"World\x21")

    # the chr() function returns the corresponding
    # character of an integer. While \n and \t are
    # just the usual notation for linefeed and tab
    print(chr(72) + "ello\n\tWorld!")

    # triple-quoting allows multi-line strings
    # %s works like in the C printf() function
    # but operates on strings
    # ord() is just the inverse of chr()
    print(
        """The answer is

    %s
    """
        % ord("*")
    )


def basic_arithmetic():
    # This is a comment, while
    a = 1  # is an integer variable
    b = 0x10  # is another integer in hex notation
    # c = 011  # ...another one in C-style oct on python 2...
    c = 0o11  # ...in python 2 and 3

    # I can sum, multiply, and modulus
    print(a + b, 5 % 2)
    print(2 * c)


def variable_assignment():
    # I can assign more than one variable on a string
    a, b, c = 1, 2, 3
    d, stringa_a, stringa_b = a + b, "pippo", "pluto"
    (a, b) = (b, a)  # ...swap them...
    e, f = c, e + d  # but if right-side values are not defined, I get an exception

    # We should respect reserved words and functions, like print, ord...
    print(("ord:\x20", ord))
    ord = 4
    ord("*")  # ...ooops!
    del ord  # fix it up!


def formatting_numbers():
    # bin() and hex() returns a string representation
    # of a number
    a, b1 = hex(10), bin(1)

    # while the format() function can be more flexible
    #  10 = 8ciphers + 2chars for the '0b' header
    binary_with_leading_zeroes = format(1, "#010b")

    # and reversible with
    b1 == int(binary_with_leading_zeroes, base=2)


def old_formatting():
    s_a = "is a string "
    s_a += "that can %s extended" % "be"
    s_a = "%s even with %.6s formatting.\n" % (s_a, "positional")
    s_a = "Align %-10d%% python!" % 100

    print("just prints a string")


def new_formatting():
    # The new str.format function just replaces
    #  %s or %d with {}.
    s_a = "is a string "
    s_a += "that can {} extended".format("be")

    # Further formatting is done using ":", eg.
    #  %.6s -> {:.6}
    #  %3.2d -> {:3.2}
    s_a = "{} even with {:.6} formatting.\n".format(s_a, "positional")

    # Alignment identifiers are simpler: < left , ^ center,  > right
    s_a = "Align {:>10}% python!".format(100)

    print("just prints a string")
