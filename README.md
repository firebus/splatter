Splatter
========

Splatter is an alert script for Splunk at posts search results to an SFDC user's chatter feed.

* Download from https://www.github.com/firebus/splatter.

## Installation

* Install the app into $SPLUNK_HOME/etc/apps/splatter.
* Copy bin/config.ini.sample to bin/config.ini and configure with your credentials.
* Create a symlink $SPLUNK_HOME/bin/scripts/splatter-alert.py -> $SPLUNK_HOME/etc/apps/splatter/bin/scripts/splatter-alert.py.
* Restart Splunk.

## Acknowledgements

* App maintained by Russell Uman.
* Initial POC code provided by Eric Woo.
* SFDC support provided by Tony Dyck.

## Support

Please open an issue on github if you have any trouble with the app, or contact the maintainer through github.
Please feel free to fork and make pull requests if you find a bug that you can fix or have an enhancement to add.