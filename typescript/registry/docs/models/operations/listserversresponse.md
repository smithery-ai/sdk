# ListServersResponse

## Example Usage

```typescript
import { ListServersResponse } from "@smithery/registry/models/operations";

let value: ListServersResponse = {
  result: {
    servers: [
      {
        qualifiedName: "smithery-ai/fetch",
        displayName: "Fetch",
        description: "A server for fetching web content",
        homepage: "https://smithery.ai/server/smithery-ai/fetch",
        iconUrl: "https://example.com/icon.png",
        verified: true,
        useCount: 12345,
        createdAt: new Date("2023-01-01T12:00:00Z"),
      },
    ],
    pagination: {
      currentPage: 1,
      pageSize: 10,
      totalPages: 5,
      totalCount: 47,
    },
  },
};
```

## Fields

| Field                                                                          | Type                                                                           | Required                                                                       | Description                                                                    |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| `result`                                                                       | [components.ServerListResponse](../../models/components/serverlistresponse.md) | :heavy_check_mark:                                                             | N/A                                                                            |