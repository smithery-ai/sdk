# DeployRequest

## Example Usage

```typescript
import { DeployRequest } from "@smithery/registry/models/components";

let value: DeployRequest = {
  payload: "<value>",
};
```

## Fields

| Field                                              | Type                                               | Required                                           | Description                                        |
| -------------------------------------------------- | -------------------------------------------------- | -------------------------------------------------- | -------------------------------------------------- |
| `payload`                                          | *string*                                           | :heavy_check_mark:                                 | JSON string of DeployPayload                       |
| `module`                                           | *string*                                           | :heavy_minus_sign:                                 | JavaScript module content (for hosted deployments) |
| `sourcemap`                                        | *string*                                           | :heavy_minus_sign:                                 | Source map content                                 |