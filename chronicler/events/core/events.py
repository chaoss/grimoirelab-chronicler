#
# Copyright (C) GrimoireLab Developers
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from dataclasses import dataclass, field
from typing import Any

from cloudevents.http import CloudEvent

from ...eventizer import GrimoireLabEvent


@dataclass(kw_only=True)
class Commit(GrimoireLabEvent):
    """A commit on a VCS repository"""

    TYPE = "org.grimoirelab.events.commit"

    author: str = field(metadata={"description": "Author of the commit"})
    author_date: str = field(
        metadata={"description": "Date when the author originally made the commit"},
    )
    committer: str = field(metadata={"description": "Committer of the changes"})
    commit_date: str = field(metadata={"description": "Date when the commit was last modified"})
    commit: str = field(metadata={"description": "Commit hash"})
    files: list[dict[str, Any]] = field(metadata={"description": "Changed files"})
    message: str = field(metadata={"description": "Commit message"})
    parents: list[str] = field(metadata={"description": "Hashes of the parents of the commit"})
    refs: list[str] = field(metadata={"description": "Commit references"})
    extra: dict[str, Any] = field(
        default_factory=dict,
        metadata={"description": "Other fields of the commit, such as the trailers"},
    )

    def to_cloudevent(self) -> CloudEvent:
        # The extra fields are part of the data, not a field on their own
        event = super().to_cloudevent()
        event.data.update(event.data.pop("extra"))
        return event


@dataclass(kw_only=True)
class MergeCommit(Commit):
    """A merge commit on a VCS repository"""

    TYPE = "org.grimoirelab.events.commit.merge"

    merge: str = field(metadata={"description": "The tips of the merged branches"})


@dataclass(kw_only=True)
class CommitFileAction(GrimoireLabEvent):
    """Base class for the actions performed on a file by a commit"""

    commit: str = field(metadata={"description": "Commit hash"})
    filename: str = field(metadata={"description": "Name of the file"})
    modes: list[str] = field(metadata={"description": "File modes"})
    indexes: list[str] = field(metadata={"description": "Repository indexes"})
    similarity: str | None = field(
        default=None,
        metadata={"description": "Percentage of unchanged lines in copied or replaced files"},
    )
    new_filename: str | None = field(default=None, metadata={"description": "Name of the new file"})
    added_lines: str | None = field(
        default=None, metadata={"description": "Number of added lines in the commit"}
    )
    deleted_lines: str | None = field(
        default=None, metadata={"description": "Number of deleted lines in the commit"}
    )


class CommitFileAdded(CommitFileAction):
    TYPE = "org.grimoirelab.events.commit.file.added"


class CommitFileModified(CommitFileAction):
    TYPE = "org.grimoirelab.events.commit.file.modified"


class CommitFileDeleted(CommitFileAction):
    TYPE = "org.grimoirelab.events.commit.file.deleted"


class CommitFileReplaced(CommitFileAction):
    TYPE = "org.grimoirelab.events.commit.file.replaced"


class CommitFileCopied(CommitFileAction):
    TYPE = "org.grimoirelab.events.commit.file.copied"


class CommitFileTypeChanged(CommitFileAction):
    TYPE = "org.grimoirelab.events.commit.file.typechanged"


@dataclass(kw_only=True)
class CommitIdentity(GrimoireLabEvent):
    """Base class for the identities that took part in a commit"""

    commit: str = field(metadata={"description": "Hash of the commit"})
    name: str | None = field(metadata={"description": "Name of the identity"})
    username: str | None = field(metadata={"description": "Username of the identity"})
    email: str | None = field(metadata={"description": "Email of the identity"})
    uuid: str = field(metadata={"description": "Unique identifier of the identity"})
    role: str = field(init=False, metadata={"description": "Role of the identity in the commit"})

    def __post_init__(self):
        self.role = self.TYPE.rsplit(".", 1)[-1]


class CommitAuthoredBy(CommitIdentity):
    TYPE = "org.grimoirelab.events.commit.authored_by"


class CommitCommittedBy(CommitIdentity):
    TYPE = "org.grimoirelab.events.commit.committed_by"


class CommitAckedBy(CommitIdentity):
    TYPE = "org.grimoirelab.events.commit.acked_by"


class CommitCoAuthoredBy(CommitIdentity):
    TYPE = "org.grimoirelab.events.commit.co_authored_by"


class CommitHelpedBy(CommitIdentity):
    TYPE = "org.grimoirelab.events.commit.helped_by"


class CommitMentoredBy(CommitIdentity):
    TYPE = "org.grimoirelab.events.commit.mentored_by"


class CommitReportedBy(CommitIdentity):
    TYPE = "org.grimoirelab.events.commit.reported_by"


class CommitReviewedBy(CommitIdentity):
    TYPE = "org.grimoirelab.events.commit.reviewed_by"


class CommitSignedOffBy(CommitIdentity):
    TYPE = "org.grimoirelab.events.commit.signed_off_by"


class CommitSuggestedBy(CommitIdentity):
    TYPE = "org.grimoirelab.events.commit.suggested_by"


class CommitTestedBy(CommitIdentity):
    TYPE = "org.grimoirelab.events.commit.tested_by"
