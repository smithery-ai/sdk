# InvocationRequest

## Example Usage

```typescript
import { InvocationRequest } from "@smithery/registry/models/components";

let value: InvocationRequest = {
  method: "POST",
  url: "https://gateway.smithery.ai/@smithery/unicorn",
};
```

## Fields

| Field                                         | Type                                          | Required                                      | Description                                   | Example                                       |
| --------------------------------------------- | --------------------------------------------- | --------------------------------------------- | --------------------------------------------- | --------------------------------------------- |
| `method`                                      | *string*                                      | :heavy_check_mark:                            | N/A                                           | POST                                          |
| `url`                                         | *string*                                      | :heavy_check_mark:                            | N/A                                           | https://gateway.smithery.ai/@smithery/unicorn |