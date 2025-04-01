# Events

## Overview

Each event is structured into two parts:

- Attributes: metadata providing contextual information about the event and present in 
all types of events. The attributes are based on the CloudEvents specification.
- Data: other information specific to the event.


### Attributes

| Field | Type | Description |
|-------|------|-------------|
| id    | `String`| Event identifier |
| source | `URI-reference` | URL to the repository |
| specversion | `String` | The version of the CloudEvents specification used |
| time  | `Timestamp` | Timestamp of when the event happened |
| type  | `String` | Defines the event type. It is prefixed by `org.grimoirelab` |


## Events

### Git

Git events are related to commits in git repositories.

#### Commit

- Event type: `org.grimoirelab.events.git.commit`

| Field | Type | Description |
|-------|------|-------------|
| Author | `String` | Author of the commit |
| AuthorDate | `String` | Date when the author originally made the commit |
| Commit | `String` | Commiter of the changes |
| CommitDate | `String` | Date when the commit was last modified |
| commit | `String` | Commit hash |
| files | `List` ([file](#file-objects)) | Information about the changed files |
| message | `String` | Commit message |
| parents | `List (string)` | Hashes of logical predecessors in the line of development. See [parent](https://git-scm.com/docs/gitglossary#Documentation/gitglossary.txt-aiddefparentaparent) in Git documentation |
| refs | `List (string)` | Git references. See [ref](https://git-scm.com/docs/gitglossary#Documentation/gitglossary.txt-aiddefrefaref) in Git documentation |
| Signed-off-by | `String` | A trailer at the end of the commit message to certify that the committer has the rights to submit the work. See [--signoff](https://git-scm.com/docs/git-commit#Documentation/git-commit.txt-code--no-signoffcode) in Git documentation


#### Merge commit

- Event type: `org.grimoirelab.events.git.merge`

| Field | Type | Description |
|-------|------|-------------|
| Author | `String` | Author of the commit |
| AuthorDate | `String` | Date when the author originally made the commit |
| Commit | `String` | Commiter of the changes |
| CommitDate | `String` | Date when the commit was last modified |
| commit | `String` | Commit hash |
| files | `List` ([file](#file-objects)) | List of files changed |
| Merge | `String` | The tips of the merged branches |
| message | `String` | Commit message |
| parents | `List (string)` | Hashes of logical predecessors in the line of development. See [parent](https://git-scm.com/docs/gitglossary#Documentation/gitglossary.txt-aiddefparentaparent) in Git documentation |
| refs | `List (string)` | Git references. See [ref](https://git-scm.com/docs/gitglossary#Documentation/gitglossary.txt-aiddefrefaref) in Git documentation |

#### Commit file actions

| Field | Type | Description |
|-------|------|-------------|
| filename | `String` | Name of the file |
| modes | `List (String)` | Git file modes |
| indexes | `List (String)` | Git indexes |
| similarity | `String` | Percentage of unchanged lines in copied or replaced files. |
| new_filename | `String` | Name of the new file |
| added_lines | `String` | Number of added lines in the commit |
| deleted_lines | `String` | Number of deleted lines in the commit |

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


| Field | Type | Description |
|-------|------|-------------|
| action | `String` | Identifier of the action performed |
| added | `String` | Number of added lines in the file  |
| file  | `String` | File name |
| indexes | `List (String)` | Git indexes |
| modes | `List (String)` | Git file modes |
| removed | `String` | Number of deleted lines in the file |
