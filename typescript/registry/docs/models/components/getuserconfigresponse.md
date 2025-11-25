# GetUserConfigResponse

## Example Usage

```typescript
import { GetUserConfigResponse } from "@smithery/registry/models/components";

let value: GetUserConfigResponse = {
  config: {
    "apiKey": "xxx",
    "debug": false,
  },
};
```

## Fields

| Field                               | Type                                | Required                            | Description                         | Example                             |
| ----------------------------------- | ----------------------------------- | ----------------------------------- | ----------------------------------- | ----------------------------------- |
| `config`                            | Record<string, *any*>               | :heavy_check_mark:                  | The saved user configuration        | {<br/>"apiKey": "xxx",<br/>"debug": false<br/>} |