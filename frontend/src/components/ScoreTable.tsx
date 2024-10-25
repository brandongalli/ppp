import { SetStateAction, useEffect, useState } from "react";
import SortIcon from "./SortIcon";
import photo from "../assets/photo.png";
import PlayerTooltip from "./PlayerTooltip";
import { getPlayerData } from "@/app/apiService";

export interface IPlayer {
  seasonRank: number;
  gameRank: number;
  number: number;
  first_name: string;
  last_name: string;
  position: string;
  height: string;
  wt: number;
  birth_year: number;
  debut_year: number;
  college: string;
  weight?: string;
}

export default function ScoreTable({ team }: any) {
  const columns = [
    { name: "Season Rank", width: 12, sort: true },
    { name: "Game Rank", width: 12, sort: true },
    { name: "#", width: 12, sort: true },
    { name: "First Name", width: 24, sort: true },
    { name: "Last Name", width: 24, sort: true },
    { name: "Pos", width: 12, sort: true },
    { name: "Ht", width: 12, sort: true },
    { name: "Wt", width: 12, sort: true },
    { name: "Age", width: 12, sort: true },
    { name: "Exp", width: 12, sort: true },
    { name: "College", width: 24, sort: true },
  ];

  const [players, setPlayer] = useState<IPlayer[]>([]);
  const [selectedRow, setSelectedRow] = useState<IPlayer | null>(null);

  const handleMouseEnter = (row: IPlayer) => {
    setSelectedRow(row);
  };

  const handleMouseLeave = () => {
    setSelectedRow(null);
  };

  const initPlayerData = async () => {
    const res = await getPlayerData(
      `/players?teams=${team.home_team_id},${team.away_team_id}`
    );
    setPlayer(res?.slice(0, 10) ?? []);
  };

  useEffect(() => {
    initPlayerData();
  }, []);

  return (
    <div className="overflow-x-auto height-full">
      <table className="min-w-full">
        <thead className="bg-[#660000] text-white border-b-8 border-[#8A0000]">
          <tr>
            {columns.map((col, index) => (
              <th
                key={index}
                className={`h-11 w-${col.width} text-center uppercase`}
              >
                <div className="flex items-center">
                  <p className="text-[11px] leading-none px-1">{col.name}</p>{" "}
                  <SortIcon />
                </div>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {players.map((row, index) => (
            <tr
              key={index}
              className="game-tr bg-white text-black cursor-pointer"
              onMouseEnter={() => handleMouseEnter(row)}
              onMouseLeave={handleMouseLeave}
              style={{ position: "relative" }}
            >
              <td className="season-rank border-b border-[#5b5b5b] text-center bg-[#333333] text-[#B3995D]">
                <div className="td-item">{row.seasonRank}</div>
              </td>
              <td className="game-rank border-b border-[#eaeaea] text-center bg-[#F5F5F5]">
                <div className="td-item">{row.gameRank}</div>
              </td>
              <td className="normal border-b border-[#f1f1f1]">
                <div className="td-item">{row.number}</div>
              </td>
              <td className="normal border-b border-[#f1f1f1]">
                <div className="td-item">{row.first_name}</div>
              </td>
              <td className="normal border-b border-[#f1f1f1]">
                <div className="td-item">{row.last_name}</div>
              </td>
              <td className="normal border-b border-[#f1f1f1]">
                <div className="td-item">{row.position}</div>
              </td>
              <td className="normal border-b border-[#f1f1f1]">
                <div className="td-item">{row.height}</div>
              </td>
              <td className="normal border-b border-[#f1f1f1]">
                <div className="td-item">{row.weight}</div>
              </td>
              <td className="normal border-b border-[#f1f1f1]">
                <div className="td-item">{row.birth_year}</div>
              </td>
              <td className="normal border-b border-[#f1f1f1]">
                <div className="td-item">{row.debut_year}</div>
              </td>
              <td className="normal border-b border-[#f1f1f1]">
                <div className="td-item">{row.college}</div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {selectedRow && <PlayerTooltip player={selectedRow} />}
    </div>
  );
}
