# tap-bexio

`tap-bexio` is a Singer tap for bexio.

Bexio API Documentation: https://docs.bexio.com/ and https://docs.bexio.com/legacy/

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Currently supported data endpoints

* [x] Contacts
    * [x] Contact Type
    * [x] Contact Group
    * [x] Titles
* [x] Sales Order Management
    * [x] Quotes (kb_offer)
    * [x] Orders (kb_order)
    * [x] Invoices (kb_invoice)
* [x] Purchase
	* [x] Bills
	* [x] Expenses
* [x] Accounting
    * [x] Accounts (accounts)
    * [x] Account Groups (account_groups)
    * [x] Manual entries (accounting_journal)
* [x] Banking
* [ ] Items & Products
* [x] Projects & Time Tracking
* [x] Files
* [ ] Payroll
  * [x] Employees
  * [ ] Absences
* [ ] Other
    * [x] Company Profile
    * [x] Countries
    * [x] Languages
    * [x] Notes
    * [x] Payment Types
    * [ ] Permissions
    * [ ] Tasks
    * [x] Units
    * [x] User Management

## Installation

Set up the tap in your meltano.yml and add `TAP_BEXIO_AUTH_TOKEN` to your `.env` file. Watch out, this is just a Singer tap for Meltano. You need a working meltano project to use this code.

```bash
meltano install
meltano elt tap-bexio target-jsonl
```

## How to add more endpoints

1. Create the corresponding schema in `schemas/`.
2. Create the corresponding stream in the file `streams.py`. Path needs to be the api path of Bexio.
3. Add your new Stream to `STREAM_TYPES` array in `tap.py` and import the class as well.
