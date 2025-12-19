# e-JSON schema

**Title:** e-JSON schema

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** JSON schema for the e-JSON data format that represents electrical networks

| Property                           | Pattern | Type             | Deprecated | Definition           | Title/Description |
| ---------------------------------- | ------- | ---------------- | ---------- | -------------------- | ----------------- |
| - [ejson_version](#ejson_version ) | No      | string           | No         | -                    | e-JSON Version    |
| - [id](#id )                       | No      | string           | No         | -                    | Network ID        |
| - [user_data](#user_data )         | No      | object           | No         | In #/$defs/user_data | User Data         |
| + [voltage_type](#voltage_type )   | No      | enum (of string) | No         | -                    | Voltage Type      |
| + [components](#components )       | No      | array            | No         | -                    | Component List    |

## <a name="ejson_version"></a>1. Property `e-JSON schema > ejson_version`

**Title:** e-JSON Version

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

## <a name="id"></a>2. Property `e-JSON schema > id`

**Title:** Network ID

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Network ID

## <a name="user_data"></a>3. Property `e-JSON schema > user_data`

**Title:** User Data

|                           |                   |
| ------------------------- | ----------------- |
| **Type**                  | `object`          |
| **Required**              | No                |
| **Additional properties** | Any type allowed  |
| **Defined in**            | #/$defs/user_data |

**Description:** Non-e-json annotations

## <a name="voltage_type"></a>4. Property `e-JSON schema > voltage_type`

**Title:** Voltage Type

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

## <a name="components"></a>5. Property `e-JSON schema > components`

**Title:** Component List

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

| Each item of this array must be       | Description                                                |
| ------------------------------------- | ---------------------------------------------------------- |
| [e-JSON Component](#components_items) | A component (Node/Infeeder/Gen/Load/Connector/Transformer) |

### <a name="components_items"></a>5.1. e-JSON schema > components > e-JSON Component

**Title:** e-JSON Component

|                           |                   |
| ------------------------- | ----------------- |
| **Type**                  | `combining`       |
| **Required**              | No                |
| **Additional properties** | Any type allowed  |
| **Defined in**            | #/$defs/component |

**Description:** A component (Node/Infeeder/Gen/Load/Connector/Transformer)

| One of(Option)                                      |
| --------------------------------------------------- |
| [Node Component](#components_items_oneOf_i0)        |
| [Infeeder Component](#components_items_oneOf_i1)    |
| [Generator Component](#components_items_oneOf_i2)   |
| [Load Component](#components_items_oneOf_i3)        |
| [Line Component](#components_items_oneOf_i4)        |
| [Connector Component](#components_items_oneOf_i5)   |
| [Transformer Component](#components_items_oneOf_i6) |

#### <a name="components_items_oneOf_i0"></a>5.1.1. Property `e-JSON schema > components > e-JSON Component > oneOf > Node Component`

**Title:** Node Component

|                           |              |
| ------------------------- | ------------ |
| **Type**                  | `object`     |
| **Required**              | No           |
| **Additional properties** | Not allowed  |
| **Defined in**            | #/$defs/Node |

**Description:** A network node (bus)

| Property                                             | Pattern | Type            | Deprecated | Definition                       | Title/Description |
| ---------------------------------------------------- | ------- | --------------- | ---------- | -------------------------------- | ----------------- |
| + [id](#components_items_oneOf_i0_id )               | No      | string          | No         | In #/$defs/component_id          | Component ID      |
| + [type](#components_items_oneOf_i0_type )           | No      | const           | No         | In #/$defs/element_type          | Element Type      |
| + [phs](#components_items_oneOf_i0_phs )             | No      | array of string | No         | In #/$defs/phs                   | List of Phases    |
| - [user_data](#components_items_oneOf_i0_user_data ) | No      | object          | No         | Same as [user_data](#user_data ) | User Data         |
| - [v](#components_items_oneOf_i0_v )                 | No      | array           | No         | In #/$defs/complex_array         | Node Voltage      |
| + [v_base](#components_items_oneOf_i0_v_base )       | No      | number          | No         | In #/$defs/positive_number       | Node Base Voltage |
| - [lat_long](#components_items_oneOf_i0_lat_long )   | No      | object          | No         | -                                | Node Lat/Long     |
| - [xy](#components_items_oneOf_i0_xy )               | No      | object          | No         | -                                | Node Coordinates  |

##### <a name="components_items_oneOf_i0_id"></a>5.1.1.1. Property `e-JSON schema > components > e-JSON Component > oneOf > Node Component > id`

**Title:** Component ID

|                |                      |
| -------------- | -------------------- |
| **Type**       | `string`             |
| **Required**   | Yes                  |
| **Defined in** | #/$defs/component_id |

**Description:** The component's unique ID

##### <a name="components_items_oneOf_i0_type"></a>5.1.1.2. Property `e-JSON schema > components > e-JSON Component > oneOf > Node Component > type`

**Title:** Element Type

|                |                      |
| -------------- | -------------------- |
| **Type**       | `const`              |
| **Required**   | Yes                  |
| **Defined in** | #/$defs/element_type |

**Description:** Element Type

##### <a name="components_items_oneOf_i0_phs"></a>5.1.1.3. Property `e-JSON schema > components > e-JSON Component > oneOf > Node Component > phs`

**Title:** List of Phases

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

###### <a name="components_items_oneOf_i0_phs_items"></a>5.1.1.3.1. e-JSON schema > components > e-JSON Component > oneOf > Node Component > phs > phs items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

##### <a name="components_items_oneOf_i0_user_data"></a>5.1.1.4. Property `e-JSON schema > components > e-JSON Component > oneOf > Node Component > user_data`

**Title:** User Data

|                           |                         |
| ------------------------- | ----------------------- |
| **Type**                  | `object`                |
| **Required**              | No                      |
| **Additional properties** | Any type allowed        |
| **Same definition as**    | [user_data](#user_data) |

**Description:** Non-e-json annotations

##### <a name="components_items_oneOf_i0_v"></a>5.1.1.5. Property `e-JSON schema > components > e-JSON Component > oneOf > Node Component > v`

**Title:** Node Voltage

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

###### <a name="components_items_oneOf_i0_v_items"></a>5.1.1.5.1. e-JSON schema > components > e-JSON Component > oneOf > Node Component > v > complex_number

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

##### <a name="components_items_oneOf_i0_v_base"></a>5.1.1.6. Property `e-JSON schema > components > e-JSON Component > oneOf > Node Component > v_base`

**Title:** Node Base Voltage

|                |                         |
| -------------- | ----------------------- |
| **Type**       | `number`                |
| **Required**   | Yes                     |
| **Defined in** | #/$defs/positive_number |

**Description:** The base voltage in V for the node, line to line or line to ground according to global voltage_type

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

##### <a name="components_items_oneOf_i0_lat_long"></a>5.1.1.7. Property `e-JSON schema > components > e-JSON Component > oneOf > Node Component > lat_long`

**Title:** Node Lat/Long

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** [latitude, longitude]

##### <a name="components_items_oneOf_i0_xy"></a>5.1.1.8. Property `e-JSON schema > components > e-JSON Component > oneOf > Node Component > xy`

**Title:** Node Coordinates

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Coordinates [x, y] e.g. for map datum

#### <a name="components_items_oneOf_i1"></a>5.1.2. Property `e-JSON schema > components > e-JSON Component > oneOf > Infeeder Component`

**Title:** Infeeder Component

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Not allowed      |
| **Defined in**            | #/$defs/Infeeder |

**Description:** Network infeeder with constant voltage

| Property                                               | Pattern | Type           | Deprecated | Definition                                       | Title/Description                     |
| ------------------------------------------------------ | ------- | -------------- | ---------- | ------------------------------------------------ | ------------------------------------- |
| + [id](#components_items_oneOf_i1_id )                 | No      | string         | No         | Same as [id](#components_items_oneOf_i0_id )     | Component ID                          |
| + [type](#components_items_oneOf_i1_type )             | No      | const          | No         | Same as [type](#components_items_oneOf_i0_type ) | Element Type                          |
| + [cons](#components_items_oneOf_i1_cons )             | No      | array          | No         | In #/$defs/one_connection                        | Single Connection                     |
| - [user_data](#components_items_oneOf_i1_user_data )   | No      | object         | No         | Same as [user_data](#user_data )                 | User Data                             |
| - [in_service](#components_items_oneOf_i1_in_service ) | No      | boolean        | No         | In #/$defs/in_service                            | In Service Indicator                  |
| + [v_setpoint](#components_items_oneOf_i1_v_setpoint ) | No      | number         | No         | In #/$defs/positive_number                       | Voltage Setpoint                      |
| - [i_max](#components_items_oneOf_i1_i_max )           | No      | number or null | No         | In #/$defs/i_max                                 | Maximum Current per Phase / Conductor |

##### <a name="components_items_oneOf_i1_id"></a>5.1.2.1. Property `e-JSON schema > components > e-JSON Component > oneOf > Infeeder Component > id`

**Title:** Component ID

|                        |                                     |
| ---------------------- | ----------------------------------- |
| **Type**               | `string`                            |
| **Required**           | Yes                                 |
| **Same definition as** | [id](#components_items_oneOf_i0_id) |

**Description:** The component's unique ID

##### <a name="components_items_oneOf_i1_type"></a>5.1.2.2. Property `e-JSON schema > components > e-JSON Component > oneOf > Infeeder Component > type`

**Title:** Element Type

|                        |                                         |
| ---------------------- | --------------------------------------- |
| **Type**               | `const`                                 |
| **Required**           | Yes                                     |
| **Same definition as** | [type](#components_items_oneOf_i0_type) |

**Description:** Element Type

##### <a name="components_items_oneOf_i1_cons"></a>5.1.2.3. Property `e-JSON schema > components > e-JSON Component > oneOf > Infeeder Component > cons`

**Title:** Single Connection

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
| [Connection](#components_items_oneOf_i1_cons_items) | A list of connections from element terminals. Each connection gives the node ID and phases to which the element is connected |

###### <a name="components_items_oneOf_i1_cons_items"></a>5.1.2.3.1. e-JSON schema > components > e-JSON Component > oneOf > Infeeder Component > cons > Connection

**Title:** Connection

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
| + [phs](#components_items_oneOf_i1_cons_items_phs )   | No      | array of string | No         | Same as [phs](#components_items_oneOf_i0_phs ) | List of Phases    |

###### <a name="components_items_oneOf_i1_cons_items_node"></a>5.1.2.3.1.1. Property `e-JSON schema > components > e-JSON Component > oneOf > Infeeder Component > cons > Connection > node`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="components_items_oneOf_i1_cons_items_phs"></a>5.1.2.3.1.2. Property `e-JSON schema > components > e-JSON Component > oneOf > Infeeder Component > cons > Connection > phs`

**Title:** List of Phases

|                        |                                       |
| ---------------------- | ------------------------------------- |
| **Type**               | `array of string`                     |
| **Required**           | Yes                                   |
| **Same definition as** | [phs](#components_items_oneOf_i0_phs) |

**Description:** A list of phases

##### <a name="components_items_oneOf_i1_user_data"></a>5.1.2.4. Property `e-JSON schema > components > e-JSON Component > oneOf > Infeeder Component > user_data`

**Title:** User Data

|                           |                         |
| ------------------------- | ----------------------- |
| **Type**                  | `object`                |
| **Required**              | No                      |
| **Additional properties** | Any type allowed        |
| **Same definition as**    | [user_data](#user_data) |

**Description:** Non-e-json annotations

##### <a name="components_items_oneOf_i1_in_service"></a>5.1.2.5. Property `e-JSON schema > components > e-JSON Component > oneOf > Infeeder Component > in_service`

**Title:** In Service Indicator

|                |                    |
| -------------- | ------------------ |
| **Type**       | `boolean`          |
| **Required**   | No                 |
| **Default**    | `true`             |
| **Defined in** | #/$defs/in_service |

**Description:** If false, the component is out of service

##### <a name="components_items_oneOf_i1_v_setpoint"></a>5.1.2.6. Property `e-JSON schema > components > e-JSON Component > oneOf > Infeeder Component > v_setpoint`

**Title:** Voltage Setpoint

|                |                         |
| -------------- | ----------------------- |
| **Type**       | `number`                |
| **Required**   | Yes                     |
| **Defined in** | #/$defs/positive_number |

**Description:** Voltage magnitude setpoint in V, line to line or line to ground according to global voltage_type

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

##### <a name="components_items_oneOf_i1_i_max"></a>5.1.2.7. Property `e-JSON schema > components > e-JSON Component > oneOf > Infeeder Component > i_max`

**Title:** Maximum Current per Phase / Conductor

|                |                  |
| -------------- | ---------------- |
| **Type**       | `number or null` |
| **Required**   | No               |
| **Defined in** | #/$defs/i_max    |

**Description:** maximum current per phase or conductor, in A

#### <a name="components_items_oneOf_i2"></a>5.1.3. Property `e-JSON schema > components > e-JSON Component > oneOf > Generator Component`

**Title:** Generator Component

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |
| **Defined in**            | #/$defs/Gen      |

**Description:** A generator, with optional voltage control

| Property                                                     | Pattern | Type             | Deprecated | Definition                                                   | Title/Description         |
| ------------------------------------------------------------ | ------- | ---------------- | ---------- | ------------------------------------------------------------ | ------------------------- |
| + [id](#components_items_oneOf_i2_id )                       | No      | string           | No         | Same as [id](#components_items_oneOf_i0_id )                 | Component ID              |
| + [type](#components_items_oneOf_i2_type )                   | No      | const            | No         | Same as [type](#components_items_oneOf_i0_type )             | Element Type              |
| + [cons](#components_items_oneOf_i2_cons )                   | No      | array            | No         | Same as [cons](#components_items_oneOf_i1_cons )             | Single Connection         |
| - [user_data](#components_items_oneOf_i2_user_data )         | No      | object           | No         | Same as [user_data](#user_data )                             | User Data                 |
| - [in_service](#components_items_oneOf_i2_in_service )       | No      | boolean          | No         | Same as [in_service](#components_items_oneOf_i1_in_service ) | In Service Indicator      |
| + [wiring](#components_items_oneOf_i2_wiring )               | No      | enum (of string) | No         | In #/$defs/wiring                                            | Element Wiring            |
| - [p_min](#components_items_oneOf_i2_p_min )                 | No      | number           | No         | -                                                            | Minimum Real Power        |
| - [p_max](#components_items_oneOf_i2_p_max )                 | No      | number           | No         | -                                                            | Maximum Real Power        |
| - [q_min](#components_items_oneOf_i2_q_min )                 | No      | number           | No         | -                                                            | Minimum Reactive Power    |
| - [q_max](#components_items_oneOf_i2_q_max )                 | No      | number           | No         | -                                                            | Maximum Reactive Power    |
| - [cost](#components_items_oneOf_i2_cost )                   | No      | number           | No         | -                                                            | Cost per Wh               |
| - [fixed_voltage](#components_items_oneOf_i2_fixed_voltage ) | No      | boolean          | No         | -                                                            | Voltage Control           |
| - [v_setpoint](#components_items_oneOf_i2_v_setpoint )       | No      | number           | No         | -                                                            | Voltage Setpoint          |
| - [is_reference](#components_items_oneOf_i2_is_reference )   | No      | boolean          | No         | -                                                            | Angle Reference Indicator |

##### <a name="components_items_oneOf_i2_id"></a>5.1.3.1. Property `e-JSON schema > components > e-JSON Component > oneOf > Generator Component > id`

**Title:** Component ID

|                        |                                     |
| ---------------------- | ----------------------------------- |
| **Type**               | `string`                            |
| **Required**           | Yes                                 |
| **Same definition as** | [id](#components_items_oneOf_i0_id) |

**Description:** The component's unique ID

##### <a name="components_items_oneOf_i2_type"></a>5.1.3.2. Property `e-JSON schema > components > e-JSON Component > oneOf > Generator Component > type`

**Title:** Element Type

|                        |                                         |
| ---------------------- | --------------------------------------- |
| **Type**               | `const`                                 |
| **Required**           | Yes                                     |
| **Same definition as** | [type](#components_items_oneOf_i0_type) |

**Description:** Element Type

##### <a name="components_items_oneOf_i2_cons"></a>5.1.3.3. Property `e-JSON schema > components > e-JSON Component > oneOf > Generator Component > cons`

**Title:** Single Connection

|                        |                                         |
| ---------------------- | --------------------------------------- |
| **Type**               | `array`                                 |
| **Required**           | Yes                                     |
| **Same definition as** | [cons](#components_items_oneOf_i1_cons) |

**Description:** A one element list of connections

##### <a name="components_items_oneOf_i2_user_data"></a>5.1.3.4. Property `e-JSON schema > components > e-JSON Component > oneOf > Generator Component > user_data`

**Title:** User Data

|                           |                         |
| ------------------------- | ----------------------- |
| **Type**                  | `object`                |
| **Required**              | No                      |
| **Additional properties** | Any type allowed        |
| **Same definition as**    | [user_data](#user_data) |

**Description:** Non-e-json annotations

##### <a name="components_items_oneOf_i2_in_service"></a>5.1.3.5. Property `e-JSON schema > components > e-JSON Component > oneOf > Generator Component > in_service`

**Title:** In Service Indicator

|                        |                                                     |
| ---------------------- | --------------------------------------------------- |
| **Type**               | `boolean`                                           |
| **Required**           | No                                                  |
| **Default**            | `true`                                              |
| **Same definition as** | [in_service](#components_items_oneOf_i1_in_service) |

**Description:** If false, the component is out of service

##### <a name="components_items_oneOf_i2_wiring"></a>5.1.3.6. Property `e-JSON schema > components > e-JSON Component > oneOf > Generator Component > wiring`

**Title:** Element Wiring

|                |                    |
| -------------- | ------------------ |
| **Type**       | `enum (of string)` |
| **Required**   | Yes                |
| **Defined in** | #/$defs/wiring     |

**Description:** Specification of load or transformer wiring; delta (LL) or wye (LG)

Must be one of:
* "delta"
* "wye"

##### <a name="components_items_oneOf_i2_p_min"></a>5.1.3.7. Property `e-JSON schema > components > e-JSON Component > oneOf > Generator Component > p_min`

**Title:** Minimum Real Power

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

**Description:** Minimum real power injection in W, (generation convention). 

##### <a name="components_items_oneOf_i2_p_max"></a>5.1.3.8. Property `e-JSON schema > components > e-JSON Component > oneOf > Generator Component > p_max`

**Title:** Maximum Real Power

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0`      |

**Description:** Maximum real power injection in W, (generation convention).

##### <a name="components_items_oneOf_i2_q_min"></a>5.1.3.9. Property `e-JSON schema > components > e-JSON Component > oneOf > Generator Component > q_min`

**Title:** Minimum Reactive Power

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

**Description:** Minimum reactive power injection in VA (generation convention). 

##### <a name="components_items_oneOf_i2_q_max"></a>5.1.3.10. Property `e-JSON schema > components > e-JSON Component > oneOf > Generator Component > q_max`

**Title:** Maximum Reactive Power

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0`      |

**Description:** Maximum reactive power injection in VA (generation convention).

##### <a name="components_items_oneOf_i2_cost"></a>5.1.3.11. Property `e-JSON schema > components > e-JSON Component > oneOf > Generator Component > cost`

**Title:** Cost per Wh

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0`      |

**Description:** Cost, in (cost unit) per Wh

##### <a name="components_items_oneOf_i2_fixed_voltage"></a>5.1.3.12. Property `e-JSON schema > components > e-JSON Component > oneOf > Generator Component > fixed_voltage`

**Title:** Voltage Control

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `false`   |

**Description:** If true, the voltage magnitude is maintained at the setpoint.

##### <a name="components_items_oneOf_i2_v_setpoint"></a>5.1.3.13. Property `e-JSON schema > components > e-JSON Component > oneOf > Generator Component > v_setpoint`

**Title:** Voltage Setpoint

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

**Description:** Voltage magnitude setpoint in V, line to line or line to ground according to global voltage_type

##### <a name="components_items_oneOf_i2_is_reference"></a>5.1.3.14. Property `e-JSON schema > components > e-JSON Component > oneOf > Generator Component > is_reference`

**Title:** Angle Reference Indicator

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `false`   |

**Description:** If true, the voltage angle is referenced to zero.

#### <a name="components_items_oneOf_i3"></a>5.1.4. Property `e-JSON schema > components > e-JSON Component > oneOf > Load Component`

**Title:** Load Component

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |
| **Defined in**            | #/$defs/Load     |

**Description:** A load

| Property                                             | Pattern | Type             | Deprecated | Definition                                           | Title/Description                         |
| ---------------------------------------------------- | ------- | ---------------- | ---------- | ---------------------------------------------------- | ----------------------------------------- |
| + [id](#components_items_oneOf_i3_id )               | No      | string           | No         | Same as [id](#components_items_oneOf_i0_id )         | Component ID                              |
| + [type](#components_items_oneOf_i3_type )           | No      | const            | No         | Same as [type](#components_items_oneOf_i0_type )     | Element Type                              |
| + [cons](#components_items_oneOf_i3_cons )           | No      | array            | No         | Same as [cons](#components_items_oneOf_i1_cons )     | Single Connection                         |
| - [user_data](#components_items_oneOf_i3_user_data ) | No      | object           | No         | Same as [user_data](#user_data )                     | User Data                                 |
| - [wiring](#components_items_oneOf_i3_wiring )       | No      | enum (of string) | No         | Same as [wiring](#components_items_oneOf_i2_wiring ) | Element Wiring                            |
| - [s](#components_items_oneOf_i3_s )                 | No      | array            | No         | -                                                    | Load Nominal or Present Power Consumption |

##### <a name="components_items_oneOf_i3_id"></a>5.1.4.1. Property `e-JSON schema > components > e-JSON Component > oneOf > Load Component > id`

**Title:** Component ID

|                        |                                     |
| ---------------------- | ----------------------------------- |
| **Type**               | `string`                            |
| **Required**           | Yes                                 |
| **Same definition as** | [id](#components_items_oneOf_i0_id) |

**Description:** The component's unique ID

##### <a name="components_items_oneOf_i3_type"></a>5.1.4.2. Property `e-JSON schema > components > e-JSON Component > oneOf > Load Component > type`

**Title:** Element Type

|                        |                                         |
| ---------------------- | --------------------------------------- |
| **Type**               | `const`                                 |
| **Required**           | Yes                                     |
| **Same definition as** | [type](#components_items_oneOf_i0_type) |

**Description:** Element Type

##### <a name="components_items_oneOf_i3_cons"></a>5.1.4.3. Property `e-JSON schema > components > e-JSON Component > oneOf > Load Component > cons`

**Title:** Single Connection

|                        |                                         |
| ---------------------- | --------------------------------------- |
| **Type**               | `array`                                 |
| **Required**           | Yes                                     |
| **Same definition as** | [cons](#components_items_oneOf_i1_cons) |

**Description:** A one element list of connections

##### <a name="components_items_oneOf_i3_user_data"></a>5.1.4.4. Property `e-JSON schema > components > e-JSON Component > oneOf > Load Component > user_data`

**Title:** User Data

|                           |                         |
| ------------------------- | ----------------------- |
| **Type**                  | `object`                |
| **Required**              | No                      |
| **Additional properties** | Any type allowed        |
| **Same definition as**    | [user_data](#user_data) |

**Description:** Non-e-json annotations

##### <a name="components_items_oneOf_i3_wiring"></a>5.1.4.5. Property `e-JSON schema > components > e-JSON Component > oneOf > Load Component > wiring`

**Title:** Element Wiring

|                        |                                             |
| ---------------------- | ------------------------------------------- |
| **Type**               | `enum (of string)`                          |
| **Required**           | No                                          |
| **Same definition as** | [wiring](#components_items_oneOf_i2_wiring) |

**Description:** Specification of load or transformer wiring; delta (LL) or wye (LG)

##### <a name="components_items_oneOf_i3_s"></a>5.1.4.6. Property `e-JSON schema > components > e-JSON Component > oneOf > Load Component > s`

**Title:** Load Nominal or Present Power Consumption

|              |         |
| ------------ | ------- |
| **Type**     | `array` |
| **Required** | No      |

**Description:** Complex power consumption, can represent present or nominal consumption

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

###### <a name="components_items_oneOf_i3_s_items"></a>5.1.4.6.1. e-JSON schema > components > e-JSON Component > oneOf > Load Component > s > complex_number

|                           |                                                                         |
| ------------------------- | ----------------------------------------------------------------------- |
| **Type**                  | `object`                                                                |
| **Required**              | No                                                                      |
| **Additional properties** | Any type allowed                                                        |
| **Same definition as**    | [components_items_oneOf_i0_v_items](#components_items_oneOf_i0_v_items) |

**Description:** Complex number, stored as [<real>, <imag>]

#### <a name="components_items_oneOf_i4"></a>5.1.5. Property `e-JSON schema > components > e-JSON Component > oneOf > Line Component`

**Title:** Line Component

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `combining`      |
| **Required**              | No               |
| **Additional properties** | Any type allowed |
| **Defined in**            | #/$defs/Line     |

**Description:** A line

| Property                                               | Pattern | Type           | Deprecated | Definition                                                   | Title/Description                     |
| ------------------------------------------------------ | ------- | -------------- | ---------- | ------------------------------------------------------------ | ------------------------------------- |
| + [id](#components_items_oneOf_i4_id )                 | No      | string         | No         | Same as [id](#components_items_oneOf_i0_id )                 | Component ID                          |
| + [type](#components_items_oneOf_i4_type )             | No      | const          | No         | Same as [type](#components_items_oneOf_i0_type )             | Element Type                          |
| + [cons](#components_items_oneOf_i4_cons )             | No      | array          | No         | In #/$defs/two_connections                                   | Two Connections                       |
| - [user_data](#components_items_oneOf_i4_user_data )   | No      | object         | No         | Same as [user_data](#user_data )                             | User Data                             |
| - [in_service](#components_items_oneOf_i4_in_service ) | No      | boolean        | No         | Same as [in_service](#components_items_oneOf_i1_in_service ) | In Service Indicator                  |
| - [i_max](#components_items_oneOf_i4_i_max )           | No      | number or null | No         | Same as [i_max](#components_items_oneOf_i1_i_max )           | Maximum Current per Phase / Conductor |
| + [length](#components_items_oneOf_i4_length )         | No      | number         | No         | -                                                            | Line length                           |

| One of(Option)                                                                                 |
| ---------------------------------------------------------------------------------------------- |
| [Line Impedance per Length as Sequence Components](#components_items_oneOf_i4_oneOf_i0)        |
| [Line Impedance per length unit as Bus Admittance Matrix](#components_items_oneOf_i4_oneOf_i1) |

##### <a name="components_items_oneOf_i4_oneOf_i0"></a>5.1.5.1. Property `e-JSON schema > components > e-JSON Component > oneOf > Line Component > oneOf > Line Impedance per Length as Sequence Components`

**Title:** Line Impedance per Length as Sequence Components

|                           |                             |
| ------------------------- | --------------------------- |
| **Type**                  | `object`                    |
| **Required**              | No                          |
| **Additional properties** | Any type allowed            |
| **Defined in**            | #/$defs/line_impedance_z_z0 |

**Description:** Line impedance as positive and zero sequence Ohms per length unit. Negative sequence is assumed to be same as positive

| Property                                              | Pattern | Type   | Deprecated | Definition                                                                       | Title/Description                          |
| ----------------------------------------------------- | ------- | ------ | ---------- | -------------------------------------------------------------------------------- | ------------------------------------------ |
| + [z](#components_items_oneOf_i4_oneOf_i0_z )         | No      | object | No         | Same as [components_items_oneOf_i0_v_items](#components_items_oneOf_i0_v_items ) | Complex number, stored as [<real>, <imag>] |
| + [z0](#components_items_oneOf_i4_oneOf_i0_z0 )       | No      | object | No         | Same as [components_items_oneOf_i0_v_items](#components_items_oneOf_i0_v_items ) | Complex number, stored as [<real>, <imag>] |
| - [b_chg](#components_items_oneOf_i4_oneOf_i0_b_chg ) | No      | number | No         | -                                                                                | -                                          |

###### <a name="components_items_oneOf_i4_oneOf_i0_z"></a>5.1.5.1.1. Property `e-JSON schema > components > e-JSON Component > oneOf > Line Component > oneOf > Line Impedance per Length as Sequence Components > z`

|                           |                                                                         |
| ------------------------- | ----------------------------------------------------------------------- |
| **Type**                  | `object`                                                                |
| **Required**              | Yes                                                                     |
| **Additional properties** | Any type allowed                                                        |
| **Same definition as**    | [components_items_oneOf_i0_v_items](#components_items_oneOf_i0_v_items) |

**Description:** Complex number, stored as [<real>, <imag>]

###### <a name="components_items_oneOf_i4_oneOf_i0_z0"></a>5.1.5.1.2. Property `e-JSON schema > components > e-JSON Component > oneOf > Line Component > oneOf > Line Impedance per Length as Sequence Components > z0`

|                           |                                                                         |
| ------------------------- | ----------------------------------------------------------------------- |
| **Type**                  | `object`                                                                |
| **Required**              | Yes                                                                     |
| **Additional properties** | Any type allowed                                                        |
| **Same definition as**    | [components_items_oneOf_i0_v_items](#components_items_oneOf_i0_v_items) |

**Description:** Complex number, stored as [<real>, <imag>]

###### <a name="components_items_oneOf_i4_oneOf_i0_b_chg"></a>5.1.5.1.3. Property `e-JSON schema > components > e-JSON Component > oneOf > Line Component > oneOf > Line Impedance per Length as Sequence Components > b_chg`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

##### <a name="components_items_oneOf_i4_oneOf_i1"></a>5.1.5.2. Property `e-JSON schema > components > e-JSON Component > oneOf > Line Component > oneOf > Line Impedance per length unit as Bus Admittance Matrix`

**Title:** Line Impedance per length unit as Bus Admittance Matrix

|                           |                              |
| ------------------------- | ---------------------------- |
| **Type**                  | `object`                     |
| **Required**              | No                           |
| **Additional properties** | Any type allowed             |
| **Defined in**            | #/$defs/line_impedance_y_bus |

**Description:** Line impedance expressed as a bus/nodal admittance matrix, in Ohms per length unit

| Property                                              | Pattern | Type  | Deprecated | Definition                | Title/Description           |
| ----------------------------------------------------- | ------- | ----- | ---------- | ------------------------- | --------------------------- |
| + [y_bus](#components_items_oneOf_i4_oneOf_i1_y_bus ) | No      | array | No         | In #/$defs/complex_matrix | A matrix of complex numbers |

###### <a name="components_items_oneOf_i4_oneOf_i1_y_bus"></a>5.1.5.2.1. Property `e-JSON schema > components > e-JSON Component > oneOf > Line Component > oneOf > Line Impedance per length unit as Bus Admittance Matrix > y_bus`

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

###### <a name="components_items_oneOf_i4_oneOf_i1_y_bus_items"></a>5.1.5.2.1.1. e-JSON schema > components > e-JSON Component > oneOf > Line Component > oneOf > Line Impedance per length unit as Bus Admittance Matrix > y_bus > complex_array

|                        |                                   |
| ---------------------- | --------------------------------- |
| **Type**               | `array`                           |
| **Required**           | No                                |
| **Same definition as** | [v](#components_items_oneOf_i0_v) |

**Description:** An array of complex numbers

##### <a name="components_items_oneOf_i4_id"></a>5.1.5.3. Property `e-JSON schema > components > e-JSON Component > oneOf > Line Component > id`

**Title:** Component ID

|                        |                                     |
| ---------------------- | ----------------------------------- |
| **Type**               | `string`                            |
| **Required**           | Yes                                 |
| **Same definition as** | [id](#components_items_oneOf_i0_id) |

**Description:** The component's unique ID

##### <a name="components_items_oneOf_i4_type"></a>5.1.5.4. Property `e-JSON schema > components > e-JSON Component > oneOf > Line Component > type`

**Title:** Element Type

|                        |                                         |
| ---------------------- | --------------------------------------- |
| **Type**               | `const`                                 |
| **Required**           | Yes                                     |
| **Same definition as** | [type](#components_items_oneOf_i0_type) |

**Description:** Element Type

##### <a name="components_items_oneOf_i4_cons"></a>5.1.5.5. Property `e-JSON schema > components > e-JSON Component > oneOf > Line Component > cons`

**Title:** Two Connections

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
| [Connection](#components_items_oneOf_i4_cons_items) | A list of connections from element terminals. Each connection gives the node ID and phases to which the element is connected |

###### <a name="components_items_oneOf_i4_cons_items"></a>5.1.5.5.1. e-JSON schema > components > e-JSON Component > oneOf > Line Component > cons > Connection

**Title:** Connection

|                           |                                                     |
| ------------------------- | --------------------------------------------------- |
| **Type**                  | `object`                                            |
| **Required**              | No                                                  |
| **Additional properties** | Any type allowed                                    |
| **Same definition as**    | [Connection](#components_items_oneOf_i1_cons_items) |

**Description:** A list of connections from element terminals. Each connection gives the node ID and phases to which the element is connected

##### <a name="components_items_oneOf_i4_user_data"></a>5.1.5.6. Property `e-JSON schema > components > e-JSON Component > oneOf > Line Component > user_data`

**Title:** User Data

|                           |                         |
| ------------------------- | ----------------------- |
| **Type**                  | `object`                |
| **Required**              | No                      |
| **Additional properties** | Any type allowed        |
| **Same definition as**    | [user_data](#user_data) |

**Description:** Non-e-json annotations

##### <a name="components_items_oneOf_i4_in_service"></a>5.1.5.7. Property `e-JSON schema > components > e-JSON Component > oneOf > Line Component > in_service`

**Title:** In Service Indicator

|                        |                                                     |
| ---------------------- | --------------------------------------------------- |
| **Type**               | `boolean`                                           |
| **Required**           | No                                                  |
| **Default**            | `true`                                              |
| **Same definition as** | [in_service](#components_items_oneOf_i1_in_service) |

**Description:** If false, the component is out of service

##### <a name="components_items_oneOf_i4_i_max"></a>5.1.5.8. Property `e-JSON schema > components > e-JSON Component > oneOf > Line Component > i_max`

**Title:** Maximum Current per Phase / Conductor

|                        |                                           |
| ---------------------- | ----------------------------------------- |
| **Type**               | `number or null`                          |
| **Required**           | No                                        |
| **Same definition as** | [i_max](#components_items_oneOf_i1_i_max) |

**Description:** maximum current per phase or conductor, in A

##### <a name="components_items_oneOf_i4_length"></a>5.1.5.9. Property `e-JSON schema > components > e-JSON Component > oneOf > Line Component > length`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** Line length

#### <a name="components_items_oneOf_i5"></a>5.1.6. Property `e-JSON schema > components > e-JSON Component > oneOf > Connector Component`

**Title:** Connector Component

|                           |                   |
| ------------------------- | ----------------- |
| **Type**                  | `object`          |
| **Required**              | No                |
| **Additional properties** | Any type allowed  |
| **Defined in**            | #/$defs/Connector |

**Description:** An optionally switchable zero impedance connection between terminals

| Property                                                   | Pattern | Type             | Deprecated | Definition                                                   | Title/Description                     |
| ---------------------------------------------------------- | ------- | ---------------- | ---------- | ------------------------------------------------------------ | ------------------------------------- |
| + [id](#components_items_oneOf_i5_id )                     | No      | string           | No         | Same as [id](#components_items_oneOf_i0_id )                 | Component ID                          |
| + [type](#components_items_oneOf_i5_type )                 | No      | const            | No         | Same as [type](#components_items_oneOf_i0_type )             | Element Type                          |
| + [cons](#components_items_oneOf_i5_cons )                 | No      | array            | No         | In #/$defs/two_or_more_connections                           | Two or More Connections               |
| - [user_data](#components_items_oneOf_i5_user_data )       | No      | object           | No         | Same as [user_data](#user_data )                             | User Data                             |
| - [in_service](#components_items_oneOf_i5_in_service )     | No      | boolean          | No         | Same as [in_service](#components_items_oneOf_i1_in_service ) | In Service Indicator                  |
| - [i_max](#components_items_oneOf_i5_i_max )               | No      | number or null   | No         | Same as [i_max](#components_items_oneOf_i1_i_max )           | Maximum Current per Phase / Conductor |
| - [switch_state](#components_items_oneOf_i5_switch_state ) | No      | enum (of string) | No         | -                                                            | -                                     |

##### <a name="components_items_oneOf_i5_id"></a>5.1.6.1. Property `e-JSON schema > components > e-JSON Component > oneOf > Connector Component > id`

**Title:** Component ID

|                        |                                     |
| ---------------------- | ----------------------------------- |
| **Type**               | `string`                            |
| **Required**           | Yes                                 |
| **Same definition as** | [id](#components_items_oneOf_i0_id) |

**Description:** The component's unique ID

##### <a name="components_items_oneOf_i5_type"></a>5.1.6.2. Property `e-JSON schema > components > e-JSON Component > oneOf > Connector Component > type`

**Title:** Element Type

|                        |                                         |
| ---------------------- | --------------------------------------- |
| **Type**               | `const`                                 |
| **Required**           | Yes                                     |
| **Same definition as** | [type](#components_items_oneOf_i0_type) |

**Description:** Element Type

##### <a name="components_items_oneOf_i5_cons"></a>5.1.6.3. Property `e-JSON schema > components > e-JSON Component > oneOf > Connector Component > cons`

**Title:** Two or More Connections

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
| [Connection](#components_items_oneOf_i5_cons_items) | A list of connections from element terminals. Each connection gives the node ID and phases to which the element is connected |

###### <a name="components_items_oneOf_i5_cons_items"></a>5.1.6.3.1. e-JSON schema > components > e-JSON Component > oneOf > Connector Component > cons > Connection

**Title:** Connection

|                           |                                                     |
| ------------------------- | --------------------------------------------------- |
| **Type**                  | `object`                                            |
| **Required**              | No                                                  |
| **Additional properties** | Any type allowed                                    |
| **Same definition as**    | [Connection](#components_items_oneOf_i1_cons_items) |

**Description:** A list of connections from element terminals. Each connection gives the node ID and phases to which the element is connected

##### <a name="components_items_oneOf_i5_user_data"></a>5.1.6.4. Property `e-JSON schema > components > e-JSON Component > oneOf > Connector Component > user_data`

**Title:** User Data

|                           |                         |
| ------------------------- | ----------------------- |
| **Type**                  | `object`                |
| **Required**              | No                      |
| **Additional properties** | Any type allowed        |
| **Same definition as**    | [user_data](#user_data) |

**Description:** Non-e-json annotations

##### <a name="components_items_oneOf_i5_in_service"></a>5.1.6.5. Property `e-JSON schema > components > e-JSON Component > oneOf > Connector Component > in_service`

**Title:** In Service Indicator

|                        |                                                     |
| ---------------------- | --------------------------------------------------- |
| **Type**               | `boolean`                                           |
| **Required**           | No                                                  |
| **Default**            | `true`                                              |
| **Same definition as** | [in_service](#components_items_oneOf_i1_in_service) |

**Description:** If false, the component is out of service

##### <a name="components_items_oneOf_i5_i_max"></a>5.1.6.6. Property `e-JSON schema > components > e-JSON Component > oneOf > Connector Component > i_max`

**Title:** Maximum Current per Phase / Conductor

|                        |                                           |
| ---------------------- | ----------------------------------------- |
| **Type**               | `number or null`                          |
| **Required**           | No                                        |
| **Same definition as** | [i_max](#components_items_oneOf_i1_i_max) |

**Description:** maximum current per phase or conductor, in A

##### <a name="components_items_oneOf_i5_switch_state"></a>5.1.6.7. Property `e-JSON schema > components > e-JSON Component > oneOf > Connector Component > switch_state`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

Must be one of:
* "closed"
* "open"
* "no_switch"

#### <a name="components_items_oneOf_i6"></a>5.1.7. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component`

**Title:** Transformer Component

|                           |                     |
| ------------------------- | ------------------- |
| **Type**                  | `combining`         |
| **Required**              | No                  |
| **Additional properties** | Any type allowed    |
| **Defined in**            | #/$defs/Transformer |

**Description:** A transformer

| Property                                                         | Pattern | Type             | Deprecated | Definition                                                                       | Title/Description                          |
| ---------------------------------------------------------------- | ------- | ---------------- | ---------- | -------------------------------------------------------------------------------- | ------------------------------------------ |
| - [id](#components_items_oneOf_i6_id )                           | No      | string           | No         | Same as [id](#components_items_oneOf_i0_id )                                     | Component ID                               |
| - [type](#components_items_oneOf_i6_type )                       | No      | const            | No         | Same as [type](#components_items_oneOf_i0_type )                                 | Element Type                               |
| - [cons](#components_items_oneOf_i6_cons )                       | No      | array            | No         | Same as [cons](#components_items_oneOf_i4_cons )                                 | Two Connections                            |
| - [user_data](#components_items_oneOf_i6_user_data )             | No      | object           | No         | Same as [user_data](#user_data )                                                 | User Data                                  |
| - [in_service](#components_items_oneOf_i6_in_service )           | No      | boolean          | No         | Same as [in_service](#components_items_oneOf_i1_in_service )                     | In Service Indicator                       |
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
| - [s_max](#components_items_oneOf_i6_s_max )                     | No      | number           | No         | -                                                                                | Maximum Apparent Power                     |
| - [tap_range](#components_items_oneOf_i6_tap_range )             | No      | array of number  | No         | In #/$defs/two_number_array                                                      | Tap Range                                  |
| - [tap_factor](#components_items_oneOf_i6_tap_factor )           | No      | number           | No         | -                                                                                | Tap Factor                                 |
| - [tap_side](#components_items_oneOf_i6_tap_side )               | No      | enum (of string) | No         | -                                                                                | Tap Side                                   |
| - [tap_changer](#components_items_oneOf_i6_tap_changer )         | No      | object           | No         | In #/$defs/tap_changer                                                           | Tap Changer for Transformer                |
| - [taps](#components_items_oneOf_i6_taps )                       | No      | array of number  | No         | -                                                                                | Tap Settings for Each Winding              |

| All of(Requirement)                           |
| --------------------------------------------- |
| [item 0](#components_items_oneOf_i6_allOf_i0) |
| [item 1](#components_items_oneOf_i6_allOf_i1) |

##### <a name="components_items_oneOf_i6_allOf_i0"></a>5.1.7.1. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > allOf > item 0`

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

##### <a name="components_items_oneOf_i6_allOf_i1"></a>5.1.7.2. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > allOf > item 1`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `combining`      |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Any of(Option)                                         |
| ------------------------------------------------------ |
| [item 0](#components_items_oneOf_i6_allOf_i1_anyOf_i0) |
| [item 1](#components_items_oneOf_i6_allOf_i1_anyOf_i1) |

###### <a name="components_items_oneOf_i6_allOf_i1_anyOf_i0"></a>5.1.7.2.1. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > allOf > item 1 > anyOf > item 0`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

###### <a name="autogenerated_heading_3"></a>5.1.7.2.1.1. The following properties are required
* z_p

###### <a name="components_items_oneOf_i6_allOf_i1_anyOf_i1"></a>5.1.7.2.2. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > allOf > item 1 > anyOf > item 1`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

###### <a name="autogenerated_heading_4"></a>5.1.7.2.2.1. The following properties are required
* z_s

##### <a name="components_items_oneOf_i6_id"></a>5.1.7.3. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > id`

**Title:** Component ID

|                        |                                     |
| ---------------------- | ----------------------------------- |
| **Type**               | `string`                            |
| **Required**           | No                                  |
| **Same definition as** | [id](#components_items_oneOf_i0_id) |

**Description:** The component's unique ID

##### <a name="components_items_oneOf_i6_type"></a>5.1.7.4. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > type`

**Title:** Element Type

|                        |                                         |
| ---------------------- | --------------------------------------- |
| **Type**               | `const`                                 |
| **Required**           | No                                      |
| **Same definition as** | [type](#components_items_oneOf_i0_type) |

**Description:** Element Type

##### <a name="components_items_oneOf_i6_cons"></a>5.1.7.5. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > cons`

**Title:** Two Connections

|                        |                                         |
| ---------------------- | --------------------------------------- |
| **Type**               | `array`                                 |
| **Required**           | No                                      |
| **Same definition as** | [cons](#components_items_oneOf_i4_cons) |

**Description:** A two element list of connections

##### <a name="components_items_oneOf_i6_user_data"></a>5.1.7.6. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > user_data`

**Title:** User Data

|                           |                         |
| ------------------------- | ----------------------- |
| **Type**                  | `object`                |
| **Required**              | No                      |
| **Additional properties** | Any type allowed        |
| **Same definition as**    | [user_data](#user_data) |

**Description:** Non-e-json annotations

##### <a name="components_items_oneOf_i6_in_service"></a>5.1.7.7. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > in_service`

**Title:** In Service Indicator

|                        |                                                     |
| ---------------------- | --------------------------------------------------- |
| **Type**               | `boolean`                                           |
| **Required**           | No                                                  |
| **Default**            | `true`                                              |
| **Same definition as** | [in_service](#components_items_oneOf_i1_in_service) |

**Description:** If false, the component is out of service

##### <a name="components_items_oneOf_i6_vector_group"></a>5.1.7.8. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > vector_group`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

##### <a name="components_items_oneOf_i6_n_winding_pairs"></a>5.1.7.9. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > n_winding_pairs`

|                        |                                             |
| ---------------------- | ------------------------------------------- |
| **Type**               | `number`                                    |
| **Required**           | No                                          |
| **Same definition as** | [v_base](#components_items_oneOf_i0_v_base) |

**Description:** A positive number

##### <a name="components_items_oneOf_i6_is_grounded_p"></a>5.1.7.10. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > is_grounded_p`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

##### <a name="components_items_oneOf_i6_is_grounded_s"></a>5.1.7.11. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > is_grounded_s`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

##### <a name="components_items_oneOf_i6_nom_turns_ratio"></a>5.1.7.12. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > nom_turns_ratio`

|                           |                                                                         |
| ------------------------- | ----------------------------------------------------------------------- |
| **Type**                  | `object`                                                                |
| **Required**              | No                                                                      |
| **Additional properties** | Any type allowed                                                        |
| **Same definition as**    | [components_items_oneOf_i0_v_items](#components_items_oneOf_i0_v_items) |

**Description:** Complex number, stored as [<real>, <imag>]

##### <a name="components_items_oneOf_i6_v_winding_base"></a>5.1.7.13. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > v_winding_base`

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

###### <a name="components_items_oneOf_i6_v_winding_base_items"></a>5.1.7.13.1. e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > v_winding_base > positive_number

|                        |                                             |
| ---------------------- | ------------------------------------------- |
| **Type**               | `number`                                    |
| **Required**           | No                                          |
| **Same definition as** | [v_base](#components_items_oneOf_i0_v_base) |

**Description:** A positive number

##### <a name="components_items_oneOf_i6_z_p"></a>5.1.7.14. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > z_p`

|                           |                                                                         |
| ------------------------- | ----------------------------------------------------------------------- |
| **Type**                  | `object`                                                                |
| **Required**              | No                                                                      |
| **Additional properties** | Any type allowed                                                        |
| **Same definition as**    | [components_items_oneOf_i0_v_items](#components_items_oneOf_i0_v_items) |

**Description:** Complex number, stored as [<real>, <imag>]

##### <a name="components_items_oneOf_i6_z_s"></a>5.1.7.15. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > z_s`

|                           |                                                                         |
| ------------------------- | ----------------------------------------------------------------------- |
| **Type**                  | `object`                                                                |
| **Required**              | No                                                                      |
| **Additional properties** | Any type allowed                                                        |
| **Same definition as**    | [components_items_oneOf_i0_v_items](#components_items_oneOf_i0_v_items) |

**Description:** Complex number, stored as [<real>, <imag>]

##### <a name="components_items_oneOf_i6_z0_p"></a>5.1.7.16. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > z0_p`

|                           |                                                                         |
| ------------------------- | ----------------------------------------------------------------------- |
| **Type**                  | `object`                                                                |
| **Required**              | No                                                                      |
| **Additional properties** | Any type allowed                                                        |
| **Same definition as**    | [components_items_oneOf_i0_v_items](#components_items_oneOf_i0_v_items) |

**Description:** Complex number, stored as [<real>, <imag>]

##### <a name="components_items_oneOf_i6_z0_s"></a>5.1.7.17. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > z0_s`

|                           |                                                                         |
| ------------------------- | ----------------------------------------------------------------------- |
| **Type**                  | `object`                                                                |
| **Required**              | No                                                                      |
| **Additional properties** | Any type allowed                                                        |
| **Same definition as**    | [components_items_oneOf_i0_v_items](#components_items_oneOf_i0_v_items) |

**Description:** Complex number, stored as [<real>, <imag>]

##### <a name="components_items_oneOf_i6_s_max"></a>5.1.7.18. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > s_max`

**Title:** Maximum Apparent Power

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

**Description:** Maximum apparent power, in VA

##### <a name="components_items_oneOf_i6_tap_range"></a>5.1.7.19. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > tap_range`

**Title:** Tap Range

|                |                          |
| -------------- | ------------------------ |
| **Type**       | `array of number`        |
| **Required**   | No                       |
| **Defined in** | #/$defs/two_number_array |

**Description:** Tap range, [min_tap, max_tap]

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

###### <a name="components_items_oneOf_i6_tap_range_items"></a>5.1.7.19.1. e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > tap_range > tap_range items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

##### <a name="components_items_oneOf_i6_tap_factor"></a>5.1.7.20. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > tap_factor`

**Title:** Tap Factor

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

**Description:** tap_factor x nom_turns_ratio is added to the turns ratio every time the tap increases by 1

##### <a name="components_items_oneOf_i6_tap_side"></a>5.1.7.21. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > tap_side`

**Title:** Tap Side

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

**Description:** Are taps on the primary or secondary side?

Must be one of:
* "primary"
* "secondary"

##### <a name="components_items_oneOf_i6_tap_changer"></a>5.1.7.22. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > tap_changer`

**Title:** Tap Changer for Transformer

|                           |                     |
| ------------------------- | ------------------- |
| **Type**                  | `object`            |
| **Required**              | No                  |
| **Additional properties** | Any type allowed    |
| **Defined in**            | #/$defs/tap_changer |

**Description:** Specification of a transformer's tap changer, if present

| Property                                                                 | Pattern | Type             | Deprecated | Definition                                                                       | Title/Description                          |
| ------------------------------------------------------------------------ | ------- | ---------------- | ---------- | -------------------------------------------------------------------------------- | ------------------------------------------ |
| + [voltage_range](#components_items_oneOf_i6_tap_changer_voltage_range ) | No      | array            | No         | -                                                                                | -                                          |
| - [indep_taps](#components_items_oneOf_i6_tap_changer_indep_taps )       | No      | boolean          | No         | -                                                                                | -                                          |
| + [winding_side](#components_items_oneOf_i6_tap_changer_winding_side )   | No      | enum (of string) | No         | -                                                                                | -                                          |
| + [winding_idx](#components_items_oneOf_i6_tap_changer_winding_idx )     | No      | Combination      | No         | -                                                                                | -                                          |
| - [ctrl](#components_items_oneOf_i6_tap_changer_ctrl )                   | No      | enum (of string) | No         | -                                                                                | -                                          |
| - [ldc_impedance](#components_items_oneOf_i6_tap_changer_ldc_impedance ) | No      | object           | No         | Same as [components_items_oneOf_i0_v_items](#components_items_oneOf_i0_v_items ) | Complex number, stored as [<real>, <imag>] |
| - [delay_seconds](#components_items_oneOf_i6_tap_changer_delay_seconds ) | No      | number           | No         | -                                                                                | -                                          |

###### <a name="components_items_oneOf_i6_tap_changer_voltage_range"></a>5.1.7.22.1. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > tap_changer > voltage_range`

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

###### <a name="components_items_oneOf_i6_tap_changer_voltage_range_items"></a>5.1.7.22.1.1. e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > tap_changer > voltage_range > positive_number

|                        |                                             |
| ---------------------- | ------------------------------------------- |
| **Type**               | `number`                                    |
| **Required**           | No                                          |
| **Same definition as** | [v_base](#components_items_oneOf_i0_v_base) |

**Description:** A positive number

###### <a name="components_items_oneOf_i6_tap_changer_indep_taps"></a>5.1.7.22.2. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > tap_changer > indep_taps`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |
| **Default**  | `false`   |

###### <a name="components_items_oneOf_i6_tap_changer_winding_side"></a>5.1.7.22.3. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > tap_changer > winding_side`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | Yes                |

Must be one of:
* "primary"
* "secondary"

###### <a name="components_items_oneOf_i6_tap_changer_winding_idx"></a>5.1.7.22.4. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > tap_changer > winding_idx`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `combining`      |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

| Any of(Option)                                                        |
| --------------------------------------------------------------------- |
| [item 0](#components_items_oneOf_i6_tap_changer_winding_idx_anyOf_i0) |
| [item 1](#components_items_oneOf_i6_tap_changer_winding_idx_anyOf_i1) |

###### <a name="components_items_oneOf_i6_tap_changer_winding_idx_anyOf_i0"></a>5.1.7.22.4.1. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > tap_changer > winding_idx > anyOf > item 0`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

###### <a name="components_items_oneOf_i6_tap_changer_winding_idx_anyOf_i1"></a>5.1.7.22.4.2. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > tap_changer > winding_idx > anyOf > item 1`

|              |         |
| ------------ | ------- |
| **Type**     | `const` |
| **Required** | No      |

Specific value: `"avg"`

###### <a name="components_items_oneOf_i6_tap_changer_ctrl"></a>5.1.7.22.5. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > tap_changer > ctrl`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |
| **Default**  | `"auto"`           |

Must be one of:
* "auto"
* "manual"

###### <a name="components_items_oneOf_i6_tap_changer_ldc_impedance"></a>5.1.7.22.6. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > tap_changer > ldc_impedance`

|                           |                                                                         |
| ------------------------- | ----------------------------------------------------------------------- |
| **Type**                  | `object`                                                                |
| **Required**              | No                                                                      |
| **Additional properties** | Any type allowed                                                        |
| **Same definition as**    | [components_items_oneOf_i0_v_items](#components_items_oneOf_i0_v_items) |

**Description:** Complex number, stored as [<real>, <imag>]

###### <a name="components_items_oneOf_i6_tap_changer_delay_seconds"></a>5.1.7.22.7. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > tap_changer > delay_seconds`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

##### <a name="components_items_oneOf_i6_taps"></a>5.1.7.23. Property `e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > taps`

**Title:** Tap Settings for Each Winding

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of number` |
| **Required** | No                |

**Description:** Tap settings, one per winding pair

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

###### <a name="components_items_oneOf_i6_taps_items"></a>5.1.7.23.1. e-JSON schema > components > e-JSON Component > oneOf > Transformer Component > taps > taps items

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2025-12-19 at 16:18:55 +1100
