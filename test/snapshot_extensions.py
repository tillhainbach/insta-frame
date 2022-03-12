"""Extension types for snapshotting."""

from syrupy.extensions.single_file import SingleFileSnapshotExtension


class JPEGImageSnapshotExtension(SingleFileSnapshotExtension):
    @property
    def _file_extension(self) -> str:
        return "jpeg"


class HTMLImageSnapshotExtension(SingleFileSnapshotExtension):
    @property
    def _file_extension(self) -> str:
        return "html"
