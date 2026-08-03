# Manual Regex find and replace

REPLACE ANY OF THESE:

```text
"","Male","","","Female","","","Total",""
"(.*)","Count","Col %","Row %","Count","Col %","Row %","Total","Col %"

"","Male","","","Female","","","Total",""
"(.*)","Count","Col %","","Row %  Count","Col %","Row %","Total","Col %"

"","Male","","","Female","","","Total",""
"(.*)","Count","Col%","Row%","Count","Col%","Row%","Total","Col%"
```

WITH THIS:

```text
"$1","M Count","M Col %","M Row %","F Count","F Col %","F Row %","Total","Col %"
```

REPLACE THIS:

`"Not Reported","(\d+)","(\d+)","(\d+)"`

WITH THIS:

`"Not Reported","$1","","","$2","","","$3",""\n`

REPLACE THIS:

`"Grand Total","([\d,]+)","([\d,]+)","([\d,]+)"\n`

WITH THIS:

`"Grand Total","$1","","","$2","","","$3",""\n`

DELETE REPREATED HEADERS

`\n".*","M Count","M Col %","M Row %","F Count","F Col %","F Row %","Total","Col %"`

DELETE INDEX NUMBER PREFIXES TO COUNTIES AND CATEGORIES

REPLACE `\n"\d+\s+([A-Z])` WITH `\n"$1`

REPLACE `Mean\s+\(average\)` WITH `Mean`
REPLACE `Median\s+\(middle\)` WITH `Median`
REPLACE `Mode\s+\(most frequent\)` WITH `Mode`
