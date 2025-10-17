# Coffee Explorer

Discover specialty coffee shops across Singapore with an interactive map-based widget. This example demonstrates a complex widget implementation with:

- Interactive Mapbox GL map integration
- React Router for navigation and deep linking
- Multiple display modes (inline, fullscreen)
- Persistent favorites using widget state
- CSP configuration for external resources
- Responsive sidebar and inspector panels
- Theme support (dark/light)

## Architecture

This example showcases the full capability of the Smithery SDK for building rich, interactive widgets with complex UX patterns.

### Server (`app/server/`)

The MCP server defines three tools using the `widget.resource` helper:

1. **search-coffee-shops** - Filter shops by neighborhood, price, rating, or vibe
2. **get-shop-details** - View detailed information about a specific shop
3. **explore-all-shops** - Browse all coffee shops on the map

The server uses:
- `widget.resource<MapState>()` to create a typed widget resource with CSP configuration
- `widget.response()` to return structured data that the widget can consume
- Metadata to pass shop data and selection state to the client

### Client (`app/web/`)

The React client features:
- **Mapbox GL** for interactive maps centered on Singapore
- **React Router** for URL-based navigation to shop details
- **useWidgetState** hook for persisting favorites across sessions
- **Display mode handling** with responsive layouts for inline/fullscreen
- **Theme support** with automatic dark/light mode styling
- **Shop Inspector** panel that slides in from the right
- **Shop Sidebar** for browsing and filtering

## Features Demonstrated

### 1. External Resource Integration (Mapbox)

The widget integrates Mapbox GL with proper CSP configuration:

```typescript
const coffeeMap = widget.resource<MapState>({
  name: "coffee-map",
  csp: {
    connect_domains: [
      "api.mapbox.com",
      "events.mapbox.com",
      "*.tiles.mapbox.com"
    ],
    resource_domains: [
      "api.mapbox.com",
      "*.tiles.mapbox.com"
    ]
  },
});
```

### 2. Client-Side Routing

Uses React Router for navigation without server roundtrips:

```typescript
// Navigate to shop details
navigate(`/shop/${shop.id}`);

// Parse current route
const match = location.pathname.match(/\/shop\/([^/]+)/);
```

### 3. Persistent State

Favorites are saved using the `useWidgetState` hook:

```typescript
const [widgetState, setWidgetState] = useWidgetState<{ favorites: string[] }>({
  favorites: []
});

// Toggle favorite
setWidgetState(prev => ({
  favorites: prev?.favorites?.includes(shopId)
    ? prev.favorites.filter(id => id !== shopId)
    : [...(prev?.favorites ?? []), shopId]
}));
```

### 4. Display Mode Adaptation

The widget adapts its layout based on display mode:

```typescript
const displayMode = useDisplayMode();
const isFullscreen = displayMode === "fullscreen";

// Show sidebar and inspector only in fullscreen
{isFullscreen && <ShopsSidebar />}
{isFullscreen && selectedShop && <ShopInspector />}
```

### 5. Theme Integration

Respects the host's theme preference:

```typescript
const theme = useTheme();
const isDark = theme === "dark";

// Use theme-aware colors
style={{
  background: isDark ? "#0a0a0a" : "#ffffff",
  color: isDark ? "#e5e5e5" : "#1f2937",
}}
```

### 6. Metadata for Rich Data

The server passes complex data through metadata:

```typescript
return coffeeMap.response({
  structuredData,
  message: `Found ${results.length} coffee shops`,
  meta: {
    shops: results,
    searchParams: params,
  },
});
```

The client accesses this via:

```typescript
const metadata = useToolResponseMetadata<{
  shops?: CoffeeShop[],
  selectedShopId?: string
}>();
const shops = metadata?.shops ?? [];
```

## Setup

### 1. Install Dependencies

```bash
npm install
cd app/web && npm install && cd ../..
```

### 2. Build the Widget

```bash
npm run build:web
```

This compiles the React app to `.smithery/coffee-map.js`.

### 3. Run Development Server

```bash
npm run dev
```

### 4. Use with MCP Client

The server registers with MCP and can be used from any compatible client. Try:

```
Show me coffee shops in Tiong Bahru
```

```
Find cozy coffee spots under $$
```

```
Get details for nylon-coffee-roasters
```

## Data Structure

### CoffeeShop Type

```typescript
interface CoffeeShop {
  id: string;
  name: string;
  coords: [number, number];  // [lng, lat] for Mapbox
  neighborhood: string;
  description: string;
  specialty: string;
  vibe: string[];
  priceRange: "$" | "$$" | "$$$";
  rating: number;
  instagram?: string;
  thumbnail: string;
  openHours: string;
}
```

### MapState Type

```typescript
interface MapState {
  center: [number, number];
  zoom: number;
  markers: Array<[number, number]>;
  favorites: string[];
}
```

## Key Patterns

### 1. Resource Configuration

The `widget.resource` helper encapsulates all widget configuration:

```typescript
const coffeeMap = widget.resource<MapState>({
  name: "coffee-map",           // Resource name and bundle path
  description: "...",            // Widget description
  prefersBorder: false,          // No border in inline mode
  csp: { ... },                  // CSP for external resources
});

// Register with server
coffeeMap.register(server);

// Use in tools
_meta: coffeeMap.toolConfig({
  invoking: "Finding coffee...",
  invoked: "Found shops!",
})

// Return responses
return coffeeMap.response({
  structuredData,
  message,
  meta,
});
```

### 2. Complex State Management

Combine multiple hooks for rich state:

```typescript
const metadata = useToolResponseMetadata();  // Server data
const [widgetState, setWidgetState] = useWidgetState();  // Persistent state
const displayMode = useDisplayMode();  // Host state
const theme = useTheme();  // Host theme
```

### 3. Responsive Layouts

Adapt UI based on display mode and screen size:

```typescript
// Different layouts for inline vs fullscreen
const layout = isFullscreen ? {
  left: "340px",  // Account for sidebar
  right: "16px",
  borderRadius: "16px",
} : {
  inset: 0,
  borderRadius: 0,
};
```

## Extending This Example

### Add New Tools

Add filtering by specialty, rating, or open hours:

```typescript
server.registerTool("find-open-now", ...);
server.registerTool("filter-by-specialty", ...);
```

### Add More Interactions

- Reviews and ratings
- Directions integration
- Photo galleries
- Social sharing
- Recommendations based on favorites

### Enhanced State

Extend the widget state:

```typescript
interface WidgetState {
  favorites: string[];
  visited: string[];
  notes: Record<string, string>;
  lastVisited: string;
}
```

## Technical Notes

### Mapbox Token

This example uses a demo Mapbox token. For production, get your own token from [mapbox.com](https://mapbox.com) and replace it in `coffee-map.tsx`:

```typescript
mapboxgl.accessToken = "YOUR_TOKEN_HERE";
```

### Bundle Size

The built widget is ~500KB including:
- React + React DOM
- React Router
- Mapbox GL JS + CSS

Consider code splitting or lazy loading for larger apps.

### CSP Configuration

The CSP domains must match exactly. Use wildcards carefully:

```typescript
"*.tiles.mapbox.com"  // Matches a1.tiles.mapbox.com, etc.
```

### Performance

For production:
- Enable minification (already configured)
- Use CDN for Mapbox assets
- Implement virtual scrolling for large lists
- Debounce map movements

## License

MIT

