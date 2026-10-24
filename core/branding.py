"""EDITH's on-disk product naming and conservative upload-folder migration.

Never overwrite an existing user file. Legacy names occur only as migration
inputs; all paths newly created by EDITH use the EDITH product name.
"""
from __future__ import annotations

from pathlib import Path

UPLOAD_FOLDER_NAME = "EDITH Uploads"
_LEGACY_UPLOAD_FOLDER_NAME = "JARVIS Uploads"


def _collision_free_path(target: Path) -> Path:
    """Find an unused destination; never overwrite a pre-existing upload."""
    if not target.exists():
        return target
    for number in range(1, 10001):
        candidate = target.with_name(f"{target.stem}_migrated_{number}{target.suffix}")
        if not candidate.exists():
            return candidate
    raise OSError(f"No safe free name for {target.name}")


def migrate_legacy_uploads(parent: Path) -> Path:
    """Migrate our former upload directory safely, preserving all contents.

    A same-volume folder rename is preferred. If EDITH Uploads already exists,
    move individual entries with collision-free names. On any filesystem error
    retain the legacy directory and its remaining files for manual recovery.
    """
    target = parent / UPLOAD_FOLDER_NAME
    legacy = parent / _LEGACY_UPLOAD_FOLDER_NAME
    if legacy.is_dir() and not legacy.is_symlink():
        if not target.exists() and not any(p.is_symlink() for p in legacy.iterdir()):
            legacy.rename(target)
        else:
            target.mkdir(parents=True, exist_ok=True)
            if target.is_symlink() or not target.is_dir():
                raise OSError("EDITH uploads target is not a regular directory")
            for entry in legacy.iterdir():
                if entry.is_symlink():
                    continue  # Never follow or move links to unknown user data
                entry.rename(_collision_free_path(target / entry.name))
            try:
                legacy.rmdir()  # Succeeds only if migration is complete
            except OSError:
                pass
    target.mkdir(parents=True, exist_ok=True)
    return target


def prepare_uploads_dir(home: Path | None = None, base_dir: Path | None = None) -> Path:
    """Make EDITH's upload directory only when the dashboard is started."""
    home = home or Path.home()
    base_dir = base_dir or Path(__file__).resolve().parent.parent
    for parent in (home / "Downloads", home / "Documents"):
        if not parent.is_dir():
            continue
        try:
            return migrate_legacy_uploads(parent)
        except OSError as exc:
            print(f"[EDITH] Upload directory unavailable at {parent}: {type(exc).__name__}")
    fallback = base_dir / "uploads"  # Existing neutral fallback remains compatible
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback
