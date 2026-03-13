## employee/employee_timesheet_merged.py 
1. Capable to set employee timesheet format on Employee Information from HR module.
2. Capable to download employee timesheet on Employee module.
3. Capable to Approve then reject timesheet from HR module.
4. Capable to automate timesheet process. However, approval still manual by DS (approve asap).

```bash
pytest employee_timesheet_merged.py --env=dev --headed
```

## unstable_feature.py
1. Need re-run to check after dev get update from staging.

# New Feature
This script can generate all personal information of user. Can be use on dev or staging.
pytest set_personal_info.py --env= --username=.com --password= --name= --headed