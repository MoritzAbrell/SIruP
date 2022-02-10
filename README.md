# SIruP - A SIP Honeypot

![SIruP Logo](/doc/sirup-logo.png)

SIruP is a SIP/VoIP honeypot developed in python.

To run SIruP, you only need to modify the config.ini file according to your needs.
Then the honeypot can be started as follows:

```
python3 sirup.py
```

The honeypot will store all data in a SQLite database.
This database can then be used for further analysis.

Besides the honeypot itself, the repository also provides an automated reporting tool that creates a nice HTML and CSV report:

```
python3 report.py -d <database> -o <outfile> --full
```

With the "--full" argument, the IP addresses are resolved by country. 
Due to the external API queries required for this, this process takes a while depending on the size of the database and the amount of IPs.


... TBC ...
