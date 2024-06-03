# -*- coding: utf-8 -*-

from prompt_ide import api


def test():
    _ = api


if __name__ == "__main__":
    from prompt_ide.tests import run_cov_test

    run_cov_test(__file__, "prompt_ide.api", preview=False)
