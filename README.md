# tap-bexio

`tap-bexio` is a Singer tap for bexio.

Bexio API Documentation: https://docs.bexio.com/

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Currently supported data endpoints

- business_activities
- pr_project
- pr_project_state
- pr_project_type
- timesheet

## Installation

Set up the tap in your meltano.yml and add `TAP_BEXIO_AUTH_TOKEN` to your `.env` file

```bash
meltano install
meltano elt tap-bexio target-jsonl
```

## How to add more endpoints

1. Create the corresponding schema in `schemas/`.
2. Create the corresponding stream in the file `streams.py`. Path needs to be the api path of Bexio.
3. Add your new Stream to `STREAM_TYPES` array in `tap.py` and import the class as well.
