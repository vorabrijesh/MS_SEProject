from pydriller import Repository
import json
import numpy as np

### csv - rows = no.of developers, columns- months/yr.
### link to apache mailing list:  http://mail-archives.apache.org/mod_mbox/
###  for each commit add modified files to map with filename as keys.

file_to_users = {}  ## for each file how many users commited
file_to_id = {}     ##
i=0
url = "E:\\MS\\Qtr1\\ecs 260 se\\project\\tvm\\.git"

for commit in Repository(url).traverse_commits():
    print(
        'The commit  has been modified by {} and files changed are {}\n'.format(
           
            commit.author.email,
            [x.filename for x in commit.modified_files]
        )
    )
    for x in commit.modified_files:
        if x.filename not in file_to_users:
            file_to_users[x.filename] = set()
            file_to_users[x.filename].add(str(commit.author.email))
            if x.filename not in file_to_id:
                file_to_id[x.filename] = i
                i = i+1
        else:
            file_to_users[x.filename].add(str(commit.author.email))
            if x.filename not in file_to_id:
                file_to_id[x.filename] = i
                i = i+1


### Identifing unique users for each files
unique_users_dict = {}
unique_users = set()
i = 0
for x in file_to_users.keys():
    file_to_users[x] = list(file_to_users[x])
    for user in file_to_users[x]:
        if user not in unique_users_dict:
            unique_users_dict[user] = i
            i=i+1
        unique_users.add(user)
            

### Calculation of Actual Coordination - fct (file changed together)
## Assumption - 1 files - n developers have changed it. So they would have communicated at one point. 

list_unique_users = unique_users
AC = [[0]*len(list_unique_users) for x in range(0,len(list_unique_users))]

for key in file_to_users.keys():
    users = file_to_users[key]
    for i in range(0, len(users)):
        for j in range(i+1,len(users)):
            AC[unique_users_dict[users[i]]][unique_users_dict[users[j]]] = 1
            AC[unique_users_dict[users[j]]][unique_users_dict[users[i]]] = 1
            

### Calculation of Coordination needs matrix: TA * TD * TAT

CR = []
TA = [[0]*len(file_to_users.keys()) for x in range(0,len(list_unique_users))]
TD = [[0]*len(file_to_users.keys()) for x in range(0,len(file_to_users.keys()))]   
### TD - m * m; m = number of files TD[i][j] = ith file and jth file are dependent on each other.
### if in commit they are changed togteher they are dependent. So we have assumption of undirected graph.

for key in file_to_users.keys():
    list_of_users = file_to_users[key]
    for x in list_of_users:
        TA[unique_users_dict[x]][file_to_id[key]] = 1 

for commit in Repository(url).traverse_commits():
    modified_files_in_commit = commit.modified_files
    for i in range(0, len(modified_files_in_commit)):
        for j in range(i, len(modified_files_in_commit)):
            TD[file_to_id[modified_files_in_commit[i].filename]][file_to_id[modified_files_in_commit[j].filename]] = 1
            TD[file_to_id[modified_files_in_commit[j].filename]][file_to_id[modified_files_in_commit[i].filename]] = 1


### dump results to json files
with open('data.json', 'w') as fp:
    json.dump(file_to_users, fp, indent = 4)

with open('unique_users.json','w') as fp:
    json.dump(unique_users_dict, fp, indent = 4)


with open('ActualCoordination.json', 'w') as filepointer:
    json.dump(AC,filepointer)

with open('TaskAssignment.json', 'w') as filepointer:
    json.dump(TA,filepointer)

with open('TaskDependency.json', 'w') as filepointer:
    json.dump(TD,filepointer)

with open('CoordinationRequirement.json', 'w') as filepointer:
    json.dump(CR,filepointer)

