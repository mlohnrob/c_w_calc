## Om
Dette program læser datasæt, der er eksporteret fra LoggerPro som .csv filer, **sorterer** dem, **fitter** dem og **plotter** dem.
Derudover udregnes åbningsvinkel, luftmodstand og c_w faktor af keglen. Luftmodstande og c_w faktorer plottes, og der fittes en andengradsregression.

## Kør programmet
Programmet kan både køres af **windows** som en .exe fil og af **python** som en .py fil.
Dog kører det meget **langsomt** som .exe fil, da det er kompileret fra python.

### Med Windows .exe
#### Uden plot:
`
.\c_w_calc.exe stig\til\csv-fil-mappe
`
#### Med plot:
`
.\c_w_calc.exe stig\til\csv-fil-mappe plot
`

### Med Python .py
#### Uden plot:
`
python c_w_calc.py stig/til/csv-fil-mappe
`

#### Med plot:
`
python c_w_calc.py stig/til/csv-fil-mappe plot
`

**Hvis du har klonet dette repo, ville kommandoen f.eks. være:**
`
.\c_w_calc.exe csv_files_30\ plot
`
**eller**
`
python c_w_calc.py csv_files_30/ plot
`

### Eksempel på både input og output af programmet

```
$ python c_w_calc.py csv_files_120/ plot

Radius of original circle in cm: 9.7

Angle of cutout: 120

120gr1.csv
Weight in grams: 1.63

120gr2.csv
Weight in grams: 1.94

120gr3.csv
Weight in grams: 2.24

120gr4.csv
Weight in grams: 2.57

120gr5.csv
Weight in grams: 2.9

120gr6.csv
Weight in grams: 3.21


====================================================================================================

angle = 83.6206297915572
c_w = 0.8040755171612669
```
