import React from 'react';
import { Layers, Calculator } from 'lucide-react';

export default function Navbar({ currentRole, onRoleChange, onOpenSimulator }) {
  const roles = [
    { id: 'CFO', name: 'CFO' },
    { id: 'DGM', name: 'DGM' },
    { id: 'RM', name: 'RM' },
  ];

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand - Clean and direct */}
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-slate-900 flex items-center justify-center text-white">
              <Layers className="w-4 h-4" />
            </div>
            <h1 className="text-base font-bold text-slate-900 tracking-tight">
              MI Net Growth Levels
            </h1>
          </div>

          {/* Right Section: Simulator & Role Switcher */}
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={onOpenSimulator}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-slate-700 bg-white border border-slate-200 hover:bg-slate-50 transition-colors cursor-pointer"
            >
              <Calculator className="w-3.5 h-3.5 text-slate-500" />
              <span>Simulator</span>
            </button>

            {/* Clean Role Switcher */}
            <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-lg border border-slate-200 text-xs font-medium">
              <span className="px-2 text-slate-500">Role:</span>
              {roles.map((r) => {
                const isSelected = r.id === currentRole;
                return (
                  <button
                    key={r.id}
                    type="button"
                    onClick={() => onRoleChange(r.id)}
                    className={`px-2.5 py-1 rounded-md transition-colors cursor-pointer ${
                      isSelected
                        ? 'bg-white text-slate-900 font-semibold shadow-xs'
                        : 'text-slate-600 hover:text-slate-900'
                    }`}
                  >
                    {r.name}
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
