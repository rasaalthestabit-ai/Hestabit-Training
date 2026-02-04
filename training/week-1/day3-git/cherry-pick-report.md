# Report for cherry-pick \n
Used when we have to pick and insert a specific commit from another branch(not the whole branch).\n
\n
## Used Commands like:\n
git cherry-pick <commit-hash> \n
git cherry-pick --continue \n
\n
## Issues faced during utilizing the cherry-pick concept \n
A conflict error arose in the process. \n
\n
## Solution \n
Manually resolved the merge conflict and executed the cherry-pick --continue command. \n
\n
## Observations \n
The hash value of the picked commit and the commit done by cherry-pick is different. This means that same link is not joined.\n
The differences in the original commit are identified and done in the different branch when the cherry-pick command is used.
