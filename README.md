## Installation

Are you shure you want to do this?
Have you read the [blog post](https://pleorama.de/blog/README/faa3ce6.html)?

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

