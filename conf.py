# See the Documenteer docs for how to customize conf.py:
# https://documenteer.lsst.io/technotes/

from documenteer.conf.technote import *  # noqa F401 F403

# Register a custom stylesheet (justified body text, see _static/custom.css).
html_static_path = ["_static"]
html_css_files = ["custom.css"]
