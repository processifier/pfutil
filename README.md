# Event Log Uploader
NOTICE: _Use **Python 3.10** to avoid issues with dependencies._

# Install dependencies
```bash
pip install -r requirements.txt
```

# Creating data for Processifier Process Mining visual

pfutil takes eventlog input file in CSV and  creates four files which are used as input for Processifier Process Mining visual [Processifier Process Mining visual](https://appsource.microsoft.com/pl-pl/product/power-bi-visuals/processifierspzoo1667474389705.processifier-process-mining-visual?tab=overview):
* case_
* eventlog
* global_stats
* variant

## Run (default configuration) 
  ```sh
  pfutil put -e 'path to eventlog csv file' 
  ```
The above execution assumes that eventlog input file satisfies the following criteria:
* contains three obligatory columns:
  * **case_id** - unique identifier of a process instance
  * **activity** - the name of the activity
  * **start_timestamp** or * **end_timestamp** - the timestamp of the activity start and completion respectively 


* optionally contains one additional column 

  * **resource** - resource assigned to specific activity execution 


* The timestamp is stored in a specific format: 
  * **"%Y-%m-%dT%H:%M:%S"**


NOTICE 1:  Presence of the both timestamps in the dataset enables additional duration statistics on activity level

NOTICE 2:  Output files are saved to the default directory: **./processifier_output**


## Run (user configuration)

You can also execute pfutil with your own column name mapping and chosen timestamp mask. Moreover, there is an option for specifying the output folder:


  ```sh
  pfutil  -c 'path to config yaml file' put -e 'path to eventlog csv file' --csv-out 'relative path to output_test directory' 
  ```

Display help
  * `pfutil -h` prints available commands and top-level options,
  * `pfutil <COMMAND> -h` shows the command's help, ex: `pfutil put -h`
  
### Structure of  config.yaml

```sh
input:
  timestampMask: "%Y-%m-%dT%H:%M:%S"  #timestamp mask used for start/end of the activity (required)
  processName: process                #process name defined by user (required)
  eventlogInputColumns:               #mapping of eventlog columns             
    caseId: case_id                   #required
    activity: activity                #required
    endTimestamp: end_time            #required/optional
    startTimestamp: start_time        #required/optional
    resource: resource                #optional
```

### Example

[example_data/p2p/](example_data/p2p/) directory contains sample data
```sh
./pfutil -c example_data/p2p/config.yaml  put -e example_data/p2p/eventlog.csv --csv-out output_test
```
NOTICE:  In order to overwrite existing files in the chosen directory add the following flag:
```sh
--force-overwrite
```
