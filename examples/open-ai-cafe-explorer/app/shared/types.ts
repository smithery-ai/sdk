export interface CoffeeShop {
  id: string;
  name: string;
  coords: [number, number];
  neighborhood: string;
  description: string;
  specialty: string;
  vibe: string[];
  priceRange: "$" | "$$" | "$$$";
  rating: number;
  openHours: string;
}

export interface SearchParams {
  neighborhood?: string;
  maxPrice?: "$" | "$$" | "$$$";
  minRating?: number;
  vibe?: string;
}

export interface MapState {
  center: [number, number];
  zoom: number;
  markers: Array<[number, number]>;
  favorites: string[];
}

