# Git and GitHub: The Robot Worked Yesterday

34 main slides and 15 appendix slides. The main lecture and questions take 45 minutes.

No live demonstration, in-class exercise or required homework. Appendix slides are outside the main lecture time.

## 1. The robot worked yesterday

00:00–00:45 · 45 seconds

Imagine a team building a line-following robot. Elif and Deniz worked on the same project yesterday. Today the robot loses the line, and different files circulate in the group chat. They do not know which one to continue from. We will follow their decisions throughout this lesson, introducing Git and GitHub when the team needs them. The aim is to understand how a change becomes traceable and shareable. This is a fictional teaching example; the threshold values on screen are not measurements from a tested robot. We will use prepared visuals to follow the problem through to a shared decision, without a live coding exercise.

Sources:


## 2. Which file can we trust?

00:45–01:30 · 45 seconds

These file names may look familiar. We go from robot to robot final to robot final final, but renaming a file does not preserve the reasoning behind a decision. When Elif sends one copy and Deniz another, the problem grows. The file with the latest timestamp is not necessarily the right one. The team needs to see what changed, why it changed, and in what order. We will record the relationships between saved versions as well as the files themselves. That lets us keep both people’s contributions instead of losing one by choosing a copy at random.

Sources:

- [Viewing commit history](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History)

## 3. We have files. Where is the decision?

01:30–03:00 · 90 seconds

Elif and Deniz can inspect the files, but they cannot find a record explaining the change behind today’s behavior. What value did they use yesterday? Which line did Deniz touch? Which copy did Elif continue from? A change history helps answer these questions without relying on memory. It does not prove that the robot works correctly; it first helps narrow the question. Our immediate goal is to identify what changed without guessing. That distinction will matter throughout the lesson: the tool keeps records, and the team makes the engineering decision.

Sources:

- [Viewing commit history](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History)

## 4. How do we compare yesterday and today?

03:00–03:30 · 30 seconds

Imagine looking through the team’s recorded history. A commit shows the sensor threshold changing from 500 to 900, alongside an author and a message. We can now name the changed line instead of saying that something is different. This record does not automatically prove the change was wrong. It gives us a possible cause to investigate. IR sensor thresholds also depend on the hardware and operating conditions; copying a value from another robot is not a calibration method. Now we should separate the tool that keeps this history from the platform where the team shares it.

Sources:

- [Viewing commit history](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History)

## 5. The robot’s settings in the animation

03:30–04:00 · 30 seconds

Read the settings shown in the English animation. SPEED starts at 200, TURN_SPEED at 120, and THRESHOLD at 900. The comment names the purpose of each setting. int defines integer variables; assignment provides their starting values. Unlike const int in later simplified examples, these variables can be reassigned by later program statements. This is only the visible fragment, not the whole robot program. THRESHOLD is the English animation’s name for the sensor threshold; the shared narrative uses ESIK. The fictional numbers illustrate a history change and require validation for actual hardware and operating conditions.

Additional explanation: A recorded threshold change is a clue. It does not establish the right setting for every robot.

What the code means:

- `//` starts a comment. `int` defines an integer variable.
- `SPEED`, `TURN_SPEED` and `THRESHOLD` name straight speed, turn speed and sensor threshold settings.
- `=` assigns the initial value. `;` ends the declaration.

Sources:

