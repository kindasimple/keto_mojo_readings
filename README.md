keto
=========

Explore nutritional content of foods. Assist glucose/ketone meter monitoring

## Introduction

The only thing useful in this repo is a script that can be used to convert a Keto Mojo glucose/ketone/hematocrit/hemoglobin export to a series of readings based on temporal proximity.

## Quickstart

On the KetoMojo iphone app, retrieve a readings csv file.

1. upload the file from your phone to some cloud service provider
2. download the file onto your compter
3. run `make`

The local project directory will now include a third file with readings

```
├── KetoMojo.csv            # KetoMojo export
├── keto_mojo_readings.csv  # script output
├── process_ketomojo.py     # processing script
```

The resulting `keto_mojo_readings` CSV file is the input for a google sheets document: https://docs.google.com/spreadsheets/d/1bKP0rKxLVvfmrYzn4RfKXkJsmHoRDLVjqHeCii7iQGs/edit?usp=sharing 

Use google sheets to monitor your GKI.

## Nutrition information

[Canadian Nutrient File](https://www.canada.ca/en/health-canada/services/food-nutrition/healthy-eating/nutrient-data/canadian-nutrient-file-2015-download-files.html)

# Future work

+ [ ] Download KetoMojo.csv from google drive from script
+ [ ] Add annotations to indicate events like meals or exercise