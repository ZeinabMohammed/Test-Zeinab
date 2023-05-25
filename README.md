## Test Zeinab

Calculate Average Power Consumption

#### License

MIT

### Usage
* Used as a custom module into ERPNext ERP system to calculate power consumptions per clients.

### Installation
+ Move to your [bench](https://github.com/frappe/bench) instance directory and do:
`bench get-app https://github.com/ZeinabMohammed/Test-Zeinab.git`
+ then run `bench install-app test_zeinab`
+ `bench setup requirements --python`
+ `bench migrate`
+ `bench build --app test_zeinab`
+ `bench restart` if you are running on production server or restart manually if you are on DEV one.
### Notes
* Developed  & tested on base `version-14` branch for both frappe & ERPNext App.
* Developed to be used by ERPNext desk.


### Further enhancements
* Make customer and project records linked to their associated doctpes in ERPNext app.
* Add more validations.
* Make fields filled with the extracted data from the file readonly.


### Functional Docs
## Customization:
+ Added 3 doctypes:
  + Power Consumption.
  + Power Consumption Details.
  + Periodic Power Consumption Details.
+ Added 1 Workspace: Power Consumption Worksapce.
 

## Cycle:
- After installing app open your desk from the browser and move to 'Power Consumption Worksapce'.
- Open 'Power Consumption' and click 'New'.
- You can find a button "Upload Entries" and you will  get a prompt to upload a file.
  - File should be an Excel sheet.
  - File template should follow the [provided file](Records%202%20%281%29.xlsx) template.
  - Make sure that all records data are valid:
    - datetime field values should be datetime type.
    - kw, kwh must be numeric or '-'.
- After selecting the file click 'Upload' then your file data will be extracted to its associated fields.
- save and then you can submit.

### Technical
#TODO