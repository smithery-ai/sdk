# Client

## Example Usage

```typescript
import { Client } from "@smithery/registry/models/operations";

let value: Client = {
  clientId: "<id>",
};
```

## Fields

| Field                   | Type                    | Required                | Description             |
| ----------------------- | ----------------------- | ----------------------- | ----------------------- |
| `clientId`              | *string*                | :heavy_check_mark:      | N/A                     |
| `clientSecret`          | *string*                | :heavy_minus_sign:      | N/A                     |
| `clientIdIssuedAt`      | *number*                | :heavy_minus_sign:      | N/A                     |
| `clientSecretExpiresAt` | *number*                | :heavy_minus_sign:      | N/A                     |