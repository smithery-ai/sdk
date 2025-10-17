import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { widget } from "@smithery/sdk/openai";
import type { MapState, SearchParams } from "../shared/types.js";
import { coffeeShops } from "./data.js";

export default function createServer() {
  const server = new McpServer({
    name: "Coffee Explorer",
    version: "1.0.0",
  });

  const coffeeMap = widget.resource<MapState>({
    name: "coffee-map",
    description: "Discover specialty coffee shops across Singapore",
    prefersBorder: false,
    csp: {
      connect_domains: [
        "https://api.mapbox.com",
        "https://events.mapbox.com",
        "https://*.tiles.mapbox.com"
      ],
      resource_domains: [
        "https://api.mapbox.com",
        "https://*.tiles.mapbox.com",
        "https://unpkg.com"
      ]
    },
    cssURLs: "https://unpkg.com/mapbox-gl@3.1.0/dist/mapbox-gl.css",
  });

  server.registerResource(
    coffeeMap.name,
    coffeeMap.uri,
    {},
    coffeeMap.handler
  );

  server.registerTool(
    "search-coffee-shops",
    {
      title: "Search Coffee Shops",
      description: "Find specialty coffee shops in Singapore with optional filters",
      inputSchema: {
        neighborhood: z.string().optional().describe("Filter by neighborhood (e.g., Tiong Bahru, Haji Lane)"),
        maxPrice: z.enum(["$", "$$", "$$$"]).optional().describe("Maximum price range"),
        minRating: z.number().min(1).max(5).optional().describe("Minimum rating (1-5)"),
        vibe: z.string().optional().describe("Filter by vibe (e.g., Cozy, Minimalist, Japanese)"),
      },
      _meta: coffeeMap.toolConfig({
        invoking: "Finding great coffee spots...",
        invoked: "Found coffee shops!",
      }),
    },
    async (args) => {
      const params = args as SearchParams;
      
      let results = [...coffeeShops];

      if (params.neighborhood) {
        results = results.filter(shop => 
          shop.neighborhood.toLowerCase().includes(params.neighborhood!.toLowerCase())
        );
      }

      if (params.maxPrice) {
        const priceOrder = { "$": 1, "$$": 2, "$$$": 3 };
        results = results.filter(shop => 
          priceOrder[shop.priceRange] <= priceOrder[params.maxPrice!]
        );
      }

      if (params.minRating) {
        results = results.filter(shop => shop.rating >= params.minRating!);
      }

      if (params.vibe) {
        results = results.filter(shop =>
          shop.vibe.some(v => v.toLowerCase().includes(params.vibe!.toLowerCase()))
        );
      }

      const structuredData: MapState = {
        center: results.length > 0 ? results[0].coords : [103.8198, 1.3521],
        zoom: 12,
        markers: results.map(shop => shop.coords),
        favorites: [],
      };

      const summary = results.length > 0
        ? `Found ${results.length} coffee shop${results.length > 1 ? 's' : ''}: ${results.map(s => s.name).join(", ")}`
        : "No coffee shops found matching your criteria";

      return coffeeMap.response({
        structuredData,
        message: summary,
        meta: {
          shops: results,
          searchParams: params,
        },
      });
    }
  );

  server.registerTool(
    "get-shop-details",
    {
      title: "Get Coffee Shop Details",
      description: "View detailed information about a specific coffee shop",
      inputSchema: {
        shopId: z.string().describe("ID of the coffee shop"),
      },
      _meta: coffeeMap.toolConfig({
        invoking: "Getting shop details...",
        invoked: "Here's the shop info!",
      }),
    },
    async (args) => {
      const shop = coffeeShops.find(s => s.id === args.shopId);

      if (!shop) {
        return widget.error(`Coffee shop with ID "${args.shopId}" not found`);
      }

      const structuredData: MapState = {
        center: shop.coords,
        zoom: 15,
        markers: [shop.coords],
        favorites: [],
      };

      return coffeeMap.response({
        structuredData,
        message: `Showing details for ${shop.name} in ${shop.neighborhood}`,
        meta: {
          shops: [shop],
          selectedShopId: shop.id,
        },
      });
    }
  );

  server.registerTool(
    "explore-all-shops",
    {
      title: "Explore All Coffee Shops",
      description: "View all specialty coffee shops in Singapore on an interactive map",
      inputSchema: {},
      _meta: coffeeMap.toolConfig({
        invoking: "Loading Singapore's best coffee...",
        invoked: "Explore away!",
      }),
    },
    async () => {
      const structuredData: MapState = {
        center: [103.8198, 1.3521],
        zoom: 12,
        markers: coffeeShops.map(shop => shop.coords),
        favorites: [],
      };

      return coffeeMap.response({
        structuredData,
        message: `Showing ${coffeeShops.length} specialty coffee shops across Singapore`,
        meta: {
          shops: coffeeShops,
        },
      });
    }
  );

  return server.server;
}

