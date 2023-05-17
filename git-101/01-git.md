# Git - simple repository management

## Agenda

- VCS intro
- tracking modifications
- using a local git repository
- remote repositories

*Beware*: commands contain small typos. You must fix them to properly complete the course!

## VCS

The importance of tracking changes.

VCS basics:

- initialize a local repo
- change the software
- acknowledge (commit) changes
- eventually revert changes

---

## Tracking modifications

Track modifications of our config files without messing
with the real /etc.

```
!mkdir -p /repo-path
!cp -v /etc/host* /etc/s* /repo-path
```

All operations are local to /repo-path

```
cd /repo-path
```

Always timestamp backup copies, don't `.ori`.

```
! SIMPLE_BACKUP_SUFFIX="$(date -I)" cp -v -bf hosts hosts
!ls -l hosts*
```

Exercise: Use `date +%s` to timestamp a backup copy of `hosts`.

```
# Use this cell for the exercise.
```

---

## Git

A better way of tracking changes.

Used to maintain the Linux Kernel.

Distributed approach.

![Checkout and Push](https://git-scm.com/figures/18333fig0106-tn.png)

---

## Tracing requires identification

Declare who's modifying files. This will be inserted in
the commit.

```
!git config --global user.email "jon@example.com"
!git config --global user.name "Jon Doe"
```

Note: authentication can not be enforced on a local repository.

---

## Create a repository

Track modifications with `git`

```
!git init /repo-path
!ls -l /repo-path/.git  # this is the index directory
```

### Exercise

- get the previous `git config ... user.email`
- remove the `--global` flag  from the previous command
- run it

```
# Write here the command
# and show the git config file.
!cat .git/config
```

---

Enter in the repo directory and check  the status: there
are a lot of files we are not interested in...

```
!git status
```

`.gitignore` lists the files we're not interested in

```
# Ignore all files not starting with h
!echo "[^h]*" >> .gitignore
!git status
```

Now we have all `host*` files to be tracked.

---

## Populate the repo

Add files to the index

```
!git add hosts
```

The file is now *staged* for commit. It's not archived though.

```
!git status
```

Save files to the local index

```
!git commit -m "Initial snapshot of hosts"
```

![Git areas](https://git-scm.com/images/about/index1@2x.png)

---

## Basic workflow

Adding a line to the file we discover that

```
!echo "127.0.0.2  localhost2.localdomain" >> hosts
!git diff hosts
```

If we like the changes, we can stage them

```
!git add hosts
!git status
```

and finally save them in the repo.

```
!git commit  "Added localhost2 to hosts"
```

---

## History changes

Now we have an history with two changes, containing:

- commit messages
- a commit hash

HEAD is the last commit.

```
!git log
```

![Basic branch](https://git-scm.com/figures/18333fig0310-tn.png)

---

## Reverting changes

We can revert a change using the hash or an history log

```
!git checkout HEAD~1 -- hosts  # revert hosts to the previous commit
```

---

## Cheatsheet

Now some git commands, but first create a dir.

```
!mkdir -p /repo-path
!date >> /repo-path/file.txt
!date >> /repo-path/hi.txt
```

---

```
!git init /repo-path    # Initialize repo eventually creating a directory
!git add /repo-path/hi.txt # Add file to index
!git commit -m "My changes"  # Save changes
```

### Exercise

- add `file.txt` to the index and commit

```
# Use this cell for the exercise
```

---

```
!date >> /repo-path/file.txt
!git diff
!git commit -a -m "Save all previously added files"
```

---

```
!git log /repo-path/file.txt  # show changes
```

```
!git checkout HEAD~1 -- file.txt # revert file
```

```
!git diff HEAD  # diff with reverted
```

```
!git checkout HEAD -- . # get *all files* from the latest commit
```

---

## Tags & Branches

Writing codes and configuration we may want to follow
different strategies and save our different attempts.

- *tag*  makes an unmodifiable snapshot of the repo instead.

```
!git tag myconfig-v1 # create a tag
!git tag -l    # list tags
```

- *branch* create a modifiable copy of the code, allowing
     to save and work on different features

![Branches](https://git-scm.com/figures/18333fig0313-tn.png)

---

## Branches

`master` is the default branch

```
!git branch -a
```

Create a branch

```
!git checkout -b work-on-my-changes
```

And list the branches, check the active one!

```
!git branch -a
```

---

Modify a file in a branch

```
!date > new-file.txt
!git add new-file.txt
```

With commit we consolidate the new file in the branch

```
!git commit -m "Added a new file"
```

---

Compare branches

```
!git diff mister
```

Diff supports some parameters

```
!git diff --ignore-all-space master
```

---

We can now switch between branches

```
!git checkout master
!cat new-file.txt
```

And switch back

```
!git checkout work-on-my-changes
!cat new-file.txt
```

---

### Exercise

- Create a new branch named `antani`
- modify `new-file.txt` as you please
- [open a terminal](/terminals/git), and use `git add -p` to stage the changes. What does it do?
- commit the changes

```
# Use this cell for the exercise
```

---

## Checkout troubleshooting

If you change a file, git won't make you checkout
to avoid missing changes.

```
!date >> new-file.txt
!git checkout master
```

You have to remove the changes or commit them (in another branch too)

```
# Use this cell for the exercise.
```

---

## Merge

Once we have consolidated some changes (e.g., test, ...)
we can *merge* the changes into the master branch

```
!git checkout master
```

Before merging, we have to check the differences

```
!git diff work-on-my-changes
```

And finally merge

```
!git merge work-on-my-changes
```

---

After a merge, if the branch is no more useful, we can remove it.
Note: before deleting a branch, you can double-check available
branches with `git branch -a`.

```
!git branch -d work-on-changes
```

If there are unmerged changes, git doesn't allow deleting a branch.

Exercise:

- use `git branch -d` to remove the `antani` branch
- what happens?
- replace `-d` with `-D`. Does it work now?

```
# use this cell for the exrcise

```

---

## Selective adding

You can stage partial changes with:

```
!git add -p
```

---

## Remote repositories

Remote repos may be either https, ssh or files.

```
! mkdir -p /repo-tmp && cd /repo-tmp && pwd # use another directory ;)
```

Exercise:

- what happens in the following cell?

```
!pwd
```

Go to the correct directory now.

```
cd /repo-tmp
```

---

### https repo

Git clone downloads a remote repo, with all its changes and history.
Try with a remote https repo.

```
!git clone https://github.com/ioggstream/python-course/ python-course
```

Now enter in the repo directory

```
cd /repo-tmp/python-course
```

Show repository configuration. Which is the remote origin?

```
!git config -l
```

The remote repo is retrieved with all its changes and history

```
! du -ms .git
```

And `log` can show branches and merges.

```
!git log --graph
```

---

### file repo

A local repo can be cloned too, and has the same features
of a remote one. It's actually a remote `file://` uri.

```
!git clone /repo-tmp/python-course /repo-tmp/my-course
```

Now move to the new directory

```
cd /repo-tmp/my-course
```

Show repository configuration. Which is the remote origin?

```
!git config -l
```

---

## Pull & push

You can add new files to a repo with the above workflow:

- create a branch with `git checkout -b test-1`
- add a new file
- stage changes with `git add`
- commit with `git commit`

```
# Use this cell for the exercise
```

Now that your changes are on your local repo, you can synchronize / upload them to the remote copy
with:

```
!git push origin test-1
```

Remember:

- origin is the URI specified by `git config -l`
- `test-1` is the branch name where you want to upload

To upload changes to the remote master (default) branch, you need to

- merge the changes to your local master

```
!git checkout master
```

Check the differences

```
!git diff test-1
```

And finally merge

```
!git merge test-1
```

Exercise:

- check the master history;
- check the difference with the last commit.


Finally, push changes to `origin/master`

```
!git push origin master
```

To make it work, you need to be authenticated/authorized with the remote repo ;)
