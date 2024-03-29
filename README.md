# celtibot
Celtibot is a mastodon bot that runs on the [Openord server](https://mastodon.celticpaganism.org/@Celtibot)
## Usage
### Testing
`SERVER='https://url.social' ACCESS_TOKEN='xxxx' ./src/celtibot.py --mode [topic, holiday, follow, quote] --dryrun 1 --date 03-01`

### Live Tooting
`SERVER='https://url.social' ACCESS_TOKEN='xxxx' ./src/celtibot.py --mode [topic, holiday, follow, quote] --dryrun 0 --date 03-01`

### Use Today
`SERVER='https://url.social' ACCESS_TOKEN='xxxx' ./src/celtibot.py --mode [topic, holiday, follow, quote]`

## Dates
Celtibot prioritizes information relevant to today. If no today specific objects are found in the `data` directory, it will switch to
a random selection mode using python's `random.shuffle()` method, selecting from the data which does not have a `date` or `day` key.

### Date word language
We've created a custom reverse query language for dates that do not fall on the same day each year. The language has three parts: `target`, `direction`, and `epoch`.

`epoch` can either be a numeric date like `01-01` or the word `easter`. The word easter is the only non numeric date it understands and the last word in the `day` property being easter makes celtibot make a few assumptions:

* Celtibot assumes that the first word is an integer for days away from easter's date
* That the second word is either `+` or `-`
* The day integer value(first word) is considered the `target`

If `epoch` is a hyphenated numeric value like `01-01`, this value represents 'month-day` format. With a numeric value, these assumptions are made:

* the second to last word is either `after` or `before` and this signifies that the `target` after or before the `epoch` is what day this falls on.
* The first word is one of `first`, `second`, `third`, `fourth`, or `last`
* The second word is a day of the week like 'sunday' or 'monday'.
* The first and second word are the `target`

#### Usage
You can use the reverse query language by placing it under the `day` attribute of an object(see the examples below). Since our forward query is always now(), Celtibot computes the query languages of each object for that year and compares it to the now() value. If they're the same, it selects that object as relevant to now. If this seems complicated, it is.

You can select for pancake tuesday's date each year by the following attribute:

`day: 47 - easter`

And you can select for the third sunday of January by the following attribute:

`day: third sunday after 01-01`

#### Year is always current year, there is no way specify next or last year relevancy.

## Quotes
```quotes.yaml|yaml
# Today relevant Quotes in numerals
- text: |
    If Candlemas is fair and clear, There'll be two winters in the year.'
  author: Unknown
  source: Scottish Saying
  date: 02-02
  tags:
    - Scottish
# Today relevant Quotes in words
    day: "first monday after 01-01"
# Today relevant quotes in time from easter
    day: easter - 47 # Shrove tuesday
# Randomly chosen quote
- text: "The best candle for man is good sense"
  author: Cynfelan
  source: Welsh by K.H. Jackson
  tags:
    - wisdom
```

## Holidays
```holidays.yaml|yaml
  - name: "The Epiphany"
    date: 01-06
    tags:
      - epiphany
      - catholic
      - pagan
      - witch
      - witchcraft
      - druid
    reconstructed: true
  - name: "Plough Monday"
    welshname: "Dydd Gwyl Geiliau"
    day: "first monday after 01-05"
    what: "Festival of the Sheepfolds is a return to ordinary working life"
    tags:
      - returntowork
      - sheep
  - name: "Handsel Monday"
    scottishname: Diluain Traoighte
    day: "first monday after 01-01"
    what: "Time to give to the poor, to sit with and be with the infirm. If you pay a debt on this day, you'll be paying it all year."
    tags:
      - charity
      - altruism
      - compassion
      - debt
```
## Topics
```topics.yaml|yaml
- name: Cailleach
  rscore: 153.33800000000014
  summary: "In Gaelic (Irish, Scottish and Manx) myth, the Cailleach (Irish:\_[\u02C8\
    kal\u0320\u02B2\u0259x, k\u0259\u02C8l\u0320\u02B2ax], Scottish\_Gaelic:\_[\u02C8\
    k\u02B0a\u028E\u0259x]) is a divine hag and ancestor, associated with the creation\
    \ of the landscape and with the weather, especially storms and winter. The word\
    \ literally means 'old woman, hag', and is found w..."
  link: http://en.wikipedia.org/wiki/Cailleach
- name: "Ois\xEDn"
  rscore: 89.68899999999991
  summary: "Ois\xEDn (Irish pronunciation:\_[\u0254\u02C8\u0283i\u02D0n\u02B2, \u02C8\
    \u0254\u0283i\u02D0n\u02B2] USH-een), Osian, Ossian (/\u02C8\u0252\u0283\u0259\
    n/ USH-\u0259n), or anglicized as  Osheen (/o\u028A\u02C8\u0283i\u02D0n/ oh-SHEEN)\
    \ was regarded in legend as the greatest poet of Ireland, a warrior of the Fianna\
    \ in the Ossianic or Fenian Cycle of Irish mythology. He is the demigod son of\
    \ Fionn ma..."
  link: "http://en.wikipedia.org/wiki/Ois\xEDn"
- name: Halloween
  date: 10-31
  rscore: 46.6413
  summary: Halloween or Hallowe'en (less commonly known as Allhalloween, All Hallows'
    Eve, or All Saints' Eve) is a celebration observed in many countries  on 31 October,
    the eve of the Western Christian feast of All Saints' Day. It begins the observance
    of Allhallowtide, the time in the liturgical year dedica...
  link: http://en.wikipedia.org/wiki/Halloween
```