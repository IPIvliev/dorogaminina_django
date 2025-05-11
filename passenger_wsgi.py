import sys, os
INTERP = os.path.expanduser("~/domains/xn--80aahdwa0ajbdax.xn--p1ai/venv311/bin/python3")

if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dorogaminina_django'))

from dorogaminina_django.wsgi import application