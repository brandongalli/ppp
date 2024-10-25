"use client";
import { useState } from "react";
import TeamCarousel from "../components/TeamCarousel";
import ScoreTable from "../components/ScoreTable";
import FilterBoard from "../components/FilterBoard";
import logo from "../assets/logo.png";
import SearchBoard from "@/components/SearchBoard";

export default function Home() {
  const [selectedTeam, setSelectedTeam] = useState<any>(null);

  return (
    <div className="page flex flex-col h-screen">
      <div className="flex justify-around items-center p-6">
        <div className="flex items-center gap-4">
          <img src={logo} alt="logo" />
          <p className="font-light text-[35px] leading-[24px]">
            San Francisco 49ers
          </p>
        </div>
        <p className="text-sm">2023-2024 SEASON</p>
      </div>

      <hr className="border-gray-400" />

      <TeamCarousel onSelect={(team) => setSelectedTeam(team)} />

      <SearchBoard />

      <div className="flex flex-grow">
        <FilterBoard />
        <div className="flex-grow bg-white relative">
          {selectedTeam ? (
            <ScoreTable team={selectedTeam} />
          ) : (
            <p className="text-center text-gray-500">
              Select a team to view details.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
