#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =============================================================================
# IMPORTS
# =============================================================================

from django.db import transaction


# =============================================================================
# FUNCTION
# =============================================================================

def commit_after(gen, fnc, ni=100, **kwargs):
    transaction.set_autocommit(False)
    try:
        cnt = 0
        for item in gen:
            cnt += 1
            fnc(item, **kwargs)
            if cnt >= ni:
                transaction.commit()
                cnt = 0
        else:
            if cnt != 0:
                transaction.commit()
    except:
        transaction.rollback()
        raise
    finally:
        transaction.set_autocommit(True)

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print(__doc__)
