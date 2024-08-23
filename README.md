# mss-python ![PyPI](https://img.shields.io/pypi/v/mss-python)

MSS API client for Python projects

<!-- ## Dependencies

This library requires an IANA Time Zone database to be present on the operating system (because it uses https://pkg.go.dev/time#LoadLocation). This database comes pre-installed with many Linux distros. If it’s unavailable (such as on Windows), https://pkg.go.dev/time/tzdata can be imported in the main program (which uses mss-go) instead. -->

## Available methods

- [x] getHotelList
- [x] getHotelListByFilter
- [x] getSpecialList
- [x] getRoomList
- [x] getWidgetConfig
- [x] getBooking
- [x] cancelBooking
- [x] prepareBooking
- [x] getAvailability
- [x] getRoomAvailability
- [x] getDayAvailability
- [x] getPriceList
- [x] createInquiry
- [x] getLocationList
- [x] getThemeList
- [x] getMasterpackagesList
- [x] notifyMasterpackages
- [x] getLastMinuteQuotation
- [x] validateCoupon
- [x] getHotelPictures
- [x] getHotelPictureGroups
- [x] getOptionalServices

## Example Execution

`pip3 install -r requirements.txt`

`python3 -m examples.simple.main`

<!-- -

TODO

- [x] getInquiry - how to find booking IDs?


- [x] getUserSources

  -->

<!-- Warning: Only the methods with a ✓ next to them have been tested so far.

## Before running examples/tests

Set the environment variables with:

```Bash
export $(make env)
```

## Examples

Run `make simple` or `make advanced`

## Tests

Run `make test` -->
