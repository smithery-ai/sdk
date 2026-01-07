# ServersListResponse

## Example Usage

```typescript
import { ServersListResponse } from "@smithery/registry/models/components";

let value: ServersListResponse = {
  servers: [
    {
      qualifiedName: "smithery/hello-world",
      displayName: "Hello World",
      description: "A simple hello world server",
      iconUrl: "https://example.com/icon.png",
      verified: true,
      useCount: 42,
      remote: true,
      isDeployed: true,
      createdAt: "1722390988610",
      homepage: "https://smithery.ai/server/smithery/hello-world",
    },
  ],
  pagination: {
    currentPage: 1,
    pageSize: 10,
    totalPages: 5,
    totalCount: 42,
  },
};
```

## Fields

| Field                                                                  | Type                                                                   | Required                                                               | Description                                                            |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `servers`                                                              | [components.ServerSummary](../../models/components/serversummary.md)[] | :heavy_check_mark:                                                     | N/A                                                                    |
| `pagination`                                                           | [components.Pagination](../../models/components/pagination.md)         | :heavy_check_mark:                                                     | N/A                                                                    |