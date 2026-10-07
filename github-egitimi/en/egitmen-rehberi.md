# Git and GitHub: How We Build Together

34 main slides and 6 appendix slides. The main lecture and questions take 45 minutes.

No live demonstration, in-class exercise or required homework. Appendix slides are outside the main lecture time.

## 1. Git and GitHub

00:00–00:45 · 45 seconds

A project is more than its final product. The decisions, experiments and lessons along the way are part of it too. Today we will look at how work changes over time and how people contribute to the same project. Our examples come from student projects, research, companies and open source. Git keeps history; GitHub provides a shared place to discuss and review changes. We will consider the benefits alongside learning, record-keeping and coordination. The aim is to understand which problems these tools address and where they could help in your own work. Being able to continue a project matters alongside finishing its first version.

Image: an illustrative drawing created for this lesson, rather than a photograph of a real group.

Sources:

- [Git What is Git?](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F)
- [GitHub What is GitHub?](https://docs.github.com/en/get-started/start-your-journey/what-is-github)

## 2. Changing projects and personal memory

00:45–01:45 · 60 seconds

A microcontroller setting, an experiment's analysis method or a report section may change. Each change involves a decision. The current file shows the result, while earlier options and reasons may disappear. When a problem appears later, even its author may struggle to remember why a change was made. Dates in filenames, extra copies and messages containing the latest version help for a while. As people and changes multiply, those copies become harder to relate to one another. Version control helps keep an understandable history, so we can revisit the work.

Sources:

- [Git About Version Control](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control)

## 3. Working alone: find your way back

01:45–03:00 · 75 seconds

You do not need a large team to benefit from Git. When you open your program three months later, you may recognize the files without remembering why a setting changed. A readable history lets you revisit those decisions, compare recorded states and continue from an earlier state. That narrows an investigation; it does not explain a bug automatically. An unsuccessful experiment need not mean abandoning all your work. You have records to examine rather than guesses. You must actually record the changes and describe them clearly. Git does not automatically remember work you have not committed.

Sources:

- [GitHub About Git](https://docs.github.com/en/get-started/using-git/about-git)

## 4. Which file should we continue from?

03:00–04:15 · 75 seconds

Imagine a student team's folder filling with copies named final, final2 and really_final. The filenames alone do not show which was handed in, which works or why it changed. One person may move a sensor, another add filtering and a third revise the chart. Separate copies do not reveal the relationships between those decisions. Version control lets us examine recorded states and their changes together. Instead of making filenames longer, we can identify the record behind each change. History gives an investigation a starting point; it does not prove the cause of a measurement problem. Hardware and environmental conditions also matter. The benefit is knowing where to continue and what to investigate.

Sources:

- [Git About Version Control](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control)

## 5. What does version control record?

04:15–05:30 · 75 seconds

Version control is the general name for methods that track work over time. Git is one tool for doing this. It keeps recorded history alongside the latest file contents. Clear descriptions can reveal the purpose of changes. Unlike copying files into separate folders, version control organizes the relationships between recorded states. It does not record every keystroke automatically: you choose what to record and when. This makes it both a tool and a working habit. Its value becomes clear when a project grows or when you need to ask a question about the past.

Sources:

- [Git What is Git?](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F)

## 6. Git: a tool for project history

05:30–07:00 · 90 seconds

Git is a version control tool that can run on your computer. A project tracked with Git is called a repository. Think of the files together with their recorded history. A robot project might contain software, setup instructions and text-based test results. You decide which files to track, rather than adding every folder indiscriminately. Git relates recorded states and lets you compare them. A GitHub account is not required. Imagine adding a history to a project folder. The tool keeps the records, but you need to explain the reasons for the changes.

Sources:

- [Git What is Git?](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F)
- [GitHub About Git](https://docs.github.com/en/get-started/using-git/about-git)

## 7. GitHub: discuss changes together

07:00–08:30 · 90 seconds

Git tracks change history. GitHub is one platform that hosts Git repositories and supports collaboration around them. You can share a project, discuss a problem, review a proposed change and decide whether to accept it. Its value goes beyond putting files online: explanations, conversations and decisions can sit alongside the work. Projects can be public or have restricted access. You can choose another hosting platform or use Git entirely offline. The idea of collaboration belongs to the people and their workflow; GitHub is one widely used place to support it.

Sources:

- [GitHub What is GitHub?](https://docs.github.com/en/get-started/start-your-journey/what-is-github)

## 8. Local work and sharing

08:30–09:45 · 75 seconds

Git is distributed. A normal full clone gives you a local copy of the project and its history. You can edit files, inspect history and make records offline, then exchange changes when you have a connection. People need not constantly edit one central file. One student can work at home while another works in the laboratory. Independence does not mean automatic agreement: combining work still requires decisions and sometimes resolving conflicts. Records you have not shared stay on your own computer. Recording locally and sharing are separate steps.

Sources:

- [Git About Version Control](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control)
- [Git What is Git?](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F)

## 9. Commit: a record with a description

09:45–11:00 · 75 seconds

Making a commit adds a recorded state to Git history. The resulting record is also called a commit. Think of a stop along the way, with a description attached. When you add a filter to sensor readings, you can group the change and its purpose in a record. This is separate from saving a file in your editor. You deliberately choose which changes enter the history. A commit does not prove the work is correct or complete. Making a local commit is also separate from sending it to GitHub: recording and sharing do different jobs.

Sources:

- [Git What is Git?](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F)

## 10. What does history establish?

11:00–12:00 · 60 seconds

History makes engineering evidence more specific. Instead of saying something changed last week, we can identify the files and record involved. A clear description explains the intended result. But a record is not a certificate of correctness: faulty code and incomplete reports can be committed too. Compilation, safe robot behavior and valid experiments need other checks. Descriptions are written by people, so their reasoning may need reconsidering. Git makes our claims easier to trace. Tests, measurements, review and scientific methods remain necessary. We can ask concrete questions and revisit the decisions we made.

Sources:

- [Google What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)

## 11. Small changes, understandable decisions

12:00–13:15 · 75 seconds

Changing motor control, interface colors, a report title and the folder layout in one commit can make it difficult to understand later. Keeping related work together and unrelated purposes separate makes history easier to read. This does not mean a record for every line; the useful measure is a clear purpose. Explaining that an average was added to reduce sensor noise tells a future reader more than saying things were fixed. Writing the explanation takes time now. It can save you or someone else from guessing weeks later.

Sources:

- [Google Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)

## 12. Branch: a separate path of work

13:15–14:30 · 75 seconds

A branch lets you develop a separate path from the same project history. While a robot's existing software is in use, you could try a new control method on another branch. Someone else can work on a different task from the same starting point. Think of branches as paths through history, rather than entirely separate copied folders. Suitable results can enter the shared work; unsuitable ones can be left out. Too many long-lived branches can make coordination harder. The idea is to give work space before deciding to put it into the version everyone uses.

Sources:

- [Git Branches in a Nutshell](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)

## 13. Merge: bring work together

14:30–16:00 · 90 seconds

Changes to different files or independent areas can often merge automatically. If two people change the same line differently, Git may be unable to choose a result. A conflict needs a human decision. Even without a visible conflict, changes may not work well together. A document could change sensor wiring while software still expects the old connection: the files combine, but the system may fail. Merging therefore needs engineering judgment as well as a technical operation. The team considers purpose, consequences and the shared project's needs.

Sources:

- [GitHub Merge conflicts](https://docs.github.com/en/pull-requests/reference/merge-conflicts)

## 14. In a team: make progress in parallel

16:00–17:15 · 75 seconds

If everyone waits for one person to send a file, tasks form a queue. Separate paths let different jobs progress together: one person can improve sensor data while another updates instructions. Independence still requires communication about boundaries, expectations and when work comes together. Git and GitHub connect those conversations to the changes. A reviewer sees the difference and the explanation. The gain is understanding contributions, requesting revisions and keeping the decisions. Disagreement does not disappear, but it can be discussed through concrete changes instead of competing file copies.

Sources:

- [GitHub GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow)

## 15. How do people use this day to day?

17:15–18:30 · 75 seconds

Work can begin with a need: an unreadable chart, missing instructions or a reported bug. Someone prepares a change, records it and shares it. Others may review it. A suitable change enters the shared project; other proposals need revision. Details vary: someone working alone may choose a simple process, while a large project may need more checks. Git records the effects on files. GitHub can connect the need, proposal, comments and decision. Issues and pull requests have places within this everyday flow. Every team need not follow exactly the same method.

Sources:

- [GitHub GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow)

## 16. Issue: a need we can discuss

18:30–19:30 · 60 seconds

An issue records discussion and follow-up around a topic. It can describe a bug, an improvement or a question. Saying a robot sometimes stops is a start; explaining the conditions, version and frequency makes it easier to investigate. Others can ask questions and add evidence in the same place. The topic stays connected to the project instead of getting buried in messages. Not every issue needs a code change: sometimes an explanation is enough or an idea is declined. Teams may use other tools. The benefit is keeping a clear, findable record of the need and expectations.

Sources:

- [GitHub About issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues)

## 17. Pull request: propose a change

19:30–20:45 · 75 seconds

A pull request, or PR, proposes bringing changes into another line of work. Differences, explanations, comments and checks can appear together. Opening a PR does not automatically add the change to the version everyone uses. Reviewers can ask questions, request revisions or decline it. Documentation changes can be proposed too. The idea is to separate preparing a change from deciding to include it. Trying an idea in your own space is one step; accepting it into shared work affects others. A PR makes that decision discussable through explanations and records.

Sources:

- [GitHub About pull requests](https://docs.github.com/en/pull-requests/get-started/about-pull-requests)

## 18. Review: a second pair of eyes

20:45–22:15 · 90 seconds

Review involves more than finding spelling mistakes. A reviewer considers purpose, effects on other parts and the available explanation. In a Matplotlib proposal, the discussion asks whether extra detail in a chart example distracts from its main topic. The concern is the reader's understanding alongside the code. This is an example of a proposal being discussed, rather than an accepted outcome. A second reader can question the author's assumptions. Review does not guarantee perfection: people have limited time and information. Specific, respectful comments with reasons are more helpful than vague criticism. Evaluate the proposed work rather than the person. Used well, review makes technical decisions easier to discuss.

Sources:

- [Google What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
- [Matplotlib PR #32416](https://github.com/matplotlib/matplotlib/pull/32416)

## 19. History, review and testing do different jobs

22:15–23:15 · 60 seconds

History traces what changed. Human review evaluates purpose and assumptions. A test or experiment checks expected behavior under selected conditions. GitHub can display automated check results, but those checks must be configured. Opening a repository does not create all the tests. A successful check is evidence for the conditions it covers, rather than an unlimited guarantee. Actual hardware and environmental conditions matter in physical systems. Git and GitHub can bring evidence together. Deciding which evidence is sufficient remains an engineering responsibility.

Sources:

- [Google What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
- [GitHub GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow)

## 20. In a student project: a shared hand-in

23:15–24:45 · 90 seconds

Four mechatronics students might divide embedded software, data logging, instructions and a report. A repository can connect suitable files to the recorded state used for the hand-in. Tasks and change proposals show what the group is waiting for. This does not automatically establish equal effort. Commit count is not a measure of quality or someone's whole contribution; laboratory work, hardware design and discussions matter too. A small group can start with a simple routine rather than every feature. The main benefit is less dependence on one person's computer and memory.

Sources:

- [GitHub GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow)

## 21. In research: keep a trail of the method

24:45–26:00 · 75 seconds

The path to a chart matters alongside the chart. Connecting analysis code, settings and method descriptions to history helps identify which state produced a result. Researchers can examine changing assumptions later. Git supports traceability but does not make a study reproducible alone. Data locations, the environment, software versions and processing steps also need explanation. Large datasets, confidential information and personal data need suitable storage and access decisions. The gain is a trail of the method. Scientific validity still requires measurement, sound methods and evaluation.

Sources:

- [Matplotlib Contributing guide](https://matplotlib.org/devdocs/devel/contributing.html)
- [GitHub About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)

## 22. In a company: share changes with checks

26:00–27:30 · 90 seconds

A product often involves different expertise. A useful feature can create costs for maintenance, security or another component. Preparing changes separately and reviewing their effects creates room for discussion. Permissions and checks can match the needs. Companies may use different platforms or simpler workflows. Connecting tests, releases and deployment to history takes effort to establish and maintain. An account alone does not create a company process. The benefit is making changes and decisions easier to trace and evaluate. Details depend on product risk and team structure.

Sources:

- [GitHub GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [Google What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)

## 23. In open source: work with people you have never met

27:30–29:00 · 90 seconds

People who have never met can contribute to open source projects. Reporting a bug or clarifying documentation is a contribution too. In Arduino Servo, a user reports a problem and another person proposes correcting related documentation, linking to that issue. This is a real path from observation to proposal, rather than an accepted result. A GitHub fork creates a related repository under your account. You can work there without permission to write directly to the original project, then propose a change. Maintainers are not obliged to accept it. A publicly readable repository is not automatically open source; the license sets reuse terms. Clear rules, explanations and visible decisions help different people collaborate.

Sources:

- [Arduino Servo issue #64](https://github.com/arduino-libraries/Servo/issues/64)
- [Arduino Servo PR #130](https://github.com/arduino-libraries/Servo/pull/130)

## 24. Hand the project over to the next person

29:00–30:15 · 75 seconds

A project may continue after students graduate or someone changes roles. Latest files alone may be insufficient. Newcomers need to know which state is in use, how to set it up, known problems and reasons behind decisions. History, documentation and discussion can answer these together. Hardware connections, physical measurements and organization-specific processes may need separate explanation. A good handover reduces the need to ask the former contributor every question again. Git and GitHub support continuity, but people must keep the relevant explanations current.

Image: an illustrative drawing created for this lesson, rather than a photograph of a real group.

Sources:

- [GitHub About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- [GitHub Backing up a repository](https://docs.github.com/en/repositories/archiving-a-github-repository/backing-up-a-repository)

## 25. README: the entrance to a project

30:15–31:30 · 75 seconds

A README is often the first explanation a repository visitor sees. It helps people understand the purpose and starting steps without guessing from the files. What does the project do, who is it for, how do you prepare and use it, and what are its limits? Hardware projects need suitable board and connection information. A README can point to more detailed documents instead of containing everything. Clear and current information serves readers. In an MDN Web Docs proposal, the author describes checking history to understand the intended meaning before correcting text. Documentation and history can work together. Handover and contributions depend on taking a new reader's questions seriously.

Sources:

- [GitHub About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- [MDN PR #45998](https://github.com/mdn/content/pull/45998)

## 26. Working culture and shared responsibility

31:30–32:45 · 75 seconds

Visible changes do not automatically mean mutual understanding. Unexplained records, unclear tasks and comments without reasons reduce the value of tools. A discussion space cannot guarantee good communication. Expectations should be clear, criticism should address the work, and decisions should have reasons. Every small preference does not need a lengthy debate, but important context should be kept. Teams decide who reviews, when work is shared and what needs checking. These are social and technical decisions. The quality of collaboration comes from the people's habits and attitudes.

Sources:

- [Google What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)

## 27. The cost: learning and keeping records

32:45–34:00 · 75 seconds

Even a freely available tool takes time and attention to learn. Understand editing, recording and sharing as separate actions. Grouping changes and writing descriptions adds immediate effort, so the first day can feel slower than copying files. Value often appears later, when revisiting history or collaborating. It differs between projects: a complex routine may be unnecessary for a small one-off draft. Beginners need not learn every feature at once. They can develop clear habits gradually. Consider the effort realistically alongside the project's needs.

Sources:

- [Git About Version Control](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control)

## 28. The cost: coordination and waiting

34:00–35:30 · 90 seconds

Sharing a change does not mean immediate use. Waiting for review, answering questions and revising take time. Coordination can grow harder in larger teams. Long-separated work may be difficult to combine, and competing changes need choices. Rigid processes may delay small tasks; loose ones can make shared work harder to understand. Changes need not all receive identical treatment. A student group and a large company have different needs. Git and GitHub support the choices but do not choose the right process automatically. People still need to organize and sustain the work. A copy of Git history does not automatically contain every platform conversation or work-tracking record. Moving platforms also needs planning.

Sources:

- [GitHub GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [Google Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)
- [GitHub — About GitHub Importer](https://docs.github.com/en/migrations/importing-source-code/using-github-importer/about-github-importer)

## 29. Visibility: set boundaries when sharing

35:30–37:00 · 90 seconds

Public repositories can help people discover and examine work, but can also expose information that should remain restricted. Passwords, access keys, personal data and confidential material need care. Removing information from the current file does not remove every earlier copy. An exposed credential must be revoked or replaced; deleting the file alone is insufficient. Private repositories also leave responsibilities around access and sharing. The basic idea is to decide deliberately who should see what, remembering that sharing may include history.

Sources:

- [GitHub Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [GitHub What is GitHub?](https://docs.github.com/en/get-started/start-your-journey/what-is-github)

## 30. Public repositories and licensing

37:00–38:15 · 75 seconds

Publicly readable content is not automatically available for unrestricted reuse. A license defines conditions for using, changing and distributing the work. Open source licenses differ. Sharing your own project also requires understanding the terms of code and materials obtained from others. Modifying a file does not remove its earlier rights. This lesson does not compare every license. The key distinction is between access and permission to reuse. Read the project's license and contribution guidance before joining its work. Clear permissions help make sharing sustainable.

Sources:

- [GitHub Licensing a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)

## 31. Which problems does Git leave to us?

38:15–39:30 · 75 seconds

Git is especially useful for comparing text-based changes. Large binary files, CAD and large datasets may need extra tools and storage choices. Keeping a file's versions does not always provide meaningful comparison or merging. Physical connections, laboratory settings and sensor positions also need suitable documentation. Git does not test the system or automatically protect unrecorded work. Other copies of history can help, but do not cover every device, data and access risk. Use history alongside appropriate engineering records, tests and a backup plan. Large-file storage services may charge according to usage.

Sources:

- [GitHub About Git LFS](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage)
- [GitHub Backing up a repository](https://docs.github.com/en/repositories/archiving-a-github-repository/backing-up-a-repository)
- [GitHub — Git LFS billing](https://docs.github.com/en/billing/concepts/product-billing/git-lfs)

## 32. Does every task need the same process?

39:30–40:45 · 75 seconds

A widely used method need not be applied identically to every task. Frequent code changes, revisiting earlier states, collaboration and handover can increase Git's value. Complex branches and mandatory review stages may be too much for a one-off draft. Basic history and a large-team process are different. A solo project can use Git simply. Specialized binary designs may call for other tools alongside it. Choose according to the problem, not merely popularity. Habits can carry to future projects, but maintaining them requires time and attention.

Sources:

- [GitHub What is GitHub?](https://docs.github.com/en/get-started/start-your-journey/what-is-github)
- [GitHub About Git LFS](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage)

## 33. Three questions for your next project

40:45–42:00 · 75 seconds

You need not memorize all the terms. Three questions may help in your next project: which state works, why was it changed, and could someone continue without you? Git and GitHub can support answers, but choosing a tool alone does not provide them. Recording, explaining and deciding together are habits. Begin simply and adapt as needs grow. Today is about understanding the value of readable history. Remembering these reasons can make the technical details more meaningful when you learn them.

Sources:

- [GitHub About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)

## 34. Questions and discussion

42:00–45:00 · 180 seconds

Leave three minutes for questions. Students can share experiences of not knowing which file to continue from, missing a teammate's reasoning or struggling with an old project. Connect the discussion to Git versus GitHub, recording versus sharing and the tool's limits. History does not guarantee correctness; future you is also a reader. Refer detailed questions about licensing or confidential data to official guidance. The learning outcome is weighing understandable history and visible decisions against the effort needed. The appendix supports detailed questions and later reading.

Sources:


## Appendix 1. Four essential terms

Appendix slide · outside the main lecture time

A repository, commit, branch and pull request are different. The repository holds the tracked project and history. A commit records a particular state with a description. A branch is a separate path from the same history. A pull request proposes bringing changes into shared work on a platform such as GitHub. Repositories and commits can be local. A PR provides discussion and a decision around the work; it does not replace a commit.

Sources:

- [Git What is Git?](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F)
- [GitHub About pull requests](https://docs.github.com/en/pull-requests/get-started/about-pull-requests)

## Appendix 2. What can a README answer?

Appendix slide · outside the main lecture time

No single README template suits every project. These questions address a new reader's needs. Setup and usage can be different steps. Hardware projects should point to appropriate connection and safe-use information. Help channels, limits and licensing may need explanation. Clarity and current information matter more than length. Help the reader get started without inspecting every file and guessing what to do.

Sources:

- [GitHub About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)

## Appendix 3. A change proposal people can understand

Appendix slide · outside the main lecture time

A PR description explains the need, scope, checks and open questions. A small correction may need little text, while a riskier change needs more context. The purpose is the information needed to decide, not length. Link to a relevant issue. Reviewers can then ask questions and request revisions. The explanation does not replace a test or experiment; it shows where to find the evidence.

Sources:

- [GitHub About pull requests](https://docs.github.com/en/pull-requests/get-started/about-pull-requests)
- [Google What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)

## Appendix 4. Choose according to the project's needs

Appendix slide · outside the main lecture time

These comparisons are not a scoring test. History helps with frequently changing code and text. Explanations and discussions gain value in collaboration and handover. Large binary files and specialized designs may need suitable storage and comparison alongside Git. The process should fit the need. A simple routine people sustain can be more useful than a detailed process they cannot maintain.

Sources:

- [GitHub About Git LFS](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage)
- [Git About Version Control](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control)

## Appendix 5. Four useful working habits

Appendix slide · outside the main lecture time

These habits make sense before learning every platform feature. Related changes grouped together make history readable. Reasons reduce future guesses. Reviewing in proportion to the effects supports decisions. Current starting instructions help handover and restarting. None guarantees perfection; the process must be sustainable. Short descriptions and a simple flow may be enough for a small project.

Sources:

- [Google Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)
- [GitHub About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)

## Appendix 6. Sources and where to go next

Appendix slide · outside the main lecture time

The links expand the concepts and support later learning. The Git book explains version control and Git's approach. GitHub documentation covers repositories, issues, PRs and review, with guides to READMEs, licenses and access. Some sections become technical; reading all of them during the lesson is not expected. Start with a question and choose the relevant section. The presentation connects later technical learning to the purposes of these tools.

Sources:

- [Pro Git: the basic approach](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F)
- [GitHub Docs: GitHub and collaboration](https://docs.github.com/en/get-started/start-your-journey/what-is-github)
- [Arduino Servo: a user's contribution](https://github.com/arduino-libraries/Servo/pull/130)
- [Matplotlib: reviewing a change together](https://github.com/matplotlib/matplotlib/pull/32416)
- [MDN: a small documentation contribution](https://github.com/mdn/content/pull/45998)
