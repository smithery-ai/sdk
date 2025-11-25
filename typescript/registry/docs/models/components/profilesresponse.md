# ProfilesResponse

## Example Usage

```typescript
import { ProfilesResponse } from "@smithery/registry/models/components";

let value: ProfilesResponse = {
  profiles: [],
  pagination: {
    page: 4843.64,
    pageSize: 5344.13,
    totalCount: 8244.1,
    totalPages: 4873.06,
  },
};
```

## Fields

| Field                                                                                          | Type                                                                                           | Required                                                                                       | Description                                                                                    |
| ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `profiles`                                                                                     | [components.Profile](../../models/components/profile.md)[]                                     | :heavy_check_mark:                                                                             | N/A                                                                                            |
| `pagination`                                                                                   | [components.ProfilesResponsePagination](../../models/components/profilesresponsepagination.md) | :heavy_check_mark:                                                                             | N/A                                                                                            |