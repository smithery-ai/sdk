# ProfileServersResponse

## Example Usage

```typescript
import { ProfileServersResponse } from "@smithery/registry/models/components";

let value: ProfileServersResponse = {
  servers: [
    {
      slug: "<value>",
      displayName: "Reva_VonRueden3",
      mcpUrl: "https://damp-embossing.com",
      description:
        "aha expostulate outside ah finally incidentally terribly however",
    },
  ],
  pagination: {
    page: 8440.76,
    pageSize: 5207.53,
    totalCount: 4062.99,
    totalPages: 8651.16,
  },
};
```

## Fields

| Field                                                                                                      | Type                                                                                                       | Required                                                                                                   | Description                                                                                                |
| ---------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `servers`                                                                                                  | [components.ProfileServersResponseServer](../../models/components/profileserversresponseserver.md)[]       | :heavy_check_mark:                                                                                         | N/A                                                                                                        |
| `pagination`                                                                                               | [components.ProfileServersResponsePagination](../../models/components/profileserversresponsepagination.md) | :heavy_check_mark:                                                                                         | N/A                                                                                                        |