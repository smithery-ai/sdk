import { useEffect, useRef, useMemo } from "react";
import { MemoryRouter, Routes, Route, useNavigate, useLocation, Outlet } from "react-router-dom";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";
import {
  useTheme,
  useDisplayMode,
  useMaxHeight,
  useToolResponseMetadata,
  useWidgetState,
  useRequestDisplayMode,
  ErrorBoundary,
} from "@smithery/sdk/react";
import type { CoffeeShop } from "../../shared/types";

mapboxgl.accessToken = "pk.eyJ1IjoiZXJpY25pbmciLCJhIjoiY21icXlubWM1MDRiczJvb2xwM2p0amNyayJ9.n-3O6JI5nOp_Lw96ZO5vJQ";

function fitMapToMarkers(map: mapboxgl.Map, coords: [number, number][]) {
  if (!map || !coords.length) return;
  if (coords.length === 1) {
    map.flyTo({ center: coords[0], zoom: 14 });
    return;
  }
  const bounds = coords.reduce(
    (b, c) => b.extend(c),
    new mapboxgl.LngLatBounds(coords[0], coords[0])
  );
  map.fitBounds(bounds, { padding: 80, animate: true, duration: 1000 });
}

function MapContainer() {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapObj = useRef<mapboxgl.Map | null>(null);
  const markerObjs = useRef<mapboxgl.Marker[]>([]);
  
  const theme = useTheme();
  const displayMode = useDisplayMode();
  const maxHeight = useMaxHeight();
  const metadata = useToolResponseMetadata<{ shops?: CoffeeShop[], selectedShopId?: string }>();
  const [widgetState, setWidgetState] = useWidgetState<{ favorites: string[] }>({ favorites: [] });
  const requestDisplayMode = useRequestDisplayMode();
  
  const navigate = useNavigate();
  const location = useLocation();
  
  const shops = metadata?.shops ?? [];
  const selectedId = useMemo(() => {
    const match = location.pathname.match(/\/shop\/([^/]+)/);
    return match?.[1] ?? null;
  }, [location.pathname]);
  
  const selectedShop = shops.find(s => s.id === selectedId) ?? null;
  const markerCoords = shops.map(s => s.coords);
  
  const isFullscreen = displayMode === "fullscreen";
  const isDark = theme === "dark";

  useEffect(() => {
    if (mapObj.current || !mapRef.current) return;
    
    const center: [number, number] = markerCoords.length > 0 ? markerCoords[0] : [103.8198, 1.3521];
    
    mapObj.current = new mapboxgl.Map({
      container: mapRef.current,
      style: isDark ? "mapbox://styles/mapbox/streets-v12" : "mapbox://styles/mapbox/streets-v12",
      center,
      zoom: 12,
      attributionControl: false,
    });

    mapObj.current.addControl(new mapboxgl.NavigationControl(), "top-right");

    requestAnimationFrame(() => {
      if (mapObj.current) {
        mapObj.current.resize();
      }
    });

    const handleResize = () => {
      mapObj.current?.resize();
    };
    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
      mapObj.current?.remove();
      mapObj.current = null;
    };
  }, []);

  useEffect(() => {
    if (!mapObj.current) return;
    
    markerObjs.current.forEach(m => m.remove());
    markerObjs.current = [];

    shops.forEach(shop => {
      const marker = new mapboxgl.Marker({ color: "#dc2626" })
        .setLngLat(shop.coords)
        .addTo(mapObj.current!);
      
      const el = marker.getElement();
      el.style.cursor = "pointer";
      el.addEventListener("click", () => {
        navigate(`/shop/${shop.id}`);
      });
      
      markerObjs.current.push(marker);
    });
    
    if (shops.length > 0 && !selectedId) {
      setTimeout(() => {
        fitMapToMarkers(mapObj.current!, markerCoords);
      }, 100);
    }
  }, [shops, navigate, markerCoords, selectedId]);

  useEffect(() => {
    if (!mapObj.current || !selectedShop) return;
    mapObj.current.flyTo({
      center: selectedShop.coords,
      zoom: 14,
      speed: 0.8,
      curve: 1,
      essential: true,
    });
  }, [selectedShop]);

  useEffect(() => {
    if (!mapObj.current) return;
    mapObj.current.resize();
  }, [maxHeight, displayMode]);

  const toggleFavorite = (shopId: string) => {
    setWidgetState(prev => ({
      favorites: prev?.favorites?.includes(shopId)
        ? prev.favorites.filter(id => id !== shopId)
        : [...(prev?.favorites ?? []), shopId],
    }));
  };

  return (
    <div
      style={{
        position: "relative",
        width: "100%",
        height: isFullscreen ? (maxHeight ?? "100vh") : "480px",
        maxHeight: maxHeight ?? "100vh",
        backgroundColor: isDark ? "#0a0a0a" : "#ffffff",
        color: isDark ? "#e5e5e5" : "#1f2937",
        overflow: "hidden",
        borderRadius: isFullscreen ? "0" : "16px",
        border: isFullscreen ? "none" : `1px solid ${isDark ? "rgba(255,255,255,0.1)" : "rgba(0,0,0,0.1)"}`,
      }}
    >
      <Outlet />
      
      {!isFullscreen && (
        <button
          onClick={() => requestDisplayMode("fullscreen")}
          style={{
            position: "absolute",
            top: "12px",
            right: "12px",
            zIndex: 30,
            background: "white",
            border: "none",
            borderRadius: "8px",
            padding: "8px 12px",
            cursor: "pointer",
            boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
            fontSize: "14px",
            fontWeight: 500,
          }}
        >
          Expand
        </button>
      )}

      {selectedShop && (
        <ShopInspector
          shop={selectedShop}
          isFavorite={widgetState?.favorites?.includes(selectedShop.id) ?? false}
          onToggleFavorite={() => toggleFavorite(selectedShop.id)}
          onClose={() => navigate("/")}
          isDark={isDark}
          displayMode={displayMode}
        />
      )}

      <div
        ref={mapRef}
        style={{
          position: "absolute",
          inset: 0,
          ...(isFullscreen && {
            left: "16px",
            right: "16px",
            top: "16px",
            bottom: "16px",
            borderRadius: "16px",
            border: `1px solid ${isDark ? "rgba(255,255,255,0.1)" : "rgba(0,0,0,0.1)"}`,
          }),
        }}
      />
    </div>
  );
}

