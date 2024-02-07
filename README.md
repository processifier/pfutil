# Event Log Uploader
NOTICE: _Use **Python 3.10** to avoid issues with dependencies._

# Install dependencies
```bash
pip install -r requirements.txt
```

# Creating data for Processifier Process Mining visual

pfutil takes eventlog input file in csv and  creates four files which are used as input for Processifier Process Mining visual (https://appsource.microsoft.com/pl-pl/product/power-bi-visuals/processifierspzoo1667474389705.processifier-process-mining-visual?tab=overview):
* case_
* eventlog
* global_stats
* variant

## Run (default configuration) 
  ```sh
  pfutil put -e 'path to eventlog csv file' 
  ```
Above execution assumes that eventlog input file satisfies the following criteria:
* contains three obligatory columns:
  * **case_id** - unique identifier of process instance
  * **activity** - name of activity
  * **end_timestamp** - timestamp of activity completion


* optionally contains two additional columns 
  * **start_timestamp** - timestamp of activity start 
  * **resource** - resource assign to specific activity execution 


* Timestamp is store in specific format: 
  * **"%Y-%m-%dT%H:%M:%S"**


NOTICE 1:  Presence start timestamp data in dataset enables additional duration statistics on activity level

NOTICE 2:  Output files are saved to default directory: **./processifier_output**


## Run (user configuration)

You can also execute pfutil with your own columns names mapping and chosen timestamp mask. Moreover there is option for specifing output folder:


  ```sh
  pfutil  -c 'path to config yaml file' put -e 'path to eventlog csv file' --csv-out 'relative path to output_test directory' 
  ```

Display help
  * `pfutil -h` prints available commands and top level options,
  * `pfutil <COMMAND> -h` shows command's help, ex: `pfutil put -h`
  
### Structure of  config.yaml

```sh
input:
  timestampMask: "%Y-%m-%dT%H:%M:%S" #timestamp mask used for start/end of activity (obligatory)
  processName: process  #process name defined by user (obligatory)
  eventlogInputColumns: #mapping of eventlog columns             
    caseId: case_id                  #required
    activity: Activity               #required
    endTimestamp: end_time           #required
    startTimestamp: start_time       #optional
    resource: Resource               #optional
```

### Example

[example_data/p2p/](example_data/p2p/) directory contains sample data
```sh
./pfutil -c example_data/p2p/config.yaml  put -e example_data/p2p/eventlog.csv --csv-out output_test
```
NOTICE:  In order to overwrite existing file in chosen directory add the following flag:
```sh
--force-overwrite
```
