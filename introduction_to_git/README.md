# Introduction to Git

- [Introduction to Git](#introduction-to-git)
  - [Introduction to version control with Git](#introduction-to-version-control-with-git)
  - [Making changes](#making-changes)
  - [Git workflows](#git-workflows)
  - [Collaborating with Git](#collaborating-with-git)
  - [Terminology](#terminology)

## Introduction to version control with Git

* **Version** is the contents of a file at a given point in time. It also includes metadata, or information associated with the file, such as the author, where it is located, the file type, and when it was last saved.
* **Version control** is a group of systems and processes to manage changes made to documents, programs, and directories. It
  * allows us to track files in different states.
  * lets multiple people work on the same files simultaneously.
  * allows us to combine different versions, identify a particular version of a file, and revert changes.
* **Git** is an opensource program for version control. It's scalable to easily track everything from small solo projects to complex collaborative efforts with large teams.
* **GitHub** is a cloud-based Git repository hosting platform.
* Adding a file to the stage: `git add [filename]`.
* Comparing file:
  * Comparing an unstaged file with the last commit: `git diff [filename]`.
  * Comparing a staged file with the last commit: `git diff -r HEAD [filename]`. The flag `-r` stands for *revision*.

## Making changes

* The **commit structure** consists of three parts:
  * The first is __*the commit itself*__, which contains metadata such as the author, commit message, and time of the commit.
  * The second part is a __*tree*__, which tracks the names and locations in the repo when that commit happened.
  * The third one is a __*blob*__, which contains a compressed snapshots of the contents of the file when the commit happened.
* **Git hash** is a 40 character string of numbers and letters.
  * Is commit identifier.
  * Hashes enable Git to share data efficiently between repos.
  * If two files are the same, their hashes will be the same.
* **Finding a particular commit**:
  * Run `git log` or `git log --oneline` to view all commits and their hashes.
  * Run `git show [hash]` to see what changed in that commit. We __*need only*__ the first six-to-eight characters of the hash.
  * The output of `git show` consists of two parts: the log entry for that commit at the top, followed by ~~a `diff`~~ **an output showing** ~~changes between the __*file in that commit*__ and the __*current version*__ in the repo~~ **the content of files in that commit**:
* **Viewing changes:**
  * `HEAD` maps to the last commit. `HEAD~[i]` maps to the `[i+1]`th-to-last commit / the `[i+1]`th most recent commit.
  * Viewing changes between a specific commit and the last commit: `git diff HEAD[~i]`.
    * `a` is the `[i+1]`th most recent commit.
    * `b` is the last commit.
  * Viewing changes between two commits: `git diff HEAD~[i] HEAD~[j]` or `git diff [hash_i] [hash_j]`.
  * Viewing who made the last change to each line of a file: `git annotate [filename]`.
* **Undo changes BEFORE committing** (in/not in the stage):
  * After adding (a `git add`) your file(s) will be added to the stage. Before the committing (a `git commit`), these files are still in the stage, its state is **_staged_**.
  * Unstage a file: `git reset HEAD [filename]`.
  * Unstage all files in the stage: `git reset HEAD`.
  * Before adding (a `git add` command), the state of your file(s) is **_unstaged_** as it hasn't yet added to the stage.
  * Undo changes to an unstaged file: `git checkout -- [filename]`.
    * `checkout` means switching to a different version. By default, it switches to the last commit.
  * Undo changes to all unstaged files: `git checkout .`
    * `.` refers to the current directory.
    * The command above will undo changes to all unstaged files in the current directory and its subdirectories.
  * We can combine commands above to **_unstage and undo_** file(s). For instance,
    * unstaged all files which are added to the stage: `git reset HEAD`.
    * then undo changes to all unstaged files: `git checkout .`.
* **Restoring and Reverting:**
  * Customizing the log output:
    * limit the number of commits to display: `git log -[n]`. For instance, `git log -3` shows the three most recent commits.
    * look at the commit history of one file: `git log -[n] [filename]`. For instance, `git log -3 report.md`.
    * restrict log from a date: `git log --since="[Month Day Year]"`. For instance, `git log --since="Apr 2 2022"`.
    * restrict log between dates: `git log --since=[Month Day Year] --until=[Month Day Year]`. For instance, `git log --since="Apr 2 2022" --until="Apr 11 2022"`.
  * Restoring an old version of a file:
    * Revert to the version of the last commit: `git checkout -- [filename]`.
    * Revert to a version from a specific commit: `git checkout [commit] [filename]` or `git checkout HEAD~[n] [filename]`.
  * Restoring a repo (all files) to their state in a particular commit: `git checkout [commit]` or `git checkout HEAD~[n]`.
* **Cleaning a repository:**
  * List all untracked files: `git clean -n`.
  * Delete all untracked files: `git clean -f`. :warning: This can't be undone.

## Git workflows

* **Configuring Git**:
  * Levels of settings: Git has a range of customizable settings that can simplify our version control tasks, resulting in improved productivity. Git has three levels of settings:
    * `--local`: settings for one specific project, stored at `.git/config` within the repo.
    * `--global`: settings for all of our projects, stored at `~/.gitconfig` or `~/.config/git/config`.
    * `--system`: settings for every users on this computer, stored at `/etc/gitconfig`.
    * Each level overrides the one above it, so `local` settings take precedence over `global` settings, taking precedence over `system` settings.
  * Access a list of customizable settings at all levels: `git config --list`.
    * at local level: `git config --list --local`.
    * at global level: `git config --list --global`.
    * at system level: `git config --list --system`.
  * Modify a setting: `git config [level] [setting] [value]`. For instance, change username to VU Anh Tuan at global level: `git config --global user.name "VU Anh Tuan"`.
  * Find out where a specific setting is set: `git config --show-origin [setting]`. For instance, `git config --show-origin user.name`.
  * List all settings and where they are: `git config --list --show-origin`. It will list all the settings going with the file where each setting is defined. Note that:
    * `.git/config`  within the repo is `local` level.
    * `~/.gitconfig` or `~/.config/git/config` is `global` level.
    * `/etc/gitconfig` is `system` level.
  * Using aliases is a cool way to to speed up our workflow for common commands. We can set up an alias through global settings by using the syntax `git config --global alias.[alias_name] [command]`. For instance, creating an alias for commiting files by executing `ci`: `git config --global alias.ci "commit -m"`. After creating that alias, we can commit files by using `git ci`.
  * Ignoring specific files by creating the file `.gitignore` then declare filenames that we want to ignore.
    * We can use wildcard patterns like `*` to specify the files that we don't want Git to pay attention to.
    * Commonly ignored files: API keys, credentials, system files, or software dependencies.
* **Branches**: enable us to have multiple versions of our work and track each version systematically.
  * Each branch is like a parallel universe: some files might be the same, others might be different, or some may not exist.
  * Branches are benificial as they allow multiple users to work simultaneously and track everything, which minimizes the risk of conflicting versions.
  * List existing branches: `git branch`.
  * Creat a new branch: `git checkout -b [branch_name]`.
  * Compare two branches: `git diff [branch_1] [branch_2]`.
* **Working with branches**:
  * Switch to a branch: `git checkout [branch_name]`.
  * Merge branches: `git merge [source] [destination]`. For instance, to merge the branch `summary-statistics` into the branch `main`, we do `git merge summary-statistics main`.
* **Handling conflict**:
  * A conflict occurs when a file in different branches (or commits) has different contents that prevent them from automatically merging into a single version.
  * An example of merging conflict is shown below. In the conflict:
    * lines before `<<<<<<< HEAD` are the same between two branches. For instance, in the given example, it's the two first lines.
    * lines between `<<<<<<< HEAD` and `=======` are only in the `HEAD` commit of the current branch. In the given example, it's the third and fourth lines.
    * lines between `=======` and `>>>>>>> feature/add-conclusions` are only in the branch `feature/add-conclusions`. In the given example, it's the fifth line.
```
# Mental Health in Tech Survey
TODO: include link to raw data.
<<<<<<< HEAD
TODO: remember to cite funding sources!
TODO: add data visualizations.
=======
TODO: add conclusions section.
>>>>>>> feature/add-conclusions
```

## Collaborating with Git

* **Creating repos**:
  * Create new repo from scratch: `git init [repo_name]`.
  * Converting an existing project into a repo: `git init`.
  * :warning: Caution: avoid creating a Git repo inside another Git repo. If we do this, Git will get confused about which directory it needs to update.
  * Generally, nested repos are not necessary except when working on extremely large and complex projects.
* **Working with remotes**:
  * Clone a local repo and name it: `git clone [local_path] [new_name]`. For instance, the command `git clone /home/john/repo john_anxiety_project` clones the repo `/home/john/repo` and names the cloned repo as `john_anxiety_project`.
  * Clone a remote repo on to a local repo: `git clone [URL]`. When cloning a repo:
    * Git remembers where the original was.
    * Git stores a remote **tag** in the new repo's configuration.
    * Git automatically names the remote `origin`.
  * List the names and URLs of a repo's remotes: `git remote -v`.
  * Add more remotes by specifying a name for Git to assign: `git remote add [name] [URL]`.
* **Gathering from a remote**:
  * Fetch updates from a remote: `git fetch [remote] [branch]`. For instance, `git fetch origin main` fetches updates from the remote `origin/main` to the local branch `main`.
  * After fetching the working directory remains unchanged. It only updates the local reference to the `[remote]/[branch]`. This means that the local Git repo now knows about any new commits or changes on the remote branch `[branch]`, but the changes are not yet merged into the local working branch.
  * Compare the remote repo with the local branch: `git diff [remote] [branch]`. For instance, `git diff origin main`.
  * To synchronize contents between `[remote]/[branch]` and local `[branch]`, we need one more step, performing a merge of the remote branch into the local branch: `git merge [remote] [branch]`. For instance, `git merge origin main`. Now, the local branch `main` is updated.
  * Pull from a remote: `git pull [remote] [branch]`. This command fetches and merges the remote `[remote]/[branch]` to the local branch `[branch]`.
  * If we have been working locally and not yet commited our changes, Git won't allow us to pull from a remote. It tells us that local changes would be overwrittten, instructs us to commit our changes, and tells us that the pull command was aborted.
* **Pushing to a remote**:
  * Push the contents of the local branch into the remote: `git push [remote] [branch]`. For instance, `git push origin main` pushes the content of the local branch `main` into the remote branch `origin/main`. :warning: Note that: we have to save locally first!
  * Resolving a conflict: in case there're different commits on the local and remote repos, Git can't just bring them in line with one another. Therefore, we needs to:
    * pull from the remote first: `git pull [remote] [branch]`. Git will automatically open the nano text editor and ask us a message for the merge. We leave a message that we are pulling the latest from the remote.
    * then we can try our push again: `git push [remote] [branch]`.

## Terminology

* the **parent** of a commit is the commit before it.
* the **child** of a commit is the commit after it.
