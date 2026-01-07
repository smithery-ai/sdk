# GetServersResponse

## Example Usage

```typescript
import { GetServersResponse } from "@smithery/registry/models/operations";

let value: GetServersResponse = {
  result: {
    servers: [],
    pagination: {
      currentPage: 1,
      pageSize: 10,
      totalPages: 5,
      totalCount: 42,
    },
  },
};
```

## Fields

| Field                                                                            | Type                                                                             | Required                                                                         | Description                                                                      |
| -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| `result`                                                                         | [components.ServersListResponse](../../models/components/serverslistresponse.md) | :heavy_check_mark:                                                               | N/A                                                                              |