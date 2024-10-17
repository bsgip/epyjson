# Conversion from e-JSON 0

e-JSON 1.0 is structurally different from e-JSON 0, and also contains some other minor content changes.

## Structural Differences
e-JSON 0.x.y organsises network components in the following nested structure:
```JSON
{
    "components": {
        "component_1_id": {
            "Component1Type": {
                "a_data_field": "value",
                "another_data_field": "another_value",
                ...
            }
        },
        "component_2_id": {
            "Component2Type": {
                ...
            }
        },
        ...
    },
    ...
}
```

Each component is specified in a dict as `<id>: {<type>: {<data>}}`

e-JSON 1.x.y instead uses a flattened list of objects, making it more convenient to parse and ensuring that order is preseved through the use of a list:
```JSON
{
    "components": [
        {
            "id": "component_1_id",
            "type": "Component1Type",
            "a_data_field": "value",
            "another_data_field": "another_value",
        },
        {
            "id": "component_2_id",
            "type": "Component2Type",
            ...
        },
        ...
    ],
    ...
}
```

## Non-Structural Differences
### New Connector component
e-JSON 1 includes a new type of component: `Connector`. `Connector`s have two or more connections, and a `switch_state` field that can take the values `"open"`, `"closed"` or "`no_switch`'. When `switch_state` is `open` the connector component is ignored. Otherwise, the connector essentially connects corresponding phases of each connected bus, using a zero impedance (copper plate) connection. Note that `Connector` components are designed to model both switches and solid / copper plate connections. 

### Units
In e-JSON 0, `units` could be specified at the top level of an e-JSON dict. In e-JSON 1, there is no `units` specification. Units are given in SI units, i.e. V, A, W/VA/VAR, Ohm, Siemens. There is one possible departure from the use of SI units: although e-JSON 1 doesn't currently include any units involving time, such as Wh, any future such units will be given in terms of hours, e.g. energy would be specified in Wh in line with typical usage in the energy industry.

### Additional Top-Level Fields
e-JSON 1 files can now take the following optional additional top-level fields:

* `ejson_version`: string e-JSON semver version e.g. "1.0.0"
* `id`: Network ID string

### Transformer Impedance
In e-JSON 0, series impedances of transformers were specified as:
```JSON
"z": [[<r_primary>, <x_primary>], [<r_secondary>, <x_secondary>]
```
In e-JSON 1, this is changed to the following:
```JSON
"z_p": [<r_primary>, <x_primary>],
"z_s": [<r_secondary>, <x_secondary>]
```
Either or both of `z_p` and `z_s` are expected to be supplied.

### Name change for Generator Type
In e-JSON 0, generators had type `Gen`. In e-JSON 1, this is changed to `Generator`.

## Conversion Script
The script `convert_from_ejson_0` is supplied in the same directory as this README, and is simply invoked from the command line as follows:
```sh
convert_from_ejson_0 <input_ejson_0_filename> <output_ejson_1_filename>
```
