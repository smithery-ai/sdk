# ConfigValidationResponse

## Example Usage

```typescript
import { ConfigValidationResponse } from "@smithery/registry/models/components";

let value: ConfigValidationResponse = {
  isComplete: false,
  hasExistingConfig: true,
  missingFields: [
    "exaApiKey",
    "enabledTools",
  ],
  fieldSchemas: {
    "exaApiKey": {
      "type": "string",
      "description": "API key",
    },
  },
};
```

## Fields

| Field                                                           | Type                                                            | Required                                                        | Description                                                     | Example                                                         |
| --------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------- |
| `isComplete`                                                    | *boolean*                                                       | :heavy_check_mark:                                              | N/A                                                             | false                                                           |
| `hasExistingConfig`                                             | *boolean*                                                       | :heavy_check_mark:                                              | N/A                                                             | true                                                            |
| `missingFields`                                                 | *string*[]                                                      | :heavy_check_mark:                                              | N/A                                                             | [<br/>"exaApiKey",<br/>"enabledTools"<br/>]                     |
| `fieldSchemas`                                                  | Record<string, *any*>                                           | :heavy_check_mark:                                              | N/A                                                             | {<br/>"exaApiKey": {<br/>"type": "string",<br/>"description": "API key"<br/>}<br/>} |