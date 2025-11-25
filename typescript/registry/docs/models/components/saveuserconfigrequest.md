# SaveUserConfigRequest

## Example Usage

```typescript
import { SaveUserConfigRequest } from "@smithery/registry/models/components";

let value: SaveUserConfigRequest = {
  config: {
    "apiKey": "xxx",
    "debug": false,
  },
};
```

## Fields

| Field                               | Type                                | Required                            | Description                         | Example                             |
| ----------------------------------- | ----------------------------------- | ----------------------------------- | ----------------------------------- | ----------------------------------- |
| `config`                            | Record<string, *any*>               | :heavy_check_mark:                  | The user configuration to save      | {<br/>"apiKey": "xxx",<br/>"debug": false<br/>} |