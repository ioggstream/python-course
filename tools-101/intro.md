<!-- #region solution="hidden" -->
# Devops Tools 101

This is a course on the tools you will need to work using the devops methodology.

The course is based on an hands-on approach, so you will need to do the exercises
and execute the commands on the course environment.

We will start presenting the course environment, then we will go through the tools:

Docker, Git and Python.
<!-- #endregion -->

---

# Jupyter

Is the course environment in your browser.
It requires a modern browser and an internet connection supporting
websockets. If your proxy does not support websockets, you will not be able to
execute the code.

While you might find the exercises' solutions in the environment,
it is important for you to spend some time trying to do your homework!
This will help you to remember the concepts and to learn how to use the tools.

---

## What can I do with Jupyter?

You can:

- [open a (named) terminal on the local machine](/terminals/example)
- [edit an existing file](/edit/notebooks/untitled.txt)
- add more cells with `ALT+ENTER`

----

Try to add a cell below this one and write some text in it.

```python
# Add a new python cell with ALT+ENTER.
```

---

## Python terminal

With Jupyter, you have a Python terminal at your disposal.
You can run Python code:

```python
# You can evaluate maths and strings
s = 1
print("a string and the number " + str(s))
```

Jupyter remembers the variables you define in a cell, so you can use them in the next cells.

```python
# Evaluate this cell with SHIFT+ENTER
s = s + 1
print("now s is increased " + str(s))
```

Since Jupyter remembers the variables, you can run the cells in any order you want.
This means that sometimes, you need to "reset" the environment, to start from scratch.

This can be done with the "Kernel > Restart" or "Kernel > Restart & Clear output" menu.

----

To run simple, non interactive bash commands in a python cell, prefix them with `!`.
When you run a cell, the output is displayed below the cell.

```python
! ls -l
```

----

Another way to run bash commands is to use the `%%bash` magic keyword.

```python
%%bash
A=1
echo $A
```

----

<!-- #region -->

During the course, you will need to execute some shell code, that is rendered like the following

```bash
# Don't execute this non-interactive cell.
echo "What is your name?"
read name
echo "Hello $name!"
```

In these cases, you need to [open a terminal on the local machine](/terminals/example), for example following links like [this one](/terminals/example) and type the commands there. This is especially required for interactive tasks.

<!-- #endregion -->

<!-- #region solution="hidden" solution_first=true -->
#### Exercises

Exercise solutions are folded. You can show them clicking on the `+` sign.

<!-- #endregion -->

```python

```

<!-- #region solution="hidden" solution_first=true -->
# Don't do that :D just try and

![Do your homework](http://s2.quickmeme.com/img/43/438ccdc454bc53dfe79f6190ee43b2be19bd578ad002426efcf90f7a327cedd1.jpg)
<!-- #endregion -->

```python solution="hidden"

```

---

# Python

Go to the [basic python course](/tree/notebooks/rendered_notebooks/python-basic)

---

# Git

is the powerful versioning system used to distribute this course

Go to your [git beginners course](/notebooks/notebooks/rendered_notebooks/git-101/01-git.ipynb)

---

# Docker

Docker is a lightweight container environment. Jupyter and all other "machines" are based on docker.

[Presentation (in Italian)](https://docs.google.com/presentation/d/15swQ2gHWAKYAm_ZbBme9rmzV1CpLNl1npvgrUyODu1s/)

Go to your [docker beginners course](/notebooks/notebooks/rendered_notebooks/docker-101/)

<!-- #region -->
## Setup with digitalocean (if you don't have your server)

Create and `ssh` into your docker droplet.

![Create droplet](https://cdn.pbrd.co/images/GA8dkaJ.png)

## Setup example

[![asciicast](https://asciinema.org/a/9xqX4akNND7Yc0Q1sTb3ZnEhI.png)](https://asciinema.org/a/9xqX4akNND7Yc0Q1sTb3ZnEhI)

## Docker must listen on 172.17.0.1:2735

```
# vim /etc/systemd/system/multi-user.target.wants/docker.service
[Service]
...
ExecStart=/usr/bin/dockerd -H fd:// -H tcp://172.17.0.1:2375
...
#wq!

systemctl daemon-reload
systemctl restart docker
```

## Clone and start

```
git clone https://github.com/ioggstream/python-course.git
cd python-course/ansible-101
make course

```

## Connect to jupyter

```
firefox http://43.32.54.212:8888/tree/notebooks/?token=....
```

<!-- #endregion -->
