# -*- coding: utf-8 -*-

from ..paths import dir_project_root

path_test_sqlite_db = dir_project_root / "prompt_ide_db.sqlite"
if 1 == 1:
    PATH_SQLITE_DB = path_test_sqlite_db
else:  # pragma: no cover
    raise NotImplementedError()
