# Git and GitHub: The Basics in One Project

32 main slides and 12 appendix slides. The main lecture and questions take 45 minutes.

No live demonstration, in-class exercise or required homework. Appendix slides are outside the main lecture time.

## 1. Git and GitHub

00:00–00:45 · 45 seconds

Welcome. Today we will follow one robot project from its first files to teamwork. We will begin with what GitHub offers us, then see how Git makes those benefits possible. By the end, I want you to understand where a change is stored and how it reaches the team, rather than memorize a list of commands. Keeping code, a circuit diagram, and an explanation together helps us manage a mechatronics project as a whole.

Sources:


## 2. The 45-minute route

00:45–01:30 · 45 seconds

The lecture has four parts. First, we will use the problem of messy project files to introduce the core concepts. Next, we will follow a file change from a computer to GitHub. The third part shows how two people can work on the same project. Finally, we will discuss choosing existing code, building a portfolio, and student resources. The last three minutes are for questions. Installation and detailed commands are in the appendix; the main lecture focuses on concepts and how they connect.

Sources:


## 3. Which file is the latest?

01:30–03:00 · 90 seconds

In our robot team, Elif works on the motors and Deniz works on the line sensors. As code is shared in a group chat, copies named robot, robot_final, and robot_final_SON appear. Their names do not tell us which version works or who changed what. Combining both people's fixes also means comparing files by hand. Git solves this by keeping project history rather than creating a new filename for every saved version. We still work on robot.ino, with a timeline showing which changes were recorded and in what order. That timeline contains the changes we selected and committed.

Sources:

- [Viewing commit history](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History)

## 4. Git and GitHub

03:00–04:30 · 90 seconds

Keeping these two names separate is the key to this lecture. Git is the version control tool on our computer. We can record changes and inspect local history without the internet. GitHub hosts Git repositories and organizes teamwork around them. Having a GitHub account does not mean that every change on our computer automatically goes online. We will explain that transfer with push and pull. GitHub can be used in a browser, and Git through a terminal or a graphical interface. The menus differ, but the underlying concepts are the same. Understanding what an operation records matters as much as knowing which button to click.

Sources:

