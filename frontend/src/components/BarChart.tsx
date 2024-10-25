export default function BarChart() {
  const data = [
    { week: "WK 1", height: 80 },
    { week: "WK 2", height: 60 },
    { week: "WK 3", height: 70 },
    { week: "WK 4", height: 85 },
    { week: "WK 5", height: 75 },
    { week: "WK 6", height: 95 },
    { week: "WK 7", height: 90 },
    { week: "WK 8", height: 60 },
    { week: "WK 9", height: 65 },
    { week: "WK 10", height: 85 },
    { week: "WK 11", height: 80 },
    { week: "WK 12", height: 75 },
    { week: "WK 13", height: 88 },
    { week: "WK 14", height: 92 },
    { week: "WK 15", height: 86 },
    { week: "WK 16", height: 100 }, // Example white bar
    { week: "WK 17", height: 85 },
    { week: "WK 18", height: 80 },
  ];

  return (
    <div className="flex items-end space-x-1 h-[120px]">
      {data.map((item, index) => (
        <div
          key={index}
          className={`w-3 ${
            item.week === "WK 16" ? "bg-white" : "bg-yellow-600"
          }`}
          style={{ height: `${item.height}%` }}
        ></div>
      ))}
    </div>
  );
}
