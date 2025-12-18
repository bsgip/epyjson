# Schema Docs

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** JSON schema for the e-JSON data format that represents electrical networks

| Property                           | Pattern | Type             | Deprecated | Definition           | Title/Description                                                                                                                                                                  |
| ---------------------------------- | ------- | ---------------- | ---------- | -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| - [ejson_version](#ejson_version ) | No      | string           | No         | -                    | Version number in the form a.b.c. Versions start at 1.0; a increments at major breaking changes, b increments at minor breaking changes, and c increments for non-breaking changes |
| - [id](#id )                       | No      | string           | No         | -                    | Network ID                                                                                                                                                                         |
| - [user_data](#user_data )         | No      | object           | No         | In #/$defs/user_data | Non-e-json annotations                                                                                                                                                             |
| + [voltage_type](#voltage_type )   | No      | enum (of string) | No         | -                    | Voltage type, ll (line to line) or lg (line to ground)                                                                                                                             |
| + [components](#components )       | No      | array            | No         | -                    | List of all network components (nodes and elements)                                                                                                                                |

## <a name="ejson_version"></a>1. Property `root > ejson_version`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Version number in the form a.b.c. Versions start at 1.0; a increments at major breaking changes, b increments at minor breaking changes, and c increments for non-breaking changes

**Example:**

```json
"1.0.0"
```

| Restrictions                      |                                                                                                                              |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **Must match regular expression** | ```[0-9]+.[0-9]+.[0.9]+``` [Test](https://regex101.com/?regex=%5B0-9%5D%2B.%5B0-9%5D%2B.%5B0.9%5D%2B&testString=%221.0.0%22) |

## <a name="id"></a>2. Property `root > id`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Network ID

## <a name="user_data"></a>3. Property `root > user_data`

|                           |                   |
| ------------------------- | ----------------- |
| **Type**                  | `object`          |
| **Required**              | No                |
| **Additional properties** | Any type allowed  |
| **Defined in**            | #/$defs/user_data |

**Description:** Non-e-json annotations

## <a name="voltage_type"></a>4. Property `root > voltage_type`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | Yes                |

**Description:** Voltage type, ll (line to line) or lg (line to ground)

**Examples:**

```json
"ll"
```

```json
"lg"
```

Must be one of:
* "ll"
* "lg"

## <a name="components"></a>5. Property `root > components`

|              |         |
| ------------ | ------- |
| **Type**     | `array` |
| **Required** | Yes     |

**Description:** List of all network components (nodes and elements)

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be | Description                                                |
| ------------------------------- | ---------------------------------------------------------- |
| [component](#components_items)  | A component (Node/Infeeder/Gen/Load/Connector/Transformer) |

### <a name="components_items"></a>5.1. root > components > component

|                           |                   |
| ------------------------- | ----------------- |
| **Type**                  | `combining`       |
| **Required**              | No                |
| **Additional properties** | Any type allowed  |
| **Defined in**            | #/$defs/component |

**Description:** A component (Node/Infeeder/Gen/Load/Connector/Transformer)

| One of(Option)                            |
| ----------------------------------------- |
| [Node](#components_items_oneOf_i0)        |
| [Infeeder](#components_items_oneOf_i1)    |
| [Gen](#components_items_oneOf_i2)         |
| [Load](#components_items_oneOf_i3)        |
| [Line](#components_items_oneOf_i4)        |
| [Connector](#components_items_oneOf_i5)   |
| [Transformer](#components_items_oneOf_i6) |

#### <a name="components_items_oneOf_i0"></a>5.1.1. Property `root > components > components items > oneOf > Node`

|                           |              |
| ------------------------- | ------------ |
| **Type**                  | `object`     |
| **Required**              | No           |
| **Additional properties** | Not allowed  |
| **Defined in**            | #/$defs/Node |

**Description:** A network node (bus)

| Property                                             | Pattern | Type            | Deprecated | Definition                       | Title/Description                                                                                        |
| ---------------------------------------------------- | ------- | --------------- | ---------- | -------------------------------- | -------------------------------------------------------------------------------------------------------- |
| + [id](#components_items_oneOf_i0_id )               | No      | string          | No         | In #/$defs/component_id          | The component's unique ID                                                                                |
| + [type](#components_items_oneOf_i0_type )           | No      | const           | No         | -                                | -                                                                                                        |
| + [phs](#components_items_oneOf_i0_phs )             | No      | array of string | No         | In #/$defs/phs                   | A list of phases                                                                                         |
| - [user_data](#components_items_oneOf_i0_user_data ) | No      | object          | No         | Same as [user_data](#user_data ) | Non-e-json annotations                                                                                   |
| - [v](#components_items_oneOf_i0_v )                 | No      | array           | No         | In #/$defs/complex_array         | The current voltage in V for each phase, line to line or line to ground according to global voltage_type |
| + [v_base](#components_items_oneOf_i0_v_base )       | No      | number          | No         | In #/$defs/positive_number       | The base voltage in V for the node, line to line or line to ground according to global voltage_type      |
| - [lat_long](#components_items_oneOf_i0_lat_long )   | No      | object          | No         | -                                | [latitude, longitude]                                                                                    |
| - [xy](#components_items_oneOf_i0_xy )               | No      | object          | No         | -                                | Coordinates [x, y] e.g. for map datum                                                                    |

##### <a name="components_items_oneOf_i0_id"></a>5.1.1.1. Property `root > components > components items > oneOf > item 0 > id`

|                |                      |
| -------------- | -------------------- |
| **Type**       | `string`             |
| **Required**   | Yes                  |
| **Defined in** | #/$defs/component_id |

**Description:** The component's unique ID

##### <a name="components_items_oneOf_i0_type"></a>5.1.1.2. Property `root > components > components items > oneOf > item 0 > type`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

Specific value: `"Node"`

##### <a name="components_items_oneOf_i0_phs"></a>5.1.1.3. Property `root > components > components items > oneOf > item 0 > phs`

|                |                   |
| -------------- | ----------------- |
| **Type**       | `array of string` |
| **Required**   | Yes               |
| **Defined in** | #/$defs/phs       |

**Description:** A list of phases

**Examples:**

```json
[
    "A"
]
```

```json
[
    "A",
    "B",
    "C"
]
```

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | 1                  |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                   | Description |
| ------------------------------------------------- | ----------- |
| [phs items](#components_items_oneOf_i0_phs_items) | -           |

###### <a name="components_items_oneOf_i0_phs_items"></a>5.1.1.3.1. root > components > components items > oneOf > item 0 > phs > phs items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

##### <a name="components_items_oneOf_i0_user_data"></a>5.1.1.4. Property `root > components > components items > oneOf > item 0 > user_data`

|                           |                         |
| ------------------------- | ----------------------- |
| **Type**                  | `object`                |
| **Required**              | No                      |
| **Additional properties** | Any type allowed        |
| **Same definition as**    | [user_data](#user_data) |

**Description:** Non-e-json annotations

##### <a name="components_items_oneOf_i0_v"></a>5.1.1.5. Property `root > components > components items > oneOf > item 0 > v`

|                |                       |
| -------------- | --------------------- |
| **Type**       | `array`               |
| **Required**   | No                    |
| **Defined in** | #/$defs/complex_array |

**Description:** The current voltage in V for each phase, line to line or line to ground according to global voltage_type

**Example:**

```json
[
    [
        1,
        2.3
    ],
    [
        2.0,
        0.0
    ],
    [
        0.0,
        -1.0
    ]
]
```

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                      | Description                                |
| ---------------------------------------------------- | ------------------------------------------ |
| [complex_number](#components_items_oneOf_i0_v_items) | Complex number, stored as [<real>, <imag>] |

###### <a name="components_items_oneOf_i0_v_items"></a>5.1.1.5.1. root > components > components items > oneOf > item 0 > v > complex_number

|                           |                        |
| ------------------------- | ---------------------- |
| **Type**                  | `object`               |
| **Required**              | No                     |
| **Additional properties** | Any type allowed       |
| **Defined in**            | #/$defs/complex_number |

**Description:** Complex number, stored as [<real>, <imag>]

**Example:**

```json
[
    4,
    7
]
```

##### <a name="components_items_oneOf_i0_v_base"></a>5.1.1.6. Property `root > components > components items > oneOf > item 0 > v_base`

|                |                         |
| -------------- | ----------------------- |
| **Type**       | `number`                |
| **Required**   | Yes                     |
| **Defined in** | #/$defs/positive_number |

**Description:** The base voltage in V for the node, line to line or line to ground according to global voltage_type

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

##### <a name="components_items_oneOf_i0_lat_long"></a>5.1.1.7. Property `root > components > components items > oneOf > item 0 > lat_long`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** [latitude, longitude]

##### <a name="components_items_oneOf_i0_xy"></a>5.1.1.8. Property `root > components > components items > oneOf > item 0 > xy`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Coordinates [x, y] e.g. for map datum

#### <a name="components_items_oneOf_i1"></a>5.1.2. Property `root > components > components items > oneOf > Infeeder`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Not allowed      |
| **Defined in**            | #/$defs/Infeeder |

**Description:** Network infeeder with constant voltage

| Property                                               | Pattern | Type           | Deprecated | Definition                                           | Title/Description                                                                                |
| ------------------------------------------------------ | ------- | -------------- | ---------- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| + [id](#components_items_oneOf_i1_id )                 | No      | string         | No         | Same as [id](#components_items_oneOf_i0_id )         | The component's unique ID                                                                        |
| + [type](#components_items_oneOf_i1_type )             | No      | const          | No         | -                                                    | -                                                                                                |
| + [cons](#components_items_oneOf_i1_cons )             | No      | array          | No         | In #/$defs/one_connection                            | A one element list of connections                                                                |
| - [user_data](#components_items_oneOf_i1_user_data )   | No      | object         | No         | Same as [user_data](#user_data )                     | Non-e-json annotations                                                                           |
| - [in_service](#components_items_oneOf_i1_in_service ) | No      | boolean        | No         | In #/$defs/in_service                                | If false, the component is out of service                                                        |
| + [v_setpoint](#components_items_oneOf_i1_v_setpoint ) | No      | number         | No         | Same as [v_base](#components_items_oneOf_i0_v_base ) | Voltage magnitude setpoint in V, line to line or line to ground according to global voltage_type |
| - [i_max](#components_items_oneOf_i1_i_max )           | No      | number or null | No         | -                                                    | maximum current per phase, in A                                                                  |

##### <a name="components_items_oneOf_i1_id"></a>5.1.2.1. Property `root > components > components items > oneOf > item 1 > id`

|                        |                                     |
| ---------------------- | ----------------------------------- |
| **Type**               | `string`                            |
| **Required**           | Yes                                 |
| **Same definition as** | [id](#components_items_oneOf_i0_id) |

**Description:** The component's unique ID

##### <a name="components_items_oneOf_i1_type"></a>5.1.2.2. Property `root > components > components items > oneOf > item 1 > type`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

Specific value: `"Infeeder"`

##### <a name="components_items_oneOf_i1_cons"></a>5.1.2.3. Property `root > components > components items > oneOf > item 1 > cons`

|                |                        |
| -------------- | ---------------------- |
| **Type**       | `array`                |
| **Required**   | Yes                    |
| **Defined in** | #/$defs/one_connection |

**Description:** A one element list of connections

**Example:**

```json
[
    {
        "node": "node_1",
        "phs": [
            "A",
            "C"
        ]
    }
]
```

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | 1                  |
| **Max items**        | 1                  |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                     | Description                                                                                                                  |
| --------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| [connection](#components_items_oneOf_i1_cons_items) | A list of connections from element terminals. Each connection gives the node ID and phases to which the element is connected |

###### <a name="components_items_oneOf_i1_cons_items"></a>5.1.2.3.1. root > components > components items > oneOf > item 1 > cons > connection

|                           |                    |
| ------------------------- | ------------------ |
| **Type**                  | `object`           |
| **Required**              | No                 |
| **Additional properties** | Any type allowed   |
| **Defined in**            | #/$defs/connection |

**Description:** A list of connections from element terminals. Each connection gives the node ID and phases to which the element is connected

**Example:**

```json
[
    {
        "node": "node_1",
        "phs": [
            "A",
            "C"
        ]
    },
    {
        "node": "node_2",
        "phs": [
            "A",
            "B",
            "C"
        ]
    }
]
```

| Property                                              | Pattern | Type            | Deprecated | Definition                                     | Title/Description |
| ----------------------------------------------------- | ------- | --------------- | ---------- | ---------------------------------------------- | ----------------- |
| + [node](#components_items_oneOf_i1_cons_items_node ) | No      | string          | No         | -                                              | -                 |
| + [phs](#components_items_oneOf_i1_cons_items_phs )   | No      | array of string | No         | Same as [phs](#components_items_oneOf_i0_phs ) | A list of phases  |

###### <a name="components_items_oneOf_i1_cons_items_node"></a>5.1.2.3.1.1. Property `root > components > components items > oneOf > item 1 > cons > cons items > node`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="components_items_oneOf_i1_cons_items_phs"></a>5.1.2.3.1.2. Property `root > components > components items > oneOf > item 1 > cons > cons items > phs`

|                        |                                       |
| ---------------------- | ------------------------------------- |
| **Type**               | `array of string`                     |
| **Required**           | Yes                                   |
| **Same definition as** | [phs](#components_items_oneOf_i0_phs) |

**Description:** A list of phases

##### <a name="components_items_oneOf_i1_user_data"></a>5.1.2.4. Property `root > components > components items > oneOf > item 1 > user_data`

|                           |                         |
| ------------------------- | ----------------------- |
| **Type**                  | `object`                |
| **Required**              | No                      |
| **Additional properties** | Any type allowed        |
| **Same definition as**    | [user_data](#user_data) |

**Description:** Non-e-json annotations

##### <a name="components_items_oneOf_i1_in_service"></a>5.1.2.5. Property `root > components > components items > oneOf > item 1 > in_service`

|                |                    |
| -------------- | ------------------ |
| **Type**       | `boolean`          |
| **Required**   | No                 |
| **Default**    | `true`             |
| **Defined in** | #/$defs/in_service |

**Description:** If false, the component is out of service

##### <a name="components_items_oneOf_i1_v_setpoint"></a>5.1.2.6. Property `root > components > components items > oneOf > item 1 > v_setpoint`

|                        |                                             |
| ---------------------- | ------------------------------------------- |
| **Type**               | `number`                                    |
| **Required**           | Yes                                         |
| **Same definition as** | [v_base](#components_items_oneOf_i0_v_base) |

**Description:** Voltage magnitude setpoint in V, line to line or line to ground according to global voltage_type

##### <a name="components_items_oneOf_i1_i_max"></a>5.1.2.7. Property `root > components > components items > oneOf > item 1 > i_max`

|              |                  |
| ------------ | ---------------- |
| **Type**     | `number or null` |
| **Required** | No               |

**Description:** maximum current per phase, in A

#### <a name="components_items_oneOf_i2"></a>5.1.3. Property `root > components > components items > oneOf > Gen`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |
| **Defined in**            | #/$defs/Gen      |

**Description:** A generator, with optional voltage control

| Property                                                     | Pattern | Type             | Deprecated | Definition                                                   | Title/Description                                                                                |
| ------------------------------------------------------------ | ------- | ---------------- | ---------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| + [id](#components_items_oneOf_i2_id )                       | No      | string           | No         | Same as [id](#components_items_oneOf_i0_id )                 | The component's unique ID                                                                        |
| + [type](#components_items_oneOf_i2_type )                   | No      | const            | No         | -                                                            | -                                                                                                |
| + [cons](#components_items_oneOf_i2_cons )                   | No      | array            | No         | Same as [cons](#components_items_oneOf_i1_cons )             | A one element list of connections                                                                |
| - [user_data](#components_items_oneOf_i2_user_data )         | No      | object           | No         | Same as [user_data](#user_data )                             | Non-e-json annotations                                                                           |
| - [in_service](#components_items_oneOf_i2_in_service )       | No      | boolean          | No         | Same as [in_service](#components_items_oneOf_i1_in_service ) | If false, the component is out of service                                                        |
| + [wiring](#components_items_oneOf_i2_wiring )               | No      | enum (of string) | No         | In #/$defs/wiring                                            | Specification of load or transformer wiring; delta (LL) or wye (LG)                              |
| - [p_min](#components_items_oneOf_i2_p_min )                 | No      | number           | No         | -                                                            | Minimum real power injection in W, (generation convention).                                      |
| - [p_max](#components_items_oneOf_i2_p_max )                 | No      | number           | No         | -                                                            | Maximum real power injection in W, (generation convention).                                      |
| - [q_min](#components_items_oneOf_i2_q_min )                 | No      | number           | No         | -                                                            | Minimum reactive power injection in VA (generation convention).                                  |
| - [q_max](#components_items_oneOf_i2_q_max )                 | No      | number           | No         | -                                                            | Maximum reactive power injection in VA (generation convention).                                  |
| - [cost](#components_items_oneOf_i2_cost )                   | No      | number           | No         | -                                                            | Cost, in (cost unit) per Wh                                                                      |
| - [fixed_voltage](#components_items_oneOf_i2_fixed_voltage ) | No      | boolean          | No         | -                                                            | If true, the voltage magnitude is maintained at the setpoint.                                    |
| - [v_setpoint](#components_items_oneOf_i2_v_setpoint )       | No      | number           | No         | -                                                            | Voltage magnitude setpoint in V, line to line or line to ground according to global voltage_type |
| - [is_reference](#components_items_oneOf_i2_is_reference )   | No      | boolean          | No         | -                                                            | If true, the voltage angle is referenced to zero.                                                |

##### <a name="components_items_oneOf_i2_id"></a>5.1.3.1. Property `root > components > components items > oneOf > item 2 > id`

|                        |                                     |
| ---------------------- | ----------------------------------- |
| **Type**               | `string`                            |
| **Required**           | Yes                                 |
| **Same definition as** | [id](#components_items_oneOf_i0_id) |

**Description:** The component's unique ID

##### <a name="components_items_oneOf_i2_type"></a>5.1.3.2. Property `root > components > components items > oneOf > item 2 > type`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

Specific value: `"Generator"`

##### <a name="components_items_oneOf_i2_cons"></a>5.1.3.3. Property `root > components > components items > oneOf > item 2 > cons`

|                        |                                         |
| ---------------------- | --------------------------------------- |
| **Type**               | `array`                                 |
| **Required**           | Yes                                     |
| **Same definition as** | [cons](#components_items_oneOf_i1_cons) |

**Description:** A one element list of connections

##### <a name="components_items_oneOf_i2_user_data"></a>5.1.3.4. Property `root > components > components items > oneOf > item 2 > user_data`

|                           |                         |
| ------------------------- | ----------------------- |
| **Type**                  | `object`                |
| **Required**              | No                      |
| **Additional properties** | Any type allowed        |
| **Same definition as**    | [user_data](#user_data) |

**Description:** Non-e-json annotations

##### <a name="components_items_oneOf_i2_in_service"></a>5.1.3.5. Property `root > components > components items > oneOf > item 2 > in_service`

|                        |                                                     |
| ---------------------- | --------------------------------------------------- |
| **Type**               | `boolean`                                           |
| **Required**           | No                                                  |
| **Default**            | `true`                                              |
| **Same definition as** | [in_service](#components_items_oneOf_i1_in_service) |

**Description:** If false, the component is out of service

##### <a name="components_items_oneOf_i2_wiring"></a>5.1.3.6. Property `root > components > components items > oneOf > item 2 > wiring`

|                |                    |
| -------------- | ------------------ |
| **Type**       | `enum (of string)` |
| **Required**   | Yes                |
| **Defined in** | #/$defs/wiring     |

**Description:** Specification of load or transformer wiring; delta (LL) or wye (LG)

Must be one of:
* "delta"
* "wye"

##### <a name="components_items_oneOf_i2_p_min"></a>5.1.3.7. Property `root > components > components items > oneOf > item 2 > p_min`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

**Description:** Minimum real power injection in W, (generation convention). 

##### <a name="components_items_oneOf_i2_p_max"></a>5.1.3.8. Property `root > components > components items > oneOf > item 2 > p_max`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0`      |

**Description:** Maximum real power injection in W, (generation convention).

##### <a name="components_items_oneOf_i2_q_min"></a>5.1.3.9. Property `root > components > components items > oneOf > item 2 > q_min`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

**Description:** Minimum reactive power injection in VA (generation convention). 

##### <a name="components_items_oneOf_i2_q_max"></a>5.1.3.10. Property `root > components > components items > oneOf > item 2 > q_max`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0`      |

**Description:** Maximum reactive power injection in VA (generation convention).

##### <a name="components_items_oneOf_i2_cost"></a>5.1.3.11. Property `root > components > components items > oneOf > item 2 > cost`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0`      |

**Description:** Cost, in (cost unit) per Wh

##### <a name="components_items_oneOf_i2_fixed_voltage"></a>5.1.3.12. Property `root > components > components items > oneOf > item 2 > fixed_voltage`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `false`   |

**Description:** If true, the voltage magnitude is maintained at the setpoint.

##### <a name="components_items_oneOf_i2_v_setpoint"></a>5.1.3.13. Property `root > components > components items > oneOf > item 2 > v_setpoint`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

**Description:** Voltage magnitude setpoint in V, line to line or line to ground according to global voltage_type

##### <a name="components_items_oneOf_i2_is_reference"></a>5.1.3.14. Property `root > components > components items > oneOf > item 2 > is_reference`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `false`   |

**Description:** If true, the voltage angle is referenced to zero.

#### <a name="components_items_oneOf_i3"></a>5.1.4. Property `root > components > components items > oneOf > Load`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |
| **Defined in**            | #/$defs/Load     |

**Description:** A load

| Property                                             | Pattern | Type             | Deprecated | Definition                                           | Title/Description                                                   |
| ---------------------------------------------------- | ------- | ---------------- | ---------- | ---------------------------------------------------- | ------------------------------------------------------------------- |
| + [id](#components_items_oneOf_i3_id )               | No      | string           | No         | Same as [id](#components_items_oneOf_i0_id )         | The component's unique ID                                           |
| + [type](#components_items_oneOf_i3_type )           | No      | const            | No         | -                                                    | -                                                                   |
| + [cons](#components_items_oneOf_i3_cons )           | No      | array            | No         | Same as [cons](#components_items_oneOf_i1_cons )     | A one element list of connections                                   |
| - [user_data](#components_items_oneOf_i3_user_data ) | No      | object           | No         | Same as [user_data](#user_data )                     | Non-e-json annotations                                              |
| - [wiring](#components_items_oneOf_i3_wiring )       | No      | enum (of string) | No         | Same as [wiring](#components_items_oneOf_i2_wiring ) | Specification of load or transformer wiring; delta (LL) or wye (LG) |
| - [s](#components_items_oneOf_i3_s )                 | No      | array            | No         | -                                                    | -                                                                   |

##### <a name="components_items_oneOf_i3_id"></a>5.1.4.1. Property `root > components > components items > oneOf > item 3 > id`

|                        |                                     |
| ---------------------- | ----------------------------------- |
| **Type**               | `string`                            |
| **Required**           | Yes                                 |
| **Same definition as** | [id](#components_items_oneOf_i0_id) |

**Description:** The component's unique ID

##### <a name="components_items_oneOf_i3_type"></a>5.1.4.2. Property `root > components > components items > oneOf > item 3 > type`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

Specific value: `"Load"`

##### <a name="components_items_oneOf_i3_cons"></a>5.1.4.3. Property `root > components > components items > oneOf > item 3 > cons`

|                        |                                         |
| ---------------------- | --------------------------------------- |
| **Type**               | `array`                                 |
| **Required**           | Yes                                     |
| **Same definition as** | [cons](#components_items_oneOf_i1_cons) |

**Description:** A one element list of connections

##### <a name="components_items_oneOf_i3_user_data"></a>5.1.4.4. Property `root > components > components items > oneOf > item 3 > user_data`

|                           |                         |
| ------------------------- | ----------------------- |
| **Type**                  | `object`                |
| **Required**              | No                      |
| **Additional properties** | Any type allowed        |
| **Same definition as**    | [user_data](#user_data) |

**Description:** Non-e-json annotations

##### <a name="components_items_oneOf_i3_wiring"></a>5.1.4.5. Property `root > components > components items > oneOf > item 3 > wiring`

|                        |                                             |
| ---------------------- | ------------------------------------------- |
| **Type**               | `enum (of string)`                          |
| **Required**           | No                                          |
| **Same definition as** | [wiring](#components_items_oneOf_i2_wiring) |

**Description:** Specification of load or transformer wiring; delta (LL) or wye (LG)

##### <a name="components_items_oneOf_i3_s"></a>5.1.4.6. Property `root > components > components items > oneOf > item 3 > s`

|              |         |
| ------------ | ------- |
| **Type**     | `array` |
| **Required** | No      |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | 1                  |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                      | Description                                |
| ---------------------------------------------------- | ------------------------------------------ |
| [complex_number](#components_items_oneOf_i3_s_items) | Complex number, stored as [<real>, <imag>] |

###### <a name="components_items_oneOf_i3_s_items"></a>5.1.4.6.1. root > components > components items > oneOf > item 3 > s > complex_number

|                           |                                                                         |
| ------------------------- | ----------------------------------------------------------------------- |
| **Type**                  | `object`                                                                |
| **Required**              | No                                                                      |
| **Additional properties** | Any type allowed                                                        |
| **Same definition as**    | [components_items_oneOf_i0_v_items](#components_items_oneOf_i0_v_items) |

**Description:** Complex number, stored as [<real>, <imag>]

#### <a name="components_items_oneOf_i4"></a>5.1.5. Property `root > components > components items > oneOf > Line`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `combining`      |
| **Required**              | No               |
| **Additional properties** | Any type allowed |
| **Defined in**            | #/$defs/Line     |

**Description:** A line

| Property                                               | Pattern | Type           | Deprecated | Definition                                                   | Title/Description                         |
| ------------------------------------------------------ | ------- | -------------- | ---------- | ------------------------------------------------------------ | ----------------------------------------- |
| + [id](#components_items_oneOf_i4_id )                 | No      | string         | No         | Same as [id](#components_items_oneOf_i0_id )                 | The component's unique ID                 |
| + [type](#components_items_oneOf_i4_type )             | No      | const          | No         | -                                                            | -                                         |
| + [cons](#components_items_oneOf_i4_cons )             | No      | array          | No         | In #/$defs/two_connections                                   | A two element list of connections         |
| - [user_data](#components_items_oneOf_i4_user_data )   | No      | object         | No         | Same as [user_data](#user_data )                             | Non-e-json annotations                    |
| - [in_service](#components_items_oneOf_i4_in_service ) | No      | boolean        | No         | Same as [in_service](#components_items_oneOf_i1_in_service ) | If false, the component is out of service |
| - [i_max](#components_items_oneOf_i4_i_max )           | No      | number or null | No         | -                                                            | -                                         |
| + [length](#components_items_oneOf_i4_length )         | No      | number         | No         | -                                                            | -                                         |

| One of(Option)                                              |
| ----------------------------------------------------------- |
| [line_impedance_z_z0](#components_items_oneOf_i4_oneOf_i0)  |
| [line_impedance_y_bus](#components_items_oneOf_i4_oneOf_i1) |

##### <a name="components_items_oneOf_i4_oneOf_i0"></a>5.1.5.1. Property `root > components > components items > oneOf > item 4 > oneOf > line_impedance_z_z0`

|                           |                             |
| ------------------------- | --------------------------- |
| **Type**                  | `object`                    |
| **Required**              | No                          |
| **Additional properties** | Any type allowed            |
| **Defined in**            | #/$defs/line_impedance_z_z0 |

| Property                                              | Pattern | Type   | Deprecated | Definition                                                                       | Title/Description                          |
| ----------------------------------------------------- | ------- | ------ | ---------- | -------------------------------------------------------------------------------- | ------------------------------------------ |
| + [z](#components_items_oneOf_i4_oneOf_i0_z )         | No      | object | No         | Same as [components_items_oneOf_i0_v_items](#components_items_oneOf_i0_v_items ) | Complex number, stored as [<real>, <imag>] |
| + [z0](#components_items_oneOf_i4_oneOf_i0_z0 )       | No      | object | No         | Same as [components_items_oneOf_i0_v_items](#components_items_oneOf_i0_v_items ) | Complex number, stored as [<real>, <imag>] |
| - [b_chg](#components_items_oneOf_i4_oneOf_i0_b_chg ) | No      | number | No         | -                                                                                | -                                          |

###### <a name="components_items_oneOf_i4_oneOf_i0_z"></a>5.1.5.1.1. Property `root > components > components items > oneOf > item 4 > oneOf > item 0 > z`

|                           |                                                                         |
| ------------------------- | ----------------------------------------------------------------------- |
| **Type**                  | `object`                                                                |
| **Required**              | Yes                                                                     |
| **Additional properties** | Any type allowed                                                        |
| **Same definition as**    | [components_items_oneOf_i0_v_items](#components_items_oneOf_i0_v_items) |

**Description:** Complex number, stored as [<real>, <imag>]

###### <a name="components_items_oneOf_i4_oneOf_i0_z0"></a>5.1.5.1.2. Property `root > components > components items > oneOf > item 4 > oneOf > item 0 > z0`

|                           |                                                                         |
| ------------------------- | ----------------------------------------------------------------------- |
| **Type**                  | `object`                                                                |
| **Required**              | Yes                                                                     |
| **Additional properties** | Any type allowed                                                        |
| **Same definition as**    | [components_items_oneOf_i0_v_items](#components_items_oneOf_i0_v_items) |

**Description:** Complex number, stored as [<real>, <imag>]

###### <a name="components_items_oneOf_i4_oneOf_i0_b_chg"></a>5.1.5.1.3. Property `root > components > components items > oneOf > item 4 > oneOf > item 0 > b_chg`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

##### <a name="components_items_oneOf_i4_oneOf_i1"></a>5.1.5.2. Property `root > components > components items > oneOf > item 4 > oneOf > line_impedance_y_bus`

|                           |                              |
| ------------------------- | ---------------------------- |
| **Type**                  | `object`                     |
| **Required**              | No                           |
| **Additional properties** | Any type allowed             |
| **Defined in**            | #/$defs/line_impedance_y_bus |

| Property                                              | Pattern | Type  | Deprecated | Definition                | Title/Description           |
| ----------------------------------------------------- | ------- | ----- | ---------- | ------------------------- | --------------------------- |
| + [y_bus](#components_items_oneOf_i4_oneOf_i1_y_bus ) | No      | array | No         | In #/$defs/complex_matrix | A matrix of complex numbers |

###### <a name="components_items_oneOf_i4_oneOf_i1_y_bus"></a>5.1.5.2.1. Property `root > components > components items > oneOf > item 4 > oneOf > item 1 > y_bus`

|                |                        |
| -------------- | ---------------------- |
| **Type**       | `array`                |
| **Required**   | Yes                    |
| **Defined in** | #/$defs/complex_matrix |

**Description:** A matrix of complex numbers

**Examples:**

```json
[
    [
        [
            1,
            0
        ],
        [
            1,
            1
        ]
    ],
    [
        [
            0,
            1
        ],
        [
            1,
            1
        ]
    ]
]
```

```json
[
    [
        [
            1,
            0
        ]
    ]
]
```

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                  | Description                 |
| ---------------------------------------------------------------- | --------------------------- |
| [complex_array](#components_items_oneOf_i4_oneOf_i1_y_bus_items) | An array of complex numbers |

###### <a name="components_items_oneOf_i4_oneOf_i1_y_bus_items"></a>5.1.5.2.1.1. root > components > components items > oneOf > item 4 > oneOf > item 1 > y_bus > complex_array

|                        |                                   |
| ---------------------- | --------------------------------- |
| **Type**               | `array`                           |
| **Required**           | No                                |
| **Same definition as** | [v](#components_items_oneOf_i0_v) |

**Description:** An array of complex numbers

##### <a name="components_items_oneOf_i4_id"></a>5.1.5.3. Property `root > components > components items > oneOf > item 4 > id`

|                        |                                     |
| ---------------------- | ----------------------------------- |
| **Type**               | `string`                            |
| **Required**           | Yes                                 |
| **Same definition as** | [id](#components_items_oneOf_i0_id) |

**Description:** The component's unique ID

##### <a name="components_items_oneOf_i4_type"></a>5.1.5.4. Property `root > components > components items > oneOf > item 4 > type`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

Specific value: `"Line"`

##### <a name="components_items_oneOf_i4_cons"></a>5.1.5.5. Property `root > components > components items > oneOf > item 4 > cons`

|                |                         |
| -------------- | ----------------------- |
| **Type**       | `array`                 |
| **Required**   | Yes                     |
| **Defined in** | #/$defs/two_connections |

**Description:** A two element list of connections

**Example:**

```json
[
    {
        "node": "node_1",
        "phs": [
            "A",
            "C"
        ]
    },
    {
        "node": "node_2",
        "phs": [
            "A",
            "B",
            "C"
        ]
    }
]
```

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | 2                  |
| **Max items**        | 2                  |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                     | Description                                                                                                                  |
| --------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| [connection](#components_items_oneOf_i4_cons_items) | A list of connections from element terminals. Each connection gives the node ID and phases to which the element is connected |

###### <a name="components_items_oneOf_i4_cons_items"></a>5.1.5.5.1. root > components > components items > oneOf > item 4 > cons > connection

|                           |                                                                               |
| ------------------------- | ----------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                      |
| **Required**              | No                                                                            |
| **Additional properties** | Any type allowed                                                              |
| **Same definition as**    | [components_items_oneOf_i1_cons_items](#components_items_oneOf_i1_cons_items) |

**Description:** A list of connections from element terminals. Each connection gives the node ID and phases to which the element is connected

##### <a name="components_items_oneOf_i4_user_data"></a>5.1.5.6. Property `root > components > components items > oneOf > item 4 > user_data`

|                           |                         |
| ------------------------- | ----------------------- |
| **Type**                  | `object`                |
| **Required**              | No                      |
| **Additional properties** | Any type allowed        |
| **Same definition as**    | [user_data](#user_data) |

**Description:** Non-e-json annotations

##### <a name="components_items_oneOf_i4_in_service"></a>5.1.5.7. Property `root > components > components items > oneOf > item 4 > in_service`

|                        |                                                     |
| ---------------------- | --------------------------------------------------- |
| **Type**               | `boolean`                                           |
| **Required**           | No                                                  |
| **Default**            | `true`                                              |
| **Same definition as** | [in_service](#components_items_oneOf_i1_in_service) |

**Description:** If false, the component is out of service

##### <a name="components_items_oneOf_i4_i_max"></a>5.1.5.8. Property `root > components > components items > oneOf > item 4 > i_max`

|              |                  |
| ------------ | ---------------- |
| **Type**     | `number or null` |
| **Required** | No               |

##### <a name="components_items_oneOf_i4_length"></a>5.1.5.9. Property `root > components > components items > oneOf > item 4 > length`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

#### <a name="components_items_oneOf_i5"></a>5.1.6. Property `root > components > components items > oneOf > Connector`

|                           |                   |
| ------------------------- | ----------------- |
| **Type**                  | `object`          |
| **Required**              | No                |
| **Additional properties** | Any type allowed  |
| **Defined in**            | #/$defs/Connector |

**Description:** An optionally switchable zero impedance connection between terminals

| Property                                                   | Pattern | Type             | Deprecated | Definition                                                   | Title/Description                              |
| ---------------------------------------------------------- | ------- | ---------------- | ---------- | ------------------------------------------------------------ | ---------------------------------------------- |
| + [id](#components_items_oneOf_i5_id )                     | No      | string           | No         | Same as [id](#components_items_oneOf_i0_id )                 | The component's unique ID                      |
| + [type](#components_items_oneOf_i5_type )                 | No      | const            | No         | -                                                            | -                                              |
| + [cons](#components_items_oneOf_i5_cons )                 | No      | array            | No         | In #/$defs/two_or_more_connections                           | A list of connections with at least 2 elements |
| - [user_data](#components_items_oneOf_i5_user_data )       | No      | object           | No         | Same as [user_data](#user_data )                             | Non-e-json annotations                         |
| - [in_service](#components_items_oneOf_i5_in_service )     | No      | boolean          | No         | Same as [in_service](#components_items_oneOf_i1_in_service ) | If false, the component is out of service      |
| - [i_max](#components_items_oneOf_i5_i_max )               | No      | number or null   | No         | -                                                            | -                                              |
| - [switch_state](#components_items_oneOf_i5_switch_state ) | No      | enum (of string) | No         | -                                                            | -                                              |

##### <a name="components_items_oneOf_i5_id"></a>5.1.6.1. Property `root > components > components items > oneOf > item 5 > id`

|                        |                                     |
| ---------------------- | ----------------------------------- |
| **Type**               | `string`                            |
| **Required**           | Yes                                 |
| **Same definition as** | [id](#components_items_oneOf_i0_id) |

**Description:** The component's unique ID

##### <a name="components_items_oneOf_i5_type"></a>5.1.6.2. Property `root > components > components items > oneOf > item 5 > type`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | Yes     |

Specific value: `"Connector"`

##### <a name="components_items_oneOf_i5_cons"></a>5.1.6.3. Property `root > components > components items > oneOf > item 5 > cons`

|                |                                 |
| -------------- | ------------------------------- |
| **Type**       | `array`                         |
| **Required**   | Yes                             |
| **Defined in** | #/$defs/two_or_more_connections |

**Description:** A list of connections with at least 2 elements

**Example:**

```json
[
    {
        "node": "node_1",
        "phs": [
            "A",
            "C"
        ]
    },
    {
        "node": "node_2",
        "phs": [
            "A",
            "B",
            "C"
        ]
    }
]
```

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | 2                  |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                     | Description                                                                                                                  |
| --------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| [connection](#components_items_oneOf_i5_cons_items) | A list of connections from element terminals. Each connection gives the node ID and phases to which the element is connected |

###### <a name="components_items_oneOf_i5_cons_items"></a>5.1.6.3.1. root > components > components items > oneOf > item 5 > cons > connection

|                           |                                                                               |
| ------------------------- | ----------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                      |
| **Required**              | No                                                                            |
| **Additional properties** | Any type allowed                                                              |
| **Same definition as**    | [components_items_oneOf_i1_cons_items](#components_items_oneOf_i1_cons_items) |

**Description:** A list of connections from element terminals. Each connection gives the node ID and phases to which the element is connected

##### <a name="components_items_oneOf_i5_user_data"></a>5.1.6.4. Property `root > components > components items > oneOf > item 5 > user_data`

|                           |                         |
| ------------------------- | ----------------------- |
| **Type**                  | `object`                |
| **Required**              | No                      |
| **Additional properties** | Any type allowed        |
| **Same definition as**    | [user_data](#user_data) |

**Description:** Non-e-json annotations

##### <a name="components_items_oneOf_i5_in_service"></a>5.1.6.5. Property `root > components > components items > oneOf > item 5 > in_service`

|                        |                                                     |
| ---------------------- | --------------------------------------------------- |
| **Type**               | `boolean`                                           |
| **Required**           | No                                                  |
| **Default**            | `true`                                              |
| **Same definition as** | [in_service](#components_items_oneOf_i1_in_service) |

**Description:** If false, the component is out of service

##### <a name="components_items_oneOf_i5_i_max"></a>5.1.6.6. Property `root > components > components items > oneOf > item 5 > i_max`

|              |                  |
| ------------ | ---------------- |
| **Type**     | `number or null` |
| **Required** | No               |

##### <a name="components_items_oneOf_i5_switch_state"></a>5.1.6.7. Property `root > components > components items > oneOf > item 5 > switch_state`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

Must be one of:
* "closed"
* "open"
* "no_switch"

#### <a name="components_items_oneOf_i6"></a>5.1.7. Property `root > components > components items > oneOf > Transformer`

|                           |                     |
| ------------------------- | ------------------- |
| **Type**                  | `combining`         |
| **Required**              | No                  |
| **Additional properties** | Any type allowed    |
| **Defined in**            | #/$defs/Transformer |

**Description:** A transformer

| Property                                                         | Pattern | Type             | Deprecated | Definition                                                                       | Title/Description                          |
| ---------------------------------------------------------------- | ------- | ---------------- | ---------- | -------------------------------------------------------------------------------- | ------------------------------------------ |
| - [id](#components_items_oneOf_i6_id )                           | No      | string           | No         | Same as [id](#components_items_oneOf_i0_id )                                     | The component's unique ID                  |
| - [type](#components_items_oneOf_i6_type )                       | No      | const            | No         | -                                                                                | -                                          |
| - [cons](#components_items_oneOf_i6_cons )                       | No      | array            | No         | Same as [cons](#components_items_oneOf_i4_cons )                                 | A two element list of connections          |
| - [user_data](#components_items_oneOf_i6_user_data )             | No      | object           | No         | Same as [user_data](#user_data )                                                 | Non-e-json annotations                     |
| - [in_service](#components_items_oneOf_i6_in_service )           | No      | boolean          | No         | Same as [in_service](#components_items_oneOf_i1_in_service )                     | If false, the component is out of service  |
| - [vector_group](#components_items_oneOf_i6_vector_group )       | No      | string           | No         | -                                                                                | -                                          |
| - [n_winding_pairs](#components_items_oneOf_i6_n_winding_pairs ) | No      | number           | No         | Same as [v_base](#components_items_oneOf_i0_v_base )                             | A positive number                          |
| - [is_grounded_p](#components_items_oneOf_i6_is_grounded_p )     | No      | boolean          | No         | -                                                                                | -                                          |
| - [is_grounded_s](#components_items_oneOf_i6_is_grounded_s )     | No      | boolean          | No         | -                                                                                | -                                          |
| - [nom_turns_ratio](#components_items_oneOf_i6_nom_turns_ratio ) | No      | object           | No         | Same as [components_items_oneOf_i0_v_items](#components_items_oneOf_i0_v_items ) | Complex number, stored as [<real>, <imag>] |
| - [v_winding_base](#components_items_oneOf_i6_v_winding_base )   | No      | array            | No         | In #/$defs/two_positive_number_array                                             | An array containing two positive numbers   |
| - [z_p](#components_items_oneOf_i6_z_p )                         | No      | object           | No         | Same as [components_items_oneOf_i0_v_items](#components_items_oneOf_i0_v_items ) | Complex number, stored as [<real>, <imag>] |
| - [z_s](#components_items_oneOf_i6_z_s )                         | No      | object           | No         | Same as [components_items_oneOf_i0_v_items](#components_items_oneOf_i0_v_items ) | Complex number, stored as [<real>, <imag>] |
| - [z0_p](#components_items_oneOf_i6_z0_p )                       | No      | object           | No         | Same as [components_items_oneOf_i0_v_items](#components_items_oneOf_i0_v_items ) | Complex number, stored as [<real>, <imag>] |
| - [z0_s](#components_items_oneOf_i6_z0_s )                       | No      | object           | No         | Same as [components_items_oneOf_i0_v_items](#components_items_oneOf_i0_v_items ) | Complex number, stored as [<real>, <imag>] |
| - [s_max](#components_items_oneOf_i6_s_max )                     | No      | number           | No         | -                                                                                | -                                          |
| - [tap_range](#components_items_oneOf_i6_tap_range )             | No      | array of number  | No         | In #/$defs/two_number_array                                                      | An array containing two numbers            |
| - [tap_factor](#components_items_oneOf_i6_tap_factor )           | No      | number           | No         | -                                                                                | -                                          |
| - [tap_side](#components_items_oneOf_i6_tap_side )               | No      | enum (of string) | No         | -                                                                                | -                                          |
| - [tap_changer](#components_items_oneOf_i6_tap_changer )         | No      | object           | No         | In #/$defs/tap_changer                                                           | Tap changer for a Transformer              |
| - [taps](#components_items_oneOf_i6_taps )                       | No      | array of number  | No         | -                                                                                | -                                          |

| All of(Requirement)                           |
| --------------------------------------------- |
| [item 0](#components_items_oneOf_i6_allOf_i0) |
| [item 1](#components_items_oneOf_i6_allOf_i1) |

##### <a name="components_items_oneOf_i6_allOf_i0"></a>5.1.7.1. Property `root > components > components items > oneOf > item 6 > allOf > item 0`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

###### <a name="autogenerated_heading_2"></a>5.1.7.1.1. The following properties are required
* id
* type
* cons
* vector_group
* nom_turns_ratio
* v_winding_base

##### <a name="components_items_oneOf_i6_allOf_i1"></a>5.1.7.2. Property `root > components > components items > oneOf > item 6 > allOf > item 1`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `combining`      |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Any of(Option)                                         |
| ------------------------------------------------------ |
| [item 0](#components_items_oneOf_i6_allOf_i1_anyOf_i0) |
| [item 1](#components_items_oneOf_i6_allOf_i1_anyOf_i1) |

###### <a name="components_items_oneOf_i6_allOf_i1_anyOf_i0"></a>5.1.7.2.1. Property `root > components > components items > oneOf > item 6 > allOf > item 1 > anyOf > item 0`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

###### <a name="autogenerated_heading_3"></a>5.1.7.2.1.1. The following properties are required
* z_p

###### <a name="components_items_oneOf_i6_allOf_i1_anyOf_i1"></a>5.1.7.2.2. Property `root > components > components items > oneOf > item 6 > allOf > item 1 > anyOf > item 1`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

###### <a name="autogenerated_heading_4"></a>5.1.7.2.2.1. The following properties are required
* z_s

##### <a name="components_items_oneOf_i6_id"></a>5.1.7.3. Property `root > components > components items > oneOf > item 6 > id`

|                        |                                     |
| ---------------------- | ----------------------------------- |
| **Type**               | `string`                            |
| **Required**           | No                                  |
| **Same definition as** | [id](#components_items_oneOf_i0_id) |

**Description:** The component's unique ID

##### <a name="components_items_oneOf_i6_type"></a>5.1.7.4. Property `root > components > components items > oneOf > item 6 > type`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

Specific value: `"Transformer"`

##### <a name="components_items_oneOf_i6_cons"></a>5.1.7.5. Property `root > components > components items > oneOf > item 6 > cons`

|                        |                                         |
| ---------------------- | --------------------------------------- |
| **Type**               | `array`                                 |
| **Required**           | No                                      |
| **Same definition as** | [cons](#components_items_oneOf_i4_cons) |

**Description:** A two element list of connections

##### <a name="components_items_oneOf_i6_user_data"></a>5.1.7.6. Property `root > components > components items > oneOf > item 6 > user_data`

|                           |                         |
| ------------------------- | ----------------------- |
| **Type**                  | `object`                |
| **Required**              | No                      |
| **Additional properties** | Any type allowed        |
| **Same definition as**    | [user_data](#user_data) |

**Description:** Non-e-json annotations

##### <a name="components_items_oneOf_i6_in_service"></a>5.1.7.7. Property `root > components > components items > oneOf > item 6 > in_service`

|                        |                                                     |
| ---------------------- | --------------------------------------------------- |
| **Type**               | `boolean`                                           |
| **Required**           | No                                                  |
| **Default**            | `true`                                              |
| **Same definition as** | [in_service](#components_items_oneOf_i1_in_service) |

**Description:** If false, the component is out of service

##### <a name="components_items_oneOf_i6_vector_group"></a>5.1.7.8. Property `root > components > components items > oneOf > item 6 > vector_group`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

##### <a name="components_items_oneOf_i6_n_winding_pairs"></a>5.1.7.9. Property `root > components > components items > oneOf > item 6 > n_winding_pairs`

|                        |                                             |
| ---------------------- | ------------------------------------------- |
| **Type**               | `number`                                    |
| **Required**           | No                                          |
| **Same definition as** | [v_base](#components_items_oneOf_i0_v_base) |

**Description:** A positive number

##### <a name="components_items_oneOf_i6_is_grounded_p"></a>5.1.7.10. Property `root > components > components items > oneOf > item 6 > is_grounded_p`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

##### <a name="components_items_oneOf_i6_is_grounded_s"></a>5.1.7.11. Property `root > components > components items > oneOf > item 6 > is_grounded_s`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

##### <a name="components_items_oneOf_i6_nom_turns_ratio"></a>5.1.7.12. Property `root > components > components items > oneOf > item 6 > nom_turns_ratio`

|                           |                                                                         |
| ------------------------- | ----------------------------------------------------------------------- |
| **Type**                  | `object`                                                                |
| **Required**              | No                                                                      |
| **Additional properties** | Any type allowed                                                        |
| **Same definition as**    | [components_items_oneOf_i0_v_items](#components_items_oneOf_i0_v_items) |

**Description:** Complex number, stored as [<real>, <imag>]

##### <a name="components_items_oneOf_i6_v_winding_base"></a>5.1.7.13. Property `root > components > components items > oneOf > item 6 > v_winding_base`

|                |                                   |
| -------------- | --------------------------------- |
| **Type**       | `array`                           |
| **Required**   | No                                |
| **Defined in** | #/$defs/two_positive_number_array |

**Description:** An array containing two positive numbers

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | 2                  |
| **Max items**        | 2                  |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                    | Description       |
| ------------------------------------------------------------------ | ----------------- |
| [positive_number](#components_items_oneOf_i6_v_winding_base_items) | A positive number |

###### <a name="components_items_oneOf_i6_v_winding_base_items"></a>5.1.7.13.1. root > components > components items > oneOf > item 6 > v_winding_base > positive_number

|                        |                                             |
| ---------------------- | ------------------------------------------- |
| **Type**               | `number`                                    |
| **Required**           | No                                          |
| **Same definition as** | [v_base](#components_items_oneOf_i0_v_base) |

**Description:** A positive number

##### <a name="components_items_oneOf_i6_z_p"></a>5.1.7.14. Property `root > components > components items > oneOf > item 6 > z_p`

|                           |                                                                         |
| ------------------------- | ----------------------------------------------------------------------- |
| **Type**                  | `object`                                                                |
| **Required**              | No                                                                      |
| **Additional properties** | Any type allowed                                                        |
| **Same definition as**    | [components_items_oneOf_i0_v_items](#components_items_oneOf_i0_v_items) |

**Description:** Complex number, stored as [<real>, <imag>]

##### <a name="components_items_oneOf_i6_z_s"></a>5.1.7.15. Property `root > components > components items > oneOf > item 6 > z_s`

|                           |                                                                         |
| ------------------------- | ----------------------------------------------------------------------- |
| **Type**                  | `object`                                                                |
| **Required**              | No                                                                      |
| **Additional properties** | Any type allowed                                                        |
| **Same definition as**    | [components_items_oneOf_i0_v_items](#components_items_oneOf_i0_v_items) |

**Description:** Complex number, stored as [<real>, <imag>]

##### <a name="components_items_oneOf_i6_z0_p"></a>5.1.7.16. Property `root > components > components items > oneOf > item 6 > z0_p`

|                           |                                                                         |
| ------------------------- | ----------------------------------------------------------------------- |
| **Type**                  | `object`                                                                |
| **Required**              | No                                                                      |
| **Additional properties** | Any type allowed                                                        |
| **Same definition as**    | [components_items_oneOf_i0_v_items](#components_items_oneOf_i0_v_items) |

**Description:** Complex number, stored as [<real>, <imag>]

##### <a name="components_items_oneOf_i6_z0_s"></a>5.1.7.17. Property `root > components > components items > oneOf > item 6 > z0_s`

|                           |                                                                         |
| ------------------------- | ----------------------------------------------------------------------- |
| **Type**                  | `object`                                                                |
| **Required**              | No                                                                      |
| **Additional properties** | Any type allowed                                                        |
| **Same definition as**    | [components_items_oneOf_i0_v_items](#components_items_oneOf_i0_v_items) |

**Description:** Complex number, stored as [<real>, <imag>]

##### <a name="components_items_oneOf_i6_s_max"></a>5.1.7.18. Property `root > components > components items > oneOf > item 6 > s_max`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

##### <a name="components_items_oneOf_i6_tap_range"></a>5.1.7.19. Property `root > components > components items > oneOf > item 6 > tap_range`

|                |                          |
| -------------- | ------------------------ |
| **Type**       | `array of number`        |
| **Required**   | No                       |
| **Defined in** | #/$defs/two_number_array |

**Description:** An array containing two numbers

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | 2                  |
| **Max items**        | 2                  |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                               | Description |
| ------------------------------------------------------------- | ----------- |
| [tap_range items](#components_items_oneOf_i6_tap_range_items) | -           |

###### <a name="components_items_oneOf_i6_tap_range_items"></a>5.1.7.19.1. root > components > components items > oneOf > item 6 > tap_range > tap_range items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

##### <a name="components_items_oneOf_i6_tap_factor"></a>5.1.7.20. Property `root > components > components items > oneOf > item 6 > tap_factor`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

##### <a name="components_items_oneOf_i6_tap_side"></a>5.1.7.21. Property `root > components > components items > oneOf > item 6 > tap_side`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

Must be one of:
* "primary"
* "secondary"

##### <a name="components_items_oneOf_i6_tap_changer"></a>5.1.7.22. Property `root > components > components items > oneOf > item 6 > tap_changer`

|                           |                     |
| ------------------------- | ------------------- |
| **Type**                  | `object`            |
| **Required**              | No                  |
| **Additional properties** | Any type allowed    |
| **Defined in**            | #/$defs/tap_changer |

**Description:** Tap changer for a Transformer

| Property                                                                 | Pattern | Type             | Deprecated | Definition                                                                       | Title/Description                          |
| ------------------------------------------------------------------------ | ------- | ---------------- | ---------- | -------------------------------------------------------------------------------- | ------------------------------------------ |
| + [voltage_range](#components_items_oneOf_i6_tap_changer_voltage_range ) | No      | array            | No         | -                                                                                | -                                          |
| - [indep_taps](#components_items_oneOf_i6_tap_changer_indep_taps )       | No      | boolean          | No         | -                                                                                | -                                          |
| + [winding_side](#components_items_oneOf_i6_tap_changer_winding_side )   | No      | enum (of string) | No         | -                                                                                | -                                          |
| + [winding_idx](#components_items_oneOf_i6_tap_changer_winding_idx )     | No      | Combination      | No         | -                                                                                | -                                          |
| - [ctrl](#components_items_oneOf_i6_tap_changer_ctrl )                   | No      | enum (of string) | No         | -                                                                                | -                                          |
| - [ldc_impedance](#components_items_oneOf_i6_tap_changer_ldc_impedance ) | No      | object           | No         | Same as [components_items_oneOf_i0_v_items](#components_items_oneOf_i0_v_items ) | Complex number, stored as [<real>, <imag>] |
| - [delay_seconds](#components_items_oneOf_i6_tap_changer_delay_seconds ) | No      | number           | No         | -                                                                                | -                                          |

###### <a name="components_items_oneOf_i6_tap_changer_voltage_range"></a>5.1.7.22.1. Property `root > components > components items > oneOf > item 6 > tap_changer > voltage_range`

|              |         |
| ------------ | ------- |
| **Type**     | `array` |
| **Required** | Yes     |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                               | Description       |
| ----------------------------------------------------------------------------- | ----------------- |
| [positive_number](#components_items_oneOf_i6_tap_changer_voltage_range_items) | A positive number |

###### <a name="components_items_oneOf_i6_tap_changer_voltage_range_items"></a>5.1.7.22.1.1. root > components > components items > oneOf > item 6 > tap_changer > voltage_range > positive_number

|                        |                                             |
| ---------------------- | ------------------------------------------- |
| **Type**               | `number`                                    |
| **Required**           | No                                          |
| **Same definition as** | [v_base](#components_items_oneOf_i0_v_base) |

**Description:** A positive number

###### <a name="components_items_oneOf_i6_tap_changer_indep_taps"></a>5.1.7.22.2. Property `root > components > components items > oneOf > item 6 > tap_changer > indep_taps`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `false`   |

###### <a name="components_items_oneOf_i6_tap_changer_winding_side"></a>5.1.7.22.3. Property `root > components > components items > oneOf > item 6 > tap_changer > winding_side`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | Yes                |

Must be one of:
* "primary"
* "secondary"

###### <a name="components_items_oneOf_i6_tap_changer_winding_idx"></a>5.1.7.22.4. Property `root > components > components items > oneOf > item 6 > tap_changer > winding_idx`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `combining`      |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

| Any of(Option)                                                        |
| --------------------------------------------------------------------- |
| [item 0](#components_items_oneOf_i6_tap_changer_winding_idx_anyOf_i0) |
| [item 1](#components_items_oneOf_i6_tap_changer_winding_idx_anyOf_i1) |

###### <a name="components_items_oneOf_i6_tap_changer_winding_idx_anyOf_i0"></a>5.1.7.22.4.1. Property `root > components > components items > oneOf > item 6 > tap_changer > winding_idx > anyOf > item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

###### <a name="components_items_oneOf_i6_tap_changer_winding_idx_anyOf_i1"></a>5.1.7.22.4.2. Property `root > components > components items > oneOf > item 6 > tap_changer > winding_idx > anyOf > item 1`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

Specific value: `"avg"`

###### <a name="components_items_oneOf_i6_tap_changer_ctrl"></a>5.1.7.22.5. Property `root > components > components items > oneOf > item 6 > tap_changer > ctrl`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |
| **Default**  | `"auto"`           |

Must be one of:
* "auto"
* "manual"

###### <a name="components_items_oneOf_i6_tap_changer_ldc_impedance"></a>5.1.7.22.6. Property `root > components > components items > oneOf > item 6 > tap_changer > ldc_impedance`

|                           |                                                                         |
| ------------------------- | ----------------------------------------------------------------------- |
| **Type**                  | `object`                                                                |
| **Required**              | No                                                                      |
| **Additional properties** | Any type allowed                                                        |
| **Same definition as**    | [components_items_oneOf_i0_v_items](#components_items_oneOf_i0_v_items) |

**Description:** Complex number, stored as [<real>, <imag>]

###### <a name="components_items_oneOf_i6_tap_changer_delay_seconds"></a>5.1.7.22.7. Property `root > components > components items > oneOf > item 6 > tap_changer > delay_seconds`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

##### <a name="components_items_oneOf_i6_taps"></a>5.1.7.23. Property `root > components > components items > oneOf > item 6 > taps`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of number` |
| **Required** | No                |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                     | Description |
| --------------------------------------------------- | ----------- |
| [taps items](#components_items_oneOf_i6_taps_items) | -           |

###### <a name="components_items_oneOf_i6_taps_items"></a>5.1.7.23.1. root > components > components items > oneOf > item 6 > taps > taps items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2025-12-19 at 10:27:14 +1100
