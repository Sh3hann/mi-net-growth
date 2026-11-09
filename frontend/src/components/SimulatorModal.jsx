import React, { useState } from 'react';
import { X, Calculator } from 'lucide-react';

export default function SimulatorModal({ isOpen, onClose, activeLevels }) {
  const [amount, setAmount] = useState('250000');

  if (!isOpen) return null;

  const numericAmount = parseFloat(amount) || 0;

  const sortedLevels = [...(activeLevels || [])]
    .filter((l) => l.status === 'Active')
    .sort((a, b) => Number(a.lower_range) - Number(b.lower_range));

  const matchedTier = sortedLevels.find((l) => {
    const low = Number(l.lower_range);
    const up = Number(l.upper_range);
    return numericAmount >= low && numericAmount <= up;
  });

  const incentiveRate = matchedTier ? Number(matchedTier.percentage) : 0;
  const calculatedPayout = (numericAmount * (incentiveRate / 100)).toFixed(2);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 animate-fade-in">
      <div className="bg-white rounded-xl border border-slate-200 shadow-xl max-w-md w-full overflow-hidden text-xs">
        {/* Header */}
        <div className="px-5 py-4 border-b border-slate-200 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Calculator className="w-4 h-4 text-slate-700" />
            <h3 className="text-sm font-bold text-slate-900">
              Incentive Simulator
            </h3>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="p-1 rounded text-slate-400 hover:text-slate-600 cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content */}
        <div className="p-5 space-y-4">
          <div>
            <label className="block font-semibold text-slate-700 mb-1">
              Net Growth Amount ($)
            </label>
            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              placeholder="0.00"
              className="w-full px-3 py-2 border border-slate-200 rounded-lg text-slate-900 font-mono text-sm focus:outline-hidden focus:border-slate-400"
            />
          </div>

          {matchedTier ? (
            <div className="p-4 rounded-lg bg-slate-50 border border-slate-200 space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-slate-500">Qualified Level:</span>
                <span className="font-semibold text-slate-900">
                  {matchedTier.net_id} - {matchedTier.level}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-500">Incentive Rate:</span>
                <span className="font-semibold font-mono text-slate-900">
                  {matchedTier.percentage}%
                </span>
              </div>
              <div className="flex justify-between items-center pt-2 border-t border-slate-200">
                <span className="font-semibold text-slate-700">Calculated Payout:</span>
                <span className="text-base font-bold font-mono text-slate-900">
                  ${Number(calculatedPayout).toLocaleString('en-US', { minimumFractionDigits: 2 })}
                </span>
              </div>
            </div>
          ) : (
            <div className="p-3 rounded-lg bg-slate-50 border border-slate-200 text-center text-slate-500">
              No matching active tier for this amount
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-5 py-3 border-t border-slate-200 flex justify-end">
          <button
            type="button"
            onClick={onClose}
            className="px-3 py-1.5 rounded-lg border border-slate-200 text-slate-700 hover:bg-slate-50 transition-colors cursor-pointer"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
