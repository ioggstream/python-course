# Git - simple repository management


## VCS

The importance of tracking changes.

VCS basics:

  - initialize a repo and creating indexes
  - change the software
  - acknowledge (commit) changes
  - eventually revert changes


## Git

Used to maintain the Linux Kernel.

Distributed approach.

## Tracking config modifications

Always timestamp backup copies, don't `.ori`.

```
! SIMPLE_BACKUP_SUFFIX="$(date -I)" cp -bf /etc/hosts /etc/hosts
!ls /etc/hosts*
```

Exercise: Use `date +%s` to timestamp a backup copy.

---

## Create a repository

Track modifications with `git`

```
!git init /etc
ls -l /etc/.git  # this is the index directory
```

```
cd /etc
```

Declare who's modifying files. This will be inserted in 
the commit.

```
!git config --global user.email "jon@example.com"
!git config --global user.name "Jon Doe"
```

### Exercise

Execute the previous command after removing the `--global` flag from the previous command
then run 

```
# Write here the command
# and show the git config file.
!cat .git/config
```

---

Add files to the index

```
! git add /etc/hosts
```

Save files to the local index

```
! git commit -m "Initial snapshot of /etc/hosts"
```

![Git areas](https://git-scm.com/images/about/index1@2x.png)

---

## Basic workflow

Adding a line to the file we discover that

```
!echo "127.0.0.2  localhost2.localdomain" | sudo tee -a /etc/hosts 
!git diff hosts
```

If we like the changes, we can stage them 

```
!git add /etc/hosts
!git status 
```

and finally save them in the repo.

```
git commit -m "Added localhost2 to /etc/hosts"
```
---

## History changes

Now we have an history with two changes, containing:

 - commit messages
 - a commit hash

HEAD is the last commit.


```
git log 
```

![Basic branch](https://git-scm.com/figures/18333fig0310-tn.png)

---

## Reverting changes

We can revert a change using the hash or an history log

```
! git checkout HEAD~1 -- /etc/hosts  # revert /etc/hosts to the previous commit
```

---

## Cheatsheet

---

```
!git init /repo-path  		# Initialize repo
!git add /repo-path/file.txt	# Add file to index
!git commit -m "My changes" 	# Save changes
```

---


```
!date >> /repo-path/file.txt
!git diff
!git commit -a -m "Save all previously added files"
```

---


```
!git log /repo-path/file.txt 	# show changes
!git checkout HEAD~2 -- file.txt # revert file
!git diff			# diff with reverted
!git checkout HEAD -- . # get latest
```


## Branches 

Writing codes and configuration we may want to follow
different strategies and save our different attempts.

git has the *branch* feature allowing to save and work on different
copies of the same repo.

The *tag* feature makes an unmodifiable snapshot of the repo instead.

![Branches](https://git-scm.com/figures/18333fig0313-tn.png)

---

```
# branch our repo
!git checkout -b work-on-my-changes

# and show all branches
!git branch -a
```

---

Modify a file

```
!date > new-file.txt
!git add new-file.txt
!git commit -m "Added a new file"
```

---

We can now switch between branches

```
!git checkout master
ls new-file.txt
```

And switch back

```
!git checkout work-on-my-changes
ls new-file.txt
```

---

## Merge

Once we have consolidated some changes (Eg. test, ...)
we can *merge* the changes into the master branch

```
!git checkout master
!git diff work-on-my-changes
!git merge work-on-my-changes
```

---

After a merge, if the branch is no more useful, we can remove the branch.

```
!git branch -d work-on-changes
```


---

## Selective adding

Selective adding 

```
!git add -p 
```


---

## Remote repositories

```
! git clone ...

```

Show repository configuration. Remote origin.

```
! git config -l 

```

## Pull & push


