/**
 * PremiumLabMap.tsx — Astro Island (client:load)
 * Interactive Google Maps for premium listings only.
 * Obsidian-themed dark map. Advanced Markers. Optional service radius.
 */
import { useEffect, useRef } from 'react';
import { Loader } from '@googlemaps/js-api-loader';

interface Props {
  lat: number;
  lng: number;
  labName: string;
  coverageRadiusKm?: number | null;
}

const DARK_STYLES = [
  { elementType: "geometry", stylers: [{ color: "#111827" }] },
  { elementType: "labels.text.fill", stylers: [{ color: "#6B7280" }] },
  { featureType: "road", elementType: "geometry", stylers: [{ color: "#1F2937" }] },
  { featureType: "water", elementType: "geometry", stylers: [{ color: "#050505" }] },
  { featureType: "poi", stylers: [{ visibility: "off" }] },
];

export default function PremiumLabMap({ lat, lng, labName, coverageRadiusKm }: Props) {
  const mapRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const loader = new Loader({
      apiKey: import.meta.env.PUBLIC_GOOGLE_MAPS_API_KEY,
      version: 'weekly',
      libraries: ['marker'],
    });

    loader.load().then(async () => {
      const { Map } = await google.maps.importLibrary('maps') as google.maps.MapsLibrary;
      const { AdvancedMarkerElement } = await google.maps.importLibrary('marker') as google.maps.MarkerLibrary;
      if (!mapRef.current) return;

      const map = new Map(mapRef.current, {
        center: { lat, lng }, zoom: 13,
        mapId: 'DEMO_MAP_ID', // Replace with your Map ID if you have one
        styles: DARK_STYLES,
        disableDefaultUI: true, zoomControl: true,
      });

      // Indigo pin — matches Obsidian design system
      const pin = document.createElement('div');
      pin.style.cssText = `
        width:36px;height:36px;border-radius:50%;background:#4F46E5;
        border:2px solid rgba(255,255,255,0.2);display:flex;
        align-items:center;justify-content:center;
        box-shadow:0 0 16px rgba(79,70,229,0.5);cursor:pointer;
      `;
      pin.innerHTML = `<svg width="18" height="18" fill="white" viewBox="0 0 24 24">
        <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/>
      </svg>`;
      pin.setAttribute('title', labName);

      new AdvancedMarkerElement({ map, position: { lat, lng }, title: labName, content: pin });

      // Emerald service radius — premium feature
      if (coverageRadiusKm && coverageRadiusKm > 0) {
        new google.maps.Circle({
          map, center: { lat, lng }, radius: coverageRadiusKm * 1000,
          strokeColor: '#10B981', strokeOpacity: 0.6, strokeWeight: 2,
          fillColor: '#10B981', fillOpacity: 0.05,
        });
      }
    });
  }, [lat, lng, labName, coverageRadiusKm]);

  return (
    <div ref={mapRef} aria-label={`Interactive map for ${labName}`}
      style={{ width:'100%', height:'380px', borderRadius:'12px',
               border:'1px solid rgba(255,255,255,0.08)', overflow:'hidden' }} />
  );
}
