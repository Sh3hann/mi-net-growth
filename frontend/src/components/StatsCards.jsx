import React from 'react';
import { Layers, CheckCircle2, XCircle, Percent, TrendingUp } from 'lucide-react';

export default function StatsCards({ stats, loading }) {
  const cards = [
    {
      title: 'Total Levels',
      value: stats?.total_levels ?? 0,
      icon: Layers,
    },
    {
      title: 'Active Levels',
      value: stats?.active_levels ?? 0,
      icon: CheckCircle2,
    },
    {
      title: 'Inactive Levels',
      value: stats?.inactive_levels ?? 0,
      icon: XCircle,
    },
    {
      title: 'Average Incentive',
      value: `${stats?.avg_percentage ?? 0}%`,
      icon: Percent,
    },
    {
      title: 'Max Range Ceiling',
      value: stats?.max_upper_range
        ? `$${Number(stats.max_upper_range).toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`
        : '$0',
      icon: TrendingUp,
    },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
      {cards.map((card, idx) => {
        const Icon = card.icon;
        return (
          <div
            key={idx}
            className="bg-white rounded-xl p-4 border border-slate-200 shadow-xs flex flex-col justify-between"
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-medium text-slate-500">
                {card.title}
              </span>
              <Icon className="w-4 h-4 text-slate-400" />
            </div>

            <div className="text-2xl font-bold text-slate-900 tabular-nums">
              {loading ? (
                <div className="h-7 w-16 bg-slate-100 animate-pulse rounded-md" />
              ) : (
                card.value
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}
