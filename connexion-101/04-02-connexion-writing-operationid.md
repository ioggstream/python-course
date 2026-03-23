# A new path: /echo

Now we're going to write a new path: `/echo`.

Our goal is the following:

- when invoking `/datetime/v1/echo` the API will return
  the current datetime;
- the response is enveloped in the following example json object:

```
{ "timestamp": "2019-12-25T00:00:00Z" }
```

- the status code for a successful response is `200`

### Exercise: write /echo specs

Edit the [ex-04-02-echo-ok.yaml](/edit/notebooks/oas3/ex-04-02-echo.yaml) and write the `echo` specifications:

1- define the new `Datetime` schema to be used in the response;

2- define the new `/echo` path supporting the `get` method and:

  * always write proper `summary` and `description` fields

3- `get /echo` possible responses are:

  * `200` returning a `Datetime` in json format, with a complete `example` for mocks
  * `503` returning a `problem+json`


4- don't forget `operationId` !

Hint: feel free to reuse as much yaml code as possible.

### Exercise: test /echo mocks

Run your spec [in the terminal](/terminals/1) and check that it properly returns the mock objects.

Use

```
connexion run --mock all /code/notebooks/oas3/ex-04-02-echo-ok.yaml
```


```python
# Use this cell to test the output
!curl http://localhost:5000/datetime/v1/echo -vk
```

    *   Trying 127.0.0.1...
    * TCP_NODELAY set
    * Connected to localhost (127.0.0.1) port 5000 (#0)
    > GET /datetime/v1/echo HTTP/1.1
    > Host: localhost:5000
    > User-Agent: curl/7.52.1
    > Accept: */*
    >
    * HTTP 1.0, assume close after body
    < HTTP/1.0 404 NOT FOUND
    < Content-Type: application/problem+json
    < Content-Length: 205
    < Server: Werkzeug/0.15.4 Python/3.6.6
    < Date: Fri, 05 Jul 2019 08:41:28 GMT
    <
    {
      "detail": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.",
      "status": 404,
      "title": "Not Found",
      "type": "about:blank"
    }
    * Curl_http_done: called premature == 0
    * Closing connection 0


## Request parameters

OAS3 allows to specify parameters both in `path`, `query` and  `headers`.

Interoperable APIs should follow simple rules when using parameters:

- define parameter conventions for common patterns, eg: limit, offset;
- use standard HTTP headers when possible.

As many APIs implement pagination, it's a good think to converge to a common
set of parameters to use. Our choice is:

- limit: max number of entries to retrieve
- offset: the number of entries to skip in a paginated request
- cursor: an identifier (cursor) of the first entry to be returned
  [Slack APIs provide an example of cursor-based pagination](https://api.slack.com/docs/pagination)

## Adding request parameters to `/echo`

`Query` and `header` request parameters can be defined in

```
components:
  parameters:
    a_sample_parameter:
      ...
```


```python
# Here's the `limit` parameter definition, including
# - it's a `query` parameter
# - its name
# - its schema
print(show_component('https://teamdigitale.github.io/openapi/0.0.5/definitions.yaml#/parameters/limit'))
```

    description: How many items to return at one time (max 100)
    in: query
    name: limit
    schema:
      format: int32
      type: integer



### Exercise: adding parameters to `/echo`

Let's add a `tz` parameter to `/echo`:

- create a `#/components/schemas/Timezone` schema definition. Valid example values are:

  * 'Europe/Rome'
  * 'UTC' (default)
  * 'Asia/Calcutta'

- create a `#/components/parameters/tz` parameter definition;
- add the `tz` query parameter to `get /echo` path checking
  the [official OAS 3.0.2 documentation](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#examples)
- add a `400 Bad Request` response in case the timezone is not in the list

Finally, check that you can run the spec.

```
connexion run --mock all /code/notebooks/oas3/ex-04-02-echo-ok.yaml
```


```python
# Use this cell to test your api
```

### Implement get_echo

Let's implement the `get_echo` in [api.py](/edit/notebooks/oas3/api.py) function that:

- takes the `tz` parameter, which defaults to `UTC`;
- returns a `Datetime` object in its current timezone.


```python
# hint: get the timezone from
!pip install pytz
```

    Requirement already satisfied: pytz in /usr/local/lib/python3.6/site-packages (2019.1)



```python
import pytz
tz = pytz.timezone('Europe/Rome')
print(tz.zone)
```

    Europe/Rome



```python
# No timezones in Neverland :)
'Neverland' in pytz.all_timezones
```


```python
### Exercise solution
```


```python
def get_echo(tz='UTC'):
    if tz not in pytz.all_timezones:
        return problem(
            status=400,
            title="Bad Timezone",
            detail="The specified timezone is not valid",
            ext={"valid_timezones": pytz.all_timezones}
        )
    d = datetime.now(tz=pytz.timezone(tz))
    return {"timestamp": d.isoformat().replace('+00:00', 'Z')}

```

Now  [run the spec in a terminal](/terminals/1) using

```
cd /code/notebooks/oas3/
connexion run /code/notebooks/oas3/ex-04-02-echo-ok.yaml
```


```python
render_markdown(f'''
play a bit with the [Swagger UI]({api_server_url('ui')})

and try making a request!
''')
```


```python
## TODO do we have enough time to show flask_testing?

# Check that default works
!curl http://localhost:5000/datetime/v1/echo -kv
```

    *   Trying 127.0.0.1...
    * TCP_NODELAY set
    * Connected to localhost (127.0.0.1) port 5000 (#0)
    > GET /datetime/v1/echo HTTP/1.1
    > Host: localhost:5000
    > User-Agent: curl/7.52.1
    > Accept: */*
    >
    * HTTP 1.0, assume close after body
    < HTTP/1.0 200 OK
    < Content-Type: application/problem+json
    < Content-Length: 49
    < Server: Werkzeug/0.15.4 Python/3.6.6
    < Date: Fri, 05 Jul 2019 09:56:00 GMT
    <
    {
      "timestamp": "2019-07-05T09:56:00.357602Z"
    }
    * Curl_http_done: called premature == 0
    * Closing connection 0



```python
# Test a valid timezone
!curl http://localhost:5000/datetime/v1/echo?tz=Europe/Rome -kv
```

    *   Trying 127.0.0.1...
    * TCP_NODELAY set
    * Connected to localhost (127.0.0.1) port 5000 (#0)
    > GET /datetime/v1/echo?tz=Europe/Rome HTTP/1.1
    > Host: localhost:5000
    > User-Agent: curl/7.52.1
    > Accept: */*
    >
    * HTTP 1.0, assume close after body
    < HTTP/1.0 200 OK
    < Content-Type: application/problem+json
    < Content-Length: 54
    < Server: Werkzeug/0.15.4 Python/3.6.6
    < Date: Fri, 05 Jul 2019 09:55:53 GMT
    <
    {
      "timestamp": "2019-07-05T11:55:53.986946+02:00"
    }
    * Curl_http_done: called premature == 0
    * Closing connection 0



```python
# Test an invalid timezone
!curl http://localhost:5000/datetime/v1/echo?tz=Frittole -kv
```

    *   Trying 127.0.0.1...
    * TCP_NODELAY set
    * Connected to localhost (127.0.0.1) port 5000 (#0)
    > GET /datetime/v1/echo?tz=Frittole HTTP/1.1
    > Host: localhost:5000
    > User-Agent: curl/7.52.1
    > Accept: */*
    >
    * HTTP 1.0, assume close after body
    < HTTP/1.0 400 BAD REQUEST
    < Content-Type: application/problem+json
    < Content-Length: 13308
    < Server: Werkzeug/0.15.4 Python/3.6.6
    < Date: Fri, 05 Jul 2019 09:56:03 GMT
    <
    {
      "detail": "The specified timezone is not valid",
      "status": 400,
      "title": "Bad Timezone",
      "type": "about:blank",
      "valid_timezones": [
        "Africa/Abidjan",
        "Africa/Accra",
        "Africa/Addis_Ababa",
        "Africa/Algiers",
        "Africa/Asmara",
        "Africa/Asmera",
        "Africa/Bamako",
        "Africa/Bangui",
        "Africa/Banjul",
        "Africa/Bissau",
        "Africa/Blantyre",
        "Africa/Brazzaville",
        "Africa/Bujumbura",
        "Africa/Cairo",
        "Africa/Casablanca",
        "Africa/Ceuta",
        "Africa/Conakry",
        "Africa/Dakar",
        "Africa/Dar_es_Salaam",
        "Africa/Djibouti",
        "Africa/Douala",
        "Africa/El_Aaiun",
        "Africa/Freetown",
        "Africa/Gaborone",
        "Africa/Harare",
        "Africa/Johannesburg",
        "Africa/Juba",
        "Africa/Kampala",
        "Africa/Khartoum",
        "Africa/Kigali",
        "Africa/Kinshasa",
        "Africa/Lagos",
        "Africa/Libreville",
        "Africa/Lome",
        "Africa/Luanda",
        "Africa/Lubumbashi",
        "Africa/Lusaka",
        "Africa/Malabo",
        "Africa/Maputo",
        "Africa/Maseru",
        "Africa/Mbabane",
        "Africa/Mogadishu",
        "Africa/Monrovia",
        "Africa/Nairobi",
        "Africa/Ndjamena",
        "Africa/Niamey",
        "Africa/Nouakchott",
        "Africa/Ouagadougou",
        "Africa/Porto-Novo",
        "Africa/Sao_Tome",
        "Africa/Timbuktu",
        "Africa/Tripoli",
        "Africa/Tunis",
        "Africa/Windhoek",
        "America/Adak",
        "America/Anchorage",
        "America/Anguilla",
        "America/Antigua",
        "America/Araguaina",
        "America/Argentina/Buenos_Aires",
        "America/Argentina/Catamarca",
        "America/Argentina/ComodRivadavia",
        "America/Argentina/Cordoba",
        "America/Argentina/Jujuy",
        "America/Argentina/La_Rioja",
        "America/Argentina/Mendoza",
        "America/Argentina/Rio_Gallegos",
        "America/Argentina/Salta",
        "America/Argentina/San_Juan",
        "America/Argentina/San_Luis",
        "America/Argentina/Tucuman",
        "America/Argentina/Ushuaia",
        "America/Aruba",
        "America/Asuncion",
        "America/Atikokan",
        "America/Atka",
        "America/Bahia",
        "America/Bahia_Banderas",
        "America/Barbados",
        "America/Belem",
        "America/Belize",
        "America/Blanc-Sablon",
        "America/Boa_Vista",
        "America/Bogota",
        "America/Boise",
        "America/Buenos_Aires",
        "America/Cambridge_Bay",
        "America/Campo_Grande",
        "America/Cancun",
        "America/Caracas",
        "America/Catamarca",
        "America/Cayenne",
        "America/Cayman",
        "America/Chicago",
        "America/Chihuahua",
        "America/Coral_Harbour",
        "America/Cordoba",
        "America/Costa_Rica",
        "America/Creston",
        "America/Cuiaba",
        "America/Curacao",
        "America/Danmarkshavn",
        "America/Dawson",
        "America/Dawson_Creek",
        "America/Denver",
        "America/Detroit",
        "America/Dominica",
        "America/Edmonton",
        "America/Eirunepe",
        "America/El_Salvador",
        "America/Ensenada",
        "America/Fort_Nelson",
        "America/Fort_Wayne",
        "America/Fortaleza",
        "America/Glace_Bay",
        "America/Godthab",
        "America/Goose_Bay",
        "America/Grand_Turk",
        "America/Grenada",
        "America/Guadeloupe",
        "America/Guatemala",
        "America/Guayaquil",
        "America/Guyana",
        "America/Halifax",
        "America/Havana",
        "America/Hermosillo",
        "America/Indiana/Indianapolis",
        "America/Indiana/Knox",
        "America/Indiana/Marengo",
        "America/Indiana/Petersburg",
        "America/Indiana/Tell_City",
        "America/Indiana/Vevay",
        "America/Indiana/Vincennes",
        "America/Indiana/Winamac",
        "America/Indianapolis",
        "America/Inuvik",
        "America/Iqaluit",
        "America/Jamaica",
        "America/Jujuy",
        "America/Juneau",
        "America/Kentucky/Louisville",
        "America/Kentucky/Monticello",
        "America/Knox_IN",
        "America/Kralendijk",
        "America/La_Paz",
        "America/Lima",
        "America/Los_Angeles",
        "America/Louisville",
        "America/Lower_Princes",
        "America/Maceio",
        "America/Managua",
        "America/Manaus",
        "America/Marigot",
        "America/Martinique",
        "America/Matamoros",
        "America/Mazatlan",
        "America/Mendoza",
        "America/Menominee",
        "America/Merida",
        "America/Metlakatla",
        "America/Mexico_City",
        "America/Miquelon",
        "America/Moncton",
        "America/Monterrey",
        "America/Montevideo",
        "America/Montreal",
        "America/Montserrat",
        "America/Nassau",
        "America/New_York",
        "America/Nipigon",
        "America/Nome",
        "America/Noronha",
        "America/North_Dakota/Beulah",
        "America/North_Dakota/Center",
        "America/North_Dakota/New_Salem",
        "America/Ojinaga",
        "America/Panama",
        "America/Pangnirtung",
        "America/Paramaribo",
        "America/Phoenix",
        "America/Port-au-Prince",
        "America/Port_of_Spain",
        "America/Porto_Acre",
        "America/Porto_Velho",
        "America/Puerto_Rico",
        "America/Punta_Arenas",
        "America/Rainy_River",
        "America/Rankin_Inlet",
        "America/Recife",
        "America/Regina",
        "America/Resolute",
        "America/Rio_Branco",
        "America/Rosario",
        "America/Santa_Isabel",
        "America/Santarem",
        "America/Santiago",
        "America/Santo_Domingo",
        "America/Sao_Paulo",
        "America/Scoresbysund",
        "America/Shiprock",
        "America/Sitka",
        "America/St_Barthelemy",
        "America/St_Johns",
        "America/St_Kitts",
        "America/St_Lucia",
        "America/St_Thomas",
        "America/St_Vincent",
        "America/Swift_Current",
        "America/Tegucigalpa",
        "America/Thule",
        "America/Thunder_Bay",
        "America/Tijuana",
        "America/Toronto",
        "America/Tortola",
        "America/Vancouver",
        "America/Virgin",
        "America/Whitehorse",
        "America/Winnipeg",
        "America/Yakutat",
        "America/Yellowknife",
        "Antarctica/Casey",
        "Antarctica/Davis",
        "Antarctica/DumontDUrville",
        "Antarctica/Macquarie",
        "Antarctica/Mawson",
        "Antarctica/McMurdo",
        "Antarctica/Palmer",
        "Antarctica/Rothera",
        "Antarctica/South_Pole",
        "Antarctica/Syowa",
        "Antarctica/Troll",
        "Antarctica/Vostok",
        "Arctic/Longyearbyen",
        "Asia/Aden",
        "Asia/Almaty",
        "Asia/Amman",
        "Asia/Anadyr",
        "Asia/Aqtau",
        "Asia/Aqtobe",
        "Asia/Ashgabat",
        "Asia/Ashkhabad",
        "Asia/Atyrau",
        "Asia/Baghdad",
        "Asia/Bahrain",
        "Asia/Baku",
        "Asia/Bangkok",
        "Asia/Barnaul",
        "Asia/Beirut",
        "Asia/Bishkek",
        "Asia/Brunei",
        "Asia/Calcutta",
        "Asia/Chita",
        "Asia/Choibalsan",
        "Asia/Chongqing",
        "Asia/Chungking",
        "Asia/Colombo",
        "Asia/Dacca",
        "Asia/Damascus",
        "Asia/Dhaka",
        "Asia/Dili",
        "Asia/Dubai",
        "Asia/Dushanbe",
        "Asia/Famagusta",
        "Asia/Gaza",
        "Asia/Harbin",
        "Asia/Hebron",
        "Asia/Ho_Chi_Minh",
        "Asia/Hong_Kong",
        "Asia/Hovd",
        "Asia/Irkutsk",
        "Asia/Istanbul",
        "Asia/Jakarta",
        "Asia/Jayapura",
        "Asia/Jerusalem",
        "Asia/Kabul",
        "Asia/Kamchatka",
        "Asia/Karachi",
        "Asia/Kashgar",
        "Asia/Kathmandu",
        "Asia/Katmandu",
        "Asia/Khandyga",
        "Asia/Kolkata",
        "Asia/Krasnoyarsk",
        "Asia/Kuala_Lumpur",
        "Asia/Kuching",
        "Asia/Kuwait",
        "Asia/Macao",
        "Asia/Macau",
        "Asia/Magadan",
        "Asia/Makassar",
        "Asia/Manila",
        "Asia/Muscat",
        "Asia/Nicosia",
        "Asia/Novokuznetsk",
        "Asia/Novosibirsk",
        "Asia/Omsk",
        "Asia/Oral",
        "Asia/Phnom_Penh",
        "Asia/Pontianak",
        "Asia/Pyongyang",
        "Asia/Qatar",
        "Asia/Qostanay",
        "Asia/Qyzylorda",
        "Asia/Rangoon",
        "Asia/Riyadh",
        "Asia/Saigon",
        "Asia/Sakhalin",
        "Asia/Samarkand",
        "Asia/Seoul",
        "Asia/Shanghai",
        "Asia/Singapore",
        "Asia/Srednekolymsk",
        "Asia/Taipei",
        "Asia/Tashkent",
        "Asia/Tbilisi",
        "Asia/Tehran",
        "Asia/Tel_Aviv",
        "Asia/Thimbu",
        "Asia/Thimphu",
        "Asia/Tokyo",
        "Asia/Tomsk",
        "Asia/Ujung_Pandang",
        "Asia/Ulaanbaatar",
        "Asia/Ulan_Bator",
        "Asia/Urumqi",
        "Asia/Ust-Nera",
        "Asia/Vientiane",
        "Asia/Vladivostok",
        "Asia/Yakutsk",
        "Asia/Yangon",
        "Asia/Yekaterinburg",
        "Asia/Yerevan",
        "Atlantic/Azores",
        "Atlantic/Bermuda",
        "Atlantic/Canary",
        "Atlantic/Cape_Verde",
        "Atlantic/Faeroe",
        "Atlantic/Faroe",
        "Atlantic/Jan_Mayen",
        "Atlantic/Madeira",
        "Atlantic/Reykjavik",
        "Atlantic/South_Georgia",
        "Atlantic/St_Helena",
        "Atlantic/Stanley",
        "Australia/ACT",
        "Australia/Adelaide",
        "Australia/Brisbane",
        "Australia/Broken_Hill",
        "Australia/Canberra",
        "Australia/Currie",
        "Australia/Darwin",
        "Australia/Eucla",
        "Australia/Hobart",
        "Australia/LHI",
        "Australia/Lindeman",
        "Australia/Lord_Howe",
        "Australia/Melbourne",
        "Australia/NSW",
        "Australia/North",
        "Australia/Perth",
        "Australia/Queensland",
        "Australia/South",
        "Australia/Sydney",
        "Australia/Tasmania",
        "Australia/Victoria",
        "Australia/West",
        "Australia/Yancowinna",
        "Brazil/Acre",
        "Brazil/DeNoronha",
        "Brazil/East",
        "Brazil/West",
        "CET",
        "CST6CDT",
        "Canada/Atlantic",
        "Canada/Central",
        "Canada/Eastern",
        "Canada/Mountain",
        "Canada/Newfoundland",
        "Canada/Pacific",
        "Canada/Saskatchewan",
        "Canada/Yukon",
        "Chile/Continental",
        "Chile/EasterIsland",
        "Cuba",
        "EET",
        "EST",
        "EST5EDT",
        "Egypt",
        "Eire",
        "Etc/GMT",
        "Etc/GMT+0",
        "Etc/GMT+1",
        "Etc/GMT+10",
        "Etc/GMT+11",
        "Etc/GMT+12",
        "Etc/GMT+2",
        "Etc/GMT+3",
        "Etc/GMT+4",
        "Etc/GMT+5",
        "Etc/GMT+6",
        "Etc/GMT+7",
        "Etc/GMT+8",
        "Etc/GMT+9",
        "Etc/GMT-0",
        "Etc/GMT-1",
        "Etc/GMT-10",
        "Etc/GMT-11",
        "Etc/GMT-12",
        "Etc/GMT-13",
        "Etc/GMT-14",
        "Etc/GMT-2",
        "Etc/GMT-3",
        "Etc/GMT-4",
        "Etc/GMT-5",
        "Etc/GMT-6",
        "Etc/GMT-7",
        "Etc/GMT-8",
        "Etc/GMT-9",
        "Etc/GMT0",
        "Etc/Greenwich",
        "Etc/UCT",
        "Etc/UTC",
        "Etc/Universal",
        "Etc/Zulu",
        "Europe/Amsterdam",
        "Europe/Andorra",
        "Europe/Astrakhan",
        "Europe/Athens",
        "Europe/Belfast",
        "Europe/Belgrade",
        "Europe/Berlin",
        "Europe/Bratislava",
        "Europe/Brussels",
        "Europe/Bucharest",
        "Europe/Budapest",
        "Europe/Busingen",
        "Europe/Chisinau",
        "Europe/Copenhagen",
        "Europe/Dublin",
        "Europe/Gibraltar",
        "Europe/Guernsey",
        "Europe/Helsinki",
        "Europe/Isle_of_Man",
        "Europe/Istanbul",
        "Europe/Jersey",
        "Europe/Kaliningrad",
        "Europe/Kiev",
        "Europe/Kirov",
        "Europe/Lisbon",
        "Europe/Ljubljana",
        "Europe/London",
        "Europe/Luxembourg",
        "Europe/Madrid",
        "Europe/Malta",
        "Europe/Mariehamn",
        "Europe/Minsk",
        "Europe/Monaco",
        "Europe/Moscow",
        "Europe/Nicosia",
        "Europe/Oslo",
        "Europe/Paris",
        "Europe/Podgorica",
        "Europe/Prague",
        "Europe/Riga",
        "Europe/Rome",
        "Europe/Samara",
        "Europe/San_Marino",
        "Europe/Sarajevo",
        "Europe/Saratov",
        "Europe/Simferopol",
        "Europe/Skopje",
        "Europe/Sofia",
        "Europe/Stockholm",
        "Europe/Tallinn",
        "Europe/Tirane",
        "Europe/Tiraspol",
        "Europe/Ulyanovsk",
        "Europe/Uzhgorod",
        "Europe/Vaduz",
        "Europe/Vatican",
        "Europe/Vienna",
        "Europe/Vilnius",
        "Europe/Volgograd",
        "Europe/Warsaw",
        "Europe/Zagreb",
        "Europe/Zaporozhye",
        "Europe/Zurich",
        "GB",
        "GB-Eire",
        "GMT",
        "GMT+0",
        "GMT-0",
        "GMT0",
        "Greenwich",
        "HST",
        "Hongkong",
        "Iceland",
        "Indian/Antananarivo",
        "Indian/Chagos",
        "Indian/Christmas",
        "Indian/Cocos",
        "Indian/Comoro",
        "Indian/Kerguelen",
        "Indian/Mahe",
        "Indian/Maldives",
        "Indian/Mauritius",
        "Indian/Mayotte",
        "Indian/Reunion",
        "Iran",
        "Israel",
        "Jamaica",
        "Japan",
        "Kwajalein",
        "Libya",
        "MET",
        "MST",
        "MST7MDT",
        "Mexico/BajaNorte",
        "Mexico/BajaSur",
        "Mexico/General",
        "NZ",
        "NZ-CHAT",
        "Navajo",
        "PRC",
        "PST8PDT",
        "Pacific/Apia",
        "Pacific/Auckland",
        "Pacific/Bougainville",
        "Pacific/Chatham",
        "Pacific/Chuuk",
        "Pacific/Easter",
        "Pacific/Efate",
        "Pacific/Enderbury",
        "Pacific/Fakaofo",
        "Pacific/Fiji",
        "Pacific/Funafuti",
        "Pacific/Galapagos",
        "Pacific/Gambier",
        "Pacific/Guadalcanal",
        "Pacific/Guam",
        "Pacific/Honolulu",
        "Pacific/Johnston",
        "Pacific/Kiritimati",
        "Pacific/Kosrae",
        "Pacific/Kwajalein",
        "Pacific/Majuro",
        "Pacific/Marquesas",
        "Pacific/Midway",
        "Pacific/Nauru",
        "Pacific/Niue",
        "Pacific/Norfolk",
        "Pacific/Noumea",
        "Pacific/Pago_Pago",
        "Pacific/Palau",
        "Pacific/Pitcairn",
        "Pacific/Pohnpei",
        "Pacific/Ponape",
        "Pacific/Port_Moresby",
        "Pacific/Rarotonga",
        "Pacific/Saipan",
        "Pacific/Samoa",
        "Pacific/Tahiti",
        "Pacific/Tarawa",
        "Pacific/Tongatapu",
        "Pacific/Truk",
        "Pacific/Wake",
        "Pacific/Wallis",
        "Pacific/Yap",
        "Poland",
        "Portugal",
        "ROC",
        "ROK",
        "Singapore",
        "Turkey",
        "UCT",
        "US/Alaska",
        "US/Aleutian",
        "US/Arizona",
        "US/Central",
        "US/East-Indiana",
        "US/Eastern",
        "US/Hawaii",
        "US/Indiana-Starke",
        "US/Michigan",
        "US/Mountain",
        "US/Pacific",
        "US/Samoa",
        "UTC",
        "Universal",
        "W-SU",
        "WET",
        "Zulu"
      ]
    }
    * Curl_http_done: called premature == 0
    * Closing connection 0



```python

```
