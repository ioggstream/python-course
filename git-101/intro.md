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
export SIMPLE_BACKUP_SUFFIX="$(date -I)"
cp -bf /etc/hosts /etc/hosts
```

Exercise: Use `date +%s` to timestamp a backup copy.


## Indexing directories

Track modifications with `git`

```
git init /etc
ls -l /etc/.git  # this is the index directory
```

Add files to the index

```
git add /etc/hosts
```

Save files to the local index

```
git commit -m "Initial snapshot of /etc/hosts"
```

![Git areas](https://git-scm.com/images/about/index1@2x.png)


---

Adding a line to the file we discover that

```
echo "127.0.0.2  localhost2.localdomain" | sudo tee -a /etc/hosts 
git diff hosts
```

If we like the changes, we can stage them 

```
git add /etc/hosts
git status 
```

and finally save them in the repo.

```
git commit -m "Added localhost2 to /etc/hosts"
```
---

Now we have an history with two changes, containing:

 - commit messages
 - a commit hash

HEAD is the last commit.


```
git log 
```

---

We can revert a change using the hash or an history log

```
git checkout HEAD~1 -- /etc/hosts  # revert /etc/hosts to the previous commit
```

---

## Cheatsheet

Create a repository: git init /path/to/repo
Add file to index: git add /path/to/file

