import BarChart from "./BarChart";
import { IPlayer } from "./ScoreTable";
import photo from "../assets/photo.png";

export default function PlayerTooltip({ player }: { player: IPlayer }) {
  return (
    <div className="tooltip">
      <div className="tooltip-content">
        <div className="p-4 bg-gradient-to-r from-red-900 to-red-600 rounded text-white">
          <div className="flex justify-between">
            <div>
              <p className="uppercase">2023-2024</p>
              <p className="uppercase">Season</p>
            </div>
            <h3 className="text-xl uppercase">
              Ranking: <strong>3</strong>
            </h3>
          </div>
          <BarChart />
        </div>
        <div className="w-full p-4 text-black">
          <div className="flex gap-3">
            <div className="flex items-center justify-center bg-gradient-to-r from-red-900 to-red-600 rounded">
              <img src={photo} alt={player.first_name} />
            </div>
            <div>
              <p className="text-2xl font-bold">{player.first_name}</p>
              <p className="text-2xl font-bold">{player.last_name}</p>
              <div className="flex gap-4">
                <p className="text-2xl font-bold">#{player.number}</p>
                <div className="border-r-[2px] border-black"></div>
                <p className="text-2xl font-bold">{player.position}</p>
              </div>
            </div>
          </div>
        </div>
        <div>
          <p>
            Honored in his hometown of Longview, Texas, with “Trent Williams
            Day” on May 12, 2010 to celebrate his selection in the NFL Draft.
          </p>
        </div>
      </div>
    </div>
  );
}