interface ShopInspectorProps {
  shop: CoffeeShop;
  isFavorite: boolean;
  onToggleFavorite: () => void;
  onClose: () => void;
  isDark: boolean;
  displayMode?: "inline" | "pip" | "fullscreen";
}

function ShopInspector({ shop, isFavorite, onToggleFavorite, onClose, isDark, displayMode = "inline" }: ShopInspectorProps) {
  
  return (
    <div
      style={{
        position: "absolute",
        right: "12px",
        bottom: "12px",
        width: "240px",
        maxWidth: "85%",
        zIndex: 30,
        background: isDark ? "rgba(20, 20, 20, 0.65)" : "rgba(255, 255, 255, 0.75)",
        borderRadius: "12px",
        boxShadow: isDark ? "0 8px 32px rgba(0,0,0,0.4)" : "0 8px 32px rgba(0,0,0,0.12)",
        overflow: "hidden",
        display: "flex",
        flexDirection: "column",
        backdropFilter: "blur(16px) saturate(180%)",
        WebkitBackdropFilter: "blur(16px) saturate(180%)",
        maxHeight: "45vh",
        border: `1px solid ${isDark ? "rgba(255,255,255,0.12)" : "rgba(255,255,255,0.3)"}`,
        fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif",
      }}
    >
      <div style={{ flex: 1, overflowY: "auto", padding: "12px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "start", marginBottom: "8px" }}>
          <h3 style={{ fontSize: "15px", fontWeight: 600, margin: 0, letterSpacing: "-0.3px", flex: 1, paddingRight: "8px", lineHeight: "1.3" }}>
            {shop.name}
            {" "}
            <button
              onClick={onToggleFavorite}
              style={{
                background: "none",
                border: "none",
                cursor: "pointer",
                fontSize: "14px",
                padding: 0,
                lineHeight: 1,
                verticalAlign: "baseline",
                color: isFavorite ? "#fbbf24" : (isDark ? "rgba(255,255,255,0.3)" : "rgba(0,0,0,0.25)"),
              }}
            >
              {isFavorite ? "★" : "☆"}
            </button>
          </h3>
          <button
            onClick={onClose}
            style={{
              background: "none",
              border: "none",
              cursor: "pointer",
              fontSize: "16px",
              color: isDark ? "rgba(255,255,255,0.4)" : "rgba(0,0,0,0.3)",
              padding: 0,
              flexShrink: 0,
            }}
          >
            ✕
          </button>
        </div>
        
        <div style={{
          fontSize: "10px",
          color: isDark ? "rgba(255,255,255,0.5)" : "rgba(0,0,0,0.5)",
          marginBottom: "6px",
          fontWeight: 500,
        }}>
          {shop.neighborhood} {shop.priceRange}
        </div>
        
        <div style={{ fontSize: "11px", marginBottom: "6px", color: isDark ? "rgba(255,255,255,0.6)" : "rgba(0,0,0,0.6)" }}>
          {shop.rating}/5
        </div>
        
        <div style={{
          display: "flex",
          gap: "3px",
          marginBottom: "7px",
          flexWrap: "wrap",
        }}>
          {shop.vibe.slice(0, 2).map(v => (
            <span
              key={v}
              style={{
                padding: "1px 5px",
                borderRadius: "3px",
                fontSize: "9px",
                background: isDark ? "rgba(255,255,255,0.08)" : "rgba(0,0,0,0.05)",
                color: isDark ? "rgba(255,255,255,0.65)" : "rgba(0,0,0,0.55)",
              }}
            >
              {v}
            </span>
          ))}
        </div>
        
        <p style={{
          fontSize: "10px",
          lineHeight: "1.35",
          margin: "0 0 8px 0",
          color: isDark ? "rgba(255,255,255,0.6)" : "rgba(0,0,0,0.6)",
        }}>
          {shop.description.substring(0, 75)}...
        </p>
        
        <div style={{ marginBottom: "0" }}>
          <div style={{ fontWeight: 500, fontSize: "9px", marginBottom: "1px", color: isDark ? "rgba(255,255,255,0.4)" : "rgba(0,0,0,0.35)", textTransform: "uppercase", letterSpacing: "0.4px" }}>
            Specialty
          </div>
          <div style={{ fontSize: "10px", color: isDark ? "rgba(255,255,255,0.7)" : "rgba(0,0,0,0.7)" }}>
            {shop.specialty}
          </div>
        </div>
      </div>
    </div>
  );
}

export default function CoffeeMap() {
  if (!window.openai) {
    return (
      <div style={{
        fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        padding: "40px 20px",
        textAlign: "center",
        color: "#6b7280",
      }}>
        <p>Please open this widget in a supported environment</p>
      </div>
    );
  }

  return (
    <ErrorBoundary>
      <MemoryRouter>
        <Routes>
          <Route path="*" element={<MapContainer />}>
            <Route path="shop/:shopId" element={<></>} />
          </Route>
        </Routes>
      </MemoryRouter>
    </ErrorBoundary>
  );
}

