export const PLANETS = [
  "Mercury",
  "Venus",
  "Earth",
  "Mars",
  "Jupiter",
  "Saturn",
  "Uranus",
  "Neptune",
] as const

export const PLANET_ALIASES: Record<string, string> = {
  terra: "Earth",
  gaia: "Earth",
  soliii: "Earth",
  tellus: "Earth",
  ares: "Mars",
  jove: "Jupiter",
  zeus: "Jupiter",
  cronus: "Saturn",
  ouranos: "Uranus",
  poseidon: "Neptune",
}

export const PLANET_DESCRIPTIONS: Record<string, string> = {
  Mercury: "Mercury is the smallest planet in the Solar System and the closest to the Sun. It has a rocky, cratered surface and extreme temperature swings.",
  Venus: "Venus, similar in size to Earth, is cloaked in thick clouds of sulfuric acid with surface temperatures hot enough to melt lead.",
  Earth: "Earth is the only known planet to support life, with liquid water covering most of its surface and a protective atmosphere.",
  Mars: "Mars, the Red Planet, shows evidence of ancient rivers and volcanoes and is a prime target in the search for past life.",
  Jupiter: "Jupiter is the largest planet, a gas giant with a Great Red Spot—an enormous storm raging for centuries.",
  Saturn: "Saturn is famous for its stunning ring system composed of billions of ice and rock particles orbiting the planet.",
  Uranus: "Uranus is an ice giant rotating on its side, giving rise to extreme seasonal variations during its long orbit.",
  Neptune: "Neptune, the farthest known giant, is a deep-blue world with supersonic winds and a faint ring system.",
}

export const DEFAULT_PLANET = "Earth"

export function normalizePlanet(name?: string): string | null {
  if (!name) {
    return DEFAULT_PLANET
  }

  const key = name.trim().toLowerCase()
  if (!key) {
    return DEFAULT_PLANET
  }

  const clean = key.replace(/[^a-z0-9]/g, '')

  for (const planet of PLANETS) {
    const planetKey = planet.toLowerCase().replace(/[^a-z0-9]/g, '')
    if (clean === planetKey || key === planet.toLowerCase()) {
      return planet
    }
  }

  const alias = PLANET_ALIASES[clean]
  if (alias) {
    return alias
  }

  for (const planet of PLANETS) {
    const planetKey = planet.toLowerCase().replace(/[^a-z0-9]/g, '')
    if (planetKey.startsWith(clean)) {
      return planet
    }
  }

  return null
}

