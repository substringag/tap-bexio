# tap-bexio

`tap-bexio` is a Singer tap for bexio.

Bexio API Documentation: https://docs.bexio.com/

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Currently supported data endpoints

- pr_project

## Installation

Set up the tap in your meltano.yml and add `TAP_BEXIO_AUTH_TOKEN` to your `.env` file

```bash
meltano install
meltano elt tap-bexio target-jsonl
```
