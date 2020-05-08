# Google Cloud Resource Cleaner  
A tool to scan and cleanup resources your Google Cloud projects and keep your bill under control !

## Summary
Scan for resources with simple rules and optionally delete them (and all their dependencies as well)

**Your rules can be as simple as:**

 - Everything I created before 10th of March 2020.
 - Everything John created.
 - Everything which is there on the cloud for more than 10 days.
 - Everything with a LABEL which says 'temp'.
 - Everything with a name like 'Bob'

**You can combine multiple rules as well to be more specific:**

 - All compute instances running for more than 7 days.
 - All SQL instances created after 10th March 2020 and with LABEL 'test'.
 - Everything that Bob created till today.

# How to Run ?
## Setup

    pip3 install -r requirements.txt

## Quickstart
Let's get you a quick start before we dive deep. Try out a sample rule that scans for all Compute Instances older than 24 hours.

    python3 main.py --scan --rules quickstart_rule_01 --project_id YOUR_GCP_PROJECT_ID