- [Arduino int type](https://github.com/arduino/reference-en/blob/master/Language/Variables/Data%20Types/int.adoc)
- [Arduino setup function](https://github.com/arduino/reference-en/blob/master/Language/Structure/Sketch/setup.adoc)
- [Arduino pinMode function](https://docs.arduino.cc/language-reference/en/functions/digital-io/pinMode/)

## 6. Preparing the two motor pins

04:00–04:30 · 30 seconds

This is the next visible fragment from the animation. Arduino calls setup once after startup or reset. void indicates no returned value. The opening and closing braces contain the body. The two pinMode calls configure pins 5 and 6 as outputs; the comments connect those pins with left and right motors. Configuring a pin is not the same operation as driving a motor or setting a speed. No loop, sensor reading, or complete movement algorithm is shown here. The lesson reads this fragment to understand the tracked file, not to build or operate a robot in class.

Additional explanation: This fragment prepares outputs; sensor readings and movement control appear elsewhere in the full program.

What the code means:

- `setup()` runs once at startup or reset. `void` means it returns no value.
- `pinMode(5, OUTPUT)` configures pin 5 as an output; the second line does the same for pin 6.
- The comments identify the left and right motor connections. `pinMode` alone does not start either motor.

Sources:

- [Arduino int type](https://github.com/arduino/reference-en/blob/master/Language/Variables/Data%20Types/int.adoc)
- [Arduino setup function](https://github.com/arduino/reference-en/blob/master/Language/Structure/Sketch/setup.adoc)
- [Arduino pinMode function](https://docs.arduino.cc/language-reference/en/functions/digital-io/pinMode/)

## 7. Which part of this is Git?

04:30–05:45 · 75 seconds

Separating Git from GitHub makes the rest of the story easier. Git is the version control tool on the computer: it records selected changes and manages local history and branches. Many local operations work without an internet connection. GitHub hosts repositories and organizes collaboration around that history. Elif saving a file does not mean Deniz can see it on GitHub. Creating a local record and transferring it to the shared repository are separate steps. We can use Git through a terminal or an editor’s interface. The buttons may differ, but the recording and sharing relationships we are about to follow stay the same.

Sources:

- [What is GitHub?](https://docs.github.com/en/get-started/start-your-journey/what-is-github)

## 8. What should we keep together?

05:45–07:00 · 75 seconds

The team brings robot.ino, the wiring diagram, a project photo, and an explanation into one repository. A repository contains the project’s files and its recorded history. That keeps the code connected to the hardware it is meant to control. The animation shows files coming together on GitHub; uploading through the browser creates a commit too. When working locally, recording and sending remain separate steps. We can inspect line changes in text files. Photos and PDFs can also be stored, but their changes are not as easy to compare as code. The repository keeps the project’s context in one place.

Sources:

- [About repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories)

## 9. What changed on that line?

07:00–08:15 · 75 seconds

This view is called a diff. The minus line belongs to the earlier side of the comparison, and the plus line to the later side. The threshold in the robot code changed from 500 to 900. These are not readings from two sensors: they are the same variable in two recorded versions. A commit records a selected state of the project in history, with an identifier and a message. Saving a file in an editor does not create one automatically. The diff focuses attention on the changed area. A small-looking line can still have a large effect. How should we assess this change?

Additional explanation: − previous line · + next line · commit: a recorded state

What the code means:

- `robot.ino` names the compared file; it is not a program statement.
- `const int ESIK` defines an integer constant. Its old value is 500; its new value is 900.
- `-` marks the removed line and `+` the added line. These signs are absent from the actual C++ file.

Sources:

- [git commit](https://git-scm.com/docs/git-commit)
- [git diff](https://git-scm.com/docs/git-diff)

## 10. Is 900 wrong?

08:15–09:15 · 60 seconds

Pause here. Having 500 in yesterday’s file and 900 in today’s does not establish that 500 is correct in every situation. Lighting, the surface, and sensor placement can affect behavior. Git tells us which line changed; the team must evaluate the expected behavior under suitable conditions. Elif and Deniz first inspect the reasoning and any available measurement records. Returning to 500 may be a candidate solution, but it is not yet an accepted result. The next step is therefore to make the investigation a visible task and work on a separate branch, rather than overwrite the shared code.

Sources:

- [Viewing commit history](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History)
- [git diff](https://git-scm.com/docs/git-diff)

## 11. Who is tracking the problem?

09:15–10:45 · 90 seconds

The team now has a concrete question: when does the robot lose the line, and how might the threshold change be involved? An issue records that question. We can describe the expected behavior, the observed problem, and the relevant file, then assign the investigation to Elif. The task no longer disappears in a group chat. This animation demonstrates the issue interface with a photo task; our story’s task concerns the sensor threshold. An issue tracks a need. Later we can connect our proposed change to it. Even after the issue closes, the discussion and reasoning remain available in the project.

The search filter is: is:issue state:open. It lists open issues without changing their state. The animation uses a photo task to demonstrate the interface; our story investigates the sensor threshold.

Sources:

- [About issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues)

## 12. How do we try it without changing main?

10:45–12:00 · 75 seconds

Elif wants to reconsider the threshold without mixing everyone’s trials into the shared main line. A branch provides a separate line of work from the same starting point. Commits Elif creates there do not automatically change main. Main may also move forward with other accepted work; the diagram shows both lines. Creating a branch does not require a new physical project folder: a branch name points to a commit. For a small team, one main branch and short-lived task branches can be enough. Review and validation will determine when the candidate is ready to join the main line.

What the code means:

- `main` is the team’s shared main branch.
- `feature/sensor-esigi` names the sensor task branch, not a new project folder.
- `git switch -c` creates and switches to a branch. `git merge` combines another branch into the current one.

Sources:

- [Git branches](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)
- [Branching workflows](https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows)

## 13. I saved it. Can Deniz see it?

12:00–13:45 · 105 seconds

Four areas answer this question. The working tree is where we edit the file. The staging area selects what will enter the next commit. The local repository is the recorded history on our computer. The remote repository is the history shared on GitHub. Editing the threshold happens in the first area. Add selects it, commit records it locally, and push transfers the commits to the shared repository. Saving in the editor has not yet reached Deniz. Likewise, a new commit on GitHub does not automatically update our computer. We will now move Elif’s single sensor change through these areas step by step.

Not yet. Editing, recording, and sharing are separate steps.
Edit → add → commit → push · Get the team’s updates: pull

What the code means:

- `index` is staging; `.git/` holds local repository data; `HEAD` names the current commit position.
- `origin` is the remote address name. `add` selects, `commit` records locally, and `push` sends commits.
- `clone` creates a local repository copy; `pull` gets updates for an existing one.

Sources:

- [How Git works](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F)

## 14. How do we get the same starting point?

13:45–15:00 · 75 seconds

Imagine Elif starting on a new computer. Clone creates a local copy of the existing robot repository. A normal clone brings the files, recorded history, and remote address connection, so she can inspect both code and earlier versions. Repository-url is a placeholder for the real cloning address. Reading a public repository over HTTPS usually does not require signing in; a private one requires access. Permission to clone is not permission to push. Downloading a ZIP provides the selected version’s files without setting up local Git history. Here we use a clone because Elif needs to work with history and send new commits.

Additional explanation: Clone brings history. A ZIP does not create a local Git history.

What the code means:

- `git clone` copies an existing repository, including its recorded history, to the computer.
- Replace `<repository-url>` with the real clone address, without the angle brackets.
- `cd robot-projem` enters the project folder. Use its actual name; `cd` is a terminal command.

Sources:

- [Cloning a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)

## 15. Which branch is the trial on?

15:00–16:15 · 75 seconds

We start on main in the cloned project. Switch with the c option creates feature/sensor-esigi and moves us to it. The star in the branch list marks the active branch. The next commits will advance this line. We have not edited the code yet: creating a branch alone does not fix the sensor problem. Naming a branch after its purpose helps the team find the relevant work. Here main is the shared main line and the task branch holds the candidate solution. Other projects may use different names and contribution rules. Next we will actually edit the file, producing a change to record.

Additional explanation: Active branch: feature/sensor-esigi · This does not change main.

What the code means:

- `git switch -c` creates a branch from the current commit and switches to it.
- `feature/sensor-esigi` is our task branch name. The slash does not create a new project folder.
- `git branch` lists local branches. A star marks the active branch.

Sources:

- [Git branches](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)
- [Branching workflows](https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows)
- [git switch](https://git-scm.com/docs/git-switch)
- [git diff](https://git-scm.com/docs/git-diff)

## 16. Which solution are we trying?

16:15–17:45 · 90 seconds

Elif now changes the threshold in robot.ino from 900 to 500 and saves the file. Returning to yesterday’s value is our candidate, not proof of a fix. Git status shows that the working tree differs from the previous commit; diff shows the changed line. No new commit exists yet, and GitHub still has the earlier version. At this point we can reread the change, define a test plan, or abandon it. Cloning and creating a branch did not produce the edit; this is where the actual work happens. The following recording and sharing steps will carry this same sensor line.

Additional explanation: Save → git status · History and GitHub have not changed yet.

What the code means:

- The removed `900` line is the previous value; the added `500` line is our candidate.
- Keep only `const int ESIK = 500;` in the real file, without the diff sign.
- `git status` checks saved file changes. Saving alone creates no commit and updates no GitHub repository.

Sources:

- [git diff](https://git-scm.com/docs/git-diff)
- [git status](https://git-scm.com/docs/git-status)

## 17. What goes into this commit?

17:45–19:15 · 90 seconds

Add selects the content of the next commit. Elif stages the sensor threshold change and checks the staged diff. If an unfinished README edit also exists, she does not have to include it in this record. That keeps the commit’s purpose clear. Diff cached shows what is about to enter history. Add stages the file’s state at that moment; if we edit it again, we may need another add to include the new version. Choosing a meaningful scope instead of combining every change makes review and later undoing easier. We will now record only the selected sensor change.

Additional explanation: Add selects. There is no new commit or upload yet.

What the code means:

- `git add robot.ino` selects the file’s current content for the next commit.
- `git diff --cached` shows all staged changes against the latest commit.
- If the file changes after `add`, its new content must be selected again. Other staged files remain selected.

Sources:

- [git add](https://git-scm.com/docs/git-add)

## 18. How do we record what we did?

19:15–20:30 · 75 seconds

Elif commits the staged sensor change to local history. The message says it is a candidate return to 500, accurately describing its status. Log oneline shows the new record’s identifier and message. A commit records the selected staged state; history on the computer advances while the earlier 900 record remains available. This can happen without an internet connection. Return to our question: has Deniz seen it? Not yet, because Elif has only made a record on her own computer. A local commit and access through the shared repository are separate things. Sending it will complete that distinction.

Additional explanation: The record is local. “Candidate” means validation is still pending.

What the code means:

- `git commit` records the staged content in local history.
- `-m` supplies the message. Quotes keep the words together as one message.
- `git log --oneline` lists reachable commits with short IDs and messages. No upload has happened yet.

Sources:

- [git commit](https://git-scm.com/docs/git-commit)
- [Viewing commit history](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History)

## 19. Can Deniz see it now?

20:30–22:00 · 90 seconds

Elif pushes the new commit to the sensor branch on origin. The u option records which remote branch this local branch tracks. Once the push succeeds, Deniz can see the candidate on GitHub. Main has not changed automatically; only the task branch has been updated. Push transfers commits, not uncommitted working-tree edits. It requires the right remote address, write permission, and authentication; the appendix contains those details. If a push is rejected, we understand the shared history before trying to overwrite it. The team can now inspect the same change. Visibility is still not acceptance: the pull request will ask that question.

Additional explanation: A shared candidate ≠ an accepted change in main

What the code means:

- `git push` sends local commits to a remote repository.
- `origin` is the saved name of the remote address; `feature/sensor-esigi` is the branch being sent.
- `-u` sets that branch’s tracking relationship for later commands.
- This needs access and write permission. Uncommitted edits are not sent; `main` is not merged.

Sources:

- [git push](https://git-scm.com/docs/git-push)
- [git branch](https://git-scm.com/docs/git-branch)

## 20. Should we bring this into main?

22:00–23:30 · 90 seconds

Elif opens a pull request from the task branch into main. The source branch contains the candidate sensor solution; the target is the shared main line. The description explains the problem, the return from 900 to 500, and the validation still required. It can also link to the issue: the issue describes the need, while the PR presents a proposed solution. Opening a PR makes it available for discussion and review. It does not immediately accept it. Other proposals could address the same problem differently. The team evaluates the source and target, the code diff, and the reasoning together. What should Deniz inspect?

Additional explanation: Issue: what do we need? · PR: should we accept this proposal?

What the code means:

- `feature/sensor-esigi` is the source branch; `main` is the proposed destination.
- Problem, Candidate and Reason explain the need, the change and its purpose.
- Validation says what is still pending. This is PR description text, not a terminal command.

Sources:

- [About issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues)
- [Pull requests](https://docs.github.com/en/pull-requests/reference/pull-requests)

## 21. What will Deniz look for?

23:30–25:00 · 90 seconds

Deniz reviews the sensor line in Files changed. Why 500? Under which conditions will it be tested? The questions examine the proposal’s basis. If Elif sends another commit to the same branch after feedback, the PR updates; she does not need a new PR. Automated checks, when present, also contribute, though a software check may not establish real robot behavior. Review approval and permission to merge can be separate. The team’s rule is to require a suitable reason and validation before accepting the candidate. If main advances with another accepted change in the meantime, the two lines may also need to be reconciled.

Sources:

- [Pull request reviews](https://docs.github.com/en/pull-requests/reference/pull-request-reviews)

## 22. What if two decisions change one line?

25:00–26:15 · 75 seconds

Add a common situation to the story. While Elif works, another change from Deniz is reviewed and accepted into main, making the same threshold 700. Elif’s branch still has the candidate 500. In this merge example, we are on the task branch and bring main into it. Git cannot automatically choose between the conflicting edits, so it stops with conflict markers. HEAD is our current branch’s side and main is the incoming side. HEAD does not mean the correct choice. Git can often combine edits in different areas, but the team must resolve the conflicting meaning on this line.

Additional explanation: We are on the task branch, merging main into it. Git cannot choose the right value.

What the code means:

- `<<<<<<< HEAD` opens our current branch’s version, with value 500.
- `=======` separates the alternatives. The incoming `main` version has value 700.
- `>>>>>>> main` closes the incoming side. These are Git markers, not C++ statements.
- The team must choose the justified result and remove the markers. `HEAD` does not mean the correct answer.

Sources:

- [Merge conflicts](https://docs.github.com/en/pull-requests/reference/merge-conflicts)

## 23. Which one do we choose?

26:15–28:00 · 105 seconds

Elif and Deniz compare the reasons for both changes and decide to continue with the 500 candidate. One threshold remains in the file, and the conflict markers are removed. The team saves the file and completes the appropriate validation. Add and commit record this merge resolution; push updates the PR. An editor’s selection buttons can simplify the operation, while the team records why it chose the result. We will show the next stage assuming the candidate has passed the required review and validation. That lets us follow this same change into the main line and onto the team’s computers.

The original workflow reminders are: Evaluate the reasoning behind both changes together. Remove the markers and save the chosen solution. After validation, finish review through the same PR.

Additional explanation: Removing conflict markers does not prove the robot’s problem is fixed.

What the code means:

- `const` defines a constant; `int` is an integer type; `ESIK` is its name.
- `= 500` supplies the example value; `;` ends the definition.
- One definition remains after the conflict markers are removed. Validate it before recording the merge resolution.

Sources:

- [Resolving a merge conflict](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/resolving-a-merge-conflict-using-the-command-line)

## 24. How does the decision enter shared history?

28:00–29:30 · 90 seconds

We have reached acceptance. For this example, assume the 500 candidate has passed the required review and validation. An authorized team member merges the change into main. The discussion and reasoning in the PR remain available later. The merge method affects how history looks; not every method produces the same kind of merge commit. For a first lesson, the essential relationship is that trying a change on a branch, sending it, approving it, and accepting it into main are separate steps. The accepted change is now in the shared repository. Elif’s computer has not been updated automatically.

Sources:

- [Pull request reviews](https://docs.github.com/en/pull-requests/reference/pull-request-reviews)
- [GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [git switch](https://git-scm.com/docs/git-switch)

## 25. GitHub is current. Is my computer?

29:30–30:45 · 75 seconds

Elif switches to local main and gets the shared repository’s updates. Pull fetches remote changes and integrates them into the local branch. Checking status first is a good habit. Here ff only advances local main when it has not diverged; if both sides have different new commits, it stops. We then decide how to reconcile the histories. Elif’s and Deniz’s computers reach the accepted shared state only after updating. Push carries commits from us to the shared repository, and pull gets updates back. Opening a PR and running pull are different operations. Now consider what a new teammate will see.

Additional explanation: Push shares. Pull gets updates. A pull request proposes a merge.

What the code means:

- `git status` reports working-tree and staging changes before we switch branches.
- `git switch main` makes local `main` the active branch.
- `git pull --ff-only` gets remote updates and advances the active branch only if its history has not diverged. Otherwise it stops.

Sources:

- [git pull](https://git-scm.com/docs/git-pull)
- [GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [git switch](https://git-scm.com/docs/git-switch)

## 26. Where does the next teammate start?

30:45–32:15 · 90 seconds

Imagine a new student joining the team. Commit history traces decisions, but it does not by itself explain the wiring or how to run the robot. The README supplies that entry point. We can state the purpose, hardware, wiring diagram, and calibration steps. Explaining when the threshold needs adjustment is more useful than asking someone to copy one number. Markdown headings organize a readable page. The README must match the real project files, as well as look clear. Even if Elif and Deniz leave, the next person receives a guide for continuing the work, alongside the latest files.

Additional explanation: Purpose · hardware · wiring · running · known limits

What the code means:

- `#` creates a Markdown title; `##` creates a section heading.
- The other lines are ordinary README text explaining hardware and how to start.
- GitHub displays this file as a readable project page. These lines are not terminal commands.

Sources:

- [About README files](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)

## 27. Can everyone see it and change it?

32:15–34:00 · 105 seconds

Before sharing, the team separates two questions. A public repository can be viewed and cloned by everyone; that does not give everyone permission to write to the main repository. A private repository limits access to authorized people. A class or team project should decide which files to publish. Code and wiring diagrams differ from passwords, access keys, and personal information. If sensitive information enters a commit, deleting it from the latest file does not remove it from earlier records. Keeping history makes that responsibility matter too. Next we will consider the conditions for using code from another project.

Sources:

- [Repository visibility](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility)
- [Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)

## 28. Should we use the code we found?

34:00–35:30 · 90 seconds

Suppose Elif finds another repository explaining sensor calibration. Existing code can speed up a start, but matching sensor names do not guarantee compatibility. Inspect the board, wiring, libraries, and conditions the example is intended for. The README and open issues provide context. Stars reflect interest or bookmarking; they do not measure correctness on our robot or the number of real deployments. A recent update is not proof of superiority either: mature projects may change less often. The team checks its needs, then compatibility and maintenance. That provides a reasoned choice before bringing a new code fragment into the project.

Sources:

- [What stars mean](https://docs.github.com/en/get-started/exploring-projects-on-github/saving-repositories-with-stars)

## 29. Can we use the code we can see?

35:30–36:30 · 60 seconds

Viewing a repository in a browser does not grant every usage right. Its license describes the conditions for using, modifying, and distributing the code. Before adding Elif’s example to the robot, inspect its license notice and any conditions on its dependencies. Some licenses require attribution or retaining the license text; other obligations may apply. Without a license, finding code on GitHub is not a basis for assuming unrestricted use. If the team wants others to use its robot project, it can state an appropriate license clearly. The lesson is to distinguish visibility from usage rights.

Sources:

- [Repository licenses](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)

## 30. How do we propose a fix to another project?

36:30–38:00 · 90 seconds

Suppose the team finds a missing explanation in the example. It may have no write permission to the original repository. Reading or cloning a public project does not require a fork; a fork gives us a remote copy on our own account where we can push. First read the contribution guide and learn the accepted target branch. Then clone the fork, make a change on a task branch, and push our commits to our fork. The PR’s source is our fork and its target is the original project. Maintainers evaluate it. The recording, sharing, and review cycle is familiar; the repositories and decision-makers differ.

Sources:

- [About forks](https://docs.github.com/en/pull-requests/reference/forks)

## 31. What does this project say about us?

38:00–39:30 · 90 seconds

A robot project used in a portfolio needs more than a repository link. Elif and Deniz can explain the problem, their own contributions, and the reasons behind decisions. A photo, short demonstration, and running guide make it concrete. Honestly describing limits and unsuccessful conditions is useful too. The profile animation demonstrates featuring projects. Green contribution squares do not measure all work time: hardware preparation and lab thinking are not fully represented. In an internship review, the purpose is to show what someone did and how they made project decisions, rather than simply report an activity count.

Sources:

- [Contribution graph criteria](https://docs.github.com/en/account-and-profile/reference/profile-contributions-reference)

## 32. Where can we continue after class?

39:30–40:30 · 60 seconds

Today we followed one change rather than using every command. Later, revisit concepts in Pro Git or find a GitHub operation’s details in GitHub Docs. GitHub Skills offers step-by-step practice at your own pace. The twelve reference slides cover setup and everyday commands. If you need student tools, check GitHub Education’s current official conditions; offers and application requirements may change. The official Copilot Student setup page is also linked as a reference. Starting with the task you need to perform, then choosing the relevant resource, is more useful than collecting a long tool list. Finally, return to the file confusion we started with.

Sources:

- [Pro Git · English](https://git-scm.com/book/en/v2)
- [Git and GitHub learning resources](https://docs.github.com/en/get-started/start-your-journey/git-and-github-learning-resources)
- [GitHub Skills](https://github.com/skills/introduction-to-github)
- [GitHub Education](https://docs.github.com/en/education/about-github-education/github-education-for-students/about-github-education-for-students)
- [Copilot Student](https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/enable-copilot/set-up-for-students)

## 33. What does the team have now?

40:30–42:00 · 90 seconds

At first, Elif and Deniz did not know what to do with different final files. We found the history and diff, then made the problem visible as an issue. We developed a candidate on a branch, selected and recorded it, shared it, and opened it for review. When a conflict appeared, the team chose the sensor solution with a reason and appropriate validation. After acceptance, local copies were updated from shared main. The README gave the next person a starting point. What we gained was a traceable project decision. Real robot behavior still requires hardware validation; Git helps organize and share its records.

Sources:

- [Git and GitHub learning resources](https://docs.github.com/en/get-started/start-your-journey/git-and-github-learning-resources)
- [GitHub Skills](https://github.com/skills/introduction-to-github)

## 34. What if it loses the line tomorrow?

42:00–45:00 · 180 seconds

Return to the robot from the opening. If its behavior changes again, we can inspect the history, diff, issue, and reasoning instead of only looking for a file called final. Saving, committing, and pushing are separate steps; the PR is where the team evaluates acceptance. These relationships help you explain where a change currently stands in your own project. We have three minutes for questions. If there are none, briefly revisit what records and explanations a new teammate would need to take over this robot. The following twelve reference slides hold setup and command details.

Sources:

- [Git and GitHub learning resources](https://docs.github.com/en/get-started/start-your-journey/git-and-github-learning-resources)
- [Pro Git · English](https://git-scm.com/book/en/v2)
- [GitHub Skills](https://github.com/skills/introduction-to-github)
- [GitHub Education](https://education.github.com/pack)

## Appendix 1. Installing Git

Appendix slide · outside the main lecture time

This appendix slide is an installation reference. Git --version shows the installed version. If Git is not installed, choose the appropriate method from the official Git website. We should not assume that every Mac already has Git; it depends on the environment. Git for Windows can provide Git Bash on Windows. A distribution's package manager is a common choice on Linux. The installation method does not change the core Git concepts.

Installation choices: Windows: Git for Windows, with Git Bash or a suitable terminal. macOS and Linux: A package or installation method suited to the operating system.

Additional explanation: Version numbers vary. Current instructions: git-scm.com/install

What the code means:

- `git --version` prints the Git version available to the terminal.
- It checks the installation; it does not install Git or create a repository.

Sources:

- [Installing Git](https://git-scm.com/install/)

## Appendix 2. Commit identity

Appendix slide · outside the main lecture time

These settings define commit identity and the default branch name for new repositories. The displayed name and email are examples; use the appropriate real information in an actual setup. Global configuration applies to the user account, and a repository can have its own local overrides. If the commit email appears in public history, privacy preferences also matter. These settings do not sign us in to GitHub or grant permission to push. Authentication is a separate concern.

Additional explanation: The name and email are examples. These settings do not authenticate you to GitHub.

What the code means:

- `git config --global` sets values for this user account. A repository can override them locally.
- `user.name` and `user.email` label new commits. They do not sign you in to GitHub.
- `init.defaultBranch main` sets the first branch name for future repositories; it renames no existing branch.

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

Additional explanation: Do not edit .git by hand. .gitignore does not remove tracked files from history.

What the code means:

- `robot-projem/` is the project folder. `.git/` holds local Git history and settings.
- `README.md` explains the project; `robot.ino` contains the source code.
- In `.gitignore`, `build/` excludes that untracked directory and `.env` excludes that untracked filename.
- `#` starts a comment. Ignore rules erase neither tracked content nor past secrets.

Sources:

- [gitignore](https://git-scm.com/docs/gitignore)
- [Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)

## Appendix 5. An SSH key pair

Appendix slide · outside the main lecture time

SSH authentication uses a public and private key pair. Current documentation recommends Ed25519, though older systems may need an alternative. The .pub file is added under SSH and GPG keys in the GitHub account. The private key is never shared or uploaded to a repository. The example email is only a label. A passphrase protects the key, and an SSH agent makes it easier to use during a session. When generating a new key, avoid accidentally overwriting an existing file.

Additional explanation: A passphrase adds protection. Do not overwrite an existing key.

What the code means:

- `ssh-keygen` creates a key pair. `-t ed25519` selects its type; `-C` adds a descriptive label.
- `~` means the user’s home directory. The example paths are filenames, not extra commands.
- Add the `.pub` public key to GitHub. Keep the private key without `.pub` to yourself.

Sources:

- [SSH keys and the SSH agent](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
- [Adding a public key to GitHub](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)

## Appendix 6. SSH agent and connection

Appendix slide · outside the main lecture time

These commands are a short agent example for Bash or Git Bash. Details differ for macOS Keychain and the Windows OpenSSH service. The same configuration is not mandatory on every operating system. On the first SSH connection, the server's identity is checked against GitHub's published key fingerprints. A successful authentication message confirms SSH access to the account, but GitHub does not provide general shell access. Even when the key connection succeeds, repository write permissions still apply separately.

Additional explanation: macOS Keychain and Windows OpenSSH steps may differ; follow the official instructions.

What the code means:

- `#` begins a comment. This setup example uses Bash or Git Bash.
- `ssh-agent -s` starts an agent; `$(...)` captures its settings; `eval` applies them to this shell.
- `ssh-add` loads the private key into the agent.
- `ssh -T` checks GitHub authentication without requesting a terminal.
- GitHub offers no shell access. Successful `ssh -T` authentication normally returns exit code 1.

Sources:

- [SSH keys and the SSH agent](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

## Appendix 7. Starting a local repository

Appendix slide · outside the main lecture time

Init starts a local Git repository in an existing folder. The example names main explicitly and records the existing README and robot code as the first commit. Remote add associates the remote address with the name origin. Origin is a conventional name, not a password or special service. Init does not create a repository on GitHub. This example assumes that the remote has already been created and is empty. If the remote contains initial commits, such as a README, cloning it may be simpler than creating two independent histories.

Additional explanation: This example starts locally. `git init` does not create a repository on GitHub.

What the code means:

- `cd robot-projem` enters an existing folder; it creates no folder.
- `git init -b main` starts a local repository with `main` as its first branch name.
- `git add README.md robot.ino` stages these two files. Nothing has been committed or uploaded yet.

Sources:

- [git init](https://git-scm.com/docs/git-init)
- [git remote](https://git-scm.com/docs/git-remote)

## Appendix 8. First commit and remote address

Appendix slide · outside the main lecture time

Init starts a local Git repository in an existing folder. The example names main explicitly and records the existing README and robot code as the first commit. Remote add associates the remote address with the name origin. Origin is a conventional name, not a password or special service. Init does not create a repository on GitHub. This example assumes that the remote has already been created and is empty. If the remote contains initial commits, such as a README, cloning it may be simpler than creating two independent histories.

Additional explanation: The local record and remote address are ready. The first push follows separately.

What the code means:

- `git commit -m` records the staged content with the quoted message in local history.
- `git remote add origin` saves the real remote address under the name `origin`.
- Replace `<repository-url>` without angle brackets. `git remote -v` lists fetch and push addresses; it uploads no files.

Sources:

- [git init](https://git-scm.com/docs/git-init)
- [git remote](https://git-scm.com/docs/git-remote)

## Appendix 9. First push and tracking

Appendix slide · outside the main lecture time

On the first push, -u establishes tracking between local main and remote origin/main. With suitable configuration, later push and pull commands can use that relationship to find their target. This tracked remote branch is sometimes called the upstream branch. That is a different context from a remote named upstream for the original project in a fork workflow. The branch does not have to be called main, though that is the name used throughout this presentation. Always check the actual branch name and remote address.

Additional explanation: Check the branch name with git branch. Commands must use the project’s actual branch name.

What the code means:

- `git push -u origin main` sends local `main` commits and records the tracking relationship.
- With suitable tracking and configuration, `git push` sends later commits without repeating the remote and branch.
- `git pull --ff-only` gets updates and stops if histories diverge. These examples are not a mandatory sequence.

Sources:

- [git branch](https://git-scm.com/docs/git-branch)

## Appendix 10. Task branch and current branch

Appendix slide · outside the main lecture time

Git switch -c creates a branch and switches to it. In the branch list, an asterisk marks the current branch. When diff compares two branch tips, the first name is the before side and the second is the after side. The minus and plus signs are read in that direction. A three-dot comparison shows the second branch's changes relative to their common starting point. If completion is available, type a prefix at the start of the name, such as feature. A word from the middle of a branch name is not guaranteed to complete in every environment. Shell settings affect the result.

Additional explanation: A branch name points to a commit; creating it creates no new project directory.

What the code means:

- `git branch` lists local branches and marks the active one with a star.
- `git switch -c` creates the named branch from the current commit and switches to it.
- Here `feature/sensor-esigi` is the branch name. To start from `main`, first be on `main`.

Sources:

- [git switch](https://git-scm.com/docs/git-switch)
- [git diff](https://git-scm.com/docs/git-diff)

## Appendix 11. Two ways to compare the branches

Appendix slide · outside the main lecture time

Git switch -c creates a branch and switches to it. In the branch list, an asterisk marks the current branch. When diff compares two branch tips, the first name is the before side and the second is the after side. The minus and plus signs are read in that direction. A three-dot comparison shows the second branch's changes relative to their common starting point. If completion is available, type a prefix at the start of the name, such as feature. A word from the middle of a branch name is not guaranteed to complete in every environment. Shell settings affect the result.

Additional explanation: The first comparison is limited to robot.ino; the three-dot example compares the feature branch’s full change.

What the code means:

- `git diff main feature/sensor-esigi` compares the final states of both branches.
- `-- robot.ino` limits comparison to this file; `--` separates branch names from the path.
- `main...feature/sensor-esigi` compares the common starting commit with the task branch tip.

Sources:

- [git switch](https://git-scm.com/docs/git-switch)
- [git diff](https://git-scm.com/docs/git-diff)

## Appendix 12. Choose what you want to undo

Appendix slide · outside the main lecture time

Before undoing, decide what should change. Restore --staged removes an accidentally added file from staging while preserving its edits in the working tree. Revert creates a new commit to reverse an earlier shared change, keeping shared history intact. Reset moves the branch's position and, depending on the mode, changes staging or working files as well. The default mixed mode preserves working files but moves the history position. Reset and revert therefore do not have the same purpose or effects.

Sources:

- [git restore](https://git-scm.com/docs/git-restore)
- [git revert](https://git-scm.com/docs/git-revert)
- [git reset](https://git-scm.com/docs/git-reset)

## Appendix 13. Hard reset and recovery limits

Appendix slide · outside the main lecture time

Hard reset moves a branch to the selected commit and makes the staging area and tracked working files match it. Uncommitted edits can be lost, and some untracked files in the way can also be affected. A previously committed state may sometimes be found in the local reflog, so calling every hard reset irreversible is inaccurate. But reflog is not a general backup and does not keep everything forever. We should not assume that work never committed can be recovered. First inspect status and the changes. Do not use hard reset without understanding its effects.

Additional explanation: Reflog may help find earlier commits; it cannot guarantee recovery of all unrecorded work.

What the code means:

- `git reset --hard <commit>` moves the branch and replaces staging and tracked working files with that commit’s state.
- Uncommitted edits can be lost. Some untracked files in the way can also be affected.
- `git reflog` lists local reference movements. It may locate earlier commits but cannot recover every unsaved change.

Sources:

- [git reset](https://git-scm.com/docs/git-reset)
- [git reflog](https://git-scm.com/docs/git-reflog)

## Appendix 14. Selecting committing and sending a file

Appendix slide · outside the main lecture time

This final appendix slide is a short reference for the daily workflow. Clone provides a starting point, but a new commit requires an actual file edit first. Status shows the state, add selects changes, commit records them, and push sends them. Pull brings in the team's updates. A branch provides a place for a separate task, and a PR supports review. We do not need to run every command in sequence each time. We choose the next operation by checking whether the change is in the working tree, staging area, or local history.

Additional explanation: Replace placeholders with real values. Installation, identity, and permissions must be in place.

What the code means:

- `git clone` copies a repository. Then enter its project folder.
- `#` starts a comment reminding us to edit and save first.
- `git status` checks files and staging.
- `git add <file>` selects that file’s current content.
- `git commit -m` records staging with a message; `git push` sends commits.
- Replace `<repository-url>` and `<file>` with real values.

Sources:

- [Git and GitHub learning resources](https://docs.github.com/en/get-started/start-your-journey/git-and-github-learning-resources)

## Appendix 15. Remote updates and a new task branch

Appendix slide · outside the main lecture time

This final appendix slide is a short reference for the daily workflow. Clone provides a starting point, but a new commit requires an actual file edit first. Status shows the state, add selects changes, commit records them, and push sends them. Pull brings in the team's updates. A branch provides a place for a separate task, and a PR supports review. We do not need to run every command in sequence each time. We choose the next operation by checking whether the change is in the working tree, staging area, or local history.

Additional explanation: Replace placeholders with real values. Installation, identity, and permissions must be in place.

What the code means:

- `git pull --ff-only` fetches remote changes and advances the active branch only if histories have not diverged.
- `git switch -c feature/<task>` creates and switches to a task branch. Replace `<task>` with its actual short name.
- `#` introduces explanatory comments. Pull needs suitable remote tracking; branch creation does not require a new folder.

Sources:

- [Git and GitHub learning resources](https://docs.github.com/en/get-started/start-your-journey/git-and-github-learning-resources)
