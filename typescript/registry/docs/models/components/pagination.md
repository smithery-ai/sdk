# Pagination

## Example Usage

```typescript
import { Pagination } from "@smithery/registry/models/components";

let value: Pagination = {
  currentPage: 1,
  pageSize: 10,
  totalPages: 5,
  totalCount: 47,
};
```

## Fields

| Field                    | Type                     | Required                 | Description              | Example                  |
| ------------------------ | ------------------------ | ------------------------ | ------------------------ | ------------------------ |
| `currentPage`            | *number*                 | :heavy_check_mark:       | Current page number      | 1                        |
| `pageSize`               | *number*                 | :heavy_check_mark:       | Number of items per page | 10                       |
| `totalPages`             | *number*                 | :heavy_check_mark:       | Total number of pages    | 5                        |
| `totalCount`             | *number*                 | :heavy_check_mark:       | Total number of items    | 47                       |