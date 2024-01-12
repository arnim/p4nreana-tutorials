## Git basics
### Basic setup (from GitLab):
1. create a new project on GitLab (tip: make it private at the beginning, you can change that later)
2. create a new folder on your laptop where the project will be stored
3. clone the repository in your local folder (i.e. make a copy of the remote project on your local machine)
   * on your project page, select Clone and copy the URL for “Clone with SSH”
   * open a terminal on your computer and go to the directory you created
   * enter  `git clone <URL you copied>`
   * go to the new directory that was created (same name you gave to the project)

Now your local directory and the remote repository are linked!  
A very useful command:  `git status`
 
### Basic setup (from local folder):
1. create or go to a folder on your local machine
2. make it a git repository:  `git init`
3. create a new EMPTY project on GitLab and copy its URL
4. link the two:  `git remote add origin <URL you copied>`

You can check all remote repositories connected to this folder with  `git remote -v`

### Basic Git workflow
Say you added or modified a file within the project on your local folder, e.g. “myscript.sh”.  
How do you synchronize these changes with the remote repository?
* add the file you want to update: `git add myscript.sh`
* commit the changes (remember to include a meaningful comment!):  
  `git commit -m "Added a new for loop to the script"`
* push (i.e. send) the changes to the remote repository: `git push origin main`

*** For now, we did not create any new branches, so the default will be “main”. ***

After each step you can (should!) run  `git status`  and see what the previous command did.  
Now the two systems are synchronized again, and you can see the updated file on GitLab together with the comment you wrote under “Last commit”.

Notice that you can add more than one file at a time (`git add .` or `git add -A` adds them all)  
For modified (NOT NEW) files, you can add and commit at the same time:  `git commit -am "Comment"`

### Branches and Merging
Say you want to modify your code without influencing the current version (very useful, e.g., when you collaborate on a project within a team). The best way to do it is to create a branch, i.e. a “parallel universe” where you can make all the changes and tests you want without any modifications to the main version:
* on your local machine, create a new branch, e.g. called “test”, with: `git switch -c test` (NB: you are automatically switched to this new branch!)
* modify your code as you want
* follow the basic Git workflow to update the code on GitLab: add, commit, push. Now when you push, you need to specify the current branch: `git push origin test`

Now the new branch is also on GitLab!

To list all the branches available: `git branch`  (the one with the * is the current one)  
To switch to another branch, e.g. master: `git switch master`  
Remember that you can check the differences between files with  `git diff`

Now your code is fully developed and tested, and you want to include it in the main release. To do so, you create a merge request (similar to a pull request on GitHub):
* on GitLab, switch to the “test” branch, and click on “Create merge request”. You should add a title and a meaningful description of the changes you developed.
* Now other people (if you are in a team) can add comments/questions/suggestions in the thread. When everything is solved and sorted, the owner of the repository can approve the request and finally merge the “test” branch into the “main” branch.  
  NB: when you create the merge request, there is an option by default saying “Delete source branch when merge request is accepted.” Check it only if you want this to happen!  
  *** It’s less common, but you can also merge directly from the local repository by switching to the “main” branch and doing  `git merge test` and then  `git push`  ***
* Locally, switch to the “main” branch (**git switch main**) and update you repository with all the new changes:  
  `git fetch –all`  *** IMPORTANT STEP ***  
  `git pull origin main`
* If you did not automatically delete the branch and you want to do it:  
  `git branch -d test`  (locally)  
  `git push origin -d test`  (remotely)

In real life, merge conflicts will happen a lot of times! For example, another person might have worked on another part of the code and already merged it to the main branch, but you don’t have those updates yet. Or you forgot that you also changed some files on the main branch. Don’t panic and see what git says to understand how to resolve them (this can be useful too: [GitLab merge conflicts](https://docs.gitlab.com/ee/user/project/merge_requests/conflicts.html)).

Another very useful command is `git log` which lists the commit history of the current branch. The long number you see after each “commit” can be very useful, e.g., to restore your code to a previous version.

### Set up a default branch
Set upstream:  `git push -u origin main`  
In the future  `git push`  will be on main by default 
