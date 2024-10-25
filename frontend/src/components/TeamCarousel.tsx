"use client";

import { getGameData } from "@/app/apiService";
import { useState, useRef, useEffect } from "react";

const logoNames = [
  "arizonacardinals",
  "baltimoreravens",
  "detroitlions",
  "eattleseahawks",
  "greenbaypackers",
  "kansascitycheifs",
];

interface TeamCarouselProps {
  onSelect: (item: any) => void;
}

export default function TeamCarousel({ onSelect }: TeamCarouselProps) {
  const [selectedIndex, setSelectedIndex] = useState<number | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [startX, setStartX] = useState(0);
  const [scrollLeft, setScrollLeft] = useState(0);
  const carouselRef = useRef<HTMLDivElement>(null);

  // Handle both mouse and touch events
  const handleDragStart = (pageX: number) => {
    setIsDragging(true);
    setStartX(pageX - (carouselRef.current?.offsetLeft || 0));
    setScrollLeft(carouselRef.current?.scrollLeft || 0);
  };

  const handleDragMove = (pageX: number) => {
    if (!isDragging || !carouselRef.current) return;
    const x = pageX - (carouselRef.current?.offsetLeft || 0);
    const walk = (x - startX) * 2; // Adjust scroll speed
    carouselRef.current.scrollLeft = scrollLeft - walk;
  };

  const handleMouseDown = (e: React.MouseEvent) => handleDragStart(e.pageX);
  const handleMouseMove = (e: React.MouseEvent) => handleDragMove(e.pageX);
  const handleTouchStart = (e: React.TouchEvent) =>
    handleDragStart(e.touches[0].pageX);
  const handleTouchMove = (e: React.TouchEvent) =>
    handleDragMove(e.touches[0].pageX);

  const handleDragEnd = () => setIsDragging(false);

  const getLogo = () => {
    const randomIndex = Math.floor(Math.random() * logoNames.length);
    const logoName = logoNames[randomIndex];
    try {
      return require(`../assets/team/${logoName}.svg`);
    } catch (err) {
      console.error(`Logo not found for: ${logoName}`);
      return null;
    }
  };

  const handleSelect = (index: number) => {
    setSelectedIndex(index);
  };

  const [games, setGames] = useState<any>([]);

  const initGameData = async () => {
    const res = await getGameData("/games");
    setGames(res ?? []);
  };

  useEffect(() => {
    initGameData();
  }, []);

  return (
    <div
      ref={carouselRef}
      className="flex space-x-4 overflow-hidden cursor-grab select-none justify-center"
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleDragEnd}
      onMouseLeave={handleDragEnd}
      onTouchStart={handleTouchStart}
      onTouchMove={handleTouchMove}
      onTouchEnd={handleDragEnd}
      style={{ padding: "10px" }}
    >
      {games.map((item: any, index: number) => (
        <div
          key={index}
          className={`flex-shrink-0 w-44 text-center p-4 rounded-lg shadow-md cursor-pointer ${
            selectedIndex === index
              ? "bg-white text-black"
              : "bg-[#b3995d] text-black"
          }`}
          onClick={() => {
            handleSelect(index);
            onSelect(item);
          }}
        >
          <p className="text-xs">{item.date}</p>
          <p className="text-xs font-bold">{item.stadium}</p>
          <div className="flex justify-center mb-4">
            <img
              src={getLogo()}
              alt={`${item.logo_uri}`}
              className="h-12 w-12"
            />
          </div>
          <p className="text-sm">vs</p>
          <p className="text-sm">{item.location}</p>
          <p className="text-sm font-bold">{item.opponent}</p>
          <p className="text-sm">
            <span className="font-bold">{item.score}</span> {item.ht}
          </p>
        </div>
      ))}
    </div>
  );
}
