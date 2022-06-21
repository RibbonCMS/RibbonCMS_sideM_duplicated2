import sys

from models.issue import Issue
from models.consts import Consts


consts = Consts()
issue = Issue(consts.ISSUE_PATH)

if issue.is_include(consts.EXEC_WORKFLOW_FLAG_LABELS):
    print('This includes PUBLISH FLAG')
    sys.exit(0)
else:
    print('This DO NOT includes PUBLISH FLAG')
    sys.exit(1)

