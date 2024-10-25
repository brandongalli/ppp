export default function SortIcon({ isSorted, isAsc }: any) {
  return (
    <div className="flex flex-col justify-center items-center w-4 h-4">
      <div
        className={`w-0 h-0 border-l-4 border-r-4 border-b-4 border-transparent ${
          isSorted && isAsc ? "border-b-black" : "border-b-white"
        }`}
      ></div>

      <div
        className={`w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent mt-1 ${
          isSorted && !isAsc ? "border-t-black" : "border-t-white"
        }`}
      ></div>
    </div>
  );
}
