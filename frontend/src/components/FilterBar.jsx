import React from 'react';
import { Search, Plus, RotateCw, Download } from 'lucide-react';

export default function FilterBar({
  search,
  onSearchChange,
  statusFilter,
  onStatusFilterChange,
  onAddNew,
  onRefresh,
  onExportCsv,
  loading,
  currentRole,
}) {
  const isReadOnly = currentRole === 'RM';

  return (
    <div className="bg-white rounded-xl p-4 border border-slate-200 shadow-xs flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3">
      {/* Search & Status Filters */}
      <div className="flex flex-1 flex-col sm:flex-row items-center gap-3">
        {/* Search */}
        <div className="relative w-full sm:w-72">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
          <input
            type="text"
            value={search}
            onChange={(e) => onSearchChange(e.target.value)}
            placeholder="Search level or NET ID..."
            className="w-full pl-9 pr-3 py-2 text-xs bg-white border border-slate-200 rounded-lg text-slate-900 placeholder-slate-400 focus:outline-hidden focus:border-slate-400 transition-colors"
          />
        </div>

        {/* Status Filter */}
        <div className="flex rounded-lg bg-slate-100 p-0.5 border border-slate-200 text-xs w-full sm:w-auto">
          {['All', 'Active', 'Inactive'].map((status) => {
            const isSelected = statusFilter === status;
            return (
              <button
                key={status}
                type="button"
                onClick={() => onStatusFilterChange(status)}
                className={`flex-1 sm:flex-initial px-3 py-1.5 rounded-md font-medium transition-colors cursor-pointer ${
                  isSelected
                    ? 'bg-white text-slate-900 font-semibold shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                {status}
              </button>
            );
          })}
        </div>
      </div>

      {/* Action Buttons - Clean white / neutral, no colourful buttons */}
      <div className="flex items-center gap-2 justify-end">
        <button
          type="button"
          onClick={onRefresh}
          disabled={loading}
          className="p-2 rounded-lg bg-white hover:bg-slate-50 text-slate-600 border border-slate-200 transition-colors cursor-pointer disabled:opacity-50"
          title="Refresh"
        >
          <RotateCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
        </button>

        <button
          type="button"
          onClick={onExportCsv}
          className="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-medium text-slate-700 bg-white hover:bg-slate-50 border border-slate-200 transition-colors cursor-pointer"
        >
          <Download className="w-3.5 h-3.5 text-slate-500" />
          <span>Export</span>
        </button>

        <button
          type="button"
          onClick={onAddNew}
          disabled={isReadOnly}
          className={`inline-flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-xs font-semibold transition-colors ${
            isReadOnly
              ? 'bg-slate-100 text-slate-400 border border-slate-200 cursor-not-allowed'
              : 'bg-slate-900 hover:bg-slate-800 text-white cursor-pointer shadow-xs'
          }`}
        >
          <Plus className="w-3.5 h-3.5" />
          <span>Add Level</span>
        </button>
      </div>
    </div>
  );
}
