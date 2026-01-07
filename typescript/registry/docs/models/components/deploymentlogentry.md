# DeploymentLogEntry

## Example Usage

```typescript
import { DeploymentLogEntry } from "@smithery/registry/models/components";

let value: DeploymentLogEntry = {
  stage: "metadata",
  level: "<value>",
  message: "<value>",
  timestamp: "<value>",
};
```

## Fields

| Field                                                                                    | Type                                                                                     | Required                                                                                 | Description                                                                              |
| ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `stage`                                                                                  | [components.Stage](../../models/components/stage.md)                                     | :heavy_check_mark:                                                                       | N/A                                                                                      |
| `level`                                                                                  | *string*                                                                                 | :heavy_check_mark:                                                                       | N/A                                                                                      |
| `message`                                                                                | *string*                                                                                 | :heavy_check_mark:                                                                       | N/A                                                                                      |
| `timestamp`                                                                              | *string*                                                                                 | :heavy_check_mark:                                                                       | N/A                                                                                      |
| `error`                                                                                  | [components.DeploymentLogEntryError](../../models/components/deploymentlogentryerror.md) | :heavy_minus_sign:                                                                       | N/A                                                                                      |