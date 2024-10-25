import { QuestionMarkCircleIcon } from "@heroicons/react/24/outline";

export default function FilterBoard() {
  return (
    <div className="w-64 bg-[#8A0000]">
      <div className="h-10 border-[#AC8553] border-b"></div>
      <div className="p-6">
        <div>
          <p className="uppercase mb-2 text-sm font-bold">User Segments</p>
          <div className="flex flex-col space-y-2">
            <label className="inline-flex items-center">
              <input
                type="checkbox"
                className="form-checkbox h-4 w-4 text-blue-500"
              />
              <span className="flex items-center gap-4 ml-2 text-sm">
                Lorem Ipsum Dolor{" "}
                <QuestionMarkCircleIcon color="#B3995D" className="h-4 w-4" />
              </span>
            </label>
            <label className="inline-flex items-center">
              <input
                type="checkbox"
                className="form-checkbox h-4 w-4 text-blue-500"
              />
              <span className="flex items-center gap-4 ml-2 text-sm">
                Sit Amet{" "}
                <QuestionMarkCircleIcon color="#B3995D" className="h-4 w-4" />
              </span>
            </label>
            <label className="inline-flex items-center">
              <input
                type="checkbox"
                className="form-checkbox h-4 w-4 text-blue-500"
              />
              <span className="flex items-center gap-4 ml-2 text-sm">
                Vivamus Interdum{" "}
                <QuestionMarkCircleIcon color="#B3995D" className="h-4 w-4" />
              </span>
            </label>
          </div>
        </div>

        <div>
          <p className="uppercase mt-6 mb-2 text-sm font-bold">
            Aliquam ornare
          </p>
          <div className="flex gap-4">
            <input
              type="text"
              placeholder="From"
              className="border flex-1 w-12 text-center text-[#AA0000] 
                 placeholder-[#AA0000] placeholder-opacity-40 border-gray-300 rounded-md p-2 
                 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <input
              type="text"
              placeholder="To"
              className="border flex-1 w-12 text-center text-[#AA0000] 
                 placeholder-[#AA0000] placeholder-opacity-40 border-gray-300 rounded-md p-2 
                 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div className="flex gap-2 mt-4 w-[80%]">
            <button className="uppercase py-2 text-sm flex-1 bg-[#b3995d] rounded-3xl ">
              Apply
            </button>
            <button className="uppercase py-2 text-sm flex-1 bg-[#3e0000] rounded-3xl">
              Clear
            </button>
          </div>
        </div>

        <div>
          <p className="uppercase mt-6 mb-2 text-sm font-bold">
            Nam Gravida Dolor
          </p>
          <input
            type="text"
            placeholder="Type Here"
            className="border text-[#AA0000] 
                 placeholder-[#AA0000] placeholder-opacity-40 border-gray-300 rounded-md p-2 
                 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <p className="uppercase mt-6 mb-2 text-sm font-bold">
            Quisque Vitae Viverra
          </p>
          <input
            type="text"
            placeholder="Type Here"
            className="border text-[#AA0000] 
                 placeholder-[#AA0000] placeholder-opacity-40 border-gray-300 rounded-md p-2 
                 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>
    </div>
  );
}
