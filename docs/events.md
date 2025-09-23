# Events

## Overview

Each event is structured into two parts:

- Attributes: metadata providing contextual information about the event and present in 
all types of events. The attributes are based on the CloudEvents specification.
- Data: other information specific to the event.


### Attributes

| Field       | Type           | Description                                               |
|------------ |---------------|-----------------------------------------------------------|
| id          | String         | Event identifier                                          |
| source      | URI-reference  | URL to the repository                                     |
| specversion | String         | The version of the CloudEvents specification used         |
| time        | Timestamp      | Timestamp of when the event happened                      |
| type        | String         | Defines the event type. Prefixed by 'org.grimoirelab'     |


## Events

### Git

Git events are related to commits in git repositories.

#### Commit

- Event type: `org.grimoirelab.events.git.commit`

| Field         | Type                           | Description                                                                                                                                                                                                                             |
|---------------|--------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Author        | `String`                       | Author of the commit                                                                                                                                                                                                                    |
| AuthorDate    | `String`                       | Date when the author originally made the commit                                                                                                                                                                                         |
| Commit        | `String`                       | Commiter of the changes                                                                                                                                                                                                                 |
| CommitDate    | `String`                       | Date when the commit was last modified                                                                                                                                                                                                  |
| commit        | `String`                       | Commit hash                                                                                                                                                                                                                             |
| files         | `List` ([file](#file-objects)) | Information about the changed files                                                                                                                                                                                                     |
| message       | `String`                       | Commit message                                                                                                                                                                                                                          |
| parents       | `List (string)`                | Hashes of logical predecessors in the line of development. See [parent](https://git-scm.com/docs/gitglossary#Documentation/gitglossary.txt-aiddefparentaparent) in Git documentation                                                    |
| refs          | `List (string)`                | Git references. See [ref](https://git-scm.com/docs/gitglossary#Documentation/gitglossary.txt-aiddefrefaref) in Git documentation                                                                                                        |
| Signed-off-by | `String`                       | A trailer at the end of the commit message to certify that the committer has the rights to submit the work. See [--signoff](https://git-scm.com/docs/git-commit#Documentation/git-commit.txt-code--no-signoffcode) in Git documentation |

#### Merge commit

- Event type: `org.grimoirelab.events.git.merge`

| Field      | Type                           | Description                                                                                                                                                                          |
|------------|--------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Author     | `String`                       | Author of the commit                                                                                                                                                                 |
| AuthorDate | `String`                       | Date when the author originally made the commit                                                                                                                                      |
| Commit     | `String`                       | Commiter of the changes                                                                                                                                                              |
| CommitDate | `String`                       | Date when the commit was last modified                                                                                                                                               |
| commit     | `String`                       | Commit hash                                                                                                                                                                          |
| files      | `List` ([file](#file-objects)) | List of files changed                                                                                                                                                                |
| Merge      | `String`                       | The tips of the merged branches                                                                                                                                                      |
| message    | `String`                       | Commit message                                                                                                                                                                       |
| parents    | `List (string)`                | Hashes of logical predecessors in the line of development. See [parent](https://git-scm.com/docs/gitglossary#Documentation/gitglossary.txt-aiddefparentaparent) in Git documentation |
| refs       | `List (string)`                | Git references. See [ref](https://git-scm.com/docs/gitglossary#Documentation/gitglossary.txt-aiddefrefaref) in Git documentation                                                     |

#### Commit file actions

| Field         | Type            | Description                                                |
|---------------|-----------------|------------------------------------------------------------|
| filename      | `String`        | Name of the file                                           |
| modes         | `List (String)` | Git file modes                                             |
| indexes       | `List (String)` | Git indexes                                                |
| similarity    | `String`        | Percentage of unchanged lines in copied or replaced files. |
| new_filename  | `String`        | Name of the new file                                       |
| added_lines   | `String`        | Number of added lines in the commit                        |
| deleted_lines | `String`        | Number of deleted lines in the commit                      |

##### File added

- Event type: `org.grimoirelab.events.git.file.added`

##### File modified

- Event type: `org.grimoirelab.events.git.file.modified`

##### File deleted

- Event type: `org.grimoirelab.events.git.file.deleted`

##### File replaced

- Event type: `org.grimoirelab.events.git.file.replaced`

##### File copied

- Event type: `org.grimoirelab.events.git.file.copied`

##### File type changed

- Event type: `org.grimoirelab.events.git.file.typechanged`

#### File objects

File objects found in the `files` field of [commit](#commit) and [merge commit](#merge-commit) events.


| Field   | Type            | Description                         |
|---------|-----------------|-------------------------------------|
| action  | `String`        | Identifier of the action performed  |
| added   | `String`        | Number of added lines in the file   |
| file    | `String`        | File name                           |
| indexes | `List (String)` | Git indexes                         |
| modes   | `List (String)` | Git file modes                      |
| removed | `String`        | Number of deleted lines in the file |


#### Commit contributors

Information about contributors related to a commit.

| Field    | Type     | Description                                       |
|----------|----------|---------------------------------------------------|
| name     | `String` | Name of the contributor                           |
| username | `String` | Username of the contributor                       |
| email    | `String` | Email of the contributor                          |
| uuid     | `String` | Unique identifier of the contributor              |
| role     | `String` | Role of the contributor.                          |
| source   | `String` | Source of the identity. Always `git` for commits. |

##### Author

Identifies the person who originally wrote the patch or commit.

- Event type: `org.grimoirelab.events.git.commit.authored_by`

##### Committer

Identifies the person who applied or committed the patch to the repository.

- Event type: `org.grimoirelab.events.git.commit.committed_by`

##### Acked-by

Identifies the person who is more familiar with the area the patch 
attempts to modify and has approved the patch.

- Event type: `org.grimoirelab.events.git.commit.acked_by`

##### Co-authored-by

Identifies people who exchanged drafts of a patch before submitting it.

- Event type: `org.grimoirelab.events.git.commit.co_authored_by`

##### Helped-by

Identifies someone who suggested ideas for changes without providing the precise 
changes in patch form.

- Event type: `org.grimoirelab.events.git.commit.helped_by`

##### Mentored-by

Identifies someone who helped develop a patch as part of a mentorship program 
(e.g., GSoC or Outreachy).

- Event type: `org.grimoirelab.events.git.commit.mentored_by`

##### Reported-by

Identifies the person who found the bug that the patch attempts to fix.

- Event type: `org.grimoirelab.events.git.commit.reported_by`

##### Reviewed-by
Identifies the reviewer who, after a detailed analysis, is completely satisfied 
with the patch.

- Event type: `org.grimoirelab.events.git.commit.reviewed_by`

##### Signed-off-by

Indicates that the committer certifies they have the rights to submit the work, 
typically by adding a sign-off line in the commit message.

- Event type: `org.grimoirelab.events.git.commit.signed_off_by`

##### Suggested-by

Identifies the person who suggested the idea for a patch.

- Event type: `org.grimoirelab.events.git.commit.suggested_by`

##### Tested-by

Identifies the person who applied the patch and found it to have the desired effect.

- Event type: `org.grimoirelab.events.git.commit.tested_by`
