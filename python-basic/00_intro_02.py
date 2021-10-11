"""Introducing lists

   Roberto Polli - rpolli@babel.it
"""
# before starting this lesson
#  import the python3 print capabilities
#  using the following statement
#  NB since now you *must* always use
#     parenthesis with print!
from __future__ import print_function


def introducing_lists():
    # it's easy to create a list
    list_a = ["this", "is", "a", "list"]
    # you can append items to a list
    # with the append method
    list_a.append("mutable")

    # check its content with print
    print(list_a)
    # see its length
    len(list_a)

    a = 11
    # range in python 2 returns a list
    # of consecutive ints
    from_0_to_10 = range(a)
    len(from_0_to_10) == a
    # in python 3 things are slightly different
    # so the above code won't work and should
    # should be replaced with the following
    from_0_to_10 = list(range(a))

    # you can get list items by index
    from_0_to_10[0]
    from_0_to_10[11]
    # python lists are doubly linked ;)
    from_0_to_10[-1]
    # please check the manual!
    # help(list)


def slicing():
    # I can slice a list with ":"
    straight = [1, 2, 3, "star"]
    straight[1:3]  # take the middle of the list...
    k = 2  # ... or using a separator
    straight[0:k], straight[k:4]

    straight[:k]  # I can omit the first...
    straight[k:]  # ...and last index


def str_and_list():
    # Strings behaves like lists
    s_a = "Counting: 123"
    # Have length..
    l_a = len(s_a)
    # ..indexes
    print(s_a[0], " ", s_a[-1])
    # and a last element
    s_a[l_a]

    # ...we can even slice them
    f = "prova.txt"
    f[:-4], f[-4], f[-3:]


def iterating_with_for():
    a_list = ["is", "iterable", "with"]
    for x in a_list:
        print(x)
    for x in a_list:
        # python2 does not support the `end` argument
        print((x), end=" ")
        y = x + str(2)
        break  # stop now
    # what's the expected output of the
    # following instruction?
    print(("x,y: ", (x, y)))
    # Differently from C, `for` does not create
    #  a scope


def iterate_with_while():
    a_list = ["is", "iterable", "with"]
    while a_list:
        # pop() modifies a list removing
        #  and returning its last element
        x = a_list.pop()
        print(("pop out %s" % x))
        break  # what happens if I remove this break?
    print(a_list)
    # What's the expected behavior of the
    #  following instructions?
    for x in a_list:
        print((x + a_list.pop()))
    # for + pop() is not always a good idea ;)