- [What is GitHub?](https://docs.github.com/en/get-started/start-your-journey/what-is-github)

## 5. A repository holds files and history

04:30–05:45 · 75 seconds

A repository is more than a folder on the internet. It contains project files and their recorded history. In our example, robot.ino, the wiring diagram for the IR sensors, the README, and a few project photographs share the same context. The animation shows those files coming together on GitHub. Uploading files in the browser also creates a commit. When we work locally, recording and sending changes are separate operations. Text files are easy to compare line by line. Photographs and PDFs can also be stored, but we should not expect the same detailed comparison that we get with text.

Sources:

- [About repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories)

## 6. A commit is a checkpoint

05:45–07:00 · 75 seconds

A commit is a recorded checkpoint in a project's history. Saving a file in an editor changes the working file, but that alone does not add it to Git history. When we select changes and commit them, we create a record that can be inspected later. Its message explains the purpose of the change. For the robot, “Increase the IR sensor threshold” tells us more than “update,” even months later. Each commit has an ID and a relationship to earlier commits, forming a timeline. A commit made on our computer is still local. It must be sent before the team can see it on GitHub. We will make that distinction clearer with the four areas.

Sources:

- [git commit](https://git-scm.com/docs/git-commit)

## 7. The README is the entry point

07:00–08:15 · 75 seconds

The README guides someone seeing the project for the first time. It does not need to explain every line of code. It should make clear what the robot does, what hardware it uses, and how to run it. Our robot has IR line sensors and an Arduino controller. A wiring diagram, a photograph, and the names of any libraries complete the explanation. README.md uses Markdown, with simple symbols for headings and lists. GitHub displays it as a readable page. Good documentation helps teammates, instructors, and people reviewing an internship application. Setup instructions that actually match the project matter more than an attractive layout alone.

Sources:

- [About README files](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)

## 8. Who can see it?

08:15–09:15 · 60 seconds

We choose a repository's visibility when we create it. Anyone can view and clone a public repository, but that does not mean anyone can change the original repository. Write access is a separate permission. A private repository limits access to authorized people. For a course or team project, we should decide in advance which files to share. A circuit diagram or robot program is different from a password or access key. If sensitive information has entered the history, deleting it from the latest file does not remove earlier commits. File contents and permissions therefore deserve attention before sharing. We will also return to licensing near the end.

Sources:

- [Repository visibility](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility)
- [Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)

## 9. It worked yesterday

09:15–10:45 · 90 seconds

The robot followed the line yesterday, but behaves differently today. Our first reaction may be to blame the latest file. History helps us identify the commit that introduced the change. The animation shows a threshold changing from 500 to 900. The robot in the course kit reads IR sensors with analogRead; these numbers are example thresholds for comparing sensor readings. They are not universal calibration values for every robot. A commit records an author, a time, and a message. Those details show who made a change, but do not prove that it is correct. We still need to inspect and validate it. History lets us compare recorded states instead of relying on memory.

Sources:

- [Viewing commit history](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History)

## 10. How to read a diff

10:45–12:00 · 75 seconds

A diff is a view of differences. A minus sign marks a line on the earlier side of the comparison; a plus sign marks a line on the later side. These are not readings from two different sensors. They show the old and new values of the same variable. Here, the threshold for an analog IR sensor reading increases from 500 to 900. The signs make the change readable even without color. During review, this lets us focus on the changed section instead of rereading the entire file. Context still matters: a small numeric change can alter the robot's behavior. When comparing branches, we should make clear which side comes first and which comes second.

Sources:

- [git diff](https://git-scm.com/docs/git-diff)

## 11. A change passes through four areas

12:00–13:45 · 105 seconds

These four areas are central to the lecture. The working tree is where we open and edit files. The staging area selects what will go into the next commit. The local repository holds commit history on our computer. The remote repository is the shared history on GitHub. This does not mean creating four separate projects; it describes different states of the same project. Editing the README happens in the working tree. Add stages the change. Commit records the staged state locally. Push sends commits to the remote repository. If something changes on GitHub, our local copy does not update automatically. We need to bring that change in. We will now follow each of these arrows in the robot repository.

Sources:

- [How Git works](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F)

## 12. Clone creates a local copy

13:45–15:00 · 75 seconds

Clone creates a local copy of an existing Git repository. A normal clone includes files, recorded history, and the remote address. After cloning robot-projem, we can edit its README and inspect earlier commits. The repository-url text on the slide is a placeholder for the actual clone URL. Reading a public repository over HTTPS usually does not require account authentication. A private repository requires access permission. Being able to clone does not mean being allowed to push changes back. Download ZIP usually gives us the files at the selected state, without creating local Git history. That distinction matters when we want to work with history.

Sources:

- [Cloning a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)

## 13. First, edit the file

15:00–16:15 · 75 seconds

There must be an actual change between cloning and making a new commit. Imagine adding the IR sensors' purpose and the location of the wiring diagram to the robot's README. We save it in the editor; the working tree now differs from the previous commit. Git status shows that state. There is no new commit yet, and nothing new is visible on GitHub. We can reread the text and check for mistakes. A command list that jumps straight from clone to add can suggest that cloning itself creates a new change. The editing step is where the change actually happens. The following operations select and record it.

Sources:

- [git status](https://git-scm.com/docs/git-status)

## 14. Add selects the change

16:15–17:45 · 90 seconds

Add does not upload a file. It prepares the contents of the next commit. Here, we select only the README change. If we are also experimenting with the robot code, we do not have to include that work in the documentation commit. Git diff --cached shows the staged difference: what we are about to record. If we edit a file again after adding it, the staging area may still hold the previously selected state. To record the later edit too, we add it again. Staging is therefore a selection made at a particular moment, rather than moving an entire folder. Small, understandable commits make review and later undoing easier.

Sources:

- [git add](https://git-scm.com/docs/git-add)

## 15. Commit records the change locally

17:45–19:15 · 90 seconds

We now record the staged README change with a commit. Its message, “Document IR sensor wiring in README,” explains why the file changed. Git log --oneline presents the history as a short list, including the new commit's ID and message. Earlier robot code commits remain in the history. This operation updates the local repository and does not require the internet. A commit message can also make a claim about a result. If we write “Fix the sensor,” we should explain what was actually checked. Our example changes documentation only; it does not demonstrate that the sensor works. Next, we will send this local commit to the team's shared repository.

Sources:

- [git commit](https://git-scm.com/docs/git-commit)
- [Viewing commit history](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History)

## 16. Push sends commits to GitHub

19:15–20:30 · 75 seconds

Push sends local commits to the remote repository. Once it succeeds, the team can read our README update on GitHub. Push is different from saving a file in the editor; it does not directly send uncommitted changes from the working tree. Sending requires a remote address, a target branch, write permission, and suitable authentication. We can use an HTTPS authentication method or an SSH key; the appendix covers details. The account's normal password is not sufficient for Git authentication here. The first push may also need a tracking relationship. If new commits exist remotely, Git may reject the push. We should understand and incorporate the team's changes instead of forcing an overwrite.

Sources:

- [git push](https://git-scm.com/docs/git-push)

## 17. Pull brings updates in

20:30–22:00 · 90 seconds

If Deniz pushes robot code to GitHub, the file on Elif's computer does not change by itself. Pull fetches remote updates and incorporates them into the local branch. First, status shows whether there are uncommitted working-tree changes. The --ff-only option advances the branch if the local history has not gone in a separate direction. If each side has different new commits, it stops; we then choose how to integrate the histories, for example with merge or rebase. General pull behavior can depend on configuration. The central relationship is simple: push goes from us to the shared repository, and pull comes back to us. Seeing the latest version on GitHub does not mean the local copy is current.

Sources:

- [git pull](https://git-scm.com/docs/git-pull)

## 18. An issue makes work visible

22:00–23:30 · 90 seconds

We open an issue so a task does not disappear in a group chat. An issue can report a bug, describe a task, or suggest an improvement. For our robot, imagine an issue titled “Investigate the IR sensor threshold.” Its description explains when the robot loses the line, what we expect, and which file is involved. We can assign an owner and add labels. The issue number gives us a reference for discussions and pull requests. The animation uses a photograph task; the same structure works for a sensor problem or missing README content. Closing the issue does not erase its history. We can find the decisions later, keeping the question “What should we do?” separate from, but connected to, the code.

Sources:

- [About issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues)

## 19. A branch is a separate line of work

23:30–25:00 · 90 seconds

A branch creates a separate line of work. Imagine starting a branch from the current main commit to adjust the IR sensor threshold. New commits on that branch do not automatically change main. Someone else can work on the README in another branch. Thinking of a branch as copying the whole project folder may seem convenient, but that is not Git's model. A branch name points to a commit and advances with new commits. The branch we check out determines which state we see in the working tree. Branches help organize work, but do not guarantee that a change is good or correct. Review and validation are still needed before merging.

Sources:

- [Git branches](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)

## 20. Start with a simple branch workflow

25:00–26:15 · 75 seconds

For a beginner robot team, one main branch and short-lived task branches are enough. We call the main branch main in this presentation. Other projects may use master or another name; commands must use the actual name. Large projects may have dev, staging, or release branches, but that is not one mandatory workflow for everyone. When contributing elsewhere, we should not choose a target branch out of habit. First, read CONTRIBUTING or the contribution documentation. Maintainers decide which branch accepts contributions and under what conditions. Adding branches should make work easier to organize, rather than create a process that is difficult to understand.

Sources:

- [Branching workflows](https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows)

## 21. A pull request is a proposal

26:15–28:00 · 105 seconds

A pull request proposes merging one branch into another. Our sensor-threshold branch is the source, and main is the target. Opening a PR does not immediately accept the change; it makes it available for review. The title describes the specific task. The description covers the problem, the change, and validation. Here, the threshold moves from 500 to 900. In a real project, we should state the conditions under which it was checked. We do not present an unperformed test as completed in this example. A PR can also link to the issue. The issue asks what we should do; the PR asks whether to accept this solution. Choosing the correct source and target matters as much as the content.

Sources:

- [Pull requests](https://docs.github.com/en/pull-requests/reference/pull-requests)

## 22. Review strengthens the solution

28:00–29:30 · 90 seconds

Code review is more than looking for typos. A teammate may ask why the threshold changed, under what conditions the analog readings were measured, or whether another behavior is affected. In GitHub's Files changed view, a comment can attach to the relevant line. If the author responds with a new commit on the same branch and pushes it, the PR updates; there is no need to start a new one. Automated checks, when configured, also show their results. Review aims to make the solution understandable and reliable. Permission to approve and permission to merge may differ. The team's rules determine when a change can enter the main branch.

Sources:

- [Pull request reviews](https://docs.github.com/en/pull-requests/reference/pull-request-reviews)

## 23. Update locally after the merge

29:30–30:45 · 75 seconds

After review, the change can be merged into main on GitHub. Our local main may still point to an earlier commit, so we switch to it and bring in the remote update. The --ff-only example assumes there are no separate new commits on local main. The sensor-threshold change is now part of the main line of work. If the task branch is no longer needed, we can remove it. The content included in main remains. The shape of the history depends on the merge method: GitHub offers several methods, and they do not all produce identical history. Before going into those details, remember the cycle: propose, review, accept, and update everyone's local copies.

Sources:

- [GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [git switch](https://git-scm.com/docs/git-switch)

## 24. A conflict asks us to decide

30:45–32:15 · 90 seconds

Git can often combine changes in different areas automatically. But if a shared starting threshold of 500 becomes 900 on one branch and 700 on another, Git cannot know which value is right. It stops and adds conflict markers. In this example, we are on the sensor-threshold branch and merging main into it. The HEAD section contains 900, while the incoming main section contains 700. HEAD does not mean “the correct side”; it identifies our current position. Deleting a file on one branch while changing it on the other can also cause a conflict. Git stopping does not mean the whole project is broken. It makes a decision visible for the team to resolve.

Sources:

- [Merge conflicts](https://docs.github.com/en/pull-requests/reference/merge-conflicts)

## 25. Resolve the meaning of the conflict

32:15–34:00 · 105 seconds

Resolving a conflict is not choosing one side at random. We read both authors' reasoning and decide on the robot's intended behavior. The final file should contain a meaningful threshold and no conflict markers. Sometimes we combine both changes or write a third solution. After saving, we perform suitable project validation. Add and commit then complete this merge resolution. The commands on this slide apply to a merge; the continuation step during rebase is different. Editors such as VS Code make the options easier to use, but we still decide which content is correct. Removing markers can finish the technical step; understanding whether the problem is solved requires looking at the code and the project's behavior.

Sources:

- [Resolving a merge conflict](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/resolving-a-merge-conflict-using-the-command-line)

## 26. How do we choose existing code?

34:00–35:30 · 90 seconds

Imagine adding an HC-SR04 distance sensor to the line-following robot. Finding a library on GitHub can speed up the start, but choosing the one with the most stars is not enough. A star can mean that someone saved a project or expressed interest; it does not directly measure real-world use or correctness. We first check compatibility with our sensor and Arduino environment. We look for wiring information and examples in the README, inspect open issues, and consider maintenance. A recent update is not automatically better; a mature project may change less often. Finally, we check the license. This slide provides selection criteria rather than recommending a particular library.

Sources:

- [What stars mean](https://docs.github.com/en/get-started/exploring-projects-on-github/saving-repositories-with-stars)

## 27. A license sets the conditions of use

35:30–36:30 · 60 seconds

A public repository does not automatically grant unrestricted use. A license explains the conditions for using, modifying, and distributing code. When adding a library to our robot, we check both its license and those of its dependencies. Some licenses require attribution or retained license notices; other obligations may apply. With no license, we should not assume that finding code on GitHub makes every use permitted. If we want others to use our own project, clearly stating an appropriate license also helps. The aim here is not to memorize license types, but to recognize that a sharing decision involves more than the technical files.

Sources:

- [Repository licenses](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)

## 28. Contribute through a fork

36:30–38:00 · 90 seconds

We may have write access to our team's repository but not to an external open-source project. A fork is not required just to read or clone a public project. It is useful when we want a remote copy in our own account that we can push to. First, we read the contribution guide and find the branch that accepts contributions. Then we clone our fork, make changes on a task branch, and push our commits to the fork. We open a PR with our fork's branch as the source and the original project's branch as the target. The target is not always dev; CONTRIBUTING or the maintainers' instructions determine it. This lets us propose an organized change without write access to the original repository.

Sources:

- [About forks](https://docs.github.com/en/pull-requests/reference/forks)

## 29. A portfolio explains your work

38:00–39:30 · 90 seconds

A GitHub profile can be a portfolio, but its repositories need to be understandable. In the robot project, we can explain the problem, our contribution within the team, the hardware, and the outcome. A photograph or short video makes the project concrete; describing its limitations honestly is also valuable. Featuring a few strong projects makes the profile easier to explore. The green contribution squares are not a complete record of working time. GitHub counts specific activities and commits under certain conditions. Laboratory work and design thinking are not fully represented. In an application, a clear project and a concrete description of your contribution matter more than the number of squares.

Sources:

- [Contribution graph criteria](https://docs.github.com/en/account-and-profile/reference/profile-contributions-reference)

## 30. Student resources

39:30–40:30 · 60 seconds

GitHub Education offers learning resources and benefits for students. The Student Developer Pack includes partner offers whose number and terms can change. Copilot Student is also available to verified students. These benefits should not be understood as unlimited services automatically granted to every account. An application requires verification of student status, with email or documents depending on the process. Some benefits may need separate activation. Instead of giving a fixed offer count or a guaranteed approval time, the slide points to the current official information. Choose tools according to your needs; being free does not by itself make a tool suitable for the project.

Sources:

- [GitHub Education](https://docs.github.com/en/education/about-github-education/github-education-for-students/about-github-education-for-students)
- [Apply as a student](https://docs.github.com/en/education/about-github-education/github-education-for-students/apply-to-github-education-as-a-student)
- [Copilot Student](https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/enable-copilot/set-up-for-students)

## 31. The whole project workflow

40:30–42:00 · 90 seconds

We started with the robot losing the line. An issue made the task visible, a branch held the change, and a commit recorded it. Push brought it to the shared platform; a PR supported review and merging, then we updated the local copy. Alongside this workflow, the README explains the project, history shows what changed, and the license sets sharing conditions. Three distinctions organize the concepts: Git and GitHub are different; saving, committing, and pushing are different; and issues and PRs answer different questions. The appendix is a reference for commands. Anyone who wants to continue later can use the official GitHub Docs, the Pro Git book, and GitHub Skills independently.

Sources:

- [Git and GitHub learning resources](https://docs.github.com/en/get-started/start-your-journey/git-and-github-learning-resources)
- [Introduction to GitHub](https://github.com/skills/introduction-to-github)

## 32. Questions

42:00–45:00 · 180 seconds

Thank you. We can think about questions in three groups: where the change is currently stored, who can see it, and how it enters the team's shared line of work. A file saved but not committed is in a different state from a commit made but not pushed. Working on a branch and merging into main are also separate steps. We can use the last three minutes to discuss these relationships or how to organize your own projects.

Sources:

- [GitHub Docs](https://docs.github.com/en/get-started/start-your-journey/git-and-github-learning-resources)
- [Pro Git · English](https://git-scm.com/book/en/v2)
- [GitHub Skills](https://github.com/skills/introduction-to-github)
- [GitHub Education](https://education.github.com/pack)

## Appendix 1. Installing Git

Appendix slide · outside the main lecture time

This appendix slide is an installation reference. Git --version shows the installed version. If Git is not installed, choose the appropriate method from the official Git website. We should not assume that every Mac already has Git; it depends on the environment. Git for Windows can provide Git Bash on Windows. A distribution's package manager is a common choice on Linux. The installation method does not change the core Git concepts.

Sources:

- [Installing Git](https://git-scm.com/install/)

## Appendix 2. Commit identity

Appendix slide · outside the main lecture time

These settings define commit identity and the default branch name for new repositories. The displayed name and email are examples; use the appropriate real information in an actual setup. Global configuration applies to the user account, and a repository can have its own local overrides. If the commit email appears in public history, privacy preferences also matter. These settings do not sign us in to GitHub or grant permission to push. Authentication is a separate concern.

Sources:

- [Git identity settings](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup)

## Appendix 3. Editor and terminal

Appendix slide · outside the main lecture time

VS Code is one editor option, while Git is a separate tool. Source Control can show changed files, staging, and commit operations visually. The same commands can run in the integrated terminal. A terminal makes operations explicit; a graphical interface can make differences easier to inspect. The two approaches can be used together, and neither guarantees understanding by itself. The main lecture's model of working tree, staging area, local repository, and remote repository applies to both.

Sources:

- [Source control in VS Code](https://code.visualstudio.com/docs/sourcecontrol/overview)

## Appendix 4. .git and .gitignore

Appendix slide · outside the main lecture time

The .git directory contains the local database for commits, branches, and settings. Deleting or editing it by hand can damage local history. The .gitignore file identifies untracked files that should normally remain outside tracking, such as build output or environment settings. But adding an already committed file to .gitignore does not remove it from history. If sensitive information was pushed accidentally, adding an ignore rule is not a complete fix. The affected credential should be revoked, and the official cleanup process followed.

Sources:

- [gitignore](https://git-scm.com/docs/gitignore)
- [Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)

## Appendix 5. An SSH key pair

Appendix slide · outside the main lecture time

SSH authentication uses a public and private key pair. Current documentation recommends Ed25519, though older systems may need an alternative. The .pub file is added under SSH and GPG keys in the GitHub account. The private key is never shared or uploaded to a repository. The example email is only a label. A passphrase protects the key, and an SSH agent makes it easier to use during a session. When generating a new key, avoid accidentally overwriting an existing file.

Sources:

- [SSH keys and the SSH agent](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
- [Adding a public key to GitHub](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)

## Appendix 6. SSH agent and connection

Appendix slide · outside the main lecture time

These commands are a short agent example for Bash or Git Bash. Details differ for macOS Keychain and the Windows OpenSSH service. The same configuration is not mandatory on every operating system. On the first SSH connection, the server's identity is checked against GitHub's published key fingerprints. A successful authentication message confirms SSH access to the account, but GitHub does not provide general shell access. Even when the key connection succeeds, repository write permissions still apply separately.

Sources:

- [SSH keys and the SSH agent](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

## Appendix 7. Turn a local folder into a repository

Appendix slide · outside the main lecture time

Init starts a local Git repository in an existing folder. The example names main explicitly and records the existing README and robot code as the first commit. Remote add associates the remote address with the name origin. Origin is a conventional name, not a password or special service. Init does not create a repository on GitHub. This example assumes that the remote has already been created and is empty. If the remote contains initial commits, such as a README, cloning it may be simpler than creating two independent histories.

Sources:

- [git init](https://git-scm.com/docs/git-init)
- [git remote](https://git-scm.com/docs/git-remote)

## Appendix 8. First push and tracking

Appendix slide · outside the main lecture time

On the first push, -u establishes tracking between local main and remote origin/main. With suitable configuration, later push and pull commands can use that relationship to find their target. This tracked remote branch is sometimes called the upstream branch. That is a different context from a remote named upstream for the original project in a fork workflow. The branch does not have to be called main, though that is the name used throughout this presentation. Always check the actual branch name and remote address.

Sources:

- [git branch](https://git-scm.com/docs/git-branch)

## Appendix 9. Branch and diff commands

Appendix slide · outside the main lecture time

Git switch -c creates a branch and switches to it. In the branch list, an asterisk marks the current branch. When diff compares two branch tips, the first name is the before side and the second is the after side. The minus and plus signs are read in that direction. A three-dot comparison shows the second branch's changes relative to their common starting point. If completion is available, type a prefix at the start of the name, such as feature. A word from the middle of a branch name is not guaranteed to complete in every environment. Shell settings affect the result.

Sources:

- [git switch](https://git-scm.com/docs/git-switch)
- [git diff](https://git-scm.com/docs/git-diff)

## Appendix 10. Choose what you want to undo

Appendix slide · outside the main lecture time

Before undoing, decide what should change. Restore --staged removes an accidentally added file from staging while preserving its edits in the working tree. Revert creates a new commit to reverse an earlier shared change, keeping shared history intact. Reset moves the branch's position and, depending on the mode, changes staging or working files as well. The default mixed mode preserves working files but moves the history position. Reset and revert therefore do not have the same purpose or effects.

Sources:

- [git restore](https://git-scm.com/docs/git-restore)
- [git revert](https://git-scm.com/docs/git-revert)
- [git reset](https://git-scm.com/docs/git-reset)

## Appendix 11. Hard reset and recovery limits

Appendix slide · outside the main lecture time

Hard reset moves a branch to the selected commit and makes the staging area and tracked working files match it. Uncommitted edits can be lost, and some untracked files in the way can also be affected. A previously committed state may sometimes be found in the local reflog, so calling every hard reset irreversible is inaccurate. But reflog is not a general backup and does not keep everything forever. We should not assume that work never committed can be recovered. First inspect status and the changes. Do not use hard reset without understanding its effects.

Sources:

- [git reset](https://git-scm.com/docs/git-reset)
- [git reflog](https://git-scm.com/docs/git-reflog)

## Appendix 12. Quick command reference

Appendix slide · outside the main lecture time

This final appendix slide is a short reference for the daily workflow. Clone provides a starting point, but a new commit requires an actual file edit first. Status shows the state, add selects changes, commit records them, and push sends them. Pull brings in the team's updates. A branch provides a place for a separate task, and a PR supports review. We do not need to run every command in sequence each time. We choose the next operation by checking whether the change is in the working tree, staging area, or local history.

Sources:

- [Git and GitHub learning resources](https://docs.github.com/en/get-started/start-your-journey/git-and-github-learning-resources)
