---
author: mkirc
title: README
...

# git blog

TL;DR - If you just want to use this project, navigate
to the [bottom](#last-words) of this page, and get going!

Well into the second wave of an well known global
pandemic, i came to the conclusion that i wanted to
start a blog. There is a wide range of solutions
for this kind of problem, some of which are
[big php frameworks](https://wordpress.com), some make
[hosting and getting started easy for you](https://guides.github.com/features/pages/)
and generally [show](https://www.gatsbyjs.com/)
[great](https://getnikola.com/)
[variety](https://hyde.github.io/).
Needless to say, none of the available options appealed to me.
What i wanted is best explained with the words of acat,
a good friend, who co-maintains this site:

> I just want to type stuff into a terminal!

All started when [fidex](https://github.com/fidex) told me
about [git hooks](https://githooks.com/), which you can think
of as entrypoints to code execution at various steps in your
interaction with git. He uses this concept at work, to autoformat
code and maybe run some tests or such, which is probably the
intended usecase. Aaanyway, instead of doing boring exiting work
for which you are paid very well, you could be, idk, writing
your _own static site generator with git hooks_ ***for no pay
whatsoever***. Sweet, huh?

# "Design Spec"

* want to write stuff in markdown

* want to use git for everything else

After a while it dawned to me that since every post would be
versioned one way or another, it would be cool (and probably
really embarrassing) to display its version history.
I talked to [fidex](https://github.com/fidex)
about this and we explored potential directory structures and
modes of operation. We came to the conclusion, that these points
should be adressed:

* sites should be static html

* commit messages should take a prominent place

* blog should be self-documenting

* the posts of name [commit-hash].html should reside in directories  
  of name [post-name]/, so the url would be `/[post-name]/[commit-hash].html`

What we came up with is the following sketch for the final website.
The observable reader will notice the similarities to this very site
she or he is experiencing ***right now***:

```
+--------------|---------------------------------------------------+
|              |   / latest \   ljds0932   ijd98u34     jids09e    |
|-----------------/          \-------------------------------------|
|              |                                                   |
| Post 1       |                                                   |
|              |    bluhblablubhalbhalabualbluablabjlluab          |
| Post 2       |    balabolablbalubalabubaualbaulbaluabla          |
|              |    and then balbalbalablaablabblablbabal.         |
| Post 3       |                                                   |
|              |                                                   |
|              |                                                   |
|              |                                                   |
|              |                                                   |
|              |                                                   |
|              |                                                   |
|              |                                                   |
+--------------|---------------------------------------------------+
```

Another thought was this:
It would be cool be possible to *flip the whole thing around*, so that the
side-nav and top-nav change roles, so you could see all the posts modified in one commit.
This should be done in js and no change in the overall directory structure should neither
be made nor the whole thing be compiled into two structures representing the two orderings.
This provides a reasonable fallback for non-js browsers.

There was a funny moment after exchanging ideas for a while, when we realized
that while fidex was talking about a git[lab|hub]-ish kind of setup with
git[lab|hub] pages, i meant just *git*, and a webserver.
Write, commit, push. The only kind of 'pipeline' existing
in a local skript which compiles the html behind a post-commit hook and a script
to copy the whole stuff to the right place behind a post-receive.
The actual difference is actual kind of subtle, since the pages approach only
would need a very easy .yml. If somebody likes, they can come up with
such a .yml, ill be happy to include it here, ht and be generally welcoming.


## The Plan

To achieve the sketched out atrocities, i propose the following deeds:

* Write a post in a posts/ directory, commit its changes to git

* get the versions from git, in reverse chronological order

* for each post, for each commit generate the content to compile a  
  self-contained .html document

* generate said documents, save it to a public/[post-name]/ directory

* auto-commit those changes

* on a 'git push', upload those changes to a server, copy public/ into  
  a webserver's web directory

* ponder about the [important things](https://www.youtube.com/watch?v=9wyhhxOZazI), collect your thoughts, repeat

Modeling the ideas above like so (pondering omitted for brevity):

```
                                              +-------------------------+
+-----------+                                 |  tmp/post-1/            |
| posts/    |                                 |-------------------------|
|-----------|                                 |                         |
|           |                                 |                         |
| post-1.md |                                 |  commit-1.md            |
|           |      +-------------------+      |  commit-1-nav-top.html  |
| ...       |----- | scripts/py/run.py |----> |  commit-1-nav-side.html |
|           |      +-------------------+      |                         |
| post-n.md |                                 |                         |
|           |                                 |   ...                   |
+-----------+                 +-------------- |                         |
                              |               |                         |
                              |               |  commit-n-md            |
                              |               |  commit-n-nav-top.html  |
                              |               |  commit-n-nav-side.html |
             +-----------------------------+  |                         |
             | scripts/bash/makePages.bash |  +-------------------------+
             +-----------------------------+                             
                              |                                          
                              |                                          
                              |                                          
                              |                                          
                              |                                          
                              |                                          
                              |                                          
                              V                                          
                 +-------------------------+                             
                 |  public/post-1/         |                             
                 |-------------------------|                             
                 |                         |                             
                 |  commit-1.html          |                             
                 |                         |                             
                 |  ...                    |                             
                 |                         |                             
                 |  commit-n.html          |                             
                 |                         |                             
                 +-------------------------+                             
```

After a nights sleep i realized, that the navigation areas have to be generated
from the list of posts/commits. Here is why:

* The top-nav has to be compiled from the list of commits touching the post  
  anyway, since its *kinda* unique to a given post.

* I'd like the current page to be highlighted and probably ignoring all kinds  
  of possible ways to do that, i just generate the nav-elements with according  
  markup and css my way around it (yes, 'to css smth' is totally a verb).


# First steps

### Setting up a simple git repository

Assuming a server with ssh access, pubkey auth and git installed.

First we create a directory in which the bare repo should reside in.
Here we set it up in the users home, but it is possible to set it in
any directory the user has read/write/execute in. This is why we
differ from the approach presented in the 
[git book](https://git-scm.com/book/en/v2/Git-on-the-Server-Setting-Up-the-Server),
where we set up a git user with a restricted shell. But for the post-commit hook
to work we need a somewhat less restricted environment. Probably some time in the
future we have to think about multi-user, but since this is a essentially single-user
right now, i just use my own account. 

On the server, in a dir $DIR with the afore mentioned permissions:

```bash
mkdir git-blog.git && cd git-blog.git
git init --bare
```
Now on the local machine:

```bash
mkdir git-blog && cd git-blog
git add .
git commit -m 'initial commit'
git remote add origin ssh://$USER@$IP:$DIR
git push -u
```

# pygit2

For the revisions to be parsed, we need some kind of interface to the git-repo at hand.
The [official git documentation](https://git-scm.com/book/en/v2/Appendix-B:-Embedding-Git-in-your-Applications-Libgit2)
suggests a variety of options to do so, but the most
appealing to me seemed [pygit2](https://www.pygit2.org/), 
since 
[you need python](https://sdtimes.com/wp-content/uploads/2014/08/0815.sdt-python.jpg).
Of course, as always, when we start to play around with some bib, lets fire up
a [virtualenv](https://virtualenv.pypa.io/en/latest/):

```
virtualenv -p $(which python3) venv/
source venv/bin/activate
pip install pygit2
```

Normally i start finding my way around new libraries in the REPL, so
ill encourage the reader to init a new git repo, commit some dummy
files and type away some of the examples from the docs.

Depending of your mental model of git you will arrive at a good grasp
what is going on in the object db soon.
To get started, have a look at the [Objects](https://www.pygit2.org/objects.html)
pygit2 provides. Those are (essentially):

* Blobs  
Those are the binary versions of the files themselves

* Commit  
Those are what you would expect ;) From the docs:  
> A commit is a snapshot of the working dir with meta informations  
> like author, committer and others.

* Trees  
The tree of directories and files a commit touched

### Index, commits and Sorting

Lets assume we made ourselves at home with pygit2, init'd a repo and commited some
changes to a bunch of files. The starting point in pygit2 is (for our purposes) 
the `Repository` class. We instantiate it with a path to the `.git/` directory:

```python
repo = Repository('./git')
```

We obtain a flat list of files in the repo via `repo.index`. Easy, right? We can now
do more complex tasks, like listing only paths under a specific directory with the usual
pythonic path tools, like `pathlib.Path`.

Next, we typically want to look at the commits we made. pygit2 again makes this easy:
We access the last commit made via `repo[repo.head.target]`. Note, that the `repo.head`
is a shorthand for `repo.references['HEAD'].resolve()`. Another nice thing to notice
is, that `repo.head.target` returns a oid, and you can access any Object via repo[oid].

Looking at the last commit is fine, but we need to go deeper, ie a time-sorted
collection of commits for a given file.

Consider the following method:

```python
def commitsForFiles(repo, lastCommit, filepathList):
    '''
    takes a repo, a commit and a list of filepaths,
    performs a TIME_SORT and
    returns {filepath: [{commit.oid, blob.object}] }
    '''
    files_commits = dict()

    for commit in repo.walk(lastCommit.id, GIT_SORT_TIME):
        for filepath in filepathList:
            if filepath in commit.tree:
                if not filepath in files_commits.keys():
                    files_commits[filepath] = []
                _oidObjTuple = (commit.oid, commit.tree[filepath])
                files_commits[filepath].append(_oidObjTuple)

    return filterUniqueCommits(files_commits)
```

We put in the repo, the head-commit, and a list of interesting files.
`repo.walk` provides a nice interface for different walks down the commit-tree.
We only care for a time-sorted view, so we go with `GIT_SORT_TIME`.
For a complete overview over the different modes please have a look at
[commit log](https://www.pygit2.org/commit_log.html).
So, after we filter out the uninteresting paths, we end up with a dict, which maps
filepaths to commits. But since a commit is essentially a snapshot of the whole repo,
we also get commits for a file in the list, if another is modified in the same commit,
so we have to filter for uniques. Since a oid of a blob is just its sha-1 hash, we
can easily do so. For my implementation check out
[github](https://github.com/mkirc/git-blog/blob/master/scripts/py/classes/helper.py).

So, we saw how to access files and commits. Blobs provide an easy interface to the
files contents via `blob.data` and i'll just skip over them.
So lets assume we found the commits for the files we are interested in, can access their
contents and write them to a tmp directory. Now its time to handle the markdown itself.

# HTML generation

## Nav-Links

Well, thats kind of boring, right? As i mentioned earlier, i need to generate the
nav-links. Its in the repo, under
[templateGenerator.py](https://github.com/mkirc/git-blog/blob/master/scripts/py/classes/templateGenerator.py).
I tried to be careful with escaping html, the rest should be straightforward.
Lets move on to...

## making Pages

[pandoc](https://pandoc.org/) is just the best. From the website:
> Pandoc is a Haskell library for converting from one markup format to another,
> and a command-line tool that uses this library.

For the purpose at hand we want to convert markdown to html, and use a html-template for that.
A quick search sent me to [jilles van gurp's site](https://dev.to/jillesvangurp/using-pandoc-to-create-a-website-1gea),
where i found a nice implementation on which i could base the skript to compile
the html on. You can find it [here](https://github.com/mkirc/git-blog/blob/master/scripts/bash/makePages.bash).
Its basically a wrapper around pandoc. Let's take a look at that:

```bash
makePagesWithPandoc() {

    echo 'Creating page for '"$2"'...'
    local outPath=("${PUBDIR:?}"/"${1##*/}"/"${2%.*}".html)
    local inPath=("$1"/"$2")
    local sideNav=("$1"/"$3")
    local topNav=("$1"/"$4")
    # cat "$inPath"
    # echo $outPath

    "$pandocPath" --from markdown_github+smart+yaml_metadata_block+auto_identifiers "$inPath" \
        -o "$outPath" \
        --template templates/page.html \
        -V topNav="$(cat "$topNav")" \
        -V sideNav="$(cat "$sideNav")" \
        -V title="${1##*/}" \
        --toc

    return

}
```
First we do some path-related shenanigans, which are layed out in [the plan](#the-plan).
The `--from`-flag allows for certain 'Extensions'. We tell pandoc to identify the
input as github-flavoured markdown, use a certain template for compilation and write
that out to an specified path. `-V` allows for definition of variables used inside
the template, where we pass in the navigation elements from before.`--toc` generates
a handy table of contents from the headlines.
Assuming we handled all paths correctly, we are almost done! We compiled html sites
in the correct directory structure, so that a webserver can serve them.
Notice, that the css is in another file and we reference it in the template as we
would usually do in an website.

# git hooks

The whole html compilation should stay local, since we dont want our
server waste precious ressources with builds, so we want to have a mechanism
which does the magic after we committed.

Enter:

## post-commit hook

[Warning]

> The following code is really hacky and can potentially insult
> the intelligence of some readers. It should not be used in ***any*** way,
> and i probably should not be posting it on the internet.

But anyway:

```bash
#!/usr/bin/env bash

set -e

assembleVersions() {
    venv/bin/python scripts/py/run.py
}

makePages() {
    bash scripts/bash/makePages.bash
}

isAutocommit() {


    if [[ "$(ps -ocommand= -p $PPID)" == "git commit --amend -m <git-blog autocommit>" ]]; then
        return 0
    else
        return 1
    fi
}

autoCommit() {
    git add -A
    git commit --amend -m '<git-blog autocommit>'
}

main() {

    if isAutocommit ;then
        exit 0
    else
        assembleVersions
        if [[ "$?" == 0 ]]; then
            makePages
            autoCommit
        fi
    fi
}

main
```

So, long story short: This automates away the compilation and and
then autocommits the changes. Since this is called every time a commit
is triggered, it has to check if it is triggered by the autocommit,
in which case it should exit, or else infinite self-calling will ensue.

You bet i felt stupid when this happened the first time. I am not
quite shure if i feel wiser now...

This is nice. *sips coffee* Now only the last step needs to be done.
When the utter crap^w^w cool blogpost we wrote and compiled finally
arrives at our faithful server, it has to be copied into the right spot.
Thankfully git hooks have our back again this time, with the

## post-recieve hook

As before, we can place a script in the `hooks/` directory, but this time in
the bare git repo we set up on our server, which we called `git-blog.git`.
It has to be called `post-recieve` and made executable.

You can find the actual script [here](https://github.com/mkirc/git-blog/blob/master/scripts/bash/post-receive), but lets focus on a function we called 'deploy':

```bash
deploy() {

    local target=("$(pwd)"/../git-blog-work/)

    while read oldrev newrev rev; do
        if [[ "${rev##*/}" == master ]]; then
            echo 'Recieved push to master, copying repo to target:'
            echo "${target:?}"
            git --work-tree="$target" --git-dir="$(pwd)" checkout -f
            echo 'done.'
            echo 'Changing dir to target'
            cd "${target:?}"
            # Making shure no container is running
            docker-compose down && \
                docker-compose -f docker-compose.prod.yml up --build -d
        else
            echo 'Pushed to '"${rev##*/}"', which is not master.'
        fi
    done
}
```
As you can see, we first declare our work-tree, which is where we want to put our
files, so a webserver can serve them. The next line is where parameters passed
to the script via are read, which is how you can determine which branch got updated
in the last push. Then we force-checkout (read: copy) the changes to our working
diractory, change into it and issue an docker-compose command to make shure
our changes are taking effect. And thats it.


# last words

## Installation

Are you shure you want to do this?

### On your local machine

This assumes you obtained a copy of [this](https://github.com/mkirc/git-blog)
unholy piece of cr^w^w^w^wi repository and
that your OS is a linux, with bash and python3 installed. I also
use the virtualenv wrapper here, which can be installed from your
package repository, but this is not an hard requirement. If you are
debian-based you can install it with apt:

```bash
sudo apt install virtualenv
```

Go to the base directory of the project and cast a new
python environment into a subdirectory called `venv/`.
After activation of said env, install the requirements.

```bash
virtualenv -p $(which python3) venv/
source venv/bin/activate
pip install pygit2
```

### On the remote machine

Here we assume [docker](https://www.docker.com/) and
[docker-compose](https://docs.docker.com/compose/) installed. The installation
process is not really in scope of this project, so i'll point you to
their documentation.

To initialize a bare git repo, we have to issue the following commands
in a directory where the user has read/write/execute-rights, and a working
directory:

```bash
mkdir git-blog.git git-blog-work && cd git-blog.git
git init --bare
```

Then all we have to do is to place [this script](https://github.com/mkirc/git-blog/blob/master/scripts/bash/post-receive)
in the git-blog.git/hooks directory and make it executable.


# Usage

In directory `posts/`:

```bash
echo '# what a nice example' > stuff.md 
git add st[TAB]uff.md
git com[TAB]mit [TAB]stuff.md -m 'wrote stuff'
git push
^D
```

You can view your local changes before pushing by leaving a
local nginx-server running, via

```bash
docker-compose up --build -d
```

It runs per default on port 80.

