# Event Log Uploader
NOTICE: _Use **Python 3.10** to avoid issues with dependencies._

# Install dependencies
```bash
pip install -r requirements.txt
```

# ETL for Processifier Process Mining visual

pfutil takes eventlog input file in CSV format and creates four files which are used as input for  [Processifier Process Mining visual](https://appsource.microsoft.com/pl-pl/product/power-bi-visuals/processifierspzoo1667474389705.processifier-process-mining-visual?tab=overview):
* case_.csv
* eventlog.csv
* global_stats.csv
* variant.csv

## Run (default configuration) 
  ```sh
  pfutil put -e 'path to eventlog csv file' 
  ```
The above execution assumes that eventlog input file satisfies the following criteria:
* contains three obligatory columns:
  * ```case_id``` - unique identifier of a process instance
  * ```activity``` - the name of the activity
  * ```start_timestamp``` or * ```end_timestamp``` - the timestamp of the activity start and completion respectively 


* optionally contains one additional column 

  * ```resource``` - resource assigned to specific activity execution 


* The timestamp is stored in a specific format: 
  * ```"%Y-%m-%dT%H:%M:%S"```


NOTICE 1:  Presence of the both timestamps in the dataset enables additional duration statistics on activity level

NOTICE 2:  Output files are created in the ```./processifier_output``` directory: 


## Run (user configuration)

If your CSV file has different column names, timestamp format or you want output files to be saved in different location you can provide additional configuration as follows:


  ```sh
  pfutil  -c 'path to config yaml file' put -e 'path to eventlog csv file' --csv-out 'relative path to output_test directory' 
  ```

Display help
  * `pfutil -h` prints available commands and top-level options,
  * `pfutil <COMMAND> -h` shows the command's help, ex: `pfutil put -h`
  
### Structure of  config.yaml

```sh
input:
  timestampMask: "%Y-%m-%dT%H:%M:%S"  # timestamp mask used for start/end of the activity (required)
  processName: process                # process name defined by user (required)
  eventlogInputColumns:               # eventlog csv input file column names             
    caseId: case_id                   # case ID column name (required)
    activity: activity                # activity column name (required)
    endTimestamp: end_time            # column with time of the activity completion (required if startTimestamp is not specified, optional otherwise)
    startTimestamp: start_time        # column with time of the activity start (required if endTimestamp is not specified, optional otherwise)
    resource: resource                # resource column name (optional), default: resource
```

### Example

[example_data/p2p/](example_data/p2p/) directory contains sample data
```sh
./pfutil -c example_data/p2p/config.yaml  put -e example_data/p2p/eventlog.csv --csv-out output_test
```
NOTICE:  In order to overwrite existing files in the chosen directory use ```--force-overwrite``` flag:

