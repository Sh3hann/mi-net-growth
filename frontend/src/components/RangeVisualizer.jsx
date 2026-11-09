import React from 'react';

export default function RangeVisualizer({ levels, onSelectTier }) {
  const activeLevels = (levels || [])
    .filter((l) => l.status === 'Active')
    .sort((a, b) => Number(a.lower_range) - Number(b.lower_range));

  if (activeLevels.length === 0) return null;

  const maxVal = Math.max(...activeLevels.map((l) => Number(l.upper_range) || 1));

  // Clean, subtle neutral shades instead of bright rainbow colors
  const shades = [
    'bg-slate-700 hover:bg-slate-800 text-white',
    'bg-slate-600 hover:bg-slate-700 text-white',
    'bg-slate-500 hover:bg-slate-600 text-white',
    'bg-slate-400 hover:bg-slate-500 text-white',
    'bg-slate-300 hover:bg-slate-400 text-slate-900',
    'bg-slate-200 hover:bg-slate-300 text-slate-900',
  ];

  return (
    <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-xs">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-sm font-semibold text-slate-900">
          Range Coverage
        </h2>
        <span className="text-xs text-slate-500 font-mono">
          $0 to ${maxVal.toLocaleString()}
        </span>
      </div>

      {/* Visual Bar */}
      <div className="w-full h-8 bg-slate-100 rounded-lg overflow-hidden flex gap-0.5 p-0.5 border border-slate-200">
        {activeLevels.map((lvl, index) => {
          const lower = Number(lvl.lower_range);
          const upper = Number(lvl.upper_range);
          const span = upper - lower;
          const pct = Math.max(8, (span / maxVal) * 100);
          const shade = shades[index % shades.length];

          return (
            <div
              key={lvl.id || index}
              style={{ width: `${pct}%` }}
              onClick={() => onSelectTier && onSelectTier(lvl)}
              className={`${shade} h-full rounded-md flex items-center justify-between px-2 text-[11px] font-medium cursor-pointer transition-colors select-none`}
              title={`${lvl.net_id} - ${lvl.level}: $${lower.toLocaleString()} to $${upper.toLocaleString()} (${lvl.percentage}%)`}
            >
              <span className="truncate">{lvl.net_id}</span>
              <span className="opacity-90">{lvl.percentage}%</span>
            </div>
          );
        })}
      </div>

      {/* Clean Legend */}
      <div className="flex flex-wrap items-center gap-4 mt-3 text-xs text-slate-600">
        {activeLevels.map((lvl, idx) => (
          <div key={lvl.id || idx} className="flex items-center gap-1.5">
            <span className="font-semibold text-slate-800">{lvl.net_id}</span>
            <span className="text-slate-400">
              (${Number(lvl.lower_range).toLocaleString()} - ${Number(lvl.upper_range).toLocaleString()} · {lvl.percentage}%)
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
