# software-tracker
[![Build Status](https://travis-ci.org/sanger-pathogens/software-tracker.svg?branch=master)](https://travis-ci.org/sanger-pathogens/software-tracker) [![codecov](https://codecov.io/gh/sanger-pathogens/software-tracker/branch/master/graph/badge.svg)](https://codecov.io/gh/sanger-pathogens/software-tracker)

## Query the database
Connect to MySQL host `pathdev-services-db` (as `pathservices_ro`), schema `pathogen_software_tracker`.
```
SELECT * FROM logging_event;
```