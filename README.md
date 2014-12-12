CFGen
=====

#### Config file format

###### JSON

```json
{
    "profiles": {
        "_": {}, /* common declarations */
        "PROFILENAME_1": {}, /* profile specific declarations */
        "PROFILENAME_N": {}
    },
    "templates": {
        "TEMPLATE_FILENAME": {
            "output": "OUTPUT_FILENAME",
            "profiles": {
                "_": {}, /* common template declarations */
                "PROFILENAME_1": {}, /* profile specific template declarations */
                "PROFILENAME_N": {}
            }
        }
    }
}
```

###### YAML

```yaml
profiles:
    _: {}
    PROFILENAME_1: {}
templates:
    TEMPLATE_FILENAME:
        output: OUTPUT_FILENAME
        profiles:
            _: {}
            PROFILENAME_1: {},
            PROFILENAME_N: {}
```


#### Value types

- simple value `name: value`
- environment variable `$(ENV_VAR_NAME)`
- config value `${CONFIG_VALUE}`
