# Solar System Explorer

An interactive MCP server that provides a 3D visualization of our solar system with CDN-based widget loading.

## Features

- Interactive 3D solar system visualization
- Focus on any planet by name
- Automatic planet name normalization (supports aliases like "Terra" for Earth)
- CDN-based widget loading (no local asset bundling required)
- Rich planet descriptions and information

## Development

```bash
npm install
npm run dev
```

## Usage

The server provides a `focus-solar-planet` tool that accepts:

- `planetName` (optional, default: "Earth"): Name of the planet to focus on
- `autoOrbit` (optional, default: true): Whether to keep camera orbiting

### Examples

Focus on Mars:
```json
{
  "planetName": "Mars"
}
```

Focus on Jupiter without auto-orbit:
```json
{
  "planetName": "Jupiter",
  "autoOrbit": false
}
```

### Supported Planets

- Mercury
- Venus  
- Earth (aliases: terra, gaia, soliii, tellus)
- Mars (alias: ares)
- Jupiter (aliases: jove, zeus)
- Saturn (alias: cronus)
- Uranus (alias: ouranos)
- Neptune (alias: poseidon)

## CDN Widget Architecture

This server demonstrates CDN-based widget loading using the `widget.cdnResource()` helper:

```typescript
const solarWidget = widget.cdnResource<SolarSystemState>({
  name: "solar-system",
  description: "Explore the Solar System...",
  cdnURL: "https://cdn.jsdelivr.net/npm/@smithery/solar-system-widget@latest/dist/solar-system.js",
  cssURLs: "https://cdn.jsdelivr.net/npm/@smithery/solar-system-widget@latest/dist/solar-system.css",
  prefersBorder: false,
})
```

### Benefits of CDN Loading

- No local asset bundling required
- Faster deployments
- Automatic widget updates when CDN package is updated
- Smaller server package size
- Better caching across multiple servers

## Building

```bash
npm run build
```

This will create a production-ready build in the `.smithery` directory.

