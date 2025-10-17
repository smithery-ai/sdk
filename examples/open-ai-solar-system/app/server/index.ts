import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js"
import { z } from "zod"
import { widget } from "@smithery/sdk/openai"
import type { SolarSystemState, FocusPlanetArgs } from "./types.js"
import { normalizePlanet, PLANET_DESCRIPTIONS, PLANETS, DEFAULT_PLANET } from "./data.js"

export default function createServer() {
  const server = new McpServer({
    name: "Solar System Explorer",
    version: "1.0.0",
  })

  const solarWidget = widget.resource<SolarSystemState>({
    name: "solar-system",
    description: "Explore the Solar System with an interactive 3D visualization",
    bundleURL: "https://persistent.oaistatic.com/ecosystem-built-assets/solar-system-0038.js",
    cssURLs: "https://persistent.oaistatic.com/ecosystem-built-assets/solar-system-0038.css",
    prefersBorder: false,
    csp: {
      resource_domains: ["https://persistent.oaistatic.com"],
    },
  })

  server.registerResource(
    solarWidget.name,
    solarWidget.uri,
    {},
    solarWidget.handler
  )

  server.registerTool(
    "focus-solar-planet",
    {
      title: "Explore the Solar System",
      description: "Render the solar system widget centered on the requested planet",
      inputSchema: {
        planetName: z
          .string()
          .optional()
          .default(DEFAULT_PLANET)
          .describe("Planet to focus in the widget (case insensitive)"),
        autoOrbit: z
          .boolean()
          .optional()
          .default(true)
          .describe("Whether to keep the camera orbiting if the target planet is missing"),
      },
      _meta: solarWidget.toolConfig({
        invoking: "Charting the solar system",
        invoked: "Solar system ready",
      }),
    },
    async (args) => {
      const { planetName, autoOrbit } = args as FocusPlanetArgs

      const planet = normalizePlanet(planetName)

      if (planet === null) {
        return widget.error(
          `Unknown planet. Provide one of: ${PLANETS.join(", ")}`
        )
      }

      const description = PLANET_DESCRIPTIONS[planet] || ""

      const structuredData: SolarSystemState = {
        planetName: planet,
        planetDescription: description,
        autoOrbit: autoOrbit ?? true,
      }

      return solarWidget.response({
        structuredData,
        message: `Centered the solar system view on ${planet}.`,
      })
    }
  )

  return server.server
}

