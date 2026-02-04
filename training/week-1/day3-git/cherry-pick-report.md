# Report for cherry-pick
Used when we have to pick and insert a specific commit from another branch(not the whole branch).
## Used Commands like:
git cherry-pick <commit-hash> \n
git cherry-pick --continue \n
\n
## Issues faced during utilizing the cherry-pick concept
A conflict error arose in the process.
## Solution 
Manually resolved the merge conflict and executed the cherry-pick --continue command.
## Observations
The hash value of the picked commit and the commit done by cherry-pick is different. This means that same link is not joined.
The differences in the original commit are identified and done in the different branch when the cherry-pick command is used.
