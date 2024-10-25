import { FunnelIcon } from "@heroicons/react/20/solid";

export default function SearchBoard() {
  return (
    <div className="flex items-center relative bg-white text-black py-2 px-6 h-16 gap-4">
      <div className="w-24 bg-[#AA0000] p-1 pb-8 rounded absolute top-2">
        <div className="flex items-center bg-white p-2 rounded gap-2 text-[#b3995d]">
          <FunnelIcon className="h-5 w-5" />
          <p className="text-sm">FILTER</p>
        </div>
      </div>
      <div className="pl-28">
        <input
          type="text"
          placeholder="SEARCH"
          className="border w-72 border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <div className="">
        <button className="text-[#AA0000]">EXPORT DATA</button>
      </div>
    </div>
  );
}
