# Event Log Uploader
NOTICE: _Use **Python 3.10** to avoid issues with dependencies._

## Install dependencies
```bash
pip install -r requirements.txt
```

## Run
NOTICE: _All command line params except `-config` can be set in config file._

* upload data 
  ```sh
  pfutil  -c 'path to congig yaml file' put -e 'path to eventlog csv file' --csv-out 'relative path to output directory' 
  ```

* display help
  * `pfutil -h` prints available commands and top level options,
  * `pfutil <COMMAND> -h` shows command's help, ex: `pfutil put -h`
  
### Example

[example_data/p2p/](example_data/p2p/) directory contains sample data
```sh
./pfutil -c example_data/p2p/config.yaml  put -e example_data/p2p/eventlog.csv --csv-out output
```
NOTICE:  In order to overwrite existing file in chosen directory add the following flag:
```sh
--force-overwrite
```

### Structure of sample config.yaml
input:
```sh
  timestampMask: "%Y-%m-%dT%H:%M:%S" (timestamp mask used for start/end of activity) 
```
```sh
  workingCalendar:                   (calendar settings for business hours calculation)
    holidayCalendar: PL              (country code, see details https://pypi.org/project/holidays/)
    workingDays: [0,1,2,3,4]         (list of working days, 0 refers to monday etc.)
    workStart: 8                     (work starting hour)
    workEnd: 16                      (work ending hour)
```
```sh
  processName: p2p                   (process name defined by user)
```
```sh
  eventlogInputColumns:              (mapping of eventlog columns)
    caseId: case_id                  (required)
    activity: Activity               (required)
    endTimestamp: end_time           (required)
    startTimestamp: start_time       (optional)
    resource: Resource               (optional)
```
