# OauthData

## Example Usage

```typescript
import { OauthData } from "@smithery/registry/models/operations";

let value: OauthData = {
  tokens: {
    accessToken: "<value>",
    tokenType: "<value>",
  },
  client: {
    clientId: "<id>",
  },
};
```

## Fields

| Field                                                  | Type                                                   | Required                                               | Description                                            |
| ------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------------ |
| `tokens`                                               | [operations.Tokens](../../models/operations/tokens.md) | :heavy_check_mark:                                     | N/A                                                    |
| `client`                                               | [operations.Client](../../models/operations/client.md) | :heavy_check_mark:                                     | N/A                                                    |