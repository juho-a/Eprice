### Scipts for populating the database

The historical data stays constant but as new datapoints arrive they are being fetched daily. If for some reason, the service has been down for a long time it might be best to run data-preparation service -- it get's the new historical data and inserts it into the database in bulk. This way the backen server is not needlessly burdened with dataloading on launch.

The service can be run using profile `data-preparation` (depends on database and migrations).