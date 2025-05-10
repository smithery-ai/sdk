# ServerDetailResponseSecurity

Information about the server's security status

## Example Usage

```typescript
import { ServerDetailResponseSecurity } from "@smithery/registry/models/components";

let value: ServerDetailResponseSecurity = {
  scanPassed: true,
};
```

## Fields

| Field                                         | Type                                          | Required                                      | Description                                   | Example                                       |
| --------------------------------------------- | --------------------------------------------- | --------------------------------------------- | --------------------------------------------- | --------------------------------------------- |
| `scanPassed`                                  | *boolean*                                     | :heavy_minus_sign:                            | Whether the server has passed security checks | true                                          